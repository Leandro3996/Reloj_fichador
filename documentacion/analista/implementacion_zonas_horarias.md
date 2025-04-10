# Implementación del soporte de zonas horarias en el sistema de fichaje

## Resumen ejecutivo

Se ha implementado con éxito el soporte de zonas horarias en la aplicación de fichaje, lo que garantiza que todas las marcaciones de tiempo y cálculos de horas trabajadas se gestionen correctamente considerando la zona horaria de Argentina (America/Argentina/Buenos_Aires). Esta implementación resuelve problemas críticos de precisión en los registros horarios y mejora la fiabilidad del sistema en general.

## Antecedentes y problemática

El sistema de fichaje de personal originalmente funcionaba con la configuración `USE_TZ = False`, lo que significa que Django no aplicaba el manejo de zonas horarias. Esto generaba inconsistencias en:

1. La visualización de las horas fichadas en diferentes interfaces
2. Los cálculos de horas trabajadas para pagos y reportes
3. La programación de tareas automáticas con Celery

Se identificaron los siguientes problemas específicos:

- Los registros se almacenaban sin información de zona horaria
- Las tareas programadas en Celery no respetaban correctamente la zona horaria local
- Al activar `USE_TZ = True`, los registros se guardaban en UTC pero se necesitaban mostrar en hora local

## Solución implementada

### 1. Activación del soporte de zonas horarias

Se modificó la configuración principal de Django para habilitar el soporte de zonas horarias:

```python
# settings.py
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_TZ = True
```

### 2. Ajuste en la configuración de Celery

Se configuró Celery para trabajar explícitamente con la zona horaria de Argentina:

```python
# celery.py
app.conf.timezone = 'America/Argentina/Buenos_Aires'
app.conf.enable_utc = False
```

La programación de tareas se ajustó para ejecutarse a horas específicas en hora local:

```python
app.conf.beat_schedule = {
    'generar-registros-asistencia-5am': {
        'task': 'apps.reloj_fichador.tasks.generar_registros_asistencia',
        'schedule': crontab(hour=1, minute=0),  # Hora local de Argentina
    },
}
```

### 3. Modificaciones en el modelo `RegistroDiario`

Se actualizaron métodos clave para manejar correctamente las zonas horarias:

#### a. Método `calcular_fecha_logica`

```python
@staticmethod
def calcular_fecha_logica(hora_fichada):
    if not hora_fichada:
        return None

    # Normalizar la fecha según la configuración de USE_TZ
    from django.conf import settings
    import pytz
    
    if getattr(settings, 'USE_TZ', False):
        # Si USE_TZ=True, asegurarse de que la fecha esté en la zona horaria de Argentina
        argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
        if hora_fichada.tzinfo is None:
            hora_fichada = pytz.utc.localize(hora_fichada)
        hora_fichada = hora_fichada.astimezone(argentina_tz)
    elif hasattr(hora_fichada, 'tzinfo') and hora_fichada.tzinfo is not None:
        # Si USE_TZ=False pero tiene zona horaria, quitarla
        hora_fichada = hora_fichada.replace(tzinfo=None)

    # Lógica para determinar si pertenece al día anterior (turno nocturno)
    hora_limite = datetime.strptime("06:00", "%H:%M").time()
    if hora_fichada.time() < hora_limite:
        return hora_fichada.date() - timedelta(days=1)
    return hora_fichada.date()
```

#### b. Método `clean`

```python
def clean(self):
    super().clean()

    from django.conf import settings
    import pytz

    if not self.hora_fichada:
        self.hora_fichada = timezone.now()
        
    # Normalizar la fecha según la configuración de USE_TZ
    hora_fichada_normalizada = self.hora_fichada
    if getattr(settings, 'USE_TZ', False):
        # Si USE_TZ=True, asegurarse de que la fecha esté en la zona horaria de Argentina
        argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
        if hora_fichada_normalizada.tzinfo is None:
            hora_fichada_normalizada = pytz.utc.localize(hora_fichada_normalizada)
        hora_fichada_normalizada = hora_fichada_normalizada.astimezone(argentina_tz)
    elif hasattr(hora_fichada_normalizada, 'tzinfo') and hora_fichada_normalizada.tzinfo is not None:
        # Si USE_TZ=False pero tiene zona horaria, quitarla
        hora_fichada_normalizada = hora_fichada_normalizada.replace(tzinfo=None)
        # Actualizar el campo para que sea compatible con la base de datos
        self.hora_fichada = hora_fichada_normalizada

    movimiento_fecha = RegistroDiario.calcular_fecha_logica(hora_fichada_normalizada)
```

### 4. Actualizaciones en la vista de registro

Se modificó la vista `registrar_movimiento_tipo` para asegurar que la hora se guarde con la zona horaria correcta:

```python
# views.py
@require_POST
def registrar_movimiento_tipo(request, tipo_movimiento):
    # ...
    # Obtener la hora actual con la zona horaria de Argentina
    argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
    hora_actual = timezone.now().astimezone(argentina_tz)
    
    registro = RegistroDiario(
        operario=operario,
        tipo_movimiento=tipo_movimiento,
        hora_fichada=hora_actual,
    )
    # ...
```

### 5. Ajustes en el panel de administración

Para asegurar que las fechas se muestren correctamente en el panel de administración, se modificó:

```python
# admin.py
def formatted_hora_fichada(self, obj):
    if obj.hora_fichada:
        # Convertir a la zona horaria de Argentina
        argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
        hora_local = obj.hora_fichada
        if hora_local.tzinfo is not None:  # Si la fecha tiene zona horaria
            hora_local = hora_local.astimezone(argentina_tz)
        return hora_local.strftime('%d/%m/%Y %H:%M:%S')
    return ''
```

Se aplicó el mismo patrón a las funciones `generar_reporte` y `exportar_excel`.

## Resultados y beneficios

La implementación de las zonas horarias ha logrado:

1. **Precisión en los registros**: Todas las marcaciones se almacenan con información de zona horaria, lo que permite cálculos precisos independientemente de la configuración del servidor.

2. **Visualización coherente**: Los usuarios ven las horas en la zona horaria local en todas las interfaces (frontend, admin y reportes).

3. **Cálculos correctos**: Los algoritmos de cálculo de horas trabajadas, nocturnas y extras ahora funcionan correctamente considerando la zona horaria.

4. **Ejecución programada fiable**: Las tareas de Celery se ejecutan en los momentos adecuados según la hora local.

5. **Robustez del sistema**: La aplicación es más robusta y preparada para posibles cambios futuros o despliegues en diferentes zonas horarias.

## Consideraciones para desarrollos futuros

1. **Siempre usar `timezone.now()`**: En lugar de `datetime.now()` para obtener fechas y horas.

2. **Mantener consistencia en conversiones**: Al convertir fechas, usar siempre el patrón:
   ```python
   argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
   hora_local = hora_utc.astimezone(argentina_tz)
   ```

3. **Verificar zonas horarias en la interfaz**: Al mostrar fechas en templates o respuestas JSON, asegurarse de que estén en la zona horaria correcta.

4. **Documentar el comportamiento**: En cualquier función que procese fechas u horas, documentar cómo maneja las zonas horarias.

## Conclusión

La implementación del soporte de zonas horarias ha sido un paso crítico para mejorar la precisión y confiabilidad del sistema de fichaje. Aunque requirió modificaciones en múltiples capas de la aplicación, el resultado es un sistema más preciso y confiable para el registro y cálculo de horas trabajadas.

---

*Documentación elaborada por: Analista de Sistemas*  
*Fecha: 23/08/2023*  
*Versión: 1.0* 