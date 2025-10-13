# Configuración de MCP para PostgreSQL en Claude Code

## 🎯 ¿Qué es esto?

Este documento te guía para configurar **MCP (Model Context Protocol)** que permite a Claude Code conectarse directamente a tu base de datos PostgreSQL y hacer consultas en lenguaje natural.

**Ejemplo de uso:**
- "Muéstrame las últimas 10 entradas de operarios"
- "¿Cuántos registros diarios hay en octubre?"
- "Describe la estructura de la tabla horas_trabajadas"
- "Haz un resumen de las horas extras del mes pasado"

---

## ✅ Prerequisitos Completados

- ✅ Node.js v22.17.0 instalado
- ✅ Servidor MCP instalado: `enhanced-postgres-mcp-server`
- ✅ PostgreSQL corriendo en puerto `54321`
- ✅ Base de datos: `docker_horesdb_pg`
- ✅ Usuario: `sistemas`
- ✅ Contraseña: `S1st3mas2024`

---

## 📝 Configuración Paso a Paso

### Opción 1: Configuración Automática (Recomendado)

Claude Code detecta automáticamente archivos de configuración MCP en el proyecto. El archivo ya está creado:

**Ubicación:** [`mcp_postgres_config.json`](mcp_postgres_config.json)

**Contenido:**
```json
{
  "mcpServers": {
    "postgres-reloj-fichador": {
      "command": "npx",
      "args": [
        "-y",
        "enhanced-postgres-mcp-server",
        "postgresql://sistemas:S1st3mas2024@localhost:54321/docker_horesdb_pg"
      ],
      "disabled": false,
      "alwaysAllow": [
        "list-tables",
        "describe-table",
        "query"
      ],
      "env": {
        "PGTZ": "America/Argentina/Buenos_Aires"
      }
    }
  }
}
```

### Opción 2: Configuración Manual en Claude Code

Si Claude Code no detecta el archivo automáticamente, configúralo manualmente:

#### En Linux:

1. Crear el directorio de configuración:
   ```bash
   mkdir -p ~/.config/Claude/
   ```

2. Crear o editar el archivo de configuración:
   ```bash
   nano ~/.config/Claude/claude_desktop_config.json
   ```

3. Agregar esta configuración:
   ```json
   {
     "mcpServers": {
       "postgres-reloj-fichador": {
         "command": "npx",
         "args": [
           "-y",
           "enhanced-postgres-mcp-server",
           "postgresql://sistemas:S1st3mas2024@localhost:54321/docker_horesdb_pg"
         ],
         "disabled": false,
         "alwaysAllow": [
           "list-tables",
           "describe-table",
           "query"
         ],
         "env": {
           "PGTZ": "America/Argentina/Buenos_Aires"
         }
       }
     }
   }
   ```

4. Guardar y reiniciar Claude Code

#### En macOS:

```bash
# Ubicación del archivo
~/Library/Application Support/Claude/claude_desktop_config.json
```

#### En Windows:

```
%APPDATA%\Claude\claude_desktop_config.json
```

---

## 🔧 Verificar que PostgreSQL está Corriendo

Antes de probar, asegúrate de que PostgreSQL esté activo:

```bash
docker compose ps db_postgres

# Debería mostrar:
# NAME                           STATUS                    PORTS
# reloj_fichador-db_postgres-1   Up XX minutes (healthy)   0.0.0.0:54321->5432/tcp
```

Si no está corriendo:

```bash
docker compose up -d db_postgres
```

---

## 🧪 Probar la Configuración

### Prueba desde Terminal

Verifica que el servidor MCP funciona:

```bash
# Probar conexión directa
npx -y enhanced-postgres-mcp-server \
  "postgresql://sistemas:S1st3mas2024@localhost:54321/docker_horesdb_pg" \
  --help
```

### Prueba desde Claude Code

Una vez configurado, abre Claude Code y prueba estos comandos:

1. **Listar tablas:**
   ```
   Lista todas las tablas en la base de datos PostgreSQL
   ```

2. **Describir estructura:**
   ```
   Describe la estructura de la tabla reloj_fichador_operario
   ```

3. **Consulta simple:**
   ```
   Muéstrame los primeros 5 operarios activos
   ```

4. **Consulta compleja:**
   ```
   ¿Cuántos registros diarios hay por mes en el año 2025?
   ```

5. **Análisis:**
   ```
   Dame un resumen de las horas trabajadas por operario en octubre
   ```

---

## 🎨 Comandos MCP Disponibles

El servidor MCP soporta estas herramientas:

### 1. `list-tables`
Lista todas las tablas disponibles en la base de datos.

**Ejemplo Claude:**
> "¿Qué tablas hay en la base de datos?"

### 2. `describe-table`
Describe la estructura de una tabla (columnas, tipos, relaciones).

**Ejemplo Claude:**
> "Describe la tabla reloj_fichador_horas_trabajadas"

### 3. `query`
Ejecuta consultas SQL de solo lectura (SELECT).

**Ejemplo Claude:**
> "Muéstrame los 10 operarios más recientes"

**SQL generado:**
```sql
SELECT * FROM reloj_fichador_operario
ORDER BY id DESC
LIMIT 10;
```

### 4. `get-schema`
Obtiene el esquema completo de la base de datos.

**Ejemplo Claude:**
> "Muéstrame el esquema completo de la base de datos"

---

## 🔒 Seguridad

### Permisos del Usuario

El usuario `sistemas` tiene permisos en PostgreSQL. Para mayor seguridad, puedes crear un usuario de solo lectura:

```sql
-- Conectarse a PostgreSQL
docker compose exec db_postgres psql -U sistemas -d docker_horesdb_pg

-- Crear usuario de solo lectura
CREATE USER claude_readonly WITH PASSWORD 'lectura_segura_2024';

-- Otorgar permisos de solo lectura
GRANT CONNECT ON DATABASE docker_horesdb_pg TO claude_readonly;
GRANT USAGE ON SCHEMA public TO claude_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO claude_readonly;

-- Para nuevas tablas
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO claude_readonly;
```

Luego actualiza la configuración MCP:

```json
"postgresql://claude_readonly:lectura_segura_2024@localhost:54321/docker_horesdb_pg"
```

### Limitaciones del Servidor MCP

- ✅ **Permite:** SELECT, EXPLAIN, SHOW
- ❌ **Bloquea:** INSERT, UPDATE, DELETE, DROP, ALTER, CREATE

Esto protege tus datos de modificaciones accidentales.

---

## 🐛 Troubleshooting

### Error: "Could not connect to database"

**Causa:** PostgreSQL no está corriendo o no es accesible.

**Solución:**
```bash
# Verificar estado
docker compose ps db_postgres

# Reiniciar si es necesario
docker compose restart db_postgres

# Ver logs
docker compose logs db_postgres
```

### Error: "Authentication failed"

**Causa:** Credenciales incorrectas.

**Solución:**
Verifica las credenciales en `.env`:
```bash
grep POSTGRES /home/leandro/Proyectos_Docker/Reloj_fichador/.env
```

### Error: "npx not found"

**Causa:** Node.js no está en el PATH.

**Solución:**
```bash
# Verificar Node.js
which node
node --version

# Si no está, cargar NVM
source ~/.nvm/nvm.sh
```

### Error: "Connection timeout"

**Causa:** Puerto bloqueado por firewall.

**Solución:**
```bash
# Verificar que el puerto 54321 esté abierto
sudo netstat -tlnp | grep 54321

# O con ss
ss -tlnp | grep 54321
```

### Claude Code no reconoce el servidor MCP

**Soluciones:**

1. **Reiniciar Claude Code** completamente
2. Verificar que el archivo de configuración esté en la ubicación correcta
3. Revisar logs de Claude Code (si están disponibles)
4. Probar ejecutando el servidor manualmente primero

---

## 📊 Ejemplos de Consultas Útiles

### Análisis de Asistencia

```
Muéstrame los operarios que han fichado hoy
```

```
¿Cuántos registros de entrada hay esta semana?
```

### Análisis de Horas

```
Dame un resumen de horas extras por operario en octubre 2025
```

```
Compara las horas normales vs nocturnas del último mes
```

### Inspección de Datos

```
Muéstrame la estructura de todas las tablas que empiezan con "reloj_fichador_"
```

```
¿Cuántos registros hay en cada tabla principal?
```

### Relaciones

```
Explica las relaciones entre las tablas operario, registro_diario y horas_trabajadas
```

---

## 🚀 Ventajas de Usar MCP

1. **Consultas en Lenguaje Natural**
   - No necesitas escribir SQL
   - Claude traduce tus preguntas a SQL automáticamente

2. **Exploración Interactiva**
   - Descubre datos sin conocer la estructura exacta
   - Pregunta y refina iterativamente

3. **Análisis Rápido**
   - Obtén insights sin escribir scripts complejos
   - Genera visualizaciones conceptuales

4. **Documentación Automática**
   - Claude puede documentar el esquema
   - Explica relaciones y estructura

5. **Seguridad**
   - Solo lectura por defecto
   - Sin riesgo de modificar datos accidentalmente

---

## 📚 Recursos Adicionales

- **Documentación Oficial MCP:** https://docs.anthropic.com/en/docs/claude-code/mcp
- **Servidor PostgreSQL MCP:** https://github.com/modelcontextprotocol/servers
- **Enhanced PostgreSQL MCP:** https://www.npmjs.com/package/enhanced-postgres-mcp-server

---

## ✨ Próximos Pasos

1. ✅ Servidor MCP instalado
2. ⏳ Configurar en Claude Code
3. ⏳ Probar consultas básicas
4. ⏳ Explorar el esquema de la base de datos
5. ⏳ (Opcional) Crear usuario de solo lectura para mayor seguridad

---

**¿Preguntas?** Prueba preguntándome:
- "¿Cómo verifico que MCP esté funcionando?"
- "Muéstrame ejemplos de consultas más avanzadas"
- "¿Cómo puedo conectar también a MySQL con MCP?"

---

**Última actualización:** 2025-10-13
