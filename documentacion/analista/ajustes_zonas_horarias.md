# Ajustes de Zonas Horarias en la Aplicación

## Problema Identificado
Tras la activación de `USE_TZ = True` en la configuración de Django (`settings.py`), se presentaron dos problemas:

1. Los registros se guardaban en UTC en la base de datos, en lugar de utilizar la zona horaria local de Argentina (`America/Argentina/Buenos_Aires`).
2. En el panel de administración de Django, los registros se mostraban con la hora UTC en lugar de la hora local de Argentina.

## Solución Implementada

### 1. Modificación en `views.py`
Se ajustó la función `registrar_movimiento_tipo` para asegurar que la hora se guarde con la zona horaria correcta:

```python
# Obtener la hora actual con la zona horaria de Argentina
argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
hora_actual = timezone.now().astimezone(argentina_tz)

# Crear registro con la hora correcta
registro = RegistroDiario(
    operario=operario,
    tipo_movimiento=tipo_movimiento,
    hora_fichada=hora_actual,
)
```

### 2. Ajustes en el modelo `RegistroDiario`
Se modificaron dos métodos clave:

#### a. Método `calcular_fecha_logica`
Este método ahora normaliza las fechas según la configuración de `USE_TZ`:

```python
if getattr(settings, 'USE_TZ', False):
    # Si USE_TZ=True, asegurarse de que la fecha esté en la zona horaria de Argentina
    argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
    if hora_fichada.tzinfo is None:
        hora_fichada = pytz.utc.localize(hora_fichada)
    hora_fichada = hora_fichada.astimezone(argentina_tz)
elif hasattr(hora_fichada, 'tzinfo') and hora_fichada.tzinfo is not None:
    # Si USE_TZ=False pero tiene zona horaria, quitarla
    hora_fichada = hora_fichada.replace(tzinfo=None)
```

#### b. Método `clean`
Se actualizó para manejar correctamente la zona horaria:

```python
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
```

### 3. Ajustes en el panel de administración (`admin.py`)

#### a. Método `formatted_hora_fichada`
Se actualizó la función que muestra las horas en el panel de administración para convertirlas a la zona horaria de Argentina:

```python
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

#### b. Métodos `generar_reporte` y `exportar_excel`
Se modificaron para asegurar que todas las fechas se muestren en la zona horaria de Argentina:

```python
# Convertir hora a zona horaria de Argentina
hora_local = registro.hora_fichada
if hora_local.tzinfo is not None:
    hora_local = hora_local.astimezone(argentina_tz)
    
# Usar la hora convertida
hora_local.strftime('%d/%m/%Y %H:%M:%S')
```

## Impacto de los Cambios
Estos cambios permiten:

1. Que la aplicación muestre correctamente las horas en la zona horaria de Argentina.
2. Que los cálculos de horas trabajadas, franjas horarias y validaciones temporales funcionen correctamente.
3. Que el panel de administración de Django muestre las horas en la zona horaria de Argentina.
4. Mantener compatibilidad tanto con `USE_TZ=True` como con posibles cambios futuros.

## Consideraciones Futuras
- Es importante asegurar que todos los nuevos desarrollos consideren el trabajo con zonas horarias.
- Se recomienda utilizar siempre `timezone.now()` en lugar de `datetime.now()` para obtener fechas.
- Para conversiones de zona horaria, utilizar siempre el patrón implementado en estos cambios.
- Al mostrar fechas en el panel de administración o en reportes, siempre verificar que estén en la zona horaria correcta.

## Fecha de Implementación
- Fecha: 23/08/2023 