#!/bin/bash
# Script de mantenimiento para el Sistema Reloj Fichador
# Uso: ./mantenimiento.sh [opción]

# Colores para mensajes
AZUL='\033[0;34m'
VERDE='\033[0;32m'
ROJO='\033[0;31m'
AMARILLO='\033[0;33m'
RESET='\033[0m'

# Directorio raíz del proyecto
DIR_PROYECTO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/../../.."
cd "$DIR_PROYECTO" || { echo -e "${ROJO}Error: No se pudo acceder al directorio del proyecto${RESET}"; exit 1; }

# Función para mostrar ayuda
mostrar_ayuda() {
    echo -e "${AZUL}=== Script de Mantenimiento del Sistema Reloj Fichador ===${RESET}"
    echo
    echo "Uso: ./mantenimiento.sh [opción]"
    echo
    echo "Opciones disponibles:"
    echo "  backup          - Crea una copia de seguridad de la base de datos"
    echo "  limpiar_logs    - Comprime y archiva logs antiguos"
    echo "  estado          - Muestra el estado actual de los contenedores"
    echo "  reiniciar       - Reinicia todos los servicios de Docker"
    echo "  actualizar      - Actualiza el código desde el repositorio"
    echo "  test            - Ejecuta las pruebas automatizadas"
    echo "  migrar          - Ejecuta migraciones pendientes de Django"
    echo "  staticfiles     - Recolecta archivos estáticos"
    echo "  ayuda           - Muestra esta información"
    echo
}

# Función para crear backup de la base de datos
crear_backup() {
    echo -e "${AZUL}Creando copia de seguridad de la base de datos...${RESET}"
    
    # Crear directorio de backups si no existe
    mkdir -p backups
    
    # Nombre del archivo de backup con timestamp
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    BACKUP_FILE="backups/db_backup_$TIMESTAMP.sql"
    
    # Ejecutar backup usando Docker
    if docker-compose exec -T db mysqldump -u root -p$MYSQL_ROOT_PASSWORD --databases docker_horesdb > "$BACKUP_FILE"; then
        echo -e "${VERDE}Backup creado exitosamente: $BACKUP_FILE${RESET}"
        # Comprimir el archivo
        gzip "$BACKUP_FILE"
        echo -e "${VERDE}Backup comprimido: $BACKUP_FILE.gz${RESET}"
    else
        echo -e "${ROJO}Error al crear el backup${RESET}"
        return 1
    fi
}

# Función para limpiar y comprimir logs antiguos
limpiar_logs() {
    echo -e "${AZUL}Comprimiendo logs antiguos...${RESET}"
    
    # Crear directorio de logs archivados si no existe
    mkdir -p logs/archivados
    
    # Buscar logs con más de 7 días de antigüedad
    find logs -name "*.log" -type f -mtime +7 | while read -r log_file; do
        nombre_base=$(basename "$log_file")
        echo -e "Archivando $nombre_base"
        gzip -c "$log_file" > "logs/archivados/${nombre_base}_$(date +%Y%m%d).gz"
        # Vaciar el contenido del archivo original
        > "$log_file"
    done
    
    echo -e "${VERDE}Limpieza de logs completada${RESET}"
}

# Función para mostrar el estado de los contenedores
mostrar_estado() {
    echo -e "${AZUL}Estado actual de los contenedores:${RESET}"
    docker-compose ps
}

# Función para reiniciar servicios
reiniciar_servicios() {
    echo -e "${AZUL}Reiniciando servicios...${RESET}"
    docker-compose down
    docker-compose up -d
    echo -e "${VERDE}Servicios reiniciados correctamente${RESET}"
}

# Función para actualizar desde repositorio
actualizar_codigo() {
    echo -e "${AZUL}Actualizando código desde el repositorio...${RESET}"
    
    # Verificar si hay cambios locales
    if [ -n "$(git status --porcelain)" ]; then
        echo -e "${AMARILLO}ADVERTENCIA: Hay cambios locales no confirmados${RESET}"
        git status --short
        echo
        read -p "¿Desea continuar con la actualización? (s/n): " respuesta
        if [[ ! $respuesta =~ ^[Ss]$ ]]; then
            echo -e "${ROJO}Actualización cancelada${RESET}"
            return 1
        fi
    fi
    
    # Crear backup antes de actualizar
    crear_backup
    
    # Actualizar el código
    git pull
    
    # Reconstruir contenedores si es necesario
    echo -e "${AZUL}Reconstruyendo contenedores...${RESET}"
    docker-compose build web
    docker-compose up -d
    
    echo -e "${VERDE}Actualización completada${RESET}"
}

# Función para ejecutar pruebas
ejecutar_pruebas() {
    echo -e "${AZUL}Ejecutando pruebas automatizadas...${RESET}"
    docker-compose exec web python manage.py test apps.reloj_fichador.tests
}

# Función para ejecutar migraciones
ejecutar_migraciones() {
    echo -e "${AZUL}Ejecutando migraciones pendientes...${RESET}"
    docker-compose exec web python manage.py migrate
}

# Función para recolectar archivos estáticos
recolectar_staticfiles() {
    echo -e "${AZUL}Recolectando archivos estáticos...${RESET}"
    docker-compose exec web python manage.py collectstatic --noinput
}

# Verificar argumentos
if [ $# -eq 0 ]; then
    mostrar_ayuda
    exit 0
fi

# Procesar opciones
case "$1" in
    backup)
        crear_backup
        ;;
    limpiar_logs)
        limpiar_logs
        ;;
    estado)
        mostrar_estado
        ;;
    reiniciar)
        reiniciar_servicios
        ;;
    actualizar)
        actualizar_codigo
        ;;
    test)
        ejecutar_pruebas
        ;;
    migrar)
        ejecutar_migraciones
        ;;
    staticfiles)
        recolectar_staticfiles
        ;;
    ayuda|--help|-h)
        mostrar_ayuda
        ;;
    *)
        echo -e "${ROJO}Opción desconocida: $1${RESET}"
        mostrar_ayuda
        exit 1
        ;;
esac

exit 0 