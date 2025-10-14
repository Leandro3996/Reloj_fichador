# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django-based time tracking system ("Reloj Fichador") deployed with Docker. The system manages employee attendance, calculates different types of working hours (normal, night, overtime, holiday), and generates comprehensive reports.

## Architecture

### Core Application
- **Django Project**: `mantenedor/` (main settings and configuration)
- **Main App**: `apps/reloj_fichador/` (contains all business logic)
- **Database**: PostgreSQL 15 (primary), MySQL 8.4.0 (legacy/secondary)
- **Task Queue**: Celery with Redis as broker
- **Web Server**: Nginx with Gunicorn
- **Deployment**: Docker Compose
- **MCP Server**: Enhanced PostgreSQL MCP for Claude Code integration

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

#### PostgreSQL (Primary Database)
```bash
# Backup database
docker compose exec db_postgres pg_dump -U sistemas docker_horesdb_pg > backup.sql

# Restore database
docker compose exec -T db_postgres psql -U sistemas docker_horesdb_pg < backup.sql

# Access PostgreSQL shell
docker compose exec db_postgres psql -U sistemas docker_horesdb_pg

# Check database status
docker compose exec db_postgres psql -U sistemas -d docker_horesdb_pg -c "SELECT version();"
```

#### MySQL (Legacy/Secondary Database)
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

The project includes MCP configuration for direct database queries from Claude Code using natural language.

#### Quick Setup
The MCP configuration file is already included: `mcp_postgres_config.json`

To use MCP with Claude Code:
1. Ensure PostgreSQL is running: `docker compose up -d db_postgres`
2. Verify Node.js is installed: `node --version` (requires v18+)
3. The MCP server will auto-connect when you use Claude Code

#### Example Queries
Once configured, you can ask Claude Code:
- "Show me the last 10 employee entries"
- "How many daily records are there in October?"
- "Describe the structure of the horas_trabajadas table"
- "Summarize overtime hours by employee for last month"

#### MCP Configuration Details
- **Server**: `enhanced-postgres-mcp-server` (installed via npx)
- **Database**: `docker_horesdb_pg` on port `54321`
- **Permissions**: Read-only (SELECT queries only)
- **Timezone**: America/Argentina/Buenos_Aires

For detailed setup instructions, see: `CONFIGURACION_MCP_POSTGRESQL.md`

#### Troubleshooting MCP
```bash
# Test MCP connection manually
npx -y enhanced-postgres-mcp-server \
  "postgresql://sistemas:S1st3mas2024@localhost:54321/docker_horesdb_pg"

# Verify PostgreSQL is accessible
docker compose exec db_postgres psql -U sistemas -d docker_horesdb_pg -c "SELECT 1;"
```

## Important Files and Locations

### Configuration
- `mantenedor/settings.py` - Django settings with timezone configuration (USE_TZ=True for timezone-aware datetimes)
- `docker-compose.yml` - Service orchestration
- `.env` - Environment variables (not in repo)
- `nginx.conf` - Web server configuration
- `mcp_postgres_config.json` - MCP server configuration for Claude Code

### Documentation
- `documentacion/` - Comprehensive project documentation
- `documentacion/analista/` - System analysis, design guides, and technical documentation
- `CONFIGURACION_MCP_POSTGRESQL.md` - Complete MCP setup guide
- `POSTGRESQL_SETUP.md` - PostgreSQL migration and setup guide

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
- Custom list displays and filters
- Export functionality (PDF/Excel)
- Import/export capabilities for bulk operations
- Historical tracking via django-simple-history

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
- PostgreSQL connection uses `timezone=America/Argentina/Buenos_Aires` in connection options
- All calculations in models.py handle timezone conversion automatically
- When creating datetime objects, always make them timezone-aware

### Database Connection Issues
Check environment variables in docker-compose.yml and ensure PostgreSQL container is healthy:
```bash
# Check PostgreSQL status
docker compose ps db_postgres

# View PostgreSQL logs
docker compose logs db_postgres

# Test connection
docker compose exec db_postgres psql -U sistemas -d docker_horesdb_pg -c "SELECT 1;"
```

For MySQL (legacy) connection issues, check the `db` container instead.

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