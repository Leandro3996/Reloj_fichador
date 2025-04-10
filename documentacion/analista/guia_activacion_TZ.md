# Guía paso a paso: Activación de USE_TZ en Django

## Introducción

Esta guía detalla el proceso para cambiar la configuración `USE_TZ = False` a `USE_TZ = True` en el proyecto Reloj Fichador. El cambio resolverá los problemas con Celery Beat y las zonas horarias, pero debe realizarse cuidadosamente para evitar efectos secundarios en la aplicación.

## Paso 1: Crear un entorno de pruebas

1. **Crear una rama de Git específica para esta tarea**
   ```bash
   git checkout -b activar_use_tz
   ```

2. **Hacer una copia de la base de datos**
   ```bash
   # Opción 1: Usando el script de mantenimiento
   ./documentacion/analista/scripts/mantenimiento.sh backup
   
   # Opción 2: Comando directo
   docker-compose exec db mysqldump -u root -p"$MYSQL_ROOT_PASSWORD" --databases docker_horesdb > backup_pre_use_tz.sql
   ```

## Paso 2: Modificar la configuración

1. **Actualizar la configuración en settings.py**
   ```python
   # Cambiar
   USE_TZ = False
   
   # Por
   USE_TZ = True
   ```

2. **Asegurar que la configuración de Celery es correcta en celery.py**
   ```python
   app.conf.timezone = 'America/Argentina/Buenos_Aires'
   app.conf.enable_utc = False
   ```

## Paso 3: Actualizar la base de datos (Importante)

1. **Crear script de migración para convertir fechas**
   
   Crear un archivo `convert_dates.py` en el directorio raíz del proyecto:
   
   ```python
   import os
   import django
   from django.apps import apps
   from django.db import models
   from django.utils import timezone
   import pytz
   
   # Configurar Django
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mantenedor.settings')
   django.setup()
   
   # Zona horaria de Argentina
   argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
   
   # Recorrer todos los modelos de la aplicación
   for model in apps.get_models():
       print(f"Procesando modelo: {model.__name__}")
       
       # Buscar campos de fecha/hora
       date_fields = []
       for field in model._meta.fields:
           if isinstance(field, (models.DateTimeField, models.DateField)):
               date_fields.append(field.name)
       
       if not date_fields:
           print(f"  No se encontraron campos de fecha en {model.__name__}")
           continue
           
       print(f"  Campos de fecha encontrados: {', '.join(date_fields)}")
       
       # Obtener todos los registros y actualizar las fechas
       try:
           objects = model.objects.all()
           count = 0
           
           for obj in objects:
               modified = False
               
               for field_name in date_fields:
                   value = getattr(obj, field_name, None)
                   
                   # Solo procesar DateTimeField, no DateField
                   field = model._meta.get_field(field_name)
                   if not isinstance(field, models.DateTimeField) or value is None:
                       continue
                       
                   # Convertir a hora con zona horaria si no la tiene
                   if timezone.is_naive(value):
                       new_value = timezone.make_aware(value, argentina_tz)
                       setattr(obj, field_name, new_value)
                       modified = True
                       
               if modified:
                   obj.save()
                   count += 1
                   
           print(f"  Actualizados {count} registros en {model.__name__}")
           
       except Exception as e:
           print(f"  Error al procesar {model.__name__}: {str(e)}")
   
   print("Conversión de fechas completada.")
   ```

2. **Ejecutar el script de migración dentro del contenedor**
   ```bash
   docker-compose exec web python convert_dates.py
   ```

## Paso 4: Actualizar el código de la aplicación

Algunos lugares clave donde verificar/actualizar el código:

1. **Formularios con campos de fecha**
   - Localizar formularios con widgets DateTimeInput y asegurar que manejan correctamente las zonas horarias

2. **Consultas de fecha en el ORM**
   - Revisar código que use `__date`, `__time` o consultas basadas en fechas
   - Ejemplo:
     ```python
     # Antes:
     queryset = Registro.objects.filter(fecha_creacion__date=date.today())
     
     # Después (podría necesitar):
     from django.utils import timezone
     today = timezone.now().date()
     queryset = Registro.objects.filter(fecha_creacion__date=today)
     ```

3. **Comparaciones directas de fechas**
   - Buscar código que compare fechas directamente y asegurar que ambas fechas tienen o no tienen zona horaria
   - Ejemplo:
     ```python
     # Problemático:
     if registro.fecha < datetime.datetime.now():
         # ...
     
     # Corrección:
     from django.utils import timezone
     if registro.fecha < timezone.now():
         # ...
     ```

4. **Serialización de fechas**
   - Revisar código que serialice o deserialice fechas (como APIs REST, importaciones/exportaciones)

## Paso 5: Pruebas exhaustivas

1. **Pruebas automatizadas**
   ```bash
   docker-compose exec web python manage.py test
   ```

2. **Pruebas manuales específicas**
   - Probar la creación y edición de registros de asistencia
   - Verificar los informes de horas trabajadas
   - Comprobar que los cálculos basados en tiempo funcionan correctamente
   - Verificar que las tareas programadas de Celery se ejecutan en la hora correcta

3. **Pruebas de Celery Beat**
   - Ejecutar el script de verificación:
     ```bash
     ./documentacion/analista/verificar_celery_timezone.sh
     ```
   - Monitorear los logs de Celery Beat durante al menos un ciclo completo:
     ```bash
     docker-compose logs -f celery-beat
     ```

## Paso 6: Implementación en producción

1. **Planificar un periodo de baja actividad para el cambio**

2. **Realizar una copia de seguridad completa**
   ```bash
   ./documentacion/analista/scripts/mantenimiento.sh backup
   ```

3. **Aplicar los cambios**
   ```bash
   git checkout master
   git merge activar_use_tz
   docker-compose down
   docker-compose up -d
   ```

4. **Ejecutar el script de conversión de fechas**
   ```bash
   docker-compose exec web python convert_dates.py
   ```

5. **Monitorizar el sistema**
   - Revisar los logs de todos los servicios por si aparecen errores
   - Verificar que las tareas programadas se ejecutan correctamente
   - Comprobar con varios usuarios que la aplicación funciona normalmente

## Consideraciones adicionales

1. **Rollback en caso de problemas**
   - Restaurar la copia de seguridad de la base de datos
   - Revertir los cambios en el código: `git revert HEAD`

2. **Actualización de documentación**
   - Actualizar las guías y documentación del proyecto para reflejar los cambios

3. **Monitoreo a largo plazo**
   - Durante las primeras semanas, verificar regularmente los logs para detectar problemas relacionados con fechas o zonas horarias

## Resumen de comandos clave

```bash
# Crear copia de seguridad
./documentacion/analista/scripts/mantenimiento.sh backup

# Aplicar cambios
git checkout -b activar_use_tz
# Editar settings.py y cambiar USE_TZ a True
git add mantenedor/settings.py
git commit -m "Activar USE_TZ para resolver problemas con Celery Beat"

# Convertir fechas en la base de datos
docker-compose exec web python convert_dates.py

# Verificar funcionamiento de Celery
./documentacion/analista/verificar_celery_timezone.sh

# Monitorear logs
docker-compose logs -f celery-beat
``` 