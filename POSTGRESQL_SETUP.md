# Setup PostgreSQL - Guía Rápida

## 🚀 Inicio Rápido

### Opción 1: Script Automático (Recomendado)

```bash
./ejecutar_migracion_postgresql.sh
```

Este script hace todo automáticamente:
- ✅ Verifica servicios
- ✅ Ejecuta migraciones
- ✅ Migra los datos
- ✅ Muestra comparación de conteos

### Opción 2: Paso a Paso Manual

#### 1. Iniciar PostgreSQL

```bash
docker compose up -d db_postgres
docker compose ps  # Verificar que esté "healthy"
```

#### 2. Reconstruir el contenedor web

```bash
docker compose build web
docker compose up -d web
```

#### 3. Ejecutar migraciones

```bash
docker compose exec web python manage.py migrate --database=postgres
```

#### 4. Migrar datos

```bash
docker compose exec web python migrate_mysql_to_postgres.py
```

---

## 📊 Estado Actual

### Configuración Dual de Bases de Datos

El sistema ahora soporta **DOS bases de datos simultáneas**:

| Base de Datos | Alias | Puerto Host | Estado |
|---------------|-------|-------------|--------|
| **MySQL 8.4.0** | `default` | 53306 | ✅ Principal (actual) |
| **PostgreSQL 16** | `postgres` | 54321 | 🆕 Clon disponible |

### Uso en Django

```python
# Usar MySQL (default)
Operario.objects.all()  # Usa MySQL
Operario.objects.using('default').all()  # Explícito

# Usar PostgreSQL
Operario.objects.using('postgres').all()  # Usa PostgreSQL
```

---

## 🔄 Cambiar a PostgreSQL como Principal

### Editar `mantenedor/settings.py`

Intercambiar las configuraciones de `default` y `postgres`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Cambiar a PostgreSQL
        'NAME': os.environ.get('POSTGRES_DATABASE', 'docker_horesdb_pg'),
        # ... resto configuración PostgreSQL
    },
    'mysql_backup': {  # MySQL pasa a ser backup
        'ENGINE': 'django.db.backends.mysql',
        # ... configuración MySQL
    }
}
```

### Reiniciar servicios

```bash
docker compose restart web celery celery-beat
```

---

## 🧪 Verificación

### Comparar conteos

```bash
# MySQL
docker compose exec db mysql -usistemas -pS1st3mas2024 docker_horesdb \
  -e "SELECT COUNT(*) FROM reloj_fichador_operario;"

# PostgreSQL
docker compose exec db_postgres psql -U sistemas -d docker_horesdb_pg \
  -c "SELECT COUNT(*) FROM reloj_fichador_operario;"
```

### Probar queries

```bash
docker compose exec web python manage.py shell
```

```python
from apps.reloj_fichador.models import Operario

# Comparar resultados
mysql_count = Operario.objects.using('default').count()
pg_count = Operario.objects.using('postgres').count()

print(f"MySQL: {mysql_count}, PostgreSQL: {pg_count}")
```

---

## 📦 Backups

### PostgreSQL

```bash
# Backup completo
docker compose exec db_postgres pg_dump -U sistemas docker_horesdb_pg > backup_pg.sql

# Restaurar
cat backup_pg.sql | docker compose exec -T db_postgres psql -U sistemas docker_horesdb_pg
```

### MySQL (actual)

```bash
# Backup completo
docker compose exec db mysqldump -usistemas -pS1st3mas2024 docker_horesdb > backup_mysql.sql

# Restaurar
cat backup_mysql.sql | docker compose exec -T db mysql -usistemas -pS1st3mas2024 docker_horesdb
```

---

## 🔙 Rollback

Si necesitas volver a MySQL como única base de datos:

```bash
# 1. Detener PostgreSQL
docker compose stop db_postgres

# 2. Revertir cambios en settings.py (si los hiciste)
git checkout mantenedor/settings.py

# 3. Reiniciar servicios
docker compose restart web celery celery-beat
```

---

## 📝 Archivos Importantes

| Archivo | Descripción |
|---------|-------------|
| [`ejecutar_migracion_postgresql.sh`](ejecutar_migracion_postgresql.sh) | Script automático de migración |
| [`migrate_mysql_to_postgres.py`](migrate_mysql_to_postgres.py) | Script Python de migración de datos |
| [`documentacion/MIGRACION_POSTGRESQL.md`](documentacion/MIGRACION_POSTGRESQL.md) | Documentación completa |
| [`docker-compose.yml`](docker-compose.yml) | Configuración de servicios |
| [`.env`](.env) | Variables de entorno |
| [`mantenedor/settings.py`](mantenedor/settings.py) | Configuración Django |

---

## ⚡ Ventajas de PostgreSQL

1. ✅ **Mejor rendimiento** en queries complejas
2. ✅ **MVCC más eficiente** (mejor concurrencia)
3. ✅ **JSON nativo** para datos no estructurados
4. ✅ **Full-text search** integrado
5. ✅ **Extensiones** (PostGIS, pg_cron, etc.)
6. ✅ **Cumplimiento SQL** más estricto
7. ✅ **Transacciones robustas** (ACID completo)

---

## 🆘 Problemas Comunes

### Error: "could not connect to server"

```bash
# Verificar que PostgreSQL esté corriendo
docker compose ps db_postgres

# Ver logs
docker compose logs db_postgres

# Reiniciar
docker compose restart db_postgres
```

### Error: "duplicate key value violates unique constraint"

Las secuencias de PostgreSQL están desincronizadas.

```bash
docker compose exec web python manage.py shell
```

```python
from django.db import connections

with connections['postgres'].cursor() as cursor:
    cursor.execute("""
        SELECT setval(
            pg_get_serial_sequence(quote_ident(table_name), quote_ident(column_name)),
            COALESCE(MAX(id), 1)
        )
        FROM information_schema.columns c
        JOIN pg_tables t ON c.table_name = t.tablename
        WHERE c.column_default LIKE 'nextval%'
        AND t.schemaname = 'public';
    """)
```

### Error: psycopg2 no instalado

```bash
docker compose build web
docker compose up -d web
```

---

## 📞 Soporte

Para más información, consulta la [documentación completa](documentacion/MIGRACION_POSTGRESQL.md).

---

**Última actualización:** 2025-10-13
