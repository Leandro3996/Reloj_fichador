"""
Script para diagnosticar y corregir problemas de indentación en el archivo models.py
"""

import os
import re
import sys

def examine_file(file_path):
    """Examina un archivo para detectar problemas de indentación en bloques elif"""
    
    if not os.path.exists(file_path):
        print(f"El archivo {file_path} no existe")
        return False
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Examinar las líneas cercanas a la 80
    start_line = max(0, 70)
    end_line = min(len(lines), 90)
    
    print(f"\nExaminando líneas {start_line+1} a {end_line} del archivo:")
    print("-" * 50)
    
    for i in range(start_line, end_line):
        line_num = i + 1
        line = lines[i].rstrip()
        print(f"{line_num:3d}: {line}")
        
        # Buscar líneas de elif sin bloque indentado a continuación
        if re.match(r'\s*elif\s+.*:', line):
            # Verificar si la siguiente línea existe y tiene indentación
            if i+1 < len(lines):
                next_line = lines[i+1]
                if not next_line.strip() or not re.match(r'\s+', next_line):
                    print(f"\n¡PROBLEMA ENCONTRADO! Línea {line_num} tiene un 'elif' sin bloque indentado")
                    return True
    
    print("\nNo se encontraron problemas obvios de indentación en las líneas examinadas.")
    return False

def fix_indentation_issue(file_path):
    """Corrige automáticamente el problema de elif sin bloque indentado"""
    
    if not os.path.exists(file_path):
        print(f"El archivo {file_path} no existe")
        return False
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Hacer una copia de seguridad
    backup_path = f"{file_path}.bak"
    with open(backup_path, 'w') as f:
        f.writelines(lines)
    
    print(f"Copia de seguridad creada en {backup_path}")
    
    # Buscar el problema específico en la línea 80 (índice 79)
    fixed = False
    for i in range(len(lines)):
        # Línea cercana a la 80 con elif sin bloque indentado
        if re.match(r'\s*elif\s+.*:', lines[i].rstrip()):
            line_num = i + 1
            if line_num >= 79 and line_num <= 81:
                # Verificar si la siguiente línea tiene indentación adecuada
                if i+1 < len(lines) and (not lines[i+1].strip() or not re.match(r'\s+', lines[i+1])):
                    # Determinar la indentación del bloque
                    current_indent = len(lines[i]) - len(lines[i].lstrip())
                    indent = ' ' * (current_indent + 4)  # 4 espacios extra para el bloque
                    
                    # Insertar un pass indentado después del elif
                    lines.insert(i+1, f"{indent}pass  # Añadido para corregir error de indentación\n")
                    
                    print(f"Se añadió 'pass' indentado después del elif en la línea {line_num}")
                    fixed = True
                    break
    
    if fixed:
        # Guardar el archivo corregido
        with open(file_path, 'w') as f:
            f.writelines(lines)
        print(f"Archivo {file_path} corregido")
        return True
    else:
        print(f"No se encontró el problema específico para corregir en {file_path}")
        return False

def restore_original(file_path):
    """Restaura el archivo original desde la copia de seguridad"""
    
    backup_path = f"{file_path}.bak"
    if os.path.exists(backup_path):
        try:
            with open(backup_path, 'r') as src, open(file_path, 'w') as dst:
                dst.write(src.read())
            print(f"Archivo {file_path} restaurado desde la copia de seguridad")
            return True
        except Exception as e:
            print(f"Error al restaurar el archivo: {e}")
            return False
    else:
        print(f"No se encontró copia de seguridad para {file_path}")
        return False

def main():
    """Función principal"""
    
    # Ruta al archivo models.py
    models_path = '/app/apps/reloj_fichador/models.py'
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'examine':
            examine_file(models_path)
        elif command == 'fix':
            fix_indentation_issue(models_path)
        elif command == 'restore':
            restore_original(models_path)
        else:
            print(f"Comando desconocido: {command}")
    else:
        print("Uso: python fix_models.py [examine|fix|restore]")

if __name__ == '__main__':
    main() 