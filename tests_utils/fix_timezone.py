"""
Script para modificar directamente el archivo models.py del proyecto
y arreglar el problema de comparación de fechas con zonas horarias.
"""

import os
import shutil

# Ruta al archivo models.py
MODELS_PATH = '/app/apps/reloj_fichador/models.py'
BACKUP_PATH = f"{MODELS_PATH}.bak"

def fix_timezone_issue():
    """Arregla el problema de zonas horarias en el archivo models.py"""
    
    print(f"Buscando el archivo: {MODELS_PATH}")
    
    # Verificar que el archivo existe
    if not os.path.exists(MODELS_PATH):
        print(f"Error: No se encontró el archivo {MODELS_PATH}")
        return False
    
    # Hacer copia de seguridad del archivo original si no existe
    if not os.path.exists(BACKUP_PATH):
        try:
            shutil.copy2(MODELS_PATH, BACKUP_PATH)
            print(f"Copia de seguridad creada en {BACKUP_PATH}")
        except Exception as e:
            print(f"Error al crear copia de seguridad: {e}")
            return False
    
    # Leer el contenido del archivo
    with open(MODELS_PATH, 'r') as f:
        lines = f.readlines()
    
    # Buscar la línea problemática y modificarla
    found = False
    for i, line in enumerate(lines):
        if "siguiente = min(fin, limites['normales_fin'])" in line:
            # Crear una nueva línea que normalice las fechas
            whitespace = line[:len(line) - len(line.lstrip())]  # Preservar indentación
            new_line = f"{whitespace}# Normalizar fechas para comparación\n"
            new_line += f"{whitespace}if hasattr(fin, 'tzinfo') and fin.tzinfo is None:\n"
            new_line += f"{whitespace}    from django.utils import timezone\n"
            new_line += f"{whitespace}    fin = timezone.make_aware(fin)\n"
            new_line += f"{whitespace}if hasattr(limites['normales_fin'], 'tzinfo') and limites['normales_fin'].tzinfo is None:\n"
            new_line += f"{whitespace}    from django.utils import timezone\n"
            new_line += f"{whitespace}    limites['normales_fin'] = timezone.make_aware(limites['normales_fin'])\n"
            new_line += line  # Preservar la línea original
            
            # Reemplazar la línea original con nuestro bloque modificado
            lines[i] = new_line
            found = True
            break
    
    if not found:
        print("No se encontró la línea problemática en el archivo")
        return False
    
    # Escribir las líneas modificadas de vuelta al archivo
    with open(MODELS_PATH, 'w') as f:
        f.writelines(lines)
    
    print("Archivo models.py modificado correctamente")
    return True

def restore_original():
    """Restaura el archivo original desde la copia de seguridad"""
    if os.path.exists(BACKUP_PATH):
        try:
            shutil.copy2(BACKUP_PATH, MODELS_PATH)
            os.remove(BACKUP_PATH)
            print("Archivo original restaurado correctamente")
            return True
        except Exception as e:
            print(f"Error al restaurar el archivo original: {e}")
            return False
    else:
        print("No se encontró copia de seguridad para restaurar")
        return False

if __name__ == "__main__":
    print("Iniciando corrección de problemas de zona horaria...")
    if fix_timezone_issue():
        print("Corrección aplicada con éxito")
    else:
        print("No se pudo aplicar la corrección") 