#!/bin/bash

################################################################################
# Script de Restauración de Backup de Producción
#
# Restaura automáticamente un backup de la base de datos de producción
# en el ambiente de desarrollo local.
#
# Uso:
#   ./restaurar_backup_produccion.sh [opciones]
#
# Opciones:
#   -h, --help              Muestra esta ayuda
#   -d, --dry-run           Simula la ejecución sin hacer cambios
#   -f, --file ARCHIVO      Especifica el archivo de backup a restaurar
#   -s, --skip-backup       Omite el backup de seguridad local
#   -y, --yes               No pide confirmación
#
# Ejemplos:
#   ./restaurar_backup_produccion.sh                    # Restaura el backup más reciente
#   ./restaurar_backup_produccion.sh -f backup.sql      # Restaura un backup específico
#   ./restaurar_backup_produccion.sh -d                 # Modo simulación
#
################################################################################

set -e  # Detener en caso de error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Variables de configuración
RUTA_PRODUCCION="/home/leandro/debian-home/sistemas/Docker_proyectos/Reloj_fichador"
RUTA_LOCAL="/home/leandro/Proyectos_Docker/Reloj_fichador"
MYSQL_USER="root"
MYSQL_PASS="S1st3mas.1999"
MYSQL_DB="docker_horesdb"
DOCKER_COMPOSE_CMD="docker compose"
CONTAINER_DB="reloj_fichador-db-1"

# Variables de script
DRY_RUN=false
SKIP_BACKUP=false
AUTO_YES=false
BACKUP_FILE=""
TIMESTAMP=$(date +%Y-%m-%d_%H.%M.%S)
LOG_FILE="${RUTA_LOCAL}/logs/restauracion_${TIMESTAMP}.log"

################################################################################
# Funciones auxiliares
################################################################################

# Función para imprimir mensajes
print_info() {
    echo -e "${CYAN}ℹ${NC}  $1" | tee -a "$LOG_FILE"
}

print_success() {
    echo -e "${GREEN}✓${NC}  $1" | tee -a "$LOG_FILE"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC}  $1" | tee -a "$LOG_FILE"
}

print_error() {
    echo -e "${RED}✗${NC}  $1" | tee -a "$LOG_FILE"
}

print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}" | tee -a "$LOG_FILE"
    echo -e "${BLUE}$1${NC}" | tee -a "$LOG_FILE"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}" | tee -a "$LOG_FILE"
}

# Función para mostrar ayuda
show_help() {
    cat << EOF
Script de Restauración de Backup de Producción

Uso: $0 [opciones]

Opciones:
  -h, --help              Muestra esta ayuda
  -d, --dry-run           Simula la ejecución sin hacer cambios
  -f, --file ARCHIVO      Especifica el archivo de backup a restaurar
  -s, --skip-backup       Omite el backup de seguridad local
  -y, --yes               No pide confirmación

Ejemplos:
  $0                                    # Restaura el backup más reciente
  $0 -f backup_2025-11-10_16.46.10.sql # Restaura un backup específico
  $0 -d                                 # Modo simulación

El script realiza los siguientes pasos:
  1. Verifica que Docker esté corriendo
  2. Hace backup de seguridad de la BD local actual
  3. Copia el backup de producción
  4. Restaura el backup en la BD local
  5. Ejecuta las migraciones pendientes
  6. Verifica que todo funcionó correctamente
  7. Muestra un resumen final

EOF
}

# Parsear argumentos
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -d|--dry-run)
                DRY_RUN=true
                shift
                ;;
            -f|--file)
                BACKUP_FILE="$2"
                shift 2
                ;;
            -s|--skip-backup)
                SKIP_BACKUP=true
                shift
                ;;
            -y|--yes)
                AUTO_YES=true
                shift
                ;;
            *)
                print_error "Opción desconocida: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# Verificar que Docker esté corriendo
check_docker() {
    print_info "Verificando Docker..."

    if ! docker ps &> /dev/null; then
        print_error "Docker no está corriendo o no tienes permisos"
        exit 1
    fi

    if ! $DOCKER_COMPOSE_CMD ps db | grep -q "healthy"; then
        print_error "El contenedor MySQL no está healthy"
        exit 1
    fi

    print_success "Docker está corriendo correctamente"
}

# Buscar el último backup de producción
find_latest_backup() {
    print_info "Buscando el backup más reciente..."

    if [ ! -d "${RUTA_PRODUCCION}/backups" ]; then
        print_error "No se encuentra la carpeta de backups de producción"
        exit 1
    fi

    BACKUP_FILE=$(ls -t "${RUTA_PRODUCCION}/backups"/backup_*.sql 2>/dev/null | head -1)

    if [ -z "$BACKUP_FILE" ]; then
        print_error "No se encontraron backups en ${RUTA_PRODUCCION}/backups"
        exit 1
    fi

    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    BACKUP_NAME=$(basename "$BACKUP_FILE")

    print_success "Backup encontrado: $BACKUP_NAME ($BACKUP_SIZE)"
}

# Hacer backup de seguridad de BD local
backup_local_db() {
    if [ "$SKIP_BACKUP" = true ]; then
        print_warning "Omitiendo backup de seguridad local (--skip-backup)"
        return
    fi

    print_info "Creando backup de seguridad de BD local..."

    BACKUP_LOCAL_FILE="${RUTA_LOCAL}/backup_local_antes_restauracion_${TIMESTAMP}.sql"

    if [ "$DRY_RUN" = true ]; then
        print_warning "[DRY-RUN] Se crearía: $BACKUP_LOCAL_FILE"
        return
    fi

    $DOCKER_COMPOSE_CMD exec -T db mysqldump \
        -u"$MYSQL_USER" \
        -p"$MYSQL_PASS" \
        --no-tablespaces \
        "$MYSQL_DB" > "$BACKUP_LOCAL_FILE" 2>/dev/null

    BACKUP_LOCAL_SIZE=$(du -h "$BACKUP_LOCAL_FILE" | cut -f1)
    print_success "Backup local creado: backup_local_antes_restauracion_${TIMESTAMP}.sql ($BACKUP_LOCAL_SIZE)"
}

# Restaurar backup de producción
restore_backup() {
    print_info "Restaurando backup de producción..."

    if [ "$DRY_RUN" = true ]; then
        print_warning "[DRY-RUN] Se restauraría: $BACKUP_FILE"
        return
    fi

    # Copiar backup al proyecto local temporalmente
    TEMP_BACKUP="${RUTA_LOCAL}/backup_produccion_temporal.sql"
    cp "$BACKUP_FILE" "$TEMP_BACKUP"

    # Restaurar
    $DOCKER_COMPOSE_CMD exec -T db mysql \
        -u"$MYSQL_USER" \
        -p"$MYSQL_PASS" \
        "$MYSQL_DB" < "$TEMP_BACKUP" 2>/dev/null

    # Limpiar archivo temporal
    rm -f "$TEMP_BACKUP"

    print_success "Backup restaurado correctamente"
}

# Ejecutar migraciones
run_migrations() {
    print_info "Ejecutando migraciones de Django..."

    if [ "$DRY_RUN" = true ]; then
        print_warning "[DRY-RUN] Se ejecutarían las migraciones"
        return
    fi

    # Marcar migraciones de axes como aplicadas (fake)
    print_info "  → Sincronizando migraciones de django-axes..."
    $DOCKER_COMPOSE_CMD exec -T web python manage.py migrate axes --fake &>> "$LOG_FILE"

    # Marcar migraciones de reloj_fichador como aplicadas (fake)
    print_info "  → Sincronizando migraciones de reloj_fichador..."
    $DOCKER_COMPOSE_CMD exec -T web python manage.py migrate reloj_fichador --fake &>> "$LOG_FILE"

    # Ejecutar migraciones finales
    print_info "  → Ejecutando migraciones restantes..."
    $DOCKER_COMPOSE_CMD exec -T web python manage.py migrate &>> "$LOG_FILE"

    print_success "Migraciones completadas"
}

# Verificar la restauración
verify_restoration() {
    print_info "Verificando restauración..."

    if [ "$DRY_RUN" = true ]; then
        print_warning "[DRY-RUN] Se verificaría la restauración"
        return
    fi

    # Contar tablas
    TOTAL_TABLES=$($DOCKER_COMPOSE_CMD exec -T db mysql \
        -u"$MYSQL_USER" \
        -p"$MYSQL_PASS" \
        -se "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '$MYSQL_DB';" \
        "$MYSQL_DB" 2>/dev/null | tr -d '\r')

    # Verificar servicios
    WEB_STATUS=$($DOCKER_COMPOSE_CMD ps web | grep -q "Up" && echo "OK" || echo "ERROR")
    DB_STATUS=$($DOCKER_COMPOSE_CMD ps db | grep -q "healthy" && echo "OK" || echo "ERROR")

    # Verificar que el admin responda
    ADMIN_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:58000/admin/login/ 2>/dev/null)

    if [ "$TOTAL_TABLES" -lt 40 ]; then
        print_error "Error: Solo se encontraron $TOTAL_TABLES tablas (se esperaban 45+)"
        exit 1
    fi

    if [ "$WEB_STATUS" != "OK" ] || [ "$DB_STATUS" != "OK" ]; then
        print_error "Error: Algunos servicios no están corriendo correctamente"
        exit 1
    fi

    if [ "$ADMIN_STATUS" != "200" ]; then
        print_warning "Advertencia: El admin no respondió correctamente (HTTP $ADMIN_STATUS)"
    fi

    print_success "Verificación completada: $TOTAL_TABLES tablas, servicios OK"
}

# Mostrar resumen final
show_summary() {
    print_header "Resumen de Restauración"

    if [ "$DRY_RUN" = true ]; then
        print_warning "MODO DRY-RUN: No se realizaron cambios reales"
        echo ""
    fi

    echo -e "${CYAN}Backup restaurado:${NC}"
    echo -e "  • Archivo: $(basename "$BACKUP_FILE")"
    echo -e "  • Tamaño: $(du -h "$BACKUP_FILE" | cut -f1)"
    echo -e ""

    if [ "$DRY_RUN" = false ]; then
        # Obtener estadísticas de la BD
        STATS=$($DOCKER_COMPOSE_CMD exec -T db mysql \
            -u"$MYSQL_USER" \
            -p"$MYSQL_PASS" \
            -se "SELECT
                (SELECT COUNT(*) FROM reloj_fichador_operario) as operarios,
                (SELECT COUNT(*) FROM reloj_fichador_registrodiario) as registros,
                (SELECT COUNT(*) FROM reloj_fichador_horas_trabajadas) as horas,
                (SELECT COUNT(*) FROM reloj_fichador_gruposabado) as grupos;" \
            "$MYSQL_DB" 2>/dev/null | tr '\t' ',' | tr -d '\r')

        IFS=',' read -r OPERARIOS REGISTROS HORAS GRUPOS <<< "$STATS"

        echo -e "${CYAN}Datos restaurados:${NC}"
        echo -e "  • Operarios: $OPERARIOS"
        echo -e "  • Registros diarios: $REGISTROS"
        echo -e "  • Horas calculadas: $HORAS"
        echo -e "  • Grupos de sábado: $GRUPOS"
        echo -e ""

        echo -e "${CYAN}Servicios:${NC}"
        echo -e "  • Admin: ${GREEN}http://localhost:58000/admin/${NC}"
        echo -e "  • Web: ${GREEN}http://localhost:5080${NC}"
        echo -e ""

        echo -e "${CYAN}Log del proceso:${NC}"
        echo -e "  • $LOG_FILE"
        echo -e ""
    fi

    print_success "Restauración completada exitosamente"
}

# Pedir confirmación
ask_confirmation() {
    if [ "$AUTO_YES" = true ]; then
        return 0
    fi

    echo -e ""
    echo -e "${YELLOW}⚠  ADVERTENCIA:${NC} Este proceso:"
    echo -e "   1. Hará un backup de la BD local actual"
    echo -e "   2. Sobrescribirá la BD local con datos de producción"
    echo -e "   3. Ejecutará migraciones de Django"
    echo -e ""
    echo -e "   Backup a restaurar: $(basename "$BACKUP_FILE")"
    echo -e ""
    read -p "¿Continuar? (s/N): " -n 1 -r
    echo

    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        print_info "Operación cancelada por el usuario"
        exit 0
    fi
}

################################################################################
# Script principal
################################################################################

main() {
    # Crear directorio de logs si no existe
    mkdir -p "${RUTA_LOCAL}/logs"

    # Header
    clear
    print_header "Restauración de Backup de Producción"
    echo -e "${CYAN}Fecha:${NC} $TIMESTAMP" | tee -a "$LOG_FILE"
    echo "" | tee -a "$LOG_FILE"

    # Parsear argumentos
    parse_args "$@"

    # Paso 1: Verificar Docker
    check_docker

    # Paso 2: Buscar backup (si no se especificó uno)
    if [ -z "$BACKUP_FILE" ]; then
        find_latest_backup
    else
        # Verificar que el archivo especificado existe
        if [ ! -f "$BACKUP_FILE" ]; then
            print_error "El archivo especificado no existe: $BACKUP_FILE"
            exit 1
        fi
    fi

    # Pedir confirmación
    if [ "$DRY_RUN" = false ]; then
        ask_confirmation
    fi

    echo "" | tee -a "$LOG_FILE"

    # Paso 3: Backup de seguridad
    backup_local_db

    # Paso 4: Restaurar backup
    restore_backup

    # Paso 5: Ejecutar migraciones
    run_migrations

    # Paso 6: Verificar
    verify_restoration

    # Paso 7: Resumen
    echo "" | tee -a "$LOG_FILE"
    show_summary
}

# Ejecutar script
main "$@"
