#!/bin/bash

# Script para configurar Claude Code en un proyecto nuevo
# Uso: ./setup-claude-config.sh [autonomo|consultivo] [directorio]

set -e

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función para mostrar uso
show_usage() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  Script de Configuración de Claude Code${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Uso: $0 [modo] [directorio]"
    echo ""
    echo "Modos disponibles:"
    echo "  autonomo    - Modo autónomo (bypassPermissions)"
    echo "  consultivo  - Modo consultivo (default con reglas)"
    echo ""
    echo "Ejemplo:"
    echo "  $0 autonomo /home/leandro/mi-proyecto"
    echo "  $0 consultivo ."
    echo ""
    exit 1
}

# Verificar argumentos
if [ $# -lt 2 ]; then
    show_usage
fi

MODE=$1
TARGET_DIR=$2

# Validar modo
if [ "$MODE" != "autonomo" ] && [ "$MODE" != "consultivo" ]; then
    echo -e "${RED}❌ Error: Modo inválido '$MODE'${NC}"
    echo ""
    show_usage
fi

# Resolver directorio absoluto
TARGET_DIR=$(cd "$TARGET_DIR" 2>/dev/null && pwd || echo "$TARGET_DIR")

# Verificar que el directorio existe
if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${RED}❌ Error: El directorio '$TARGET_DIR' no existe${NC}"
    exit 1
fi

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Configurando Claude Code${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "📁 Directorio: ${YELLOW}$TARGET_DIR${NC}"
echo -e "🎯 Modo: ${YELLOW}$MODE${NC}"
echo ""

# Crear directorio .claude
CLAUDE_DIR="$TARGET_DIR/.claude"
mkdir -p "$CLAUDE_DIR"
echo -e "${GREEN}✅${NC} Directorio .claude creado"

# Crear settings.json según el modo
if [ "$MODE" = "autonomo" ]; then
    cat > "$CLAUDE_DIR/settings.json" << 'EOF'
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  }
}
EOF
    echo -e "${GREEN}✅${NC} settings.json creado (modo autónomo)"

    # Crear CLAUDE.md para proyecto autónomo
    cat > "$CLAUDE_DIR/CLAUDE.md" << 'EOF'
# Proyecto Autónomo

Este proyecto está configurado para trabajo autónomo.

## Modo
- **bypassPermissions**: Claude trabaja sin pedir confirmaciones
- Ideal para: experimentación, prototipos, desarrollo rápido

## Reglas
- Mantén el bucle de verificación (heredado de config global)
- Experimenta libremente
- NO usar para código de producción
EOF
    echo -e "${GREEN}✅${NC} CLAUDE.md creado"

elif [ "$MODE" = "consultivo" ]; then
    cat > "$CLAUDE_DIR/settings.json" << 'EOF'
{
  "permissions": {
    "defaultMode": "default",
    "ask": [
      "Bash(*)",
      "Write(*)",
      "Edit(*)"
    ],
    "allow": [
      "Read(*)",
      "Grep(*)",
      "Glob(*)"
    ]
  }
}
EOF
    echo -e "${GREEN}✅${NC} settings.json creado (modo consultivo)"

    # Crear CLAUDE.md para proyecto consultivo
    cat > "$CLAUDE_DIR/CLAUDE.md" << 'EOF'
# Proyecto Consultivo

Este proyecto está configurado para trabajo consultivo.

## Modo
- **default + reglas**: Claude pide aprobación para cambios
- Ideal para: producción, código crítico, datos sensibles

## Permisos
- ✅ Lectura libre (Read, Grep, Glob)
- ⏸️ Pregunta antes de: Bash, Write, Edit

## Seguridad
- Apropiado para código de producción
- Revisión antes de cada cambio
EOF
    echo -e "${GREEN}✅${NC} CLAUDE.md creado"
fi

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Configuración completada${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Archivos creados:"
echo "  📄 $CLAUDE_DIR/settings.json"
echo "  📄 $CLAUDE_DIR/CLAUDE.md"
echo ""
echo "Próximos pasos:"
echo "  1. cd $TARGET_DIR"
echo "  2. code ."
echo "  3. ¡Claude Code usará esta configuración automáticamente!"
echo ""
