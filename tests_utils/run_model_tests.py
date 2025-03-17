#!/usr/bin/env python
"""
Script para ejecutar pruebas de modelos con SQLite en memoria.
Este script configura temporalmente Django para usar SQLite,
permitiendo ejecutar las pruebas sin problemas de permisos.
"""

import os
import sys
import subprocess
import colorama
from datetime import datetime

# Inicializar colorama para que los colores funcionen en Windows
colorama.init()

# Colores para una mejor visualización
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'

def print_header(message):
    """Imprime un encabezado formateado"""
    width = 60
    print("\n" + "=" * width)
    print(f"{Colors.BLUE}{message.center(width)}{Colors.ENDC}")
    print("=" * width + "\n")

def print_success(message):
    """Imprime un mensaje de éxito"""
    print(f"{Colors.GREEN}{message}{Colors.ENDC}")

def print_error(message):
    """Imprime un mensaje de error"""
    print(f"{Colors.RED}{message}{Colors.ENDC}")

def print_info(message):
    """Imprime un mensaje informativo"""
    print(f"{Colors.YELLOW}{message}{Colors.ENDC}")

def run_tests(test_module, verbosity=2):
    """Ejecuta las pruebas para un módulo específico"""
    # Asegurarse de que estamos en el directorio del proyecto
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    
    # Establecer variable de entorno para usar la configuración especial
    settings_module = 'tests_utils.sqlite_settings'
    os.environ['DJANGO_SETTINGS_MODULE'] = settings_module
    
    # Comando para ejecutar las pruebas
    test_command = [
        sys.executable,  # usa el intérprete Python actual
        'manage.py',
        'test',
        test_module,
        '--settings=' + settings_module,
        '-v', str(verbosity)
    ]
    
    time_start = datetime.now()
    
    print_info(f"Ejecutando: {' '.join(test_command)}")
    
    # Ejecutar el comando
    result = subprocess.run(test_command)
    
    time_end = datetime.now()
    time_diff = (time_end - time_start).total_seconds()
    
    print_info(f"\nTiempo total de ejecución: {time_diff:.2f} segundos")
    
    # Devolver el código de salida
    return result.returncode

def main():
    """Función principal del script"""
    print_header("PRUEBAS DE MODELOS - RELOJ FICHADOR")
    print_info("Fecha y hora: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    
    # Ejecutar pruebas de modelos
    test_module = 'apps.reloj_fichador.tests.test_models'
    return_code = run_tests(test_module)
    
    if return_code == 0:
        print_success("\n✅ Todas las pruebas se ejecutaron correctamente.")
    else:
        print_error("\n❌ Se encontraron errores en las pruebas.")
    
    print_header("FIN DE PRUEBAS")
    
    return return_code

if __name__ == '__main__':
    sys.exit(main()) 