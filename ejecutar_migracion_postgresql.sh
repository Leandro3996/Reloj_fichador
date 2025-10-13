#!/bin/bash
#
# Script de ejecución de migración MySQL → PostgreSQL
# Sistema: Reloj Fichador
#
# Uso: ./ejecutar_migracion_postgresql.sh
#

set -e  # Salir si hay algún error

echo "╔══════════════════════════════════════════════════════════╗"
echo "║   MIGRACIÓN DE MYSQL A POSTGRESQL                        ║"
echo "║   Sistema: Reloj Fichador                                ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función para mostrar mensajes
info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Paso 1: Verificar que los servicios estén corriendo
info "Paso 1: Verificando servicios..."
docker compose ps db db_postgres | grep -q "healthy" || {
    warning "Los contenedores de base de datos no están saludables. Iniciando..."
    docker compose up -d db db_postgres
    sleep 15
}
info "✓ Servicios de bases de datos están corriendo"

# Paso 2: Verificar conexión a MySQL
info "Paso 2: Verificando conexión a MySQL..."
docker compose exec -T db mysql -usistemas -pS1st3mas2024 -e "SELECT 1;" docker_horesdb > /dev/null 2>&1 || {
    error "No se puede conectar a MySQL"
    exit 1
}
info "✓ MySQL conectada"

# Paso 3: Verificar conexión a PostgreSQL
info "Paso 3: Verificando conexión a PostgreSQL..."
docker compose exec -T db_postgres psql -U sistemas -d docker_horesdb_pg -c "SELECT 1;" > /dev/null 2>&1 || {
    error "No se puede conectar a PostgreSQL"
    exit 1
}
info "✓ PostgreSQL conectada"

# Paso 4: Reconstruir contenedor web si es necesario
info "Paso 4: Verificando contenedor web..."
if ! docker compose ps web | grep -q "running"; then
    warning "Contenedor web no está corriendo. Reconstruyendo..."
    docker compose build web
    docker compose up -d web
    sleep 10
fi
info "✓ Contenedor web listo"

# Paso 5: Ejecutar migraciones en PostgreSQL
info "Paso 5: Ejecutando migraciones de Django en PostgreSQL..."
docker compose exec -T web python manage.py migrate --database=postgres || {
    error "Error al ejecutar migraciones"
    exit 1
}
info "✓ Migraciones completadas"

# Paso 6: Mostrar conteo de registros en MySQL
info "Paso 6: Contando registros en MySQL..."
echo ""
echo "=== REGISTROS EN MYSQL ==="
docker compose exec -T db mysql -usistemas -pS1st3mas2024 docker_horesdb -e "
SELECT 'Operarios' as Tabla, COUNT(*) as Registros FROM reloj_fichador_operario
UNION ALL SELECT 'RegistroDiario', COUNT(*) FROM reloj_fichador_registrodiario
UNION ALL SELECT 'Horas Trabajadas', COUNT(*) FROM reloj_fichador_horas_trabajadas
UNION ALL SELECT 'Usuarios', COUNT(*) FROM auth_user;
"
echo ""

# Paso 7: Confirmar migración
warning "⚠️  ATENCIÓN ⚠️"
echo "Se migrará toda la información de MySQL a PostgreSQL."
echo "Este proceso puede tardar varios minutos dependiendo del volumen de datos."
echo ""
read -p "¿Desea continuar con la migración? (s/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[SsYy]$ ]]; then
    warning "Migración cancelada por el usuario"
    exit 0
fi

# Paso 8: Ejecutar script de migración
info "Paso 8: Ejecutando script de migración de datos..."
echo ""
docker compose exec web python migrate_mysql_to_postgres.py || {
    error "Error durante la migración de datos"
    exit 1
}
echo ""

# Paso 9: Verificar registros en PostgreSQL
info "Paso 9: Verificando registros en PostgreSQL..."
echo ""
echo "=== REGISTROS EN POSTGRESQL ==="
docker compose exec -T db_postgres psql -U sistemas -d docker_horesdb_pg -c "
SELECT 'Operarios' as tabla, COUNT(*) as registros FROM reloj_fichador_operario
UNION ALL SELECT 'RegistroDiario', COUNT(*) FROM reloj_fichador_registrodiario
UNION ALL SELECT 'Horas Trabajadas', COUNT(*) FROM reloj_fichador_horas_trabajadas
UNION ALL SELECT 'Usuarios', COUNT(*) FROM auth_user;
"
echo ""

# Paso 10: Resumen
info "╔══════════════════════════════════════════════════════════╗"
info "║   MIGRACIÓN COMPLETADA                                   ║"
info "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "✅ La base de datos PostgreSQL ha sido creada y poblada"
echo ""
echo "📝 Próximos pasos:"
echo "   1. Verificar la integridad de los datos"
echo "   2. Probar la aplicación conectando a PostgreSQL"
echo "   3. Revisar la documentación en documentacion/MIGRACION_POSTGRESQL.md"
echo ""
echo "🔧 Para usar PostgreSQL como base de datos principal:"
echo "   - Editar mantenedor/settings.py"
echo "   - Cambiar DATABASES['default'] a PostgreSQL"
echo "   - Reiniciar servicios: docker compose restart web celery celery-beat"
echo ""
echo "💾 Para hacer backup de PostgreSQL:"
echo "   docker compose exec db_postgres pg_dump -U sistemas docker_horesdb_pg > backup.sql"
echo ""
