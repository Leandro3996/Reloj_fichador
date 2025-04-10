# Guía para el manejo de zonas horarias en el sistema

Esta guía tiene como objetivo proporcionar instrucciones claras y prácticas sobre cómo manejar correctamente las zonas horarias en el desarrollo de nuevas funcionalidades para el sistema de fichaje.

## Conceptos básicos

**¿Qué es USE_TZ=True?**
- Cuando `USE_TZ=True`, Django almacena todas las fechas en la base de datos en UTC.
- Las fechas se convierten automáticamente a la zona horaria configurada en `TIME_ZONE` al presentarse en templates.
- Sin embargo, para operaciones personalizadas, es responsabilidad del desarrollador manejar explícitamente las conversiones.

**¿Por qué usamos zonas horarias?**
- Para garantizar cálculos precisos y coherentes de horas trabajadas.
- Para mostrar fechas y horas correctas a los usuarios, independientemente de la ubicación del servidor.
- Para asegurar que las tareas programadas se ejecuten en el momento adecuado.

## Reglas importantes

### 1. Obtener la hora actual

✅ **CORRECTO**:
```python
from django.utils import timezone

# Obtener la hora actual en UTC
hora_actual = timezone.now()

# Si necesitas la hora en Argentina
argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
hora_argentina = timezone.now().astimezone(argentina_tz)
```

❌ **INCORRECTO**:
```python
from datetime import datetime

# No usar datetime.now() directamente
hora_actual = datetime.now()  # ❌ No tiene en cuenta las zonas horarias
```

### 2. Convertir entre zonas horarias

✅ **CORRECTO**:
```python
import pytz
from django.utils import timezone

# Definir la zona horaria de Argentina
argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')

# Convertir de UTC a hora Argentina
hora_utc = timezone.now()
hora_argentina = hora_utc.astimezone(argentina_tz)

# Formatear para mostrar al usuario
hora_formateada = hora_argentina.strftime('%d/%m/%Y %H:%M:%S')
```

### 3. Almacenar fechas

✅ **CORRECTO**:
```python
# Al crear un registro con fecha/hora
from django.utils import timezone
import pytz

argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
hora_actual = timezone.now().astimezone(argentina_tz)

registro = RegistroDiario(
    operario=operario,
    hora_fichada=hora_actual,
    # otros campos...
)
registro.save()
```

### 4. Comparar fechas

✅ **CORRECTO**:
```python
# Al comparar fechas de la base de datos
from django.utils import timezone
import pytz

argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
hoy = timezone.now().astimezone(argentina_tz).date()

# Buscar registros de hoy
registros_hoy = RegistroDiario.objects.filter(
    hora_fichada__date=hoy
)
```

### 5. Mostrar fechas en plantillas

En los templates de Django, las fechas se convierten automáticamente a la zona horaria configurada si se usan filtros de fecha:

✅ **CORRECTO**:
```html
<p>Fecha: {{ registro.hora_fichada|date:"d/m/Y H:i:s" }}</p>
```

Para funciones personalizadas que devuelven JSON o generan reportes:

✅ **CORRECTO**:
```python
def obtener_datos_json(request):
    registros = RegistroDiario.objects.all()
    datos = []
    
    argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
    
    for registro in registros:
        hora_local = registro.hora_fichada.astimezone(argentina_tz)
        
        datos.append({
            'id': registro.id,
            'operario': registro.operario.nombre,
            'fecha': hora_local.strftime('%d/%m/%Y'),
            'hora': hora_local.strftime('%H:%M:%S'),
        })
    
    return JsonResponse({'registros': datos})
```

## Patrones comunes en nuestro sistema

### Patrón para normalizar fechas

Este es el patrón estándar para normalizar fechas en el sistema:

```python
def normalizar_fecha(fecha):
    """Normaliza una fecha según la configuración de USE_TZ"""
    from django.conf import settings
    import pytz
    
    if not fecha:
        return None
        
    if getattr(settings, 'USE_TZ', False):
        # Si USE_TZ=True, asegurarse de que la fecha esté en la zona horaria de Argentina
        argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
        if fecha.tzinfo is None:
            fecha = pytz.utc.localize(fecha)
        return fecha.astimezone(argentina_tz)
    elif hasattr(fecha, 'tzinfo') and fecha.tzinfo is not None:
        # Si USE_TZ=False pero tiene zona horaria, quitarla
        return fecha.replace(tzinfo=None)
    return fecha
```

### Patrón para calcular diferencias de tiempo

Al calcular diferencias de tiempo, asegúrate de que ambas fechas estén en la misma zona horaria:

```python
def calcular_diferencia(inicio, fin):
    """Calcula la diferencia entre dos fechas asegurando que estén en la misma zona horaria"""
    inicio_normalizado = normalizar_fecha(inicio)
    fin_normalizado = normalizar_fecha(fin)
    
    return fin_normalizado - inicio_normalizado
```

## Consideraciones para tareas programadas con Celery

Para tareas de Celery, siempre usa la configuración explícita de zona horaria:

```python
# En celery.py
app.conf.timezone = 'America/Argentina/Buenos_Aires'
app.conf.enable_utc = False

# Para programar tareas
app.conf.beat_schedule = {
    'tarea-diaria': {
        'task': 'app.tasks.mi_tarea',
        'schedule': crontab(hour=8, minute=0),  # Se ejecutará a las 8:00 AM hora Argentina
    },
}
```

En las tareas, usa `timezone.now()` para obtener la hora actual:

```python
@shared_task
def mi_tarea():
    ahora = timezone.now()  # Ya estará en la zona horaria configurada en Celery
    # Resto de la lógica...
```

## Solución de problemas comunes

### Problema: "La fecha se muestra incorrectamente en el admin"

**Solución**: Personaliza el método `formatted_field` en el ModelAdmin:

```python
def formatted_hora_fichada(self, obj):
    if obj.hora_fichada:
        argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
        hora_local = obj.hora_fichada
        if hora_local.tzinfo is not None:
            hora_local = hora_local.astimezone(argentina_tz)
        return hora_local.strftime('%d/%m/%Y %H:%M:%S')
    return ''
```

### Problema: "Los cálculos de horas trabajadas son incorrectos"

**Solución**: Asegúrate de normalizar las fechas antes de hacer cálculos:

```python
def calcular_horas_trabajadas(entrada, salida):
    # Normalizar a la misma zona horaria
    entrada_normalizada = normalizar_fecha(entrada)
    salida_normalizada = normalizar_fecha(salida)
    
    # Ahora es seguro calcular la diferencia
    return salida_normalizada - entrada_normalizada
```

## Recursos adicionales

- [Documentación de Django sobre zonas horarias](https://docs.djangoproject.com/en/stable/topics/i18n/timezones/)
- [Documentación de pytz](https://pythonhosted.org/pytz/)
- [Documentación detallada del proyecto](documentacion/analista/implementacion_zonas_horarias.md)

---

*Guía elaborada por: Analista de Sistemas*  
*Fecha: 23/08/2023*  
*Versión: 1.0* 