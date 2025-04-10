#!/bin/bash
# verificacion_docker.sh - Script para verificar y reiniciar servicios Docker
# Autor: Analista de sistemas
# Fecha: 10/04/2025
# Uso: ./verificacion_docker.sh [reiniciar]

# Colores para output
ROJO='\033[0;31m'
VERDE='\033[0;32m'
AMARILLO='\033[1;33m'
NC='\033[0m' # Sin Color

# Función para mostrar mensajes de log con timestamp
log() {
    local nivel=$1
    local mensaje=$2
    local timestamp
    timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    
    case $nivel in
        ERROR)
            echo -e "${ROJO}[$timestamp] ERROR: $mensaje${NC}"
            ;;
        INFO)
            echo -e "${VERDE}[$timestamp] INFO: $mensaje${NC}"
            ;;
        WARN)
            echo -e "${AMARILLO}[$timestamp] WARN: $mensaje${NC}"
            ;;
    esac
}

# Verificar que Docker está instalado y corriendo
if ! command -v docker &> /dev/null; then
    log ERROR "Docker no está instalado o no está en el PATH."
    exit 1
fi

if ! docker info &> /dev/null; then
    log ERROR "El servicio Docker no está en ejecución o tienes problemas de permisos."
    exit 1
fi

log INFO "Verificando servicios Docker..."

# Comprobar si docker-compose está disponible
if command -v docker compose &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
else
    log ERROR "No se encontró docker compose. Instálalo para continuar."
    exit 1
fi

# Obtener lista de contenedores definidos en docker-compose.yml
COMPOSE_FILE="../../../docker-compose.yml"
if [ ! -f "$COMPOSE_FILE" ]; then
    log ERROR "No se encontró el archivo docker-compose.yml en la ruta esperada."
    exit 1
fi

# Mostrar estado actual de los contenedores
log INFO "Estado actual de los contenedores:"
"$DOCKER_COMPOSE" -f "$COMPOSE_FILE" ps

# Verificar si todos los contenedores están en funcionamiento
TOTAL_CONTAINERS=$("$DOCKER_COMPOSE" -f "$COMPOSE_FILE" ps --services | wc -l)
RUNNING_CONTAINERS=$("$DOCKER_COMPOSE" -f "$COMPOSE_FILE" ps | grep -c "Up")

log INFO "Contenedores totales: $TOTAL_CONTAINERS, En ejecución: $RUNNING_CONTAINERS"

if [ "$RUNNING_CONTAINERS" -lt "$TOTAL_CONTAINERS" ]; then
    log WARN "No todos los contenedores están en ejecución."
    
    # Verificar logs de los contenedores con problemas
    for service in $("$DOCKER_COMPOSE" -f "$COMPOSE_FILE" ps --services); do
        if ! "$DOCKER_COMPOSE" -f "$COMPOSE_FILE" ps | grep "$service" | grep -q "Up"; then
            log WARN "El servicio $service no está en ejecución. Revisando logs..."
            "$DOCKER_COMPOSE" -f "$COMPOSE_FILE" logs --tail=50 "$service" | grep -i "error\|fail\|exception"
        fi
    done
    
    # Verificar específicamente si MySQL muestra errores relacionados con la autenticación
    if "$DOCKER_COMPOSE" -f "$COMPOSE_FILE" logs db | grep -q "unknown variable 'default-authentication-plugin"; then
        log ERROR "Detectado problema de configuración en MySQL: default-authentication-plugin"
        log INFO "Este error debe corregirse modificando docker-compose.yml para usar --authentication_policy en lugar de --default-authentication-plugin"
    fi
    
    # Verificar error de valor inválido en authentication_policy
    if "$DOCKER_COMPOSE" -f "$COMPOSE_FILE" logs db | grep -q "Option --authentication-policy is set to an invalid value"; then
        log ERROR "Detectado valor inválido en --authentication-policy"
        log INFO "Este error debe corregirse modificando docker-compose.yml para usar --authentication_policy='*,,' en lugar del valor actual"
    fi
    
    # Reiniciar servicios si se pasó el parámetro "reiniciar"
    if [ "$1" = "reiniciar" ]; then
        log INFO "Reiniciando todos los contenedores..."
        "$DOCKER_COMPOSE" -f "$COMPOSE_FILE" down
        "$DOCKER_COMPOSE" -f "$COMPOSE_FILE" up -d
        
        # Esperar y verificar de nuevo
        log INFO "Esperando 30 segundos para que los servicios arranquen..."
        sleep 30
        
        RUNNING_CONTAINERS_AFTER=$("$DOCKER_COMPOSE" -f "$COMPOSE_FILE" ps | grep -c "Up")
        if [ "$RUNNING_CONTAINERS_AFTER" -eq "$TOTAL_CONTAINERS" ]; then
            log INFO "Todos los contenedores están ahora en ejecución."
        else
            log ERROR "Algunos contenedores siguen sin iniciarse. Revisa los logs para más detalles."
            "$DOCKER_COMPOSE" -f "$COMPOSE_FILE" ps
        fi
    else
        log INFO "Para reiniciar los contenedores, ejecuta: $0 reiniciar"
    fi
else
    log INFO "Todos los contenedores están en ejecución correctamente."
fi

# Función para verificar la conexión a la base de datos MySQL
check_mysql_connection() {
    log INFO "Verificando conexión a MySQL..."
    if "$DOCKER_COMPOSE" -f "$COMPOSE_FILE" exec -T db mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "SELECT 1;" &> /dev/null; then
        log INFO "Conexión a MySQL exitosa."
        return 0
    else
        log ERROR "No se pudo conectar a MySQL. Verifica las credenciales y el estado del servidor."
        return 1
    fi
}

# Extraer variables de entorno del archivo .env
ENV_FILE="../../../.env"
if [ -f "$ENV_FILE" ]; then
    # shellcheck disable=SC1090
    source "$ENV_FILE"
    # Verificar conexión a MySQL solo si tenemos las credenciales
    if [ -n "$MYSQL_USER" ] && [ -n "$MYSQL_PASSWORD" ]; then
        check_mysql_connection
    else
        log WARN "No se encontraron credenciales de MySQL en el archivo .env"
    fi
else
    log WARN "No se encontró el archivo .env para obtener credenciales de MySQL"
fi

log INFO "Verificación completada." 