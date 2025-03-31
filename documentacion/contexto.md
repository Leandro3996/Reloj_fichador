# Contexto del Proyecto "Reloj Fichador"

> [!info] Navegación
> **Índice Principal:** [[Indice_Reloj_Fichador|Índice del Sistema]]  
> **Diagramas:** [[Diagrama_de_flujo_Fichador|Mermaid]] | [[Diagrama_de_flujo_Visual|Visual]] | [[Diagrama_de_flujo_ASCII|ASCII]]  
> **Arquitectura:** [[estructura|Estructura del Proyecto]]

## Descripción General

El "Reloj Fichador" es un sistema integral para gestionar y controlar la asistencia y horas trabajadas de operarios en un entorno laboral. El sistema permite registrar entradas y salidas de los operarios, calcular automáticamente las horas trabajadas según diferentes conceptos (normales, nocturnas, extras, feriados), y generar informes detallados.

## Propósito

Este sistema está diseñado para resolver los siguientes problemas:

1. Registrar con precisión la asistencia de los operarios
2. Calcular automáticamente las horas trabajadas según diversas reglas
3. Gestionar diferentes tipos de horarios y áreas de trabajo
4. Administrar justificaciones y licencias
5. Generar reportes para análisis y gestión

## Componentes Principales

### 1. Sistema de Registro de Asistencia

El componente central del proyecto es el sistema de registro de asistencia o "fichaje". Los operarios pueden registrar cuatro tipos de movimientos:
- **Entrada**: Inicio de la jornada laboral
- **Salida transitoria**: Salida temporal durante la jornada
- **Entrada transitoria**: Regreso después de una salida temporal
- **Salida**: Finalización de la jornada laboral

El sistema valida estos movimientos para asegurar su consistencia (por ejemplo, una entrada debe ser seguida por una salida).

### 2. Cálculo de Horas Trabajadas

El sistema implementa un sofisticado algoritmo para calcular diferentes tipos de horas:

- **Horas normales**: Trabajadas en horario regular (06:00 a 20:00)
- **Horas nocturnas**: Trabajadas en horario nocturno (20:00 a 06:00)
- **Horas extras**: Excedentes al horario regular
- **Horas feriado**: Trabajadas en días festivos

Además, aplica reglas específicas de redondeo:
- Para la entrada: redondeo hacia arriba a la siguiente hora completa
- Para la salida: redondeo hacia abajo a la hora anterior (si se cumplieron al menos 8 horas de trabajo)

### 3. Gestión de Operarios y Áreas

El sistema permite administrar:
- **Operarios**: Información personal, historial, áreas asignadas, estado (activo/inactivo)
- **Áreas**: Divisiones organizacionales con horarios específicos
- **Horarios**: Definición de diferentes turnos de trabajo

### 4. Sistema de Licencias y Justificaciones

Permite gestionar:
- Licencias con documentación adjunta (archivos PDF, imágenes)
- Fechas de inicio y fin de las licencias
- Justificaciones de ausencias

### 5. Reportes y Análisis

El sistema utiliza BIRT (Business Intelligence and Reporting Tools) para generar informes detallados sobre:
- Asistencia diaria
- Horas trabajadas por operario
- Horas totales mensuales
- Análisis por áreas y conceptos

### 6. Automatización con Tareas Programadas

Utiliza Celery para ejecutar tareas automáticas como:
- Generación diaria de registros de asistencia
- Verificación automática de la asistencia
- Cálculos periódicos de horas trabajadas

## Reglas de Negocio para Horarios y Tolerancias

### Horarios de Ingreso Estándar

#### Turnos de Mañana
- **5:00 AM**: Jornada completa (8 horas)
- **6:00 AM**: Jornada completa (8 horas)
- **7:00 AM**: Media jornada (4-5 horas)
- **8:00 AM**: Media jornada (4-5 horas)
- **9:00 AM**: Media jornada (4 horas)
- **Otros horarios**: Inusuales, generalmente por trámites o asuntos médicos del personal

#### Turnos de Tarde
- **1:00 PM**: Jornada completa (8 horas)
- **2:00 PM**: Media jornada (3-4 horas)
- **3:00 PM**: Media jornada (3-4 horas)
- **4:00 PM**: Media jornada (3 horas) o capacitación/horas extras
- **5:00 PM**: Casos excepcionales, mayormente capacitación o horas extras
- **6:00 PM**: Muy raro, reservado para roles con responsabilidades especiales

#### Turnos de Noche
- **9:00 PM**: Horario estándar para el personal nocturno, incluyendo a dirigentes
- **10:00 PM**: Excepcional, generalmente con permiso previo
- **11:00 PM**: Muy improbable

### Políticas de Puntualidad y Fichaje

#### Anticipación Normal
- Los operarios habitualmente fichan entre 0 y 30 minutos antes de su horario oficial de ingreso
- **Ejemplo**: Si el ingreso es a las 8:00 AM, lo normal es que fiche entre las 7:30 AM y las 7:59:59 AM

#### Tolerancia a Retrasos
- **Hasta 5 minutos de retraso**: Tolerado, pero el operario pierde el premio mensual de asistencia
  - Se le pagan las 8 horas completas de trabajo
- **Entre 15-20 minutos de retraso**: Posible negación de ingreso al trabajo
  - Excepciones: Notificación previa con días de anticipación

#### Consideraciones para el Sistema
- El sistema debe distinguir entre llegada tardía e ingreso temprano
- La determinación se basa principalmente en si el operario completó su jornada laboral (8 horas para jornada completa)
- El sistema de redondeo debe ajustarse a estas reglas específicas de la empresa
- Se requiere flexibilidad para casos especiales con autorización previa

## Tecnologías Utilizadas

### Backend
- **Django**: Framework web principal
- **MySQL**: Base de datos relacional
- **Celery**: Sistema de procesamiento de tareas asíncronas
- **Redis**: Broker de mensajes para Celery

### Frontend
- **HTML/CSS/JavaScript**: Interfaz de usuario
- **Bootstrap**: Framework CSS para diseño responsivo

### Infraestructura
- **Docker**: Contenedores para cada servicio
- **Docker Compose**: Orquestación de servicios
- **Nginx**: Servidor web
- **Gunicorn**: Servidor WSGI para Django
- **BIRT**: Sistema de informes

## Flujos de Datos y Procesos

### Registro de Asistencia
1. El operario se identifica con su DNI
2. Selecciona el tipo de movimiento (entrada, salida, etc.)
3. El sistema valida el movimiento para evitar inconsistencias
4. Se registra el movimiento con marca de tiempo

### Cálculo de Horas
1. Para cada operario y fecha, el sistema recopila todos los registros de entrada/salida
2. Aplica reglas de redondeo según configuración
3. Clasifica las horas según el tipo (normales, nocturnas, extras, feriado)
4. Almacena los resultados en tablas específicas para cada concepto
5. Calcula totales mensuales

### Generación de Reportes
1. El usuario selecciona el tipo de reporte
2. Define parámetros (fechas, operarios, áreas)
3. El sistema recupera los datos necesarios
4. BIRT procesa y formatea la información
5. Se genera el reporte en el formato solicitado (PDF, Excel, etc.)

## Mantenimiento y Administración

### Panel de Administración
- Django Admin personalizado para gestionar todos los aspectos del sistema
- Interfaces especializadas para operarios, áreas, horarios, etc.
- Filtros avanzados para consultas específicas

### Copias de Seguridad
- Sistema automatizado de backups de la base de datos
- Programación configurable (por defecto cada 2 horas)
- Almacenamiento de copias con marcas temporales

### Registros (Logs)
- Sistema de logging detallado
- Registros separados para errores y operaciones
- Configuración de niveles de detalle según entorno

## Estrategia de Pruebas

El proyecto incluye herramientas para pruebas automatizadas:
- Pruebas unitarias para modelos y funciones críticas
- Scripts de prueba para entornos específicos (SQLite para desarrollo rápido)
- Documentación de pruebas en `TESTING.md`

## Consideraciones Futuras

Aspectos que podrían considerarse para futuras mejoras:
1. Implementación de APIs REST para integración con otros sistemas
2. Aplicación móvil para registro de asistencia
3. Sistema de notificaciones en tiempo real
4. Análisis predictivo de ausencias y patrones de asistencia
5. Integración con sistemas de nómina y recursos humanos

---

> [!tip] Documentos Relacionados
> - Para ver los diagramas de flujo detallados, consulta [[Diagrama_de_flujo_Fichador|Diagramas Mermaid]]
> - Para una visualización avanzada, revisa [[Diagrama_de_flujo_Visual|Diagramas Visuales]]
> - Para diagramas en texto plano, consulta [[Diagrama_de_flujo_ASCII|Diagramas ASCII]]
> - Para entender la estructura técnica, ve a [[estructura|Arquitectura del Proyecto]]
> - Regresa al [[Indice_Reloj_Fichador|Índice Principal]] 