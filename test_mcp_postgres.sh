#!/bin/bash
#
# Script de prueba para verificar la conexión MCP a PostgreSQL
#

echo "╔══════════════════════════════════════════════════════════╗"
echo "║   PRUEBA DE CONEXIÓN MCP → POSTGRESQL                    ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 1. Verificar PostgreSQL
echo -e "${GREEN}[1/5]${NC} Verificando PostgreSQL..."
if docker compose ps db_postgres | grep -q "healthy"; then
    echo -e "  ${GREEN}✓${NC} PostgreSQL está corriendo"
else
    echo -e "  ${RED}✗${NC} PostgreSQL no está disponible"
    echo "  Iniciando PostgreSQL..."
    docker compose up -d db_postgres
    sleep 10
fi

# 2. Verificar Node.js
echo ""
echo -e "${GREEN}[2/5]${NC} Verificando Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "  ${GREEN}✓${NC} Node.js instalado: $NODE_VERSION"
else
    echo -e "  ${RED}✗${NC} Node.js no encontrado"
    exit 1
fi

# 3. Verificar npx
echo ""
echo -e "${GREEN}[3/5]${NC} Verificando npx..."
if command -v npx &> /dev/null; then
    echo -e "  ${GREEN}✓${NC} npx disponible"
else
    echo -e "  ${RED}✗${NC} npx no encontrado"
    exit 1
fi

# 4. Probar conexión directa a PostgreSQL
echo ""
echo -e "${GREEN}[4/5]${NC} Probando conexión directa a PostgreSQL..."
if docker compose exec -T db_postgres psql -U sistemas -d docker_horesdb_pg -c "SELECT 1;" > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓${NC} Conexión exitosa"
else
    echo -e "  ${RED}✗${NC} No se puede conectar"
    exit 1
fi

# 5. Probar servidor MCP
echo ""
echo -e "${GREEN}[5/5]${NC} Probando servidor MCP de PostgreSQL..."
echo "  Ejecutando: npx -y enhanced-postgres-mcp-server"
echo "  Cadena de conexión: postgresql://sistemas:***@localhost:54321/docker_horesdb_pg"
echo ""

# Crear un script temporal para probar
cat > /tmp/test_mcp.js << 'EOF'
const { spawn } = require('child_process');

const mcp = spawn('npx', [
    '-y',
    'enhanced-postgres-mcp-server',
    'postgresql://sistemas:S1st3mas2024@localhost:54321/docker_horesdb_pg'
]);

let output = '';
let errorOutput = '';

mcp.stdout.on('data', (data) => {
    output += data.toString();
});

mcp.stderr.on('data', (data) => {
    errorOutput += data.toString();
});

setTimeout(() => {
    mcp.kill();

    if (output.includes('error') || errorOutput.includes('error')) {
        console.log('❌ Error al iniciar servidor MCP:');
        console.log(errorOutput);
        process.exit(1);
    } else if (output.length > 0 || errorOutput.includes('listening')) {
        console.log('✅ Servidor MCP iniciado correctamente');
        console.log('El servidor está listo para recibir conexiones desde Claude Code');
        process.exit(0);
    } else {
        console.log('⚠️  El servidor se inició pero no hay salida visible');
        console.log('Esto es normal - el servidor MCP espera comandos de Claude Code');
        process.exit(0);
    }
}, 3000);
EOF

node /tmp/test_mcp.js

TEST_RESULT=$?

# Limpiar
rm /tmp/test_mcp.js

echo ""
if [ $TEST_RESULT -eq 0 ]; then
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║   ✅ CONFIGURACIÓN MCP LISTA                             ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo ""
    echo "📝 Próximos pasos:"
    echo ""
    echo "1. Configurar Claude Code:"
    echo "   - Copia el contenido de: mcp_postgres_config.json"
    echo "   - Pégalo en la configuración de MCP de Claude Code"
    echo ""
    echo "2. Reinicia Claude Code"
    echo ""
    echo "3. Prueba con comandos como:"
    echo "   • \"Lista las tablas de la base de datos PostgreSQL\""
    echo "   • \"Describe la tabla reloj_fichador_operario\""
    echo "   • \"Muéstrame los últimos 5 operarios\""
    echo ""
    echo "📖 Documentación completa: CONFIGURACION_MCP_POSTGRESQL.md"
else
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║   ⚠️  PROBLEMAS DETECTADOS                               ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo ""
    echo "Revisa los errores anteriores y consulta:"
    echo "CONFIGURACION_MCP_POSTGRESQL.md (sección Troubleshooting)"
fi
