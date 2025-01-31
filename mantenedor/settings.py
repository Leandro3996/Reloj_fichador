"""
Django settings for reloj_fichador project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


SECRET_KEY = 'django-insecure-mp&6m=!k202ckikyskc^td9pj3r&luzc$kuo+v1!9@$q@l7c0q'

DEBUG = True

ALLOWED_HOSTS = ['*']
#ALLOWED_HOSTS = ['localhost', '192.168.10.11', '192.168.100.111', '192.168.10.18', '192.168.10.46', '192.168.68.51', '192.168.68.54']

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.reloj_fichador',

    # Aplicaciones de terceros
    'simple_history',
    'rangefilter',
    'django_celery_beat',
    'django_celery_results',
    'django_tables2',
    'import_export',
    'weasyprint',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'mantenedor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

WSGI_APPLICATION = 'mantenedor.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'docker_horesdb'),
        'USER': os.environ.get('DB_USER', 'Leandro.3996'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'S1st3mas.1999'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'auth_plugin': 'caching_sha2_password',
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_TZ = False

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://redis:6379/5')
CELERY_BEAT_SCHEDULER = env('CELERY_BEAT_SCHEDULER', default='django_celery_beat.schedulers:DatabaseScheduler')

CSRF_TRUSTED_ORIGINS = ['http://localhost:5080','http://192.168.0.228:5080','http://192.168.10.11:5080',]


# Configuraciones adicionales para sesiones y CSRF

# Duración de la sesión y el token CSRF
SESSION_COOKIE_AGE = 60 * 60 * 24 * 365  # 1 año
CSRF_COOKIE_AGE = 60 * 60 * 24 * 365  # 1 año

# Guardar la sesión en cada solicitud para prolongar su duración
SESSION_SAVE_EVERY_REQUEST = True

# Desactivar la seguridad de las cookies ya que no estás utilizando HTTPS
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# Establecer SameSite para proteger las cookies contra CSRF
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'

# Desactivar HTTPOnly para permitir acceso al token CSRF desde JavaScript si es necesario
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_HTTPONLY = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',  # Cambia a DEBUG temporalmente para más detalles
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',  # Mantén INFO para evitar demasiados detalles en el core
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARNING',  # Mantén WARNING para evitar SQL detallado
            'propagate': False,
        },
        'reloj_fichador': {  # Agrega tu módulo aquí
            'handlers': ['console'],
            'level': 'DEBUG',  # Permite mensajes DEBUG para tu app
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
    },
}
