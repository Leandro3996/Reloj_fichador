# Sistema de Reloj Fichador

Un sistema integral para gestión de asistencia, cálculo de horas trabajadas y generación de reportes, desarrollado con Django y desplegado con Docker.

![Versión](https://img.shields.io/badge/versión-1.0-blue)
![Plataforma](https://img.shields.io/badge/plataforma-Docker-informational)
![Framework](https://img.shields.io/badge/framework-Django-success)

## Descripción

El "Reloj Fichador" es un sistema completo para controlar la asistencia y calcular horas trabajadas de operarios en entornos laborales. Permite registrar entradas y salidas, calcular diferentes tipos de horas (normales, nocturnas, extras, feriados), gestionar justificaciones y licencias, y generar informes detallados.

## Características Principales

- **Registro de Asistencia**: Sistema de fichaje con cuatro tipos de movimientos (entrada, salida, entrada transitoria, salida transitoria)
- **Cálculo Automático**: Algoritmo sofisticado para calcular diferentes tipos de horas trabajadas
- **Gestión de Operarios**: Administración de empleados, áreas y horarios
- **Sistema de Licencias**: Gestión de permisos y justificaciones con documentación adjunta
- **Reportes Avanzados**: Generación de informes con BIRT (Business Intelligence and Reporting Tools)
- **Automatización**: Tareas programadas con Celery para procesos recurrentes

## Requisitos

- Docker y Docker Compose
- 4GB RAM mínimo recomendado
- 10GB espacio en disco

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd Reloj_fichador
```

2. Configurar variables de entorno (opcional - ya incluye valores por defecto):
```bash
# Editar archivo .env según necesidades
```

3. Iniciar los servicios con Docker Compose:
```bash
docker-compose up -d
```

4. Acceder a la aplicación:
```
http://localhost:5080
```

## Estructura del Proyecto

```
.
├── apps/                  # Aplicaciones Django
│   └── reloj_fichador/    # Aplicación principal
├── backups/               # Copias de seguridad de la BD
├── birt/                  # Sistema de informes
├── mantenedor/            # Configuración principal de Django
├── templates/             # Plantillas HTML
└── ... (otros directorios)
```

Para una descripción completa de la estructura, consultar [estructura.md](estructura.md).

## Servicios Docker

El proyecto está compuesto por varios servicios:

- **db**: Base de datos MySQL
- **web**: Aplicación Django principal
- **celery** y **celery-beat**: Procesamiento de tareas asíncronas
- **redis**: Broker de mensajes
- **nginx**: Servidor web
- **backup**: Copias de seguridad automáticas
- **birt**: Servidor para reportes

## Uso Básico

### Acceso al sistema
1. Acceder a través del navegador: `http://localhost:5080`
2. Ingresar credenciales de administrador (por defecto admin/admin)

### Registro de movimientos
1. En la pantalla principal, ingresar el DNI del operario
2. Seleccionar el tipo de movimiento (entrada, salida, etc.)
3. Confirmar el registro

### Administración
1. Acceder al panel de administración: `http://localhost:5080/admin/`
2. Gestionar operarios, áreas, horarios, licencias, etc.

### Reportes
1. Acceder a la sección de reportes
2. Seleccionar el tipo de informe
3. Configurar parámetros (fechas, operarios, etc.)
4. Generar y descargar el reporte

## Configuración Avanzada

### Ajustar variables de entorno
Editar el archivo `.env` para modificar:
- Credenciales de base de datos
- Configuración de debug
- URLs permitidas
- Configuración de Celery

### Personalizar reportes
Los reportes BIRT se encuentran en el directorio `reportes/` y pueden ser modificados usando el diseñador BIRT.

## Mantenimiento

### Copias de seguridad
Se generan automáticamente cada 2 horas en el directorio `backups/`. Para restaurar:

```bash
docker-compose exec db mysql -u root -p docker_horesdb < backups/nombre_backup.sql
```

### Logs
Los logs se encuentran en:
- `logs/` para logs de aplicación
- `error.log` para errores generales

## Pruebas

Para ejecutar las pruebas automatizadas:

```bash
# Pruebas con SQLite (rápidas)
./run_sqlite_tests.bat

# Pruebas con MySQL (completas)
./run_tests.bat
```

## Tecnologías Utilizadas

- **Backend**: Django, MySQL, Celery, Redis
- **Frontend**: HTML/CSS/JavaScript, Bootstrap
- **Infraestructura**: Docker, Nginx, Gunicorn, BIRT

## Documentación Adicional

- [Contexto del Proyecto](contexto.md) - Explicación detallada del funcionamiento
- [Estructura del Proyecto](estructura.md) - Arquitectura completa
- [TESTING.md](TESTING.md) - Información sobre pruebas

## Contribución

1. Crear una rama (`git checkout -b feature/nombre-caracteristica`)
2. Realizar cambios y pruebas
3. Confirmar cambios (`git commit -m 'Descripción del cambio'`)
4. Enviar a la rama (`git push origin feature/nombre-caracteristica`)
5. Crear un Pull Request

## Soporte

Para reportar problemas, utilizar el sistema de issues del repositorio o contactar al equipo de desarrollo.

## Licencia

Este proyecto está bajo licencia privada. Todos los derechos reservados.

# Sistema Reloj Fichador - Documentación

## Introducción

Este repositorio contiene la documentación completa del Sistema Reloj Fichador, estructurada para ser utilizada con [Obsidian](https://obsidian.md/), una potente herramienta para gestión de conocimiento y notas enlazadas.

## Estructura de la Documentación

La documentación está organizada en varios archivos Markdown interconectados:

- **[Índice Principal](Indice_Reloj_Fichador.md)**: Punto central de navegación para acceder a todos los documentos
- **[Contexto del Proyecto](contexto.md)**: Descripción general, reglas de negocio y objetivos del sistema
- **[Arquitectura](estructura.md)**: Estructura técnica del proyecto, directorios y componentes
- **Diagramas de Flujo**:
  - [Diagramas Mermaid](Diagrama_de_flujo_Fichador.md): Representación en formato Mermaid
  - [Diagramas Visuales](Diagrama_de_flujo_Visual.md): Versión mejorada con elementos gráficos
  - [Diagramas ASCII](Diagrama_de_flujo_ASCII.md): Versión en arte ASCII para máxima compatibilidad

## Cómo Usar esta Documentación con Obsidian

1. **Instalación de Obsidian**:
   - Descarga e instala [Obsidian](https://obsidian.md/download)
   - Crea un nuevo vault o abre uno existente

2. **Importación de los Archivos**:
   - Copia todos los archivos `.md` en la carpeta de tu vault de Obsidian
   - Obsidian automáticamente reconocerá los enlaces entre archivos

3. **Navegación**:
   - Comienza por abrir `Indice_Reloj_Fichador.md`
   - Navega a través de los enlaces con doble corchete `[[archivo]]`
   - Utiliza los bloques de navegación ubicados al principio y final de cada documento

4. **Características Útiles**:
   - Utiliza el panel de gráfico de Obsidian para visualizar las conexiones entre documentos
   - Aprovecha la búsqueda rápida (Ctrl+P en Windows/Linux, Cmd+P en Mac) para encontrar secciones específicas
   - Los enlaces a secciones específicas utilizan la sintaxis `[[archivo#sección]]`

## Visualización de Diagramas

- Para ver correctamente los diagramas Mermaid, asegúrate de tener activado el plugin "Mermaid" en Obsidian
- Puedes encontrarlo en Configuración → Plugins del núcleo → Mermaid
- Los diagramas ASCII son compatibles con cualquier editor de texto

## Recomendaciones

- Utiliza el modo de vista previa de Obsidian para una mejor experiencia de lectura
- Aprovecha la característica de "Linked Mentions" para ver qué otros documentos hacen referencia al que estás leyendo
- Explora los diferentes temas disponibles en Obsidian para personalizar la apariencia

---

Para cualquier duda o sugerencia sobre esta documentación, por favor contacta al equipo de desarrollo. 