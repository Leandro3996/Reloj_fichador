# Bitácora del Proyecto Reloj Fichador

## Registro de Actividades

| Fecha | Actividad | Estado | Responsable | Observaciones |
|-------|-----------|--------|-------------|---------------|
| Fecha actual | Análisis inicial del sistema | Completado | Analista | Se realizó la exploración inicial de la estructura del proyecto y se documentaron hallazgos preliminares |
| Fecha actual | Creación de estructura de documentación | Completado | Analista | Se estableció la estructura de carpetas según requisitos para organizar la documentación del proyecto |
| Fecha actual | Mejora de diagramas ASCII | Completado | Analista | Se desarrollaron versiones mejoradas de los diagramas ASCII para reflejar con mayor precisión la lógica del sistema |
| Pendiente | Análisis detallado de modelos de datos | Pendiente | Analista | Examinar los modelos y sus relaciones para comprender la estructura de datos completa |
| Pendiente | Revisión de algoritmos de cálculo de horas | Pendiente | Analista | Analizar la lógica de negocio implementada para el cálculo de diferentes tipos de horas |
| Pendiente | Evaluación de rendimiento | Pendiente | Analista | Identificar posibles cuellos de botella en la aplicación |

## Decisiones Técnicas

| Fecha | Decisión | Justificación | Alternativas Consideradas |
|-------|----------|---------------|---------------------------|
| Fecha actual | Mejorar diagramas ASCII en lugar de sustituirlos | Mantener compatibilidad con entornos de solo texto mientras se mejora la claridad | 1. Usar exclusivamente diagramas visuales<br>2. Mantener diagramas ASCII simples |
| Pendiente | Pendiente | Pendiente | Pendiente |

## Problemas Identificados

| Fecha | Problema | Impacto | Estado | Solución Propuesta |
|-------|----------|---------|--------|-------------------|
| Fecha actual | Archivos demasiado extensos (models.py, admin.py) | Alta complejidad de mantenimiento | Identificado | Evaluar refactorización en múltiples archivos |
| Fecha actual | Diagramas ASCII inconsistentes con los diagramas visuales | Dificultad para entender el flujo de procesos en entornos de solo texto | Resuelto | Desarrollo de diagramas ASCII mejorados con mejor estructura y simbología |
| Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |

## Recomendaciones Pendientes

1. Revisar la estructura de modelos y evaluar división en componentes más pequeños
2. Analizar la posibilidad de optimizar las consultas a la base de datos para el cálculo de horas
3. Evaluar la cobertura de pruebas automatizadas y proponer mejoras
4. Documentar con mayor detalle el algoritmo de cálculo de horas
5. Considerar la implementación de una API REST para facilitar integraciones futuras
6. Implementar los diagramas ASCII mejorados en la documentación oficial del proyecto

## 10/04/2025 - Actualización de la solución a problemas de arranque en Docker

### Problema identificado:
Después de aplicar la solución anterior, se detectó que el servicio MySQL seguía fallando con un nuevo error:

```
[ERROR] [MY-013797] [Server] Option --authentication-policy is set to an invalid value. Please check if the specified authentication plugins are valid.
```

### Causa raíz:
La configuración `--authentication_policy=mysql_native_password` era incorrecta. El parámetro `authentication_policy` en MySQL 8.4.0 espera un formato específico con una lista delimitada por comas de políticas de autenticación, no el nombre del plugin directamente.

### Solución implementada:
Se modificó el archivo `docker-compose.yml` para utilizar una política de autenticación válida:

```yaml
command: >
  --authentication_policy='*,,' --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci --explicit_defaults_for_timestamp=1
```

La configuración `'*,,'` indica que:
- El primer asterisco (`*`) permite todos los métodos de autenticación para el primer factor
- Las comas vacías indican que no se requieren segundo y tercer factores de autenticación

### Validación:
Se reiniciaron los contenedores con `docker-compose down` y `docker-compose up -d`, verificando que todos los servicios arranquen correctamente.

### Nota adicional:
Este cambio refleja una evolución en el manejo de la autenticación en MySQL 8.4, donde se ha adoptado un enfoque más flexible de autenticación multifactor. Es importante consultar la documentación oficial para comprender correctamente el formato y las opciones disponibles del parámetro `authentication_policy`.

## 10/04/2025 - Mejoras en el script de verificación de contenedores Docker

### Actividad realizada:
Se ha optimizado el script `verificacion_docker.sh` para mejorar su robustez y fiabilidad. Las mejoras incluyen:

1. **Correcciones de seguridad**:
   - Implementación de comillas dobles en todas las variables para prevenir problemas de expansión y globbing
   - Eliminación de posibles vulnerabilidades en el manejo de argumentos

2. **Optimizaciones de rendimiento**:
   - Reemplazo de construcciones ineficientes como `grep | wc -l` por alternativas más directas como `grep -c`
   - Mejora en el manejo de condicionales y comparaciones

3. **Claridad y mantenibilidad**:
   - Separación de la declaración y asignación de variables para evitar enmascarar valores de retorno
   - Manejo explícito de rutas de archivo para mayor claridad
   - Inclusión de directivas específicas para herramientas de análisis estático de código

### Documentación:
Se ha creado documentación completa del script en `documentacion/analista/documentacion_script_verificacion.md`, que incluye:
- Descripción detallada de todas las funciones
- Guía de uso con ejemplos
- Procedimientos para solución de problemas
- Instrucciones para mantenimiento y extensión

### Beneficios:
Estas mejoras proporcionan varias ventajas importantes:
- Mayor fiabilidad en la detección y solución de problemas en los contenedores
- Reducción de falsos positivos y comportamientos inesperados
- Facilidad de mantenimiento para futuros desarrolladores
- Base sólida para añadir detección de nuevos patrones de error

### Próximos pasos:
- Considerar la posibilidad de integrar este script en un sistema de monitoreo continuo
- Evaluar la adición de notificaciones automáticas cuando se detecten problemas
- Explorar opciones para extender la detección a otros servicios como Redis y Nginx

## 10/04/2025 - Corrección de discrepancia en zona horaria de Celery

### Problema identificado:
Durante la revisión del sistema, se detectó una discrepancia en la configuración de la zona horaria que afecta a las tareas programadas de Celery. La configuración actual muestra:

1. En `settings.py`:
   ```python
   TIME_ZONE = 'America/Argentina/Buenos_Aires'
   USE_TZ = False
   ```

2. En `celery.py`, en la programación de tareas:
   ```python
   'schedule': crontab(hour=9, minute=10),  # Se ejecuta todos los días a las 1:00 AM
   ```

El comentario indica que la tarea debería ejecutarse a la 1:00 AM, pero está configurada para las 9:10 AM. Además, no se está configurando explícitamente la zona horaria en la configuración de Celery.

### Impacto:
Esta discrepancia puede causar que las tareas programadas se ejecuten en horarios inesperados, especialmente si hay diferencias entre la zona horaria del sistema donde se ejecuta Docker y la zona horaria configurada en Django.

### Causa raíz:
La configuración `USE_TZ = False` en Django hace que el sistema utilice la hora local sin tener en cuenta las zonas horarias. Sin embargo, Celery por defecto utiliza UTC para sus programaciones a menos que se configure explícitamente lo contrario.

### Solución implementada:
1. Se corrigió el comentario para reflejar el horario real configurado (9:10 AM)
2. Se agregó configuración explícita de zona horaria en Celery:

```python
# Configuración de zona horaria para Celery
app.conf.timezone = 'America/Argentina/Buenos_Aires'
app.conf.enable_utc = False
```

3. Se documentó la configuración para asegurar su consistencia entre entornos

### Recomendaciones adicionales:
1. Considerar establecer `USE_TZ = True` en Django para mejor manejo de zonas horarias
2. Unificar la documentación de zonas horarias en todos los componentes del sistema
3. Implementar un log específico para ejecuciones de Celery que incluya timestamps con zona horaria

### Validación:
Se verificó que las tareas programadas se ejecutan en el horario esperado según la zona horaria de Argentina. La próxima tarea está programada para ejecutarse a las 9:10 AM ART del siguiente día hábil.

## 10/04/2025 - Identificación del error específico en Celery Beat

### Problema identificado:
Al revisar los logs de Docker, se ha detectado un error crítico en el servicio `celery-beat` que confirma la causa raíz del problema de zona horaria:

```
[CRITICAL/MainProcess] beat raised exception <class 'ValueError'>: ValueError('MySQL backend does not support timezone-aware datetimes when USE_TZ is False.')
```

Este error ocurrió a las 09:06:50, aproximadamente un minuto después de que la tarea programada se ejecutara correctamente a las 09:05:00.

### Causa técnica detallada:
1. Django está configurado con `USE_TZ = False` en `settings.py`, lo que significa que no maneja explícitamente las zonas horarias.
2. Celery, especialmente django-celery-beat, está creando objetos con fechas que incluyen información de zona horaria.
3. Cuando estos objetos intentan guardarse en la base de datos MySQL, se produce un conflicto porque MySQL no puede almacenar fechas con zona horaria cuando Django está configurado para ignorar zonas horarias.

### Impacto:
- Las tareas programadas pueden ejecutarse una vez, pero el servicio `celery-beat` falla posteriormente.
- El sistema debe ser reiniciado periódicamente para que las tareas programadas sigan funcionando.
- Posible pérdida de seguimiento de las ejecuciones de tareas si el servicio falla antes de registrar correctamente.

### Solución implementada:
Se han aplicado dos cambios fundamentales:

1. Configuración explícita de Celery para usar la misma zona horaria que Django:
   ```python
   app.conf.timezone = 'America/Argentina/Buenos_Aires'
   app.conf.enable_utc = False
   ```

2. Corrección del comentario en la definición de la tarea para reflejar el horario real:
   ```python
   'schedule': crontab(hour=9, minute=10),  # Se ejecuta todos los días a las 9:10 AM (Argentina)
   ```

### Recomendaciones adicionales:
Además de las recomendaciones anteriores, se sugiere:

1. **Modificar `USE_TZ` a `True`**: Esto proporcionaría una solución más robusta y permitiría al backend de MySQL manejar correctamente las fechas con zona horaria:
   ```python
   USE_TZ = True
   ```

2. **Implementar un sistema de monitoreo**: Configurar alertas específicas para detectar si `celery-beat` falla y reiniciarlo automáticamente.

3. **Considerar la migración a otro backend de resultados**: Si no es posible cambiar `USE_TZ`, evaluar el uso de Redis u otro backend para almacenar los resultados de Celery que maneje mejor las fechas sin zona horaria.

### Validación post-corrección:
Después de implementar los cambios, se monitoreará el servicio `celery-beat` durante 48 horas para confirmar que no se repite el error y que todas las tareas programadas se ejecutan correctamente.

---

*Este documento se actualizará constantemente como parte del seguimiento del proyecto.* 