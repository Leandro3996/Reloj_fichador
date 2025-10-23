# CLAUDE.md - Reloj Fichador

> **📍 CONFIGURACIÓN GLOBAL:** Este proyecto usa MCPs centralizados en `~/.claude.json`
>
> **Instrucciones Globales:** `~/.claude/CLAUDE.md` (⭐ LEER PRIMERO)
>
> **Documentación de MCPs:** Ver archivos en `~/.claude/`:
> - `CONFIGURACION_GLOBAL.md` - Guía completa de MCPs
> - `ANADIR_NUEVOS_MCPS.md` - Cómo añadir nuevas BDs
> - `MULTIPLES_CONFIGURACIONES.md` - Opciones avanzadas

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
- **Admin Interface**: Django Unfold 0.42.0 (modern admin theme)
- **MCP Servers**: Context7, BrowserMCP, Chrome DevTools (PostgreSQL MCP obsoleto)

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

#### 🔗 CONFIGURACIÓN GLOBAL DE MCPs

**⭐ IMPORTANTE:** Todos los MCPs están configurados centralmente en `~/.claude.json`

No necesitas configurar nada en este proyecto. Los MCPs ya están disponibles globalmente:

| MCP | Base de Datos | Ubicación | Estado |
|-----|---------------|-----------|--------|
| `postgres-reloj-fichador` | docker_horesdb_pg | localhost:54321 | ⚠️ Obsoleto (PostgreSQL eliminado) |
| `context7` | (documentación) | - | ✅ Activo |
| `browsermcp` | (navegador) | - | ✅ Activo |
| `chrome-devtools` | (Chrome) | - | ✅ Activo |

**Documentación Completa:**
- Instrucciones globales: `~/.claude/CLAUDE.md`
- Configuración: `~/.claude/CONFIGURACION_GLOBAL.md`
- Cómo añadir nuevos MCPs: `~/.claude/ANADIR_NUEVOS_MCPS.md`

---

**⚠️ NOTA IMPORTANTE - PostgreSQL Obsoleto:**
PostgreSQL ha sido eliminado como base de datos del proyecto. El MCP `postgres-reloj-fichador` se mantiene configurado para futuros proyectos que utilicen PostgreSQL, pero **NO ES UTILIZADO** en este proyecto. Para consultas a la base de datos en este proyecto, usar **MySQL directamente** con comandos Docker o herramientas SQL estándar.


## Important Files and Locations

### Configuration
- `mantenedor/settings.py` - Django settings with timezone configuration (USE_TZ=True for timezone-aware datetimes)
- `mantenedor/utils.py` - Utility functions for Unfold callbacks (environment badges, dashboard statistics)
- `docker-compose.yml` - Service orchestration
- `.env` - Environment variables (not in repo)
- `nginx.conf` - Web server configuration
- `mcp_postgres_config.json` - MCP server configuration for Claude Code

### Documentation
- `documentacion/` - Comprehensive project documentation
- `documentacion/analista/` - System analysis, design guides, and technical documentation
- `documentacion/django-unfold-manual.md` - Complete guide for Django Unfold implementation

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
- **Django Unfold Theme**: Modern, responsive interface with dark mode support
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

## Django Unfold Implementation

### Overview
The project uses **Django Unfold 0.42.0** as a modern admin theme, replacing the default Django admin interface with a clean, responsive, and feature-rich interface.

### Key Features Implemented
- **Modern UI**: Clean, responsive design with dark mode support
- **Custom Navigation**: Hierarchical sidebar menu with Material Design icons
- **Dashboard**: Real-time statistics showing active operators, daily records, and attendance
- **Environment Badge**: Visual indicator showing Development/Production environment
- **Integration**: Seamless integration with django-import-export and django-simple-history
- **Personalization**: Custom colors, logo, and site branding

### Configuration Location
All Unfold configuration is centralized in `mantenedor/settings.py` under the `UNFOLD` dictionary (lines 145-377):
- **SITE_TITLE**: "Reloj Fichador - Administración"
- **SITE_HEADER**: "Sistema de Control de Asistencia"
- **THEME**: Dark mode by default
- **SIDEBAR**: Custom navigation with 7 main sections
- **COLORS**: Purple-based color scheme (primary color: #A855F7)

### Admin Classes Structure
All admin classes in `apps/reloj_fichador/admin.py` inherit from `UnfoldModelAdmin`:
- 15 model admins fully migrated to Unfold
- 2 configuration admins with restricted permissions
- Custom user and group admins integrated with Unfold
- Historical tracking admins for audit purposes

### Utility Functions
Located in `mantenedor/utils.py`:
- `environment_callback()`: Shows environment badge (Development/Production)
- `dashboard_callback()`: Provides real-time statistics for the dashboard

### Access
Admin interface accessible at: `http://localhost:58000/admin/` (or configured domain)

### Maintenance
When adding new models:
1. Inherit from `UnfoldModelAdmin` instead of `admin.ModelAdmin`
2. Import: `from unfold.admin import ModelAdmin as UnfoldModelAdmin`
3. Use `@admin.register(YourModel)` decorator or `admin.site.register()`
4. Collect static files: `docker compose exec web python manage.py collectstatic --noinput`

For detailed Unfold configuration options, see `documentacion/django-unfold-manual.md`