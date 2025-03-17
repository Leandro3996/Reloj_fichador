"""
Script para corregir permanentemente el problema de indentación en models.py
"""

import os
import re
import shutil

# Ruta al archivo models.py
MODELS_PATH = 'apps/reloj_fichador/models.py'
BACKUP_PATH = f"{MODELS_PATH}.bak"

def fix_indentation_issue():
    """Corrige permanentemente el problema de indentación en el archivo models.py"""
    
    print(f"Corrigiendo problema de indentación en {MODELS_PATH}")
    
    # Verificar si el archivo existe
    if not os.path.exists(MODELS_PATH):
        print(f"Error: El archivo {MODELS_PATH} no existe")
        return False
    
    # Hacer copia de seguridad
    shutil.copy2(MODELS_PATH, BACKUP_PATH)
    print(f"Copia de seguridad creada en {BACKUP_PATH}")
    
    with open(MODELS_PATH, 'r') as f:
        lines = f.readlines()
    
    # Buscar el bloque problemático
    in_calcular_horas = False
    indentation_fixed = False
    for i, line in enumerate(lines):
        if "def calcular_horas_por_franjas" in line:
            in_calcular_horas = True
        
        if in_calcular_horas and "elif (" in line and "):'" in line.replace(" ", ""):
            # Encontramos el elif problemático
            # Buscar el final del bloque elif
            j = i
            while j < len(lines) and not lines[j].strip().endswith('):'):
                j += 1
            
            if j < len(lines):
                # Tenemos el final del bloque elif en la línea j
                # Ahora buscamos las líneas que deberían estar indentadas
                k = j + 1
                
                # Determinar el nivel de indentación base
                base_indent = len(line) - len(line.lstrip())
                # El bloque elif debe tener 4 espacios más
                indent = ' ' * (base_indent + 4)
                
                # Desde k+1 hasta encontrar otra línea con la misma indentación que el elif
                while k < len(lines):
                    if lines[k].strip() and not lines[k].startswith(indent) and not lines[k].strip().startswith('#'):
                        # Si encontramos una línea con menos indentación que no es un comentario, 
                        # es el fin del bloque
                        if len(lines[k]) - len(lines[k].lstrip()) <= base_indent:
                            break
                    
                    # Procesar líneas que necesitan indentación
                    if lines[k].strip() and not lines[k].strip().startswith('#'):
                        current_indent = len(lines[k]) - len(lines[k].lstrip())
                        # Si la línea no tiene suficiente indentación para estar dentro del elif
                        if current_indent <= base_indent:
                            # Añadir indentación
                            lines[k] = indent + lines[k].lstrip()
                            indentation_fixed = True
                    k += 1
    
    if indentation_fixed:
        # Guardar los cambios
        with open(MODELS_PATH, 'w') as f:
            f.writelines(lines)
        print(f"¡Corrección aplicada con éxito! El archivo {MODELS_PATH} ha sido actualizado.")
        return True
    else:
        print("No se encontró el problema específico o ya está corregido.")
        return False

if __name__ == "__main__":
    success = fix_indentation_issue()
    if success:
        print("La corrección se aplicó correctamente. Comprueba el archivo para verificar los cambios.")
        print(f"Se ha creado una copia de seguridad en {BACKUP_PATH} por si necesitas restaurar el archivo original.")
    else:
        print("No se pudo aplicar la corrección automáticamente.") 