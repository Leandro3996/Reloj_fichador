# CLAUDE.md - Reloj Fichador

> **📍 CONFIGURACIÓN DE MCPs:** Este proyecto usa configuración mixta
> - **MCPs Globales:** `~/.claude.json` (Context7, BrowserMCP, Chrome DevTools)
> - **MCP Local:** `.mcp.json` (MySQL del proyecto)
>
> **Instrucciones Globales:** `~/.claude/CLAUDE.md` (⭐ LEER PRIMERO)
>
> **Documentación de MCPs:** Ver archivos en `~/.claude/`:
> - `CONFIGURACION_GLOBAL.md` - Guía completa de MCPs globales
> - `ANADIR_NUEVOS_MCPS.md` - Cómo añadir nuevas BDs
> - `.mcp.json` - Configuración local del proyecto (MySQL)

---

## 🔄 Bucle de Verificación (Verificación Obligatoria)

Este proyecto sigue el **protocolo global de verificación** de Claude Code:

**Ciclo:** PLAN → EXEC → VERIFY → CORRECT (si falla)

**Documentación Completa:** Ver `~/.claude/CLAUDE.md` - Sección "Bucle de Verificación"

**Resumen:**
- ✅ Usar TodoWrite para planificar pasos
- ✅ Siempre verificar que las tareas funcionan
- ✅ Ejecutar tests después de cambios
- ✅ Capturar evidencia (logs, screenshots)
- ❌ NUNCA asumir que algo funcionó sin probar

---

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django-based time tracking system ("Reloj Fichador") deployed with Docker. The system manages employee attendance, calculates different types of working hours (normal, night, overtime, holiday), and generates comprehensive reports.

## Architecture

### Core Application
- **Django Project**: `mantenedor/` (main settings and configuration)
- **Main App**: `apps/reloj_fichador/` (contains all business logic)
- **Database**: MySQL 8.4.0 (primary)
- **Task Queue**: Celery with Redis as broker
- **Web Server**: Nginx with Gunicorn
- **Deployment**: Docker Compose
- **Admin Interface**: django-admin-interface (customizable admin theme)
- **MCP Servers**: MySQL (local), Context7, BrowserMCP, Chrome DevTools

### Key Models (apps/reloj_fichador/models.py)

1. **Operario** - Employee information with historical tracking
2. **RegistroDiario** - Daily attendance records (entrada/salida movements)
3. **Horas_trabajadas** - Calculated working hours (normal, night, overtime)
4. **Area/Horario** - Work areas and schedule definitions
5. **Licencia** - Leave/license documents with file attachments
6. **RegistroAsistencia** - Attendance summary with justification tracking

### Time Calculation Rules (Critical Business Logic)
- **Normal Hours**: 06:00 to 20:00
- **Night Hours**: 20:00 to 06:00 next day
- **Entry Rounding**: Round to nearest 15-minute interval (configurable via ConfiguracionRedondeo)
- **Exit Rounding**: Round down to hour (configurable via ConfiguracionRedondeoSalida)
- **Overtime**: Hours exceeding 8 per day, rounded to 30-minute blocks
- **Timezone**: All times in 'America/Argentina/Buenos_Aires'

## Common Development Commands

### Docker Operations
```bash
# Start all services
docker compose up -d

# View logs
docker compose logs web
docker compose logs celery

# Access Django shell
docker compose exec web python manage.py shell

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# Collect static files
docker compose exec web python manage.py collectstatic --noinput
```

### Testing
```bash
# Run all tests with SQLite (faster)
python manage.py test --settings=tests_utils.sqlite_settings

# Run specific test module
python manage.py test apps.reloj_fichador.tests.test_models

# Run with MySQL (full environment)
docker compose exec web python manage.py test
```

### Database Operations

#### MySQL (Primary Database)
```bash
# Backup MySQL database
docker compose exec db mysqldump -u root -p docker_horesdb > backup_mysql.sql

# Restore MySQL database
docker compose exec -T db mysql -u root -p docker_horesdb < backup_mysql.sql

# Access MySQL shell
docker compose exec db mysql -u root -p docker_horesdb
```

### Celery Tasks
```bash
# Check Celery worker status
docker compose exec celery celery -A mantenedor status

# Check scheduled tasks
docker compose exec celery-beat celery -A mantenedor inspect active

# Restart Celery services
docker compose restart celery celery-beat
```

### MCP (Model Context Protocol) for Claude Code

#### 🔗 CONFIGURACIÓN DE MCPs

Este proyecto utiliza una **configuración mixta** de MCPs:

**MCPs Globales** (configurados en `~/.claude.json`):
- `context7` - Documentación de bibliotecas
- `browsermcp` - Automatización web
- `chrome-devtools` - Análisis de rendimiento

**MCPs Locales** (configurados en `.mcp.json` del proyecto):
- `mysql-reloj-fichador` - Base de datos MySQL del proyecto

| MCP | Base de Datos | Ubicación | Estado |
|-----|---------------|-----------|--------|
| `mysql-reloj-fichador` | docker_horesdb | localhost:53306 | ✅ Activo (Local) |
| `context7` | (documentación) | - | ✅ Activo (Global) |
| `browsermcp` | (navegador) | - | ✅ Activo (Global) |
| `chrome-devtools` | (Chrome) | - | ✅ Activo (Global) |

**Documentación Completa:**
- Instrucciones globales: `~/.claude/CLAUDE.md`
- Configuración local: `.mcp.json` (en raíz del proyecto)
- MCP MySQL: https://github.com/benborla/mcp-server-mysql

---

### 🎯 MySQL MCP - Reloj Fichador

**Configuración Local:** Ver archivo `.mcp.json` en la raíz del proyecto

**Credenciales de Conexión:**
```
Host: localhost
Puerto: 53306
Usuario: root
Password: S1st3mas.1999
Database: docker_horesdb
```

**Paquete NPM:** `@benborla29/mcp-server-mysql`

**Herramientas Disponibles:**
- `mysql_query` - Ejecutar consultas SQL (solo SELECT, modo lectura)

**Permisos (Configuración Actual):**
- INSERT: ❌ Deshabilitado
- UPDATE: ❌ Deshabilitado
- DELETE: ❌ Deshabilitado
- SELECT: ✅ Habilitado (solo lectura)

**Ejemplo de Uso:**
```
"Muestra todas las tablas de la base de datos"
"¿Cuántos operarios hay registrados?"
"Obtén todos los registros de asistencia de hoy"
"Muestra la estructura de la tabla Horas_trabajadas"
```

**Nota de Seguridad:** Las operaciones de escritura están deshabilitadas para proteger los datos. Solo se permiten consultas de lectura (SELECT).


## Important Files and Locations

### Configuration
- `mantenedor/settings.py` - Django settings with timezone configuration (USE_TZ=True for timezone-aware datetimes)
- `mantenedor/utils.py` - Utility functions and callbacks
- `docker-compose.yml` - Service orchestration
- `.env` - Environment variables (not in repo)
- `nginx.conf` - Web server configuration
- `mcp_postgres_config.json` - MCP server configuration for Claude Code

### Documentation
- `documentacion/` - Comprehensive project documentation
- `documentacion/analista/` - System analysis, design guides, and technical documentation

### Business Logic
- `apps/reloj_fichador/models.py` - Core data models and time calculations (LINE 61-140: redondear_entrada/salida functions, LINE 504-562: Horas_trabajadas.calcular_horas_trabajadas)
- `apps/reloj_fichador/admin.py` - Django admin with extensive customizations for reports
- `apps/reloj_fichador/views.py` - API endpoints for attendance recording
- `apps/reloj_fichador/signals.py` - Automatic hour recalculation triggers

### Templates and Static Files
- `templates/` - HTML templates including error pages
- `static/` - CSS, images, and JavaScript files
- `staticfiles/` - Collected static files for production

### Testing Infrastructure
- `tests_utils/` - Test utilities and database configurations
- `apps/reloj_fichador/tests/` - Comprehensive test suite

## Development Guidelines

### Working with Time Calculations
The time calculation logic is complex and mission-critical. Key functions:
- `redondear_entrada()` and `redondear_salida()` in models.py:61-106
- `calcular_horas_por_franjas()` in models.py:108-140
- `Horas_trabajadas.calcular_horas_trabajadas()` in models.py:504-562

Always run tests when modifying time calculations:
```bash
python manage.py test apps.reloj_fichador.tests.test_calculo_horas
```

### Database Migrations
When modifying models, create and apply migrations:
```bash
docker compose exec web python manage.py makemigrations reloj_fichador
docker compose exec web python manage.py migrate
```

### Admin Interface Customizations
The Django admin is heavily customized with:
- **django-admin-interface**: Customizable theme with dark mode support
- Custom list displays and filters
- Export functionality (PDF/Excel)
- Import/export capabilities for bulk operations
- Historical tracking via django-simple-history
- Custom navigation sidebar with icons
- Personalized dashboard with real-time statistics

### Error Handling and Logging
- Logs are stored in `logs/` directory
- Custom middleware handles errors and permissions
- Comprehensive logging configured in settings.py:191-256

### Signal Handlers
The system uses Django signals for automatic recalculation:
- `actualizar_horas_despues_de_guardar` in signals.py
- Triggered after RegistroDiario save/delete operations

## Security Considerations

- HTTPS configuration in settings.py:145-190
- CSRF protection with custom middleware
- Permission-based admin access
- File upload validation for licenses
- Custom user admin with restricted permissions

## Performance Notes

- Database queries optimized with select_related/prefetch_related
- Celery for background task processing
- Redis for caching and task queuing  
- Automatic database backups every 30 minutes

## Common Troubleshooting

### Time Zone Issues
**IMPORTANT:** The project uses `USE_TZ = True` in settings.py, meaning Django stores all datetimes as timezone-aware UTC internally and converts to the configured timezone (America/Argentina/Buenos_Aires) for display and calculations.

All datetime operations should use timezone-aware datetimes:
```python
import pytz
from django.utils import timezone

# Get current time (timezone-aware)
now = timezone.now()

# Convert to Argentina timezone
argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
local_time = now.astimezone(argentina_tz)
```

**Key points:**
- Database stores datetimes in UTC
- MySQL connection uses timezone configured in Django settings (America/Argentina/Buenos_Aires)
- All calculations in models.py handle timezone conversion automatically
- When creating datetime objects, always make them timezone-aware

### Database Connection Issues
Check environment variables in docker-compose.yml and ensure MySQL container is healthy:
```bash
# Check MySQL status
docker compose ps db

# View MySQL logs
docker compose logs db

# Test connection
docker compose exec db mysql -u root -p -e "SELECT 1;"
```

### Celery Not Processing Tasks
Verify Redis connection and check celery logs:
```bash
docker compose logs celery
docker compose exec redis redis-cli ping
```

### Import/Export Issues
The system has sophisticated import/export functionality in admin.py:230-520. Check RegistroDiarioResource for data format requirements.

## Additional Context

### Project Language and Documentation Standards
This project follows Spanish (Castellano de España) as the primary language for documentation and communication. All technical documentation, analysis, and system design documents are maintained in the `documentacion/analista/` directory structure.

The project emphasizes:
- Continuous improvement of existing processes
- Comprehensive documentation of all technical decisions
- Design consistency across interfaces (typography, colors, icons)
- Systematic organization of documentation for future reference

### Development Environment
- Primary OS: Linux (Ubuntu/Debian-based)
- Shell: Bash for scripting and automation
- All scripts and automation tools are documented in `documentacion/analista/scripts/`

For complete project rules and guidelines, see `.cursor/rules/instrucciones.mdc`

## Django Admin Interface

### Overview
The project uses **django-admin-interface** as a customizable admin theme. This package allows visual customization of the Django admin directly from the admin panel.

### Key Features
- **Customizable UI**: Colors, logo, and theme configurable from admin
- **Dark mode support**: Toggle between light and dark themes
- **Logo configuration**: Upload logo directly from Admin > Admin Interface > Themes
- **Integration**: Works seamlessly with django-import-export and django-simple-history

### Configuration
The theme is configured directly from the admin panel:
1. Go to Admin > Admin Interface > Themes
2. Edit the active theme to customize colors, logo, title, etc.

### Access
Admin interface accessible at: `http://localhost:58000/admin/` (or configured domain)

---

## 🚀 Migración de Commits a Producción

### Contexto
- **Desarrollo (local)**: `/home/leandro/Proyectos_Docker/Reloj_fichador`
- **Producción (remoto montado)**: `/home/leandro/debian-home/sistemas/Docker_proyectos/Reloj_fichador`
- **Servidor producción**: `192.168.10.39` (SSH: `sistemas@192.168.10.39`)

### Procedimiento Seguro de Migración

#### 1. Análisis previo
```bash
# Ver commits a migrar (ejemplo: commits de hoy)
git log --oneline --since="2025-12-30 00:00:00" --until="2025-12-31 00:00:00"

# Ver archivos afectados
git diff --name-only COMMIT_INICIAL^..COMMIT_FINAL

# Verificar estado en producción
cd /home/leandro/debian-home/sistemas/Docker_proyectos/Reloj_fichador
git status
```

#### 2. Detectar conflictos potenciales
Si producción tiene cambios sin commitear en los mismos archivos:
```bash
# Ver diferencias en producción
cd /home/leandro/debian-home/sistemas/Docker_proyectos/Reloj_fichador
git diff archivo.py
```

#### 3. Crear backup de cambios en producción
```bash
cd /home/leandro/debian-home/sistemas/Docker_proyectos/Reloj_fichador
git diff > /tmp/backup_produccion_$(date +%Y%m%d_%H%M%S).patch
```

#### 4. Estrategias de migración

**Opción A: Cherry-pick (si las ramas son compatibles)**
```bash
# Crear patches desde desarrollo
git format-patch -N COMMIT_HASH -o /tmp/commits/

# Aplicar en producción
cd /home/leandro/debian-home/sistemas/Docker_proyectos/Reloj_fichador
git am /tmp/commits/*.patch
```

**Opción B: Copia directa de archivos (si cherry-pick falla)**
```bash
# Copiar archivos específicos
cp apps/reloj_fichador/admin.py /home/leandro/debian-home/sistemas/Docker_proyectos/Reloj_fichador/apps/reloj_fichador/admin.py

# Crear commit consolidado en producción
cd /home/leandro/debian-home/sistemas/Docker_proyectos/Reloj_fichador
git add .
git commit -m "feat: Descripción de los cambios migrados

🔄 Trasladado desde rama [nombre-rama-desarrollo]"
```

#### 5. Reiniciar servicios en producción
```bash
# Via SSH
ssh sistemas@192.168.10.39 "cd /home/sistemas/Docker_proyectos/Reloj_fichador && docker compose restart web"

# Verificar estado
ssh sistemas@192.168.10.39 "cd /home/sistemas/Docker_proyectos/Reloj_fichador && docker compose ps"
```

#### 6. Verificación post-migración
```bash
# Verificar respuesta HTTP
curl -s -o /dev/null -w "%{http_code}" http://192.168.10.39:5080/admin/

# Verificar logs sin errores
ssh sistemas@192.168.10.39 "cd /home/sistemas/Docker_proyectos/Reloj_fichador && docker compose logs web --tail 20"
```

### Checklist de Migración

- [ ] Identificar commits a migrar
- [ ] Verificar estado de producción (cambios sin commit)
- [ ] Crear backup si hay cambios sin commit
- [ ] Descartar o integrar cambios existentes
- [ ] Aplicar commits (cherry-pick o copia directa)
- [ ] Crear commit en producción
- [ ] Reiniciar servicios Docker
- [ ] Verificar funcionamiento (HTTP + logs)
- [ ] Probar funcionalidad específica en navegador

### Notas Importantes

1. **Nunca hacer push forzado** en producción
2. **Siempre crear backup** antes de descartar cambios
3. **Si cherry-pick falla**, usar copia directa de archivos
4. **Verificar visualmente** que los cambios funcionan (usar Chrome DevTools MCP)
5. El backup de patches se guarda en `/tmp/` por si necesitas restaurar