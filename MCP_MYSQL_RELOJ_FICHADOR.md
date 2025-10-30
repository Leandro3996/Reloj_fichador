# MCP MySQL - Reloj Fichador

> Documentación de la configuración del servidor MCP para MySQL en el proyecto Reloj Fichador

## 📍 Ubicación de Configuración

```
~/.claude.json → mcpServers → mysql-reloj-fichador
```

## ⚙️ Detalles de Conexión

| Campo | Valor |
|-------|-------|
| **Host** | localhost |
| **Puerto** | 53306 |
| **Usuario** | root |
| **Contraseña** | S1st3mas.1999 |
| **Base de Datos** | docker_horesdb |

**Variables de Entorno (exactas):**
```
MYSQL_HOST=127.0.0.1
MYSQL_PORT=53306
MYSQL_USER=root
MYSQL_PASS=S1st3mas.1999
MYSQL_DB=docker_horesdb
```

## 🛠️ Herramientas Disponibles

### 1. `list-tables`
Obtiene todas las tablas de la base de datos.

**Uso:**
```
"Muestra todas las tablas de la base de datos"
```

**Respuesta:** Lista de tablas presentes en `docker_horesdb`

### 2. `describe-table`
Obtiene la estructura y campos de una tabla específica.

**Uso:**
```
"Describe la estructura de la tabla operario"
"Muestra los campos de RegistroDiario"
```

**Respuesta:**
```
Campo          | Tipo              | Null | Key | Default | Extra
-------        | ----------------  | ---- | --- | ------- | -----
id             | int(11)          | NO   | PRI | NULL    | auto_increment
nombre         | varchar(255)     | NO   |     | NULL    |
```

### 3. `query`
Ejecuta consultas SELECT contra la base de datos.

**Uso:**
```
"Obtén el total de operarios registrados"
"Muestra los registros de hoy en RegistroDiario"
"Calcula las horas totales trabajadas por operario"
```

**Respuesta:** Resultados en formato tabular

### 4. `execute`
Ejecuta consultas que modifican datos (INSERT, UPDATE, DELETE).

**⚠️ Uso Cuidadoso:**
```
"Actualiza el estado del operario con ID 5"
"Inserta un nuevo registro de asistencia"
```

## 📊 Tablas Principales en `docker_horesdb`

Basándose en el modelo de Django, las tablas principales son:

- `reloj_fichador_operario` - Información de empleados
- `reloj_fichador_registrodiario` - Registros de entrada/salida
- `reloj_fichador_horas_trabajadas` - Horas calculadas por tipo
- `reloj_fichador_area` - Áreas de trabajo
- `reloj_fichador_horario` - Horarios de trabajo
- `reloj_fichador_licencia` - Licencias/permisos
- `reloj_fichador_registroasistencia` - Resumen de asistencia

## 🔗 Ejemplos Prácticos

### Obtener información de un operario
```
query: "SELECT id, nombre, apellido FROM reloj_fichador_operario WHERE id = 1"
```

### Ver registros de hoy
```
query: "SELECT * FROM reloj_fichador_registrodiario WHERE DATE(fecha_entrada) = CURDATE()"
```

### Calcular horas totales por operario
```
query: "SELECT operario_id, SUM(horas_normales) as total_normales
        FROM reloj_fichador_horas_trabajadas
        GROUP BY operario_id"
```

### Registrar nueva entrada
```
execute: "INSERT INTO reloj_fichador_registrodiario (operario_id, fecha_entrada, tipo_movimiento)
          VALUES (1, NOW(), 'ENTRADA')"
```

## 🔒 Consideraciones de Seguridad

- ✅ Las herramientas están configuradas con permisos por defecto (`alwaysAllow`)
- ✅ Se recomienda revisar cambios antes de ejecutar en producción
- ⚠️ Las contraseñas están almacenadas en `~/.claude.json` - manejar con cuidado
- ✅ Los cambios se registran en los logs de Docker: `docker compose logs db`

## 🧪 Verificar Conexión

Para probar que todo funciona:

```bash
# Ver si MySQL está corriendo
docker compose ps | grep db

# Acceder directamente a MySQL
docker compose exec db mysql -u root -p docker_horesdb

# Ejecutar una consulta de prueba
docker compose exec db mysql -u root -p docker_horesdb -e "SELECT COUNT(*) as total FROM reloj_fichador_operario;"
```

## 📝 Notas Importantes

- La contraseña de MySQL debe coincidir con la configurada en el archivo `.env` del proyecto
- El MCP está configurado con permisos totales (`alwaysAllow`) - no requiere confirmación
- Las consultas se ejecutan directamente contra la base de datos en vivo
- Se recomienda usar `query` (SELECT) para exploración y `execute` (INSERT/UPDATE/DELETE) con cuidado

## 🚀 Cómo Iniciar a Usarlo

1. Asegúrate de que Docker Compose está en ejecución:
   ```bash
   docker compose up -d
   ```

2. En Claude Code, simplemente menciona la base de datos:
   ```
   "Muestra todas las tablas de la base de datos"
   ```

3. Claude Code usará automáticamente el MCP `mysql-reloj-fichador` para conectarse

## 📚 Referencias

- [Django Models - Reloj Fichador](apps/reloj_fichador/models.py)
- [Docker Compose Config](docker-compose.yml)
- [Instrucciones Globales](~/.claude/CLAUDE.md)
- [Configuración Global de MCPs](~/.claude/CONFIGURACION_GLOBAL.md)

---

**Última actualización:** 2025-10-30
**Versión:** 1.0
**Estado:** ✅ Activo
