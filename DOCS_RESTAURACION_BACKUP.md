# Documentación: Restauración Automática de Backup de Producción

## 📋 Descripción

Script automatizado para restaurar backups de la base de datos de producción en el ambiente de desarrollo local.

**Ubicación:** `restaurar_backup_produccion.sh`

---

## 🎯 ¿Qué hace el script?

El script ejecuta los siguientes pasos de forma automática y segura:

1. ✅ **Verifica** que Docker esté corriendo y los servicios estén saludables
2. 💾 **Crea un backup de seguridad** de la BD local actual
3. 📥 **Copia el backup de producción** (el más reciente o uno específico)
4. 🔄 **Restaura el backup** en la BD local
5. 🔧 **Ejecuta las migraciones** de Django (sincroniza tablas nuevas)
6. ✓ **Verifica** que todo funcionó correctamente
7. 📊 **Muestra un resumen** con estadísticas

---

## 🚀 Uso Básico

### Restaurar el backup más reciente

```bash
./restaurar_backup_produccion.sh
```

El script pedirá confirmación antes de proceder.

### Modo automático (sin confirmación)

```bash
./restaurar_backup_produccion.sh -y
```

### Modo simulación (dry-run)

```bash
./restaurar_backup_produccion.sh --dry-run
```

Muestra qué haría sin hacer cambios reales.

---

## 📚 Opciones Disponibles

| Opción | Descripción |
|--------|-------------|
| `-h`, `--help` | Muestra la ayuda del script |
| `-d`, `--dry-run` | Simula la ejecución sin hacer cambios |
| `-f`, `--file ARCHIVO` | Restaura un backup específico |
| `-s`, `--skip-backup` | Omite el backup de seguridad local |
| `-y`, `--yes` | No pide confirmación |

---

## 🔧 Ejemplos de Uso

### 1. Restaurar backup más reciente (modo interactivo)

```bash
./restaurar_backup_produccion.sh
```

**Output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Restauración de Backup de Producción
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Fecha: 2025-11-10_14.03.52

ℹ  Verificando Docker...
✓  Docker está corriendo correctamente
ℹ  Buscando el backup más reciente...
✓  Backup encontrado: backup_2025-11-10_16.46.10.sql (9,9M)

⚠  ADVERTENCIA: Este proceso:
   1. Hará un backup de la BD local actual
   2. Sobrescribirá la BD local con datos de producción
   3. Ejecutará migraciones de Django

   Backup a restaurar: backup_2025-11-10_16.46.10.sql

¿Continuar? (s/N):
```

### 2. Restaurar un backup específico

```bash
./restaurar_backup_produccion.sh -f /ruta/al/backup_2025-11-09_10.30.00.sql
```

### 3. Restaurar sin hacer backup de seguridad

```bash
./restaurar_backup_produccion.sh -s -y
```

**⚠️ Advertencia:** Solo usar si estás seguro de lo que haces.

### 4. Simular la restauración (prueba)

```bash
./restaurar_backup_produccion.sh -d
```

Útil para verificar qué backup se usaría sin hacer cambios.

### 5. Restaurar automáticamente (sin interacción)

```bash
./restaurar_backup_produccion.sh -y
```

Ideal para scripts automatizados o cron jobs.

---

## 📂 Ubicaciones de Archivos

### Backup de Producción

**Carpeta:** `/home/leandro/debian-home/sistemas/Docker_proyectos/Reloj_fichador/backups/`

**Formato:** `backup_YYYY-MM-DD_HH.MM.SS.sql`

**Frecuencia:** Cada 30 minutos (automático por Docker)

### Backup de Seguridad Local

**Carpeta:** `/home/leandro/Proyectos_Docker/Reloj_fichador/`

**Formato:** `backup_local_antes_restauracion_YYYY-MM-DD_HH.MM.SS.sql`

**Creación:** Antes de cada restauración

### Logs del Script

**Carpeta:** `/home/leandro/Proyectos_Docker/Reloj_fichador/logs/`

**Formato:** `restauracion_YYYY-MM-DD_HH.MM.SS.log`

**Contiene:** Output completo del proceso

---

## ✅ Verificaciones Automáticas

El script verifica automáticamente:

1. **Docker corriendo:** Verifica que `docker ps` funcione
2. **MySQL healthy:** Verifica que el contenedor MySQL esté saludable
3. **Backup existe:** Verifica que el archivo de backup exista
4. **Tablas restauradas:** Cuenta las tablas después de restaurar (debe haber 45+)
5. **Servicios activos:** Verifica que web y db estén corriendo
6. **Admin accesible:** Verifica que http://localhost:58000/admin/ responda

---

## 🔄 Proceso de Migraciones

El script maneja automáticamente las tablas que ya existen en el backup de producción:

### Tablas de Django Axes

```bash
python manage.py migrate axes --fake
```

Marca como aplicadas las migraciones de `django-axes` (tablas de seguridad).

### Tablas del Proyecto

```bash
python manage.py migrate reloj_fichador --fake
```

Marca como aplicadas las migraciones que crean tablas ya presentes en el backup.

### Migraciones Restantes

```bash
python manage.py migrate
```

Aplica cualquier migración adicional pendiente.

---

## 📊 Resumen Final

Al finalizar, el script muestra:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Resumen de Restauración
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Backup restaurado:
  • Archivo: backup_2025-11-10_16.46.10.sql
  • Tamaño: 9,9M

Datos restaurados:
  • Operarios: 348
  • Registros diarios: 36,858
  • Horas calculadas: 9,327
  • Grupos de sábado: 96

Servicios:
  • Admin: http://localhost:58000/admin/
  • Web: http://localhost:5080

Log del proceso:
  • /home/leandro/Proyectos_Docker/Reloj_fichador/logs/restauracion_2025-11-10_14.03.52.log

✓  Restauración completada exitosamente
```

---

## ⚠️ Casos de Error

### Error: Docker no está corriendo

**Mensaje:**
```
✗  Docker no está corriendo o no tienes permisos
```

**Solución:**
```bash
sudo systemctl start docker
# o
sudo service docker start
```

### Error: MySQL no está healthy

**Mensaje:**
```
✗  El contenedor MySQL no está healthy
```

**Solución:**
```bash
docker compose restart db
# Esperar 10-15 segundos
docker compose ps db
```

### Error: No se encontraron backups

**Mensaje:**
```
✗  No se encontraron backups en /ruta/backups
```

**Solución:**
- Verificar que la ruta de producción esté montada
- Verificar que haya archivos `backup_*.sql` en la carpeta

### Error: Pocas tablas restauradas

**Mensaje:**
```
✗  Error: Solo se encontraron 30 tablas (se esperaban 45+)
```

**Solución:**
- El backup puede estar corrupto o incompleto
- Restaurar el backup de seguridad local:
  ```bash
  docker compose exec -T db mysql -u root -pS1st3mas.1999 docker_horesdb < backup_local_antes_restauracion_*.sql
  ```

---

## 🔐 Seguridad

### Credenciales

Las credenciales están **hardcodeadas** en el script:
- Usuario: `root`
- Password: `S1st3mas.1999`
- Base de datos: `docker_horesdb`

**⚠️ Recomendación:** Si usas este script en producción o lo compartes, considera usar variables de entorno:

```bash
MYSQL_USER=${MYSQL_USER:-root}
MYSQL_PASS=${MYSQL_PASS:-S1st3mas.1999}
```

### Backup de Seguridad

El script **SIEMPRE** crea un backup de seguridad antes de restaurar, a menos que uses `-s` (no recomendado).

**Conservar backups de seguridad:**
```bash
# Los backups locales se guardan en la raíz del proyecto
ls -lh backup_local_antes_restauracion_*.sql
```

---

## 📝 Logs

Cada ejecución genera un log detallado:

```bash
# Ver el último log
tail -f logs/restauracion_*.log | tail -1

# Ver todos los logs
ls -lht logs/restauracion_*.log
```

---

## 🔄 Automatización

### Cron Job (restaurar cada noche a las 2 AM)

```bash
crontab -e
```

Agregar:
```cron
0 2 * * * cd /home/leandro/Proyectos_Docker/Reloj_fichador && ./restaurar_backup_produccion.sh -y >> logs/cron_restauracion.log 2>&1
```

### Script de actualización rápida

Crear `actualizar_local.sh`:
```bash
#!/bin/bash
cd /home/leandro/Proyectos_Docker/Reloj_fichador
./restaurar_backup_produccion.sh -y
```

---

## 🆘 Recuperación de Emergencia

### Si algo sale mal durante la restauración

1. **Detener servicios:**
   ```bash
   docker compose stop web celery celery-beat
   ```

2. **Restaurar backup de seguridad:**
   ```bash
   docker compose exec -T db mysql -u root -pS1st3mas.1999 docker_horesdb < backup_local_antes_restauracion_*.sql
   ```

3. **Reiniciar servicios:**
   ```bash
   docker compose up -d
   ```

### Backup de seguridad más reciente

```bash
# Listar backups locales ordenados por fecha
ls -lht backup_local_antes_restauracion_*.sql | head -5
```

---

## 📞 Soporte

**Documentación adicional:**
- `CLAUDE.md` - Instrucciones generales del proyecto
- `docker-compose.yml` - Configuración de servicios
- `DOCS/` - Documentación técnica

**Logs útiles:**
- `logs/restauracion_*.log` - Logs del script
- `docker compose logs db` - Logs de MySQL
- `docker compose logs web` - Logs de Django

---

## 🎓 Casos de Uso Comunes

### 1. Empezar a trabajar con datos frescos

```bash
# Cada lunes por la mañana
./restaurar_backup_produccion.sh -y
```

### 2. Probar un bug reportado en producción

```bash
# Restaurar datos de producción
./restaurar_backup_produccion.sh -y

# Reproducir el bug con datos reales
# ...

# Cuando termines, puedes restaurar tu backup local anterior
docker compose exec -T db mysql -u root -pS1st3mas.1999 docker_horesdb < backup_local_antes_restauracion_*.sql
```

### 3. Verificar qué backup se usaría sin hacer cambios

```bash
./restaurar_backup_produccion.sh -d
```

### 4. Restaurar un backup específico de hace 2 días

```bash
# Listar backups disponibles
ls -lht /home/leandro/debian-home/sistemas/Docker_proyectos/Reloj_fichador/backups/backup_2025-11-08*.sql

# Restaurar uno específico
./restaurar_backup_produccion.sh -f /home/leandro/debian-home/sistemas/Docker_proyectos/Reloj_fichador/backups/backup_2025-11-08_10.30.00.sql
```

---

## ✨ Características Avanzadas

### Colores en Terminal

El script usa colores ANSI para mejor legibilidad:
- 🔵 Azul: Headers y títulos
- 🟢 Verde: Éxitos
- 🟡 Amarillo: Advertencias
- 🔴 Rojo: Errores
- 🔷 Cyan: Información

### Logs Persistentes

Todos los outputs se guardan en `logs/restauracion_*.log` para auditoría.

### Validación de Integridad

Verifica automáticamente:
- Número de tablas (debe ser 45+)
- Estado de servicios Docker
- Accesibilidad del admin

---

**Última actualización:** 10 de Noviembre, 2025
**Versión del script:** 1.0
**Autor:** Sistema automatizado - Reloj Fichador
