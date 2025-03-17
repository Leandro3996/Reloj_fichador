"""
Script para modificar directamente los archivos fuente en el contenedor Docker
para manejar correctamente las fechas con zonas horarias.
"""

import os
import re

def patch_models_file():
    """
    Aplica un parche directamente al archivo models.py para
    asegurar que todas las fechas tengan información de zona horaria
    antes de ser comparadas.
    """
    # Ruta al archivo models.py
    models_path = '/app/apps/reloj_fichador/models.py'
    
    if not os.path.exists(models_path):
        print(f"¡Error! No se encontró el archivo {models_path}")
        return False
    
    print(f"Modificando archivo {models_path}...")
    
    # Leer el archivo original
    with open(models_path, 'r') as f:
        content = f.read()
    
    # Crear una copia de seguridad
    with open(f"{models_path}.bak", 'w') as f:
        f.write(content)
    print(f"Backup creado en {models_path}.bak")
    
    # Encontrar la función calcular_horas_por_franjas y modificarla
    pattern = r'def calcular_horas_por_franjas\(inicio, fin, limites=None\):'
    if not re.search(pattern, content):
        print("No se encontró la función calcular_horas_por_franjas")
        return False
    
    # Añadir código para normalizar las fechas al principio de la función
    replacement = """def calcular_horas_por_franjas(inicio, fin, limites=None):
    # Asegurar que todas las fechas tengan información de zona horaria
    from django.utils import timezone
    
    # Normalizar fechas de entrada
    if hasattr(inicio, 'tzinfo') and inicio.tzinfo is None:
        inicio = timezone.make_aware(inicio)
    if hasattr(fin, 'tzinfo') and fin.tzinfo is None:
        fin = timezone.make_aware(fin)
        
    # Normalizar fechas en limites
    if limites:
        for key, value in limites.items():
            if hasattr(value, 'tzinfo') and value.tzinfo is None:
                limites[key] = timezone.make_aware(value)
    """
    
    # Reemplazar la definición de la función
    modified_content = re.sub(pattern, replacement, content)
    
    # Guardar el archivo modificado
    with open(models_path, 'w') as f:
        f.write(modified_content)
    
    print("Archivo modificado correctamente")
    return True

if __name__ == "__main__":
    if patch_models_file():
        print("Parche aplicado correctamente")
    else:
        print("Error al aplicar el parche") 