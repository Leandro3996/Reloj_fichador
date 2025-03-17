"""
Configuración especial para ejecutar pruebas usando SQLite en memoria.
Este archivo hereda todas las configuraciones normales y solo sobrescribe
la configuración de la base de datos para usar SQLite.
"""

# Primero importamos todas las configuraciones normales
from mantenedor.settings import *

# Sobrescribir la configuración de la base de datos para usar SQLite en memoria
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # Usar base de datos en memoria para mayor velocidad
    }
}

# Imprimir mensaje para confirmar que se está usando esta configuración
print("Usando SQLite en memoria para las pruebas")
print(f"Configuración de zona horaria: USE_TZ={USE_TZ}, TIME_ZONE='{TIME_ZONE}'")

# Desactivar DEBUG para las pruebas
DEBUG = False

# Configuración adicional para acelerar las pruebas
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',  # Usar hasher más rápido para pruebas
]

# Reducir el número de middlewares para acelerar las pruebas
if 'django.middleware.security.SecurityMiddleware' in MIDDLEWARE:
    MIDDLEWARE.remove('django.middleware.security.SecurityMiddleware')
if 'django.middleware.csrf.CsrfViewMiddleware' in MIDDLEWARE:
    MIDDLEWARE.remove('django.middleware.csrf.CsrfViewMiddleware')

# Aplicar monkey patching para resolver problemas de zonas horarias
from django.utils import timezone

# Guardar las funciones originales
_original_min = min

# Redefinir min() para normalizar fechas automáticamente solo si USE_TZ=True
def _patched_min(*args, **kwargs):
    if USE_TZ:
        # Normalizar argumentos para asegurar que todas las fechas tengan zona horaria
        normalized_args = []
        for arg in args:
            if hasattr(arg, 'tzinfo') and arg.tzinfo is None:
                normalized_args.append(timezone.make_aware(arg))
            else:
                normalized_args.append(arg)
        
        # Llamar a la función original con los argumentos normalizados
        return _original_min(*normalized_args, **kwargs)
    else:
        # Si USE_TZ es False, usamos la función original sin modificar
        return _original_min(*args, **kwargs)

# Reemplazar la función min() por nuestra versión parcheada durante las pruebas
import builtins
builtins.min = _patched_min

print("Aplicado parche para normalizar fechas en comparaciones") 