# Arquitectura del Proyecto "Reloj Fichador"

> [!info] Navegación
> **Índice Principal:** [[Indice_Reloj_Fichador|Índice del Sistema]]  
> **Contexto del Proyecto:** [[contexto|Contexto y Reglas de Negocio]]  
> **Diagramas:** [[Diagrama_de_flujo_Fichador|Mermaid]] | [[Diagrama_de_flujo_Visual|Visual]] | [[Diagrama_de_flujo_ASCII|ASCII]]

## Estructura General

El proyecto "Reloj Fichador" es una aplicación de control de asistencia y registro de horas trabajadas desarrollada con Django y desplegada con Docker.

## Directorio Raíz

```
.
├── .devcontainer/         # Configuración para desarrollo en contenedores
├── .vscode/               # Configuración de Visual Studio Code
├── apps/                  # Aplicaciones Django
│   └── reloj_fichador/    # Aplicación principal para el control de asistencia
├── backups/               # Directorio para almacenar copias de seguridad de la base de datos
├── birt/                  # Sistema de informes BIRT para generación de reportes
├── birt_drivers/          # Drivers para la conexión de BIRT con MySQL
├── config/                # Archivos de configuración adicionales
├── data/                  # Datos iniciales para la base de datos
├── logs/                  # Archivos de registro de la aplicación
├── mantenedor/            # Aplicación principal del proyecto Django
├── media/                 # Archivos subidos por los usuarios (fotos de operarios, licencias, etc.)
├── mysql_data/            # Datos persistentes de MySQL
├── reportes/              # Plantillas de reportes para BIRT
├── static/                # Archivos estáticos (CSS, JS, imágenes)
├── staticfiles/           # Archivos estáticos recopilados para producción
├── templates/             # Plantillas HTML
└── tests_utils/           # Utilidades para pruebas
```

## Estructura de Servicios (Docker)

El proyecto utiliza Docker Compose para definir y ejecutar múltiples servicios:

1. **db**: Servidor MySQL para almacenamiento de datos.
2. **web**: Aplicación Django principal.
3. **celery**: Procesamiento de tareas asíncronas.
4. **celery-beat**: Programador de tareas periódicas.
5. **redis**: Broker de mensajes para Celery.
6. **nginx**: Servidor web para servir la aplicación.
7. **backup**: Servicio para realizar copias de seguridad automáticas de la base de datos.
8. **birt**: Servidor Tomcat con BIRT para la generación de reportes.

## Aplicación Principal: Reloj Fichador

La aplicación principal se encuentra en `apps/reloj_fichador/` y contiene:

```
apps/reloj_fichador/
├── migrations/            # Migraciones de la base de datos
├── tests/                 # Pruebas automatizadas
├── __init__.py            # Inicializador del paquete
├── admin.py               # Configuración del panel de administración
├── apps.py                # Configuración de la aplicación
├── context_processors.py  # Procesadores de contexto personalizados
├── decorators.py          # Decoradores personalizados para vistas
├── filters.py             # Filtros para vistas y modelos
├── forms.py               # Formularios
├── middleware.py          # Middleware personalizado
├── models.py              # Modelos de datos
├── signals.py             # Señales para automatización
├── tables.py              # Definiciones de tablas para django-tables2
├── tasks.py               # Tareas asíncronas para Celery
├── tests.py               # Pruebas básicas
├── urls.py                # Configuración de URLs
├── utils.py               # Funciones de utilidad
└── views.py               # Vistas
```

## Configuración del Proyecto Django

El núcleo de configuración de Django se encuentra en `mantenedor/`:

```
mantenedor/
├── __init__.py            # Inicializador del paquete
├── asgi.py                # Configuración ASGI para servidores asíncronos
├── celery.py              # Configuración de Celery
├── settings.py            # Configuración principal de Django
├── urls.py                # Rutas URL del proyecto
└── wsgi.py                # Configuración WSGI para servidores web
```

---

> [!tip] Documentos Relacionados
> - Para entender el propósito y reglas de negocio, consulta [[contexto|Contexto del Proyecto]]
> - Para ver los diagramas de flujo detallados, revisa [[Diagrama_de_flujo_Fichador|Diagramas Mermaid]]
> - Para una visualización avanzada, ve a [[Diagrama_de_flujo_Visual|Diagramas Visuales]]
> - Para diagramas en texto plano, consulta [[Diagrama_de_flujo_ASCII|Diagramas ASCII]]
> - Regresa al [[Indice_Reloj_Fichador|Índice Principal]] 