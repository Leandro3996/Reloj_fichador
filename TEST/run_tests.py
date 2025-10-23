#!/usr/bin/env python
"""
Script para ejecutar todos los tests del módulo TEST.

Uso:
    python TEST/run_tests.py
    python manage.py test TEST
"""

import os
import sys
import django
from io import StringIO

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mantenedor.settings')
django.setup()

from django.test.utils import get_runner
from django.conf import settings

def run_all_tests():
    """Ejecuta todos los tests del módulo TEST."""
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=False, keepdb=True)

    # Ejecutar tests del módulo TEST
    failures = test_runner.run_tests(["TEST"])

    return failures

if __name__ == '__main__':
    print("\n" + "="*70)
    print("EJECUTANDO SUITE DE TESTS - RELOJ FICHADOR")
    print("="*70 + "\n")

    failures = run_all_tests()

    print("\n" + "="*70)
    if failures == 0:
        print("✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
    else:
        print(f"❌ {failures} TEST(S) FALLARON")
    print("="*70 + "\n")

    sys.exit(bool(failures))
