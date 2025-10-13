# Migración de MySQL a PostgreSQL - Sistema Reloj Fichador

## Resumen

Este documento describe el proceso de migración de la base de datos del sistema Reloj Fichador de MySQL 8.4.0 a PostgreSQL 16.

## Tabla de Contenidos

1. [Arquitectura Dual](#arquitectura-dual)
2. [Configuración Realizada](#configuración-realizada)
3. [Proceso de Migración](#proceso-de-migración)
4. [Verificación de Datos](#verificación-de-datos)
5. [Cambio de Base de Datos Principal](#cambio-de-base-de-datos-principal)
6. [Rollback](#rollback)
7. [Optimizaciones PostgreSQL](#optimizaciones-postgresql)

---

## Arquitectura Dual

El sistema ahora soporta **dos bases de datos simultáneamente**:

- **MySQL** (default): Base de datos actual, continúa funcionando normalmente
- **PostgreSQL** (postgres): Nueva base de datos clon

### Ventajas de la Arquitectura Dual

- ✅ Sin downtime durante la migración
- ✅ Posibilidad de probar PostgreSQL sin afectar producción
- ✅ Rollback inmediato si hay problemas
- ✅ Comparación de rendimiento entre motores

---

## Configuración Realizada

### 1. Docker Compose (`docker-compose.yml`)

Se agregó un nuevo servicio PostgreSQL:

```yaml
db_postgres:
  image: postgres:16-alpine
  restart: unless-stopped
  environment:
    POSTGRES_DB: "${POSTGRES_DATABASE}"
    POSTGRES_USER: "${POSTGRES_USER}"
    POSTGRES_PASSWORD: "${POSTGRES_PASSWORD}"
    PGDATA: /var/lib/postgresql/data/pgdata
    TZ: America/Argentina/Buenos_Aires
  volumes:
    - postgres_data:/var/lib/postgresql/data
  ports:
    - "54321:5432"
  networks:
    - app_network_fichador
  command: >
    postgres
    -c timezone=America/Argentina/Buenos_Aires
    -c log_timezone=America/Argentina/Buenos_Aires
    -c max_connections=200
    -c shared_buffers=256MB
  healthcheck:
    test: [ "CMD-SHELL", "pg_isready -U $POSTGRES_USER -d $POSTGRES_DATABASE" ]
    interval: 5s
    timeout: 5s
    retries: 10
```

**Puertos:**
- MySQL: `53306` (host) → `3306` (contenedor)
- PostgreSQL: `54321` (host) → `5432` (contenedor)

### 2. Variables de Entorno (`.env`)

Se agregaron las siguientes variables:

```bash
# Configuración de PostgreSQL
POSTGRES_DATABASE=docker_horesdb_pg
POSTGRES_USER=sistemas
POSTGRES_PASSWORD=S1st3mas2024
POSTGRES_HOST=db_postgres
POSTGRES_PORT=5432
```

### 3. Django Settings (`mantenedor/settings.py`)

Se configuró el diccionario `DATABASES` con ambas conexiones:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'",
            'charset': 'utf8mb4',
            'connect_timeout': 30,
            'autocommit': True,
            'isolation_level': 'READ COMMITTED',
        },
    },
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DATABASE', 'docker_horesdb_pg'),
        'USER': os.environ.get('POSTGRES_USER', 'sistemas'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'S1st3mas2024'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db_postgres'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        'OPTIONS': {
            'connect_timeout': 30,
            'options': '-c timezone=America/Argentina/Buenos_Aires',
        },
        'CONN_MAX_AGE': 600,
        'ATOMIC_REQUESTS': True,
    }
}
```

### 4. Dependencias (`requirements.txt`)

Se agregó el driver de PostgreSQL:

```
psycopg2-binary==2.9.9
```

### 5. Dockerfile

Se agregó `libpq-dev` para soportar psycopg2:

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    ...
    libpq-dev \
    ...
```

---

## Proceso de Migración

### Paso 1: Iniciar los Servicios

```bash
# Iniciar ambas bases de datos
docker compose up -d db db_postgres

# Verificar que estén saludables
docker compose ps
```

### Paso 2: Reconstruir el Contenedor Web

```bash
# Reconstruir con las nuevas dependencias
docker compose build web

# Iniciar el servicio web
docker compose up -d web
```

### Paso 3: Crear el Esquema en PostgreSQL

```bash
# Ejecutar las migraciones en PostgreSQL
docker compose exec web python manage.py migrate --database=postgres

# Verificar que se crearon todas las tablas
docker compose exec db_postgres psql -U sistemas -d docker_horesdb_pg -c "\dt"
```

### Paso 4: Migrar los Datos

```bash
# Opción 1: Usando el script de migración (RECOMENDADO)
docker compose exec web python migrate_mysql_to_postgres.py

# Opción 2: Usando dumpdata/loaddata de Django (más lento)
docker compose exec web python manage.py dumpdata --database=default --natural-foreign --natural-primary > data.json
docker compose exec web python manage.py loaddata data.json --database=postgres
```

**El script `migrate_mysql_to_postgres.py` realiza:**

1. ✅ Migra los modelos en orden de dependencias (respeta FK)
2. ✅ Preserva los IDs originales
3. ✅ Muestra progreso en tiempo real
4. ✅ Reinicia las secuencias de PostgreSQL
5. ✅ Maneja errores de forma granular
6. ✅ Permite continuar si ya existen datos

---

## Verificación de Datos

### 1. Comparar Conteos

```bash
# MySQL
docker compose exec db mysql -usistemas -pS1st3mas2024 docker_horesdb -e "
SELECT
    'Operarios' as tabla, COUNT(*) as registros FROM reloj_fichador_operario
UNION ALL
SELECT
    'RegistroDiario', COUNT(*) FROM reloj_fichador_registrodiario
UNION ALL
SELECT
    'Horas Trabajadas', COUNT(*) FROM reloj_fichador_horas_trabajadas;
"

# PostgreSQL
docker compose exec db_postgres psql -U sistemas -d docker_horesdb_pg -c "
SELECT
    'Operarios' as tabla, COUNT(*) as registros FROM reloj_fichador_operario
UNION ALL
SELECT
    'RegistroDiario', COUNT(*) FROM reloj_fichador_registrodiario
UNION ALL
SELECT
    'Horas Trabajadas', COUNT(*) FROM reloj_fichador_horas_trabajadas;
"
```

### 2. Probar Consultas Complejas

```bash
docker compose exec web python manage.py shell
```

```python
from apps.reloj_fichador.models import Operario, RegistroDiario, Horas_trabajadas
from datetime import date

# Probar consultas en ambas bases de datos
operarios_mysql = Operario.objects.using('default').filter(activo=True).count()
operarios_pg = Operario.objects.using('postgres').filter(activo=True).count()

print(f"Operarios activos - MySQL: {operarios_mysql}, PostgreSQL: {operarios_pg}")

# Verificar relaciones FK
registro_mysql = RegistroDiario.objects.using('default').select_related('operario').first()
registro_pg = RegistroDiario.objects.using('postgres').select_related('operario').first()

print(f"Registro MySQL: {registro_mysql.operario.nombre if registro_mysql else 'N/A'}")
print(f"Registro PostgreSQL: {registro_pg.operario.nombre if registro_pg else 'N/A'}")
```

### 3. Verificar Integridad Referencial

```bash
docker compose exec db_postgres psql -U sistemas -d docker_horesdb_pg -c "
SELECT
    tc.table_name,
    tc.constraint_name,
    tc.constraint_type
FROM information_schema.table_constraints tc
WHERE tc.constraint_type = 'FOREIGN KEY'
AND tc.table_schema = 'public'
ORDER BY tc.table_name;
"
```

---

## Cambio de Base de Datos Principal

### Opción 1: Cambiar `default` a PostgreSQL (Recomendado después de pruebas)

Editar `mantenedor/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DATABASE', 'docker_horesdb_pg'),
        'USER': os.environ.get('POSTGRES_USER', 'sistemas'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'S1st3mas2024'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db_postgres'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        'OPTIONS': {
            'connect_timeout': 30,
            'options': '-c timezone=America/Argentina/Buenos_Aires',
        },
        'CONN_MAX_AGE': 600,
        'ATOMIC_REQUESTS': True,
    },
    'mysql_backup': {  # Mantener MySQL como backup
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        # ... resto de la configuración
    }
}
```

Luego reiniciar los servicios:

```bash
docker compose restart web celery celery-beat
```

### Opción 2: Usar Variable de Entorno

Agregar a `.env`:

```bash
# Opciones: mysql o postgres
DATABASE_ENGINE=postgres
```

Y modificar `settings.py` para leer esta variable y cambiar dinámicamente.

---

## Rollback

Si hay problemas con PostgreSQL, volver a MySQL es inmediato:

### Rollback Rápido (sin cambios en código)

```bash
# Si solo cambiaste el default en settings.py, revertir el cambio
git checkout mantenedor/settings.py

# Reiniciar servicios
docker compose restart web celery celery-beat
```

### Rollback con Datos

Si se agregaron datos nuevos en PostgreSQL que no están en MySQL:

```bash
# Exportar datos nuevos de PostgreSQL
docker compose exec web python manage.py dumpdata --database=postgres \
    reloj_fichador.RegistroDiario \
    --indent 2 > nuevos_registros.json

# Importar a MySQL
docker compose exec web python manage.py loaddata nuevos_registros.json --database=default
```

---

## Optimizaciones PostgreSQL

### 1. Índices Recomendados

```sql
-- Índices para búsquedas frecuentes
CREATE INDEX idx_registro_diario_fecha ON reloj_fichador_registrodiario(fecha);
CREATE INDEX idx_registro_diario_operario_fecha ON reloj_fichador_registrodiario(operario_id, fecha);
CREATE INDEX idx_horas_trabajadas_operario_fecha ON reloj_fichador_horas_trabajadas(operario_id, fecha);
CREATE INDEX idx_operario_dni ON reloj_fichador_operario(dni);
CREATE INDEX idx_operario_activo ON reloj_fichador_operario(activo) WHERE activo = true;
```

### 2. Configuración de Rendimiento

Editar `docker-compose.yml` para optimizar PostgreSQL:

```yaml
command: >
  postgres
  -c timezone=America/Argentina/Buenos_Aires
  -c max_connections=200
  -c shared_buffers=256MB
  -c effective_cache_size=1GB
  -c maintenance_work_mem=128MB
  -c checkpoint_completion_target=0.9
  -c wal_buffers=16MB
  -c default_statistics_target=100
  -c random_page_cost=1.1
  -c effective_io_concurrency=200
  -c work_mem=4MB
  -c min_wal_size=1GB
  -c max_wal_size=4GB
```

### 3. Vacuuming y Analyze

```bash
# Ejecutar análisis de estadísticas
docker compose exec db_postgres psql -U sistemas -d docker_horesdb_pg -c "
VACUUM ANALYZE;
"

# Configurar autovacuum más agresivo para tablas grandes
docker compose exec db_postgres psql -U sistemas -d docker_horesdb_pg -c "
ALTER TABLE reloj_fichador_registrodiario
SET (autovacuum_vacuum_scale_factor = 0.1, autovacuum_analyze_scale_factor = 0.05);
"
```

### 4. Monitoreo

```bash
# Ver conexiones activas
docker compose exec db_postgres psql -U sistemas -d docker_horesdb_pg -c "
SELECT
    datname,
    count(*) as connections,
    state
FROM pg_stat_activity
WHERE datname = 'docker_horesdb_pg'
GROUP BY datname, state;
"

# Ver queries lentas
docker compose exec db_postgres psql -U sistemas -d docker_horesdb_pg -c "
SELECT
    query,
    calls,
    total_exec_time / 1000 as total_time_seconds,
    mean_exec_time / 1000 as mean_time_seconds
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
"
```

---

## Ventajas de PostgreSQL sobre MySQL

1. **Mejor manejo de concurrencia** (MVCC más eficiente)
2. **JSON nativo** (útil para futuras extensiones)
3. **Full-text search** integrado
4. **Mejor rendimiento** en queries complejas
5. **Transacciones más robustas**
6. **Cumplimiento de estándares SQL** más estricto
7. **Extensiones** (PostGIS, pg_cron, etc.)

---

## Problemas Comunes y Soluciones

### Problema 1: Secuencias desincronizadas

**Síntoma:** Error al insertar: "duplicate key value violates unique constraint"

**Solución:**

```bash
docker compose exec web python manage.py shell
```

```python
from django.db import connections

with connections['postgres'].cursor() as cursor:
    cursor.execute("""
        SELECT
            'SELECT setval(''' ||
            pg_get_serial_sequence(quote_ident(table_name), quote_ident(column_name)) ||
            ''', COALESCE(MAX(' || quote_ident(column_name) || '), 1)) FROM ' ||
            quote_ident(table_name) || ';'
        FROM information_schema.columns
        WHERE table_schema = 'public'
        AND column_default LIKE 'nextval%';
    """)
    for row in cursor.fetchall():
        cursor.execute(row[0])
```

### Problema 2: Diferencias de timezone

**Síntoma:** Las fechas tienen diferencias de horas

**Solución:** Asegurarse de que todas las configuraciones usen la misma zona horaria:
- Docker: `TZ=America/Argentina/Buenos_Aires`
- PostgreSQL: `-c timezone=America/Argentina/Buenos_Aires`
- Django: `TIME_ZONE = 'America/Argentina/Buenos_Aires'` y `USE_TZ = True`

### Problema 3: Campos AUTO_INCREMENT vs SERIAL

**Síntoma:** No se generan IDs automáticamente

**Solución:** El script de migración ya maneja esto, pero si es necesario:

```sql
-- Verificar que las secuencias existen
SELECT * FROM pg_sequences WHERE schemaname = 'public';

-- Crear secuencia manualmente si falta
CREATE SEQUENCE IF NOT EXISTS reloj_fichador_operario_id_seq;
ALTER TABLE reloj_fichador_operario
ALTER COLUMN id SET DEFAULT nextval('reloj_fichador_operario_id_seq');
```

---

## Backup y Restauración

### Backup de PostgreSQL

```bash
# Backup completo
docker compose exec db_postgres pg_dump -U sistemas docker_horesdb_pg > backup_postgres_$(date +%Y%m%d).sql

# Backup solo esquema
docker compose exec db_postgres pg_dump -U sistemas --schema-only docker_horesdb_pg > schema_postgres.sql

# Backup solo datos
docker compose exec db_postgres pg_dump -U sistemas --data-only docker_horesdb_pg > data_postgres.sql
```

### Restauración

```bash
# Restaurar desde backup
docker compose exec -T db_postgres psql -U sistemas docker_horesdb_pg < backup_postgres_20251013.sql
```

---

## Conclusión

La migración a PostgreSQL proporciona una base de datos más robusta y escalable para el Sistema Reloj Fichador. La arquitectura dual permite una transición gradual y segura, minimizando riesgos.

### Próximos Pasos Recomendados

1. ✅ Completar la migración de datos
2. ⏳ Período de pruebas (1-2 semanas) usando PostgreSQL
3. ⏳ Monitorear rendimiento y logs
4. ⏳ Optimizar queries si es necesario
5. ⏳ Cambiar `default` a PostgreSQL
6. ⏳ Mantener MySQL como backup por 1 mes
7. ⏳ Desactivar MySQL si todo funciona correctamente

---

**Fecha de creación:** 2025-10-13
**Autor:** Sistema de Migración Automática
**Versión:** 1.0
