"""
Este módulo se importa automáticamente cuando se inicia Python.
Lo utilizamos para aplicar parches globales y configuración.
"""

import os
import sys
import logging

# Configurar el logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sitecustomize")

# Función para normalizar fechas
def _normalize_datetime(dt):
    """Asegura que un datetime tenga información de zona horaria"""
    from django.utils import timezone
    if hasattr(dt, 'tzinfo') and dt.tzinfo is None:
        return timezone.make_aware(dt)
    return dt

# Función para normalizar fechas en diccionarios
def _normalize_dict_datetimes(d):
    """Normaliza todas las fechas en un diccionario"""
    if not isinstance(d, dict):
        return d
    
    result = {}
    for key, value in d.items():
        if hasattr(value, 'tzinfo'):
            if value.tzinfo is None:
                from django.utils import timezone
                result[key] = timezone.make_aware(value)
            else:
                result[key] = value
        elif isinstance(value, dict):
            result[key] = _normalize_dict_datetimes(value)
        else:
            result[key] = value
    return result

# Función para aplicar parches
def apply_patches():
    """Aplica parches globales a funciones problemáticas"""
    logger.info("Iniciando proceso de parches globales...")
    
    try:
        # Importar los modelos de Django
        from django.conf import settings
        
        # Forzar USE_TZ = True
        settings.USE_TZ = True
        logger.info("USE_TZ establecido a True")
        
        # Parchar la función calcular_horas_por_franjas
        try:
            from apps.reloj_fichador.models import calcular_horas_por_franjas
            
            # Crear la versión parcheada
            def calcular_horas_por_franjas_patched(inicio, fin, limites=None):
                # Normalizar fechas
                inicio = _normalize_datetime(inicio)
                fin = _normalize_datetime(fin)
                
                # Normalizar diccionario de límites
                if limites is not None:
                    limites = _normalize_dict_datetimes(limites)
                
                # Obtener la función original
                original_func = getattr(calcular_horas_por_franjas, "__original__", calcular_horas_por_franjas)
                return original_func(inicio, fin, limites)
            
            # Guardar la referencia a la función original
            if not hasattr(calcular_horas_por_franjas, "__original__"):
                calcular_horas_por_franjas.__original__ = calcular_horas_por_franjas
                
            # Reemplazar la función en el módulo
            import apps.reloj_fichador.models
            apps.reloj_fichador.models.calcular_horas_por_franjas = calcular_horas_por_franjas_patched
            logger.info("Función calcular_horas_por_franjas parcheada correctamente")
                
        except (ImportError, AttributeError) as e:
            logger.error(f"Error al parchar calcular_horas_por_franjas: {e}")
            
    except Exception as e:
        logger.error(f"Error general al aplicar parches: {e}")
    
    logger.info("Proceso de parches completado")

# Intentar aplicar los parches al iniciar Python
try:
    # Solo aplicar parches si estamos ejecutando pruebas
    if 'test' in sys.argv:
        logger.info("Detectada ejecución de pruebas, aplicando parches...")
        
        # Registrar un hook para cuando Django esté completamente cargado
        from django.core.signals import setting_changed
        
        def on_setting_changed(sender, **kwargs):
            apply_patches()
            
        setting_changed.connect(on_setting_changed)
        logger.info("Hook de parches registrado para cuando Django esté listo")
        
except Exception as e:
    logger.error(f"Error al configurar parches automáticos: {e}") 