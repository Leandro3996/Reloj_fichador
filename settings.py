# Configuración especial para las pruebas
import sys
if 'test' in sys.argv:
    print("Usando SQLite en memoria para las pruebas")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
    
    # Acelerar las pruebas
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]
    
    # Desactivar algunas funcionalidades no necesarias en pruebas
    DEBUG = False 