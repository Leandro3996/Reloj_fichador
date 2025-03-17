"""
Utilidades para manejar fechas correctamente en pruebas, respetando
la configuración de zonas horarias del proyecto principal.
"""

from django.conf import settings
from django.utils import timezone
from datetime import datetime, date, time

def ensure_timezone_consistency(dt1, dt2):
    """
    Asegura que dos fechas tengan compatibilidad de zonas horarias
    para poder ser comparadas sin errores.
    """
    # Si alguno es None, no hay nada que hacer
    if dt1 is None or dt2 is None:
        return dt1, dt2
        
    # Si solo uno tiene timezone, normalizamos según la configuración del proyecto
    if hasattr(dt1, 'tzinfo') and hasattr(dt2, 'tzinfo'):
        if dt1.tzinfo is None and dt2.tzinfo is not None:
            if settings.USE_TZ:
                dt1 = timezone.make_aware(dt1)
            else:
                dt2 = timezone.make_naive(dt2)
        elif dt1.tzinfo is not None and dt2.tzinfo is None:
            if settings.USE_TZ:
                dt2 = timezone.make_aware(dt2)
            else:
                dt1 = timezone.make_naive(dt1)
    
    return dt1, dt2

def normalize_datetime(dt):
    """
    Normaliza un datetime según la configuración del proyecto.
    Si USE_TZ está activado, asegura que la fecha tenga timezone.
    Si USE_TZ está desactivado, elimina la información de timezone.
    """
    if dt is None:
        return None
        
    if hasattr(dt, 'tzinfo'):
        if settings.USE_TZ and dt.tzinfo is None:
            return timezone.make_aware(dt)
        elif not settings.USE_TZ and dt.tzinfo is not None:
            return timezone.make_naive(dt)
    
    return dt

def create_datetime(year, month, day, hour=0, minute=0, second=0):
    """
    Crea un objeto datetime con la configuración de timezone adecuada
    según la configuración del proyecto.
    """
    dt = datetime(year, month, day, hour, minute, second)
    if settings.USE_TZ:
        return timezone.make_aware(dt)
    return dt

def create_test_datetime(year, month, day, hour=0, minute=0, second=0):
    """
    Crea un objeto datetime para usar en pruebas, respetando la configuración USE_TZ.
    Si USE_TZ es True, devuelve un datetime con zona horaria.
    Si USE_TZ es False, devuelve un datetime sin zona horaria.
    
    Args:
        year: Año
        month: Mes
        day: Día
        hour: Hora (opcional, por defecto 0)
        minute: Minuto (opcional, por defecto 0)
        second: Segundo (opcional, por defecto 0)
        
    Returns:
        Un objeto datetime compatible con la configuración USE_TZ
    """
    dt = datetime(year, month, day, hour, minute, second)
    
    if getattr(settings, 'USE_TZ', False):
        return timezone.make_aware(dt)
    else:
        return dt
        
def strip_timezone(dt):
    """
    Elimina la información de zona horaria de un datetime si tiene
    
    Args:
        dt: Objeto datetime, posiblemente con zona horaria
        
    Returns:
        Objeto datetime sin zona horaria
    """
    if dt and hasattr(dt, 'tzinfo') and dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt 