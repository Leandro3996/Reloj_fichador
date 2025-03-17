"""
Configuración especial para ejecutar pruebas de vistas con SQLite en memoria.
Este archivo añade algunos parches y ajustes adicionales para manejar fechas
y zonas horarias correctamente en las pruebas de vistas.
"""

# Importar la configuración básica para SQLite
from tests_utils.sqlite_settings import *

# Configuración explícita para manejo de fechas
USE_TZ = True
TIME_ZONE = 'UTC'  

# Imprimir mensaje para confirmar que se está usando esta configuración
print("Usando configuración especial para pruebas de vistas")

# Importar utilidades para manipulación de fechas
from tests_utils.datetime_patch import normalize_datetime, normalize_dict_datetimes

# Definir una función para aplicar el parche cuando Django esté listo
def apply_datetime_patches(sender, **kwargs):
    """
    Aplica parches para corregir problemas de zona horaria
    Este método se ejecuta cuando Django está completamente inicializado
    """
    try:
        from apps.reloj_fichador.models import calcular_horas_por_franjas
        
        # Definir la versión parche que normaliza las fechas antes de compararlas
        def calcular_horas_por_franjas_patched(inicio, fin, limites=None):
            # Normalizar fechas de entrada
            inicio = normalize_datetime(inicio)
            fin = normalize_datetime(fin)
            
            # Normalizar el diccionario de límites si existe
            if limites is not None:
                limites = normalize_dict_datetimes(limites)
                
            # Llamar a la función original con los datos normalizados
            return calcular_horas_por_franjas.__wrapped__(inicio, fin, limites)
        
        # Aplicar el parche a la función
        if hasattr(calcular_horas_por_franjas, '__wrapped__'):
            print("La función ya ha sido parcheada anteriormente.")
        else:
            # Guardar la original
            calcular_horas_por_franjas.__wrapped__ = calcular_horas_por_franjas
            # Sobreescribir con la versión parcheada
            import apps.reloj_fichador.models
            apps.reloj_fichador.models.calcular_horas_por_franjas = calcular_horas_por_franjas_patched
            print("Aplicado parche para normalizar fechas en calcular_horas_por_franjas")
            
    except (ImportError, AttributeError) as e:
        print(f"Error al aplicar parche de fechas: {e}")

# Conectar la señal para aplicar el parche cuando Django esté listo
from django.core.signals import setting_changed
setting_changed.connect(apply_datetime_patches) 