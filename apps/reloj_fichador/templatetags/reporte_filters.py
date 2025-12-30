from django import template
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
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
    Si no hay fecha, devuelve texto en rojo
    """
    if not fecha:
        return mark_safe('<span style="color: #dc3545; font-weight: 500;">No registró fichada</span>')

    # Convertir a timezone de Argentina si la fecha está en UTC
    if timezone.is_aware(fecha):
        argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
        fecha_local = fecha.astimezone(argentina_tz)
    else:
        fecha_local = fecha

    dia = dia_es(fecha_local)
    fecha_str = fecha_local.strftime('%d/%m/%Y - %H:%M:%S')
    return f"{dia} - {fecha_str}"

@register.filter
def fecha_corta_es(fecha):
    """
    Formatea fecha corta en español: "Lunes 01/11/2025"
    """
    if not fecha:
        return ""

    dia = dia_es(fecha)
    fecha_str = fecha.strftime('%d/%m/%Y')
    return f"{dia} {fecha_str}"


@register.filter
def horas_formato(valor):
    """
    Formatea un timedelta a formato de horas totales "XXh YYm"
    Uso: {{ mi_timedelta|horas_formato }}

    Ejemplos:
        timedelta(days=1, hours=16) → "40h 00m"
        timedelta(hours=2, minutes=30) → "02h 30m"
        timedelta(days=2) → "48h 00m"
    """
    if valor is None or valor == "":
        return "00h 00m"

    if not isinstance(valor, timedelta):
        # Intentar convertir si es un número (segundos)
        try:
            valor = timedelta(seconds=float(valor))
        except (ValueError, TypeError):
            return str(valor)

    # Convertir todo a segundos y luego calcular horas y minutos totales
    total_segundos = int(valor.total_seconds())
    horas = total_segundos // 3600
    minutos = (total_segundos % 3600) // 60

    return f"{horas:02d}h {minutos:02d}m"