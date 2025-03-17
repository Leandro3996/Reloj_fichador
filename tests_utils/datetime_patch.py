"""
Utilidades para normalizar fechas en las pruebas y evitar problemas
con las zonas horarias (offset-aware vs offset-naive datetimes).
"""

from django.utils import timezone
from functools import wraps
import inspect

def ensure_tz_consistency(func):
    """
    Decorator que asegura que todas las fechas pasadas a la función
    tengan una configuración consistente de zona horaria.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Normalizar los argumentos posicionales
        normalized_args = []
        for arg in args:
            if hasattr(arg, 'tzinfo'):
                if arg.tzinfo is None:
                    normalized_args.append(timezone.make_aware(arg))
                else:
                    normalized_args.append(arg)
            else:
                normalized_args.append(arg)
        
        # Normalizar los argumentos con nombre
        normalized_kwargs = {}
        for key, value in kwargs.items():
            if hasattr(value, 'tzinfo'):
                if value.tzinfo is None:
                    normalized_kwargs[key] = timezone.make_aware(value)
                else:
                    normalized_kwargs[key] = value
            else:
                normalized_kwargs[key] = value
        
        return func(*normalized_args, **normalized_kwargs)
    return wrapper

# Para usar en diccionarios, normaliza todas las fechas en un diccionario
def normalize_dict_datetimes(d):
    """
    Normaliza todas las fechas en un diccionario para que todas tengan 
    información de zona horaria.
    """
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

# Función para normalizar cualquier fecha
def normalize_datetime(dt):
    """
    Asegura que un datetime tenga información de zona horaria.
    Si no la tiene, le asigna la zona horaria predeterminada.
    """
    if hasattr(dt, 'tzinfo') and dt.tzinfo is None:
        return timezone.make_aware(dt)
    return dt 