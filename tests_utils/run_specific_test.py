#!/usr/bin/env python
"""
Script para ejecutar pruebas específicas del sistema Reloj Fichador.
Permite ejecutar pruebas individuales o clases específicas de test.
"""

import os
import sys
import argparse
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
    width = 70
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

def run_tests(test_path, verbosity=2):
    """Ejecuta las pruebas para un módulo o test específico"""
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
        test_path,
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
    parser = argparse.ArgumentParser(description='Ejecuta pruebas específicas del Reloj Fichador.')
    parser.add_argument('test_path', nargs='?', default='apps.reloj_fichador.tests',
                        help='Ruta del test a ejecutar (ej: apps.reloj_fichador.tests.test_views.ReporteViewTest)')
    parser.add_argument('-v', '--verbosity', type=int, default=2,
                        help='Nivel de detalle (1-3, donde 3 es máximo detalle)')
    
    args = parser.parse_args()
    
    print_header(f"EJECUTANDO PRUEBA: {args.test_path}")
    print_info("Fecha y hora: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    
    # Ejecutar las pruebas especificadas
    return_code = run_tests(args.test_path, args.verbosity)
    
    if return_code == 0:
        print_success("\n✅ Todas las pruebas se ejecutaron correctamente.")
    else:
        print_error("\n❌ Se encontraron errores en las pruebas.")
    
    print_header("FIN DE PRUEBAS")
    
    return return_code

if __name__ == '__main__':
    sys.exit(main()) 