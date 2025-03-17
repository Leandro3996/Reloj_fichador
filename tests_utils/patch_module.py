"""
Script independiente para aplicar parches a funciones con problemas de zona horaria.
Este script debe ejecutarse dentro del contenedor Docker antes de correr las pruebas.
"""

import sys
import importlib

def apply_patches():
    """Aplica parches a las funciones problemáticas"""
    
    print("Aplicando parches para resolver problemas de zona horaria...")
    
    # Importar bibliotecas necesarias
    from django.utils import timezone
    
    # Intentar importar la función problemática
    try:
        from apps.reloj_fichador.models import calcular_horas_por_franjas
        print("Función encontrada, aplicando parche...")
        
        # Crear funciones auxiliares para normalizar fechas
        def normalize_datetime(dt):
            """Asegura que un datetime tenga información de zona horaria"""
            if hasattr(dt, 'tzinfo') and dt.tzinfo is None:
                return timezone.make_aware(dt)
            return dt
            
        def normalize_dict_datetimes(d):
            """Normaliza todas las fechas en un diccionario"""
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
            
        # Definir la versión parche de la función
        def calcular_horas_por_franjas_patched(inicio, fin, limites=None):
            # Normalizar fechas de entrada
            inicio = normalize_datetime(inicio)
            fin = normalize_datetime(fin)
            
            # Normalizar el diccionario de límites si existe
            if limites is not None:
                limites = normalize_dict_datetimes(limites)
                
            # Llamar a la función original con los datos normalizados
            original_func = getattr(calcular_horas_por_franjas, '__wrapped__', calcular_horas_por_franjas)
            return original_func(inicio, fin, limites)
        
        # Guardar referencia a la función original y aplicar el parche
        if not hasattr(calcular_horas_por_franjas, '__wrapped__'):
            calcular_horas_por_franjas.__wrapped__ = calcular_horas_por_franjas
            
        # Reemplazar la función en el módulo
        import apps.reloj_fichador.models
        apps.reloj_fichador.models.calcular_horas_por_franjas = calcular_horas_por_franjas_patched
        print("Parche aplicado correctamente.")
        
    except (ImportError, AttributeError) as e:
        print(f"Error al aplicar parche: {e}")
        
if __name__ == "__main__":
    apply_patches() 