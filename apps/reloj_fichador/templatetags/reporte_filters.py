from django import template
from datetime import datetime
from django.utils import timezone
import pytz

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """
    Template filter para acceder a valores de diccionarios usando claves dinámicas
    Uso: {{ diccionario|lookup:clave }}
    """
    if dictionary and key:
        return dictionary.get(key)
    return None

@register.filter
def dia_es(fecha):
    """
    Convierte el día de la semana al español
    Uso: {{ fecha|dia_es }}
    """
    if not fecha:
        return ""
    
    dias_es = {
        'Monday': 'Lunes',
        'Tuesday': 'Martes', 
        'Wednesday': 'Miércoles',
        'Thursday': 'Jueves',
        'Friday': 'Viernes',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    
    dia_en = fecha.strftime('%A')
    return dias_es.get(dia_en, dia_en)

@register.filter
def fecha_completa_es(fecha):
    """
    Formatea fecha completa en español: "Lunes - 06/08/2025 - 06:57:27"
    Convierte de UTC a timezone local de Argentina
    """
    if not fecha:
        return "-"
    
    # Convertir a timezone de Argentina si la fecha está en UTC
    if timezone.is_aware(fecha):
        argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
        fecha_local = fecha.astimezone(argentina_tz)
    else:
        fecha_local = fecha
    
    dia = dia_es(fecha_local)
    fecha_str = fecha_local.strftime('%d/%m/%Y - %H:%M:%S')
    return f"{dia} - {fecha_str}"