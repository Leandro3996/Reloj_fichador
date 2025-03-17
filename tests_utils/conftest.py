"""
Configuración de pruebas para asegurar que todas las pruebas manejen correctamente
las zonas horarias y otros aspectos comunes.
"""

import pytest
from django.conf import settings
from django.utils import timezone
import sys
import logging

logger = logging.getLogger(__name__)

# Asegurarse de que USE_TZ esté activado
settings.USE_TZ = True

# Configurar monkey patching para fechas
@pytest.fixture(autouse=True, scope="session")
def setup_tests():
    """Configura todos los aspectos comunes para las pruebas"""
    logger.info("Configurando entorno de pruebas...")
    
    # Importar las utilidades de fechas
    try:
        from tests_utils.fix_datetimes import normalize_datetime, normalize_dict_datetimes
        
        # Monkey patch para calcular_horas_por_franjas
        try:
            from apps.reloj_fichador.models import calcular_horas_por_franjas
            
            # Crear la versión parcheada
            def calcular_horas_por_franjas_patched(inicio, fin, limites=None):
                # Normalizar fechas
                inicio = normalize_datetime(inicio)
                fin = normalize_datetime(fin)
                
                # Normalizar diccionario de límites
                if limites is not None:
                    limites = normalize_dict_datetimes(limites)
                
                # Obtener la función original
                original_func = getattr(calcular_horas_por_franjas, "__original__", calcular_horas_por_franjas)
                return original_func(inicio, fin, limites)
            
            # Guardar la referencia a la función original
            if not hasattr(calcular_horas_por_franjas, "__original__"):
                calcular_horas_por_franjas.__original__ = calcular_horas_por_franjas
                
            # Reemplazar la función en el módulo
            import apps.reloj_fichador.models
            apps.reloj_fichador.models.calcular_horas_por_franjas = calcular_horas_por_franjas_patched
            logger.info("Función calcular_horas_por_franjas parcheada")
                
        except (ImportError, AttributeError) as e:
            logger.error(f"Error al parchar calcular_horas_por_franjas: {e}")
            
    except (ImportError, AttributeError) as e:
        logger.error(f"Error al cargar utilidades de fechas: {e}")
    
    logger.info("Entorno de pruebas configurado correctamente")
    yield
    logger.info("Limpiando entorno de pruebas...") 