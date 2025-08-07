# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django-based time tracking system ("Reloj Fichador") deployed with Docker. The system manages employee attendance, calculates different types of working hours (normal, night, overtime, holiday), and generates comprehensive reports.

## Architecture

### Core Application
- **Django Project**: `mantenedor/` (main settings and configuration)
- **Main App**: `apps/reloj_fichador/` (contains all business logic)
- **Database**: MySQL 8.4.0
- **Task Queue**: Celery with Redis as broker
- **Web Server**: Nginx with Gunicorn
- **Deployment**: Docker Compose

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
```bash
# Backup database
docker compose exec db mysqldump -u root -p docker_horesdb > backup.sql

# Restore database
docker compose exec -T db mysql -u root -p docker_horesdb < backup.sql

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

## Important Files and Locations

### Configuration
- `mantenedor/settings.py` - Django settings with timezone configuration
- `docker-compose.yml` - Service orchestration
- `.env` - Environment variables (not in repo)
- `nginx.conf` - Web server configuration

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
All datetime operations should use Argentina timezone:
```python
import pytz
argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
```

### Database Connection Issues
Check environment variables in docker-compose.yml and ensure MySQL container is healthy.

### Celery Not Processing Tasks
Verify Redis connection and check celery logs:
```bash
docker compose logs celery
docker compose exec redis redis-cli ping
```

### Import/Export Issues
The system has sophisticated import/export functionality in admin.py:230-520. Check RegistroDiarioResource for data format requirements.