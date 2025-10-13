#!/bin/bash
#
# Script para verificar el contenido del admin log antes de la migración
#

echo "╔══════════════════════════════════════════════════════════╗"
echo "║   VERIFICACIÓN DE DJANGO ADMIN LOG                       ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}[INFO]${NC} Verificando registros en django_admin_log..."
echo ""

# Contar total de registros
echo "📊 TOTAL DE REGISTROS DE AUDITORÍA:"
docker compose exec -T db mysql -usistemas -pS1st3mas2024 docker_horesdb -e "
SELECT COUNT(*) as total_acciones FROM django_admin_log;
"

echo ""
echo "📈 DISTRIBUCIÓN POR TIPO DE ACCIÓN:"
docker compose exec -T db mysql -usistemas -pS1st3mas2024 docker_horesdb -e "
SELECT
    CASE action_flag
        WHEN 1 THEN '✏️  Creaciones'
        WHEN 2 THEN '📝 Modificaciones'
        WHEN 3 THEN '🗑️  Eliminaciones'
    END as tipo_accion,
    COUNT(*) as cantidad
FROM django_admin_log
GROUP BY action_flag
ORDER BY action_flag;
"

echo ""
echo "👥 ACCIONES POR USUARIO:"
docker compose exec -T db mysql -usistemas -pS1st3mas2024 docker_horesdb -e "
SELECT
    u.username as usuario,
    COUNT(*) as total_acciones,
    MAX(al.action_time) as ultima_accion
FROM django_admin_log al
JOIN auth_user u ON al.user_id = u.id
GROUP BY u.username
ORDER BY total_acciones DESC
LIMIT 10;
"

echo ""
echo "🔝 ÚLTIMAS 10 ACCIONES:"
docker compose exec -T db mysql -usistemas -pS1st3mas2024 docker_horesdb -e "
SELECT
    DATE_FORMAT(al.action_time, '%Y-%m-%d %H:%i:%s') as fecha,
    u.username as usuario,
    CASE al.action_flag
        WHEN 1 THEN 'ADD'
        WHEN 2 THEN 'CHANGE'
        WHEN 3 THEN 'DELETE'
    END as accion,
    al.object_repr as objeto
FROM django_admin_log al
JOIN auth_user u ON al.user_id = u.id
ORDER BY al.action_time DESC
LIMIT 10;
"

echo ""
echo "📋 MODELOS MÁS MODIFICADOS:"
docker compose exec -T db mysql -usistemas -pS1st3mas2024 docker_horesdb -e "
SELECT
    ct.app_label as app,
    ct.model as modelo,
    COUNT(*) as cambios
FROM django_admin_log al
JOIN django_content_type ct ON al.content_type_id = ct.id
GROUP BY ct.app_label, ct.model
ORDER BY cambios DESC
LIMIT 10;
"

echo ""
echo -e "${GREEN}✅ Verificación completada${NC}"
echo ""
echo "💡 Este historial será incluido en la migración a PostgreSQL."
echo "   Contiene información valiosa sobre quién hizo qué cambios y cuándo."
