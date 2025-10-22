# Configuración de MCP para Reloj Fichador

## ⭐ Única Fuente de Verdad: `~/.claude.json`

Toda la configuración de MCPs se encuentra centralizada en **`~/.claude.json`** (configuración global de Claude Code).

### MCPs Configurados Globalmente

```json
{
  "mcpServers": {
    "context7": { ... },
    "browsermcp": { ... },
    "postgres-reloj-fichador": { ... },
    "chrome-devtools": { ... }
  }
}
```

**MCPs Disponibles:**
1. **context7** - Documentación de librerías y frameworks
2. **browsermcp** - Automatización de navegador web  
3. **postgres-reloj-fichador** - Conexión a PostgreSQL (docker_horesdb_pg)
4. **chrome-devtools** - DevTools de Chrome para análisis de rendimiento

---

## Jerarquía de Configuración (NO USAR)

Los siguientes archivos están presentes pero **NO deben ser utilizados para Claude Code CLI**:

- `~/.cursor/mcp.json` → Para Cursor (no interfiere)
- `~/.config/Claude/claude_desktop_config.json` → Para Claude Desktop (app de escritorio)
- `.vscode/mcp.json` → Vacío (para evitar conflictos)

---

## Cómo Usar los MCPs

### PostgreSQL MCP
```
"Muestra todos los operarios registrados"
"¿Cuántos registros diarios hay en octubre?"
"Dame el resumen de horas trabajadas por empleado"
```

### Chrome DevTools MCP
```
"Abre http://localhost:5080 y toma una captura de pantalla"
"Analiza el rendimiento de http://localhost:5080"
"Navega a http://localhost:58000/admin y verifica que la página carga"
```

### Context7 MCP
```
"Documenta la función calcular_horas_trabajadas"
"Busca ejemplos de Django ORM"
```

### BrowserMCP
```
"Abre http://localhost:5080 en el navegador"
"Navega a localhost y haz clic en el botón de entrada"
```

---

## Reinicio de Claude Code

Si cambias la configuración en `~/.claude.json`:
1. Edita el archivo
2. **Reinicia Claude Code** completamente
3. Los MCPs deberían estar disponibles inmediatamente

---

## Verificación

Para verificar que los MCPs están cargados correctamente en Claude Code:
- Todos los MCPs deberían aparecer en la lista de herramientas disponibles
- No deberían haber errores de "servidor no encontrado"

Última actualización: 22/10/2025
