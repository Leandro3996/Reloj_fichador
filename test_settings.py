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