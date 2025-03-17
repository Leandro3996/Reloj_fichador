"""
Utilidades para arreglar problemas de zona horaria en las pruebas de Django.
Este archivo debe ser importado en los archivos de test antes de ejecutarlos.
"""

from django.utils import timezone
from datetime import datetime

# Guardar la función original
_original_datetime = datetime

# Crear una versión mejorada de datetime que siempre tenga información de zona horaria
class AwareDatetime(type):
    def __call__(cls, *args, **kwargs):
        dt = _original_datetime(*args, **kwargs)
        if hasattr(dt, 'tzinfo') and dt.tzinfo is None:
            return timezone.make_aware(dt)
        return dt

# Reemplazar la clase datetime por nuestra versión
class DatetimeMeta(AwareDatetime):
    pass

# Función para normalizar una fecha
def normalize_datetime(dt):
    if hasattr(dt, 'tzinfo') and dt.tzinfo is None:
        return timezone.make_aware(dt)
    return dt

# Función para normalizar fechas en un diccionario
def normalize_dict_datetimes(d):
    if not isinstance(d, dict):
        return d
    
    result = {}
    for key, value in d.items():
        if hasattr(value, 'tzinfo'):
            if value.tzinfo is None:
                result[key] = timezone.make_aware(value)
            else:
                result[key] = value
        elif isinstance(value, dict):
            result[key] = normalize_dict_datetimes(value)
        else:
            result[key] = value
    return result 