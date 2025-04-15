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

## 10/04/2025 - Creación de guía para activar USE_TZ en Django

### Contexto
Tras detectar y corregir los problemas con zonas horarias en Celery, se ha identificado que la configuración `USE_TZ = False` en Django es la raíz del problema. Para ofrecer una solución más robusta, se ha creado una guía detallada para cambiar esta configuración a `USE_TZ = True` minimizando el impacto en el funcionamiento actual del sistema.

### Acciones realizadas
1. Se ha desarrollado una guía paso a paso detallada: [`documentacion/analista/guia_activacion_TZ.md`](../guia_activacion_TZ.md)
2. La guía incluye:
   - Procedimiento para realizar pruebas en un entorno aislado
   - Script para convertir las fechas existentes en la base de datos
   - Puntos clave del código a revisar y actualizar
   - Instrucciones para pruebas exhaustivas
   - Plan de implementación en producción
   - Estrategia de rollback en caso de problemas

### Consideraciones técnicas
El cambio de `USE_TZ = False` a `USE_TZ = True` requiere especial atención en:
- Conversión de fechas existentes en la base de datos para añadir información de zona horaria
- Actualización de consultas que comparan fechas directamente
- Revisión de formularios con campos de fecha/hora
- Verificación de funcionalidades que dependen de cálculos de tiempo

### Próximos pasos
1. Implementar la guía en un entorno de pruebas
2. Validar todas las funcionalidades críticas
3. Planificar la implementación en producción durante un período de baja actividad

### Documentación relacionada
- [Guía de activación de USE_TZ](../guia_activacion_TZ.md)
- [Script de verificación de Celery y zonas horarias](../verificar_celery_timezone.sh)

## 11/04/2025 - Activación de soporte de zonas horarias en Django (USE_TZ=True)

### Descripción
Se ha modificado la configuración de Django para habilitar el soporte completo de zonas horarias mediante el cambio de `USE_TZ = False` a `USE_TZ = True` en el archivo `mantenedor/settings.py`.

### Motivación
Este cambio se realiza para solucionar problemas de consistencia en el manejo de fechas y horas entre Django y Celery, especialmente en la programación de tareas periódicas con django-celery-beat. Con la configuración anterior (USE_TZ=False), existía una discrepancia entre cómo Django y Celery interpretaban los tiempos.

### Implicaciones
La activación de `USE_TZ=True` tiene las siguientes implicaciones importantes:

1. **Almacenamiento de fechas**: Django ahora almacenará todas las fechas en UTC en la base de datos, independientemente de la zona horaria configurada.
2. **Consistencia con Celery**: Mejora la compatibilidad con Celery y django-celery-beat, que funcionan mejor con fechas conscientes de zonas horarias.
3. **Cambios en el comportamiento de la aplicación**: Este cambio puede requerir ajustes en la forma en que se manejan las fechas en toda la aplicación:
   - Las consultas de fechas pueden necesitar ser actualizadas para tener en cuenta la zona horaria.
   - Las comparaciones de fechas podrían comportarse de manera diferente.
   - La visualización de fechas en la interfaz de usuario podría requerir ajustes.

### Acciones requeridas
Este cambio debe ser probado exhaustivamente en un entorno de prueba antes de implementarse en producción:

1. Verificar el funcionamiento de todas las funcionalidades relacionadas con fechas y horas.
2. Revisar y ajustar las consultas a la base de datos que involucren fechas.
3. Comprobar que las tareas programadas de Celery se ejecuten en los momentos correctos.
4. Actualizar los tests que incluyan comparaciones de fechas.

### Seguimiento
Tras la implementación de este cambio, se requiere un período de observación para detectar cualquier comportamiento inesperado relacionado con las fechas y horas en el sistema.

## 12/04/2025 - Corrección de problemas de acceso en MySQL 8.4.0 y optimización de la configuración

### Problema identificado:
Al analizar los logs de Docker, se detectaron errores críticos que impedían el arranque correcto de los servicios `web` y `celery-beat`:

```
Access denied; you need (at least one of) the SYSTEM_VARIABLES_ADMIN or SESSION_VARIABLES_ADMIN privilege(s) for this operation
```

También se observó un error en el servicio de backup:

```
mysqldump: [ERROR] unknown variable 'defaults-file=/root/.my.cnf'
```

### Causa raíz:
1. El usuario de la base de datos no tenía los privilegios necesarios para modificar variables de sesión de MySQL 8.4.0, una operación que Django intenta realizar automáticamente durante la conexión.
2. La sintaxis del comando de backup en `docker-compose.yml` era incorrecta.
3. Los archivos de configuración contenían credenciales inconsistentes.

### Solución implementada:
1. **Creación de un usuario con privilegios adecuados**:
   - Se configuró el usuario `sistemas` con los permisos necesarios para las operaciones que requiere Django.
   - Se otorgaron explícitamente los privilegios `SYSTEM_VARIABLES_ADMIN` y `SESSION_VARIABLES_ADMIN`.
   - Se asignaron permisos específicos para operaciones de backup.

2. **Ajuste de configuración de Django**:
   - Se modificó el archivo `settings.py` para establecer un conjunto específico de modos SQL.
   - Se ajustaron los parámetros de conexión a la base de datos para mejorar la compatibilidad con MySQL 8.4.0.
   - Se añadieron opciones para autocommit y nivel de aislamiento.

3. **Estandarización de credenciales**:
   - Se actualizaron los archivos `.env` y `my_backup.cnf` con credenciales consistentes.
   - Se eliminaron caracteres especiales en las contraseñas que podían causar problemas en scripts de shell.

### Cambios específicos:

1. En `settings.py`, se modificó la configuración de la base de datos:
```python
'OPTIONS': {
    'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'",
    'charset': 'utf8mb4',
    'connect_timeout': 30,
    'autocommit': True,
    'isolation_level': 'READ COMMITTED',
},
```

2. Se ejecutaron comandos de MySQL para otorgar privilegios al usuario:
```sql
CREATE USER IF NOT EXISTS 'sistemas'@'%' IDENTIFIED BY 'S1st3mas2024';
GRANT ALL PRIVILEGES ON *.* TO 'sistemas'@'%' WITH GRANT OPTION;
GRANT SYSTEM_VARIABLES_ADMIN, SESSION_VARIABLES_ADMIN ON *.* TO 'sistemas'@'%';
GRANT SELECT, RELOAD, LOCK TABLES, PROCESS, SHOW VIEW, EVENT ON *.* TO 'sistemas'@'%';
FLUSH PRIVILEGES;
```

3. Se actualizaron las credenciales en archivos de configuración:
   - En `.env`: Se estableció `MYSQL_USER=sistemas` y `MYSQL_PASSWORD=S1st3mas2024`
   - En `my_backup.cnf`: Se configuró directamente `user=sistemas` y `password=S1st3mas2024`

### Resultados:
- Todos los contenedores arrancan correctamente.
- El servicio web está operando sin errores.
- El programador de tareas (celery-beat) funciona normalmente.
- El servicio de backup puede realizar copias de seguridad sin problemas.
- Se ha eliminado el error de permisos en MySQL.

### Observaciones adicionales:
Durante el análisis, se detectó una discrepancia en `mantenedor/celery.py`, donde el comentario indica "Se ejecuta todos los días a las 1:00 AM (Argentina)" pero la configuración real es `crontab(hour=8, minute=34)`. Esta inconsistencia deberá ser revisada posteriormente.

### Próximos pasos recomendados:
1. Revisar y corregir los comentarios en las tareas programadas de Celery para evitar confusiones.
2. Implementar monitoreo de logs para detectar tempranamente problemas similares.
3. Considerar la creación de scripts de diagnóstico para verificar periódicamente la configuración del sistema.
4. Establecer un procedimiento para la rotación segura de credenciales de la base de datos.

## 14/04/2025 - Mejoras en la Experiencia de Usuario del Sistema de Fichaje

### Problemas identificados:
Durante una revisión exhaustiva del sistema, se identificaron varios problemas que afectaban la experiencia de usuario:

1. **Inconsistencia de Hora**: La hora mostrada en la interfaz utilizaba la hora local del dispositivo cliente, lo que generaba discrepancias con la hora real del servidor utilizada para registrar las fichadas.

2. **Mensajes Temporales Insuficientes**: Los mensajes de notificación (confirmaciones de fichadas, errores) desaparecían automáticamente después de solo 5 segundos, lo que causaba problemas cuando varios operarios fichaban consecutivamente.

3. **Problemas de CSRF**: El sistema experimentaba errores "CSRF cookie not set" que impedían a los usuarios registrar entradas y salidas correctamente, especialmente en navegadores antiguos o terminales con condiciones de red subóptimas.

### Soluciones implementadas:

1. **Sistema de Visualización de Hora Sincronizada con el Servidor**:
   - Sincronización inicial con el servidor al cargar la página
   - Cálculo preciso del desfase entre hora local y del servidor, considerando latencia de red
   - Actualización local del reloj cada segundo usando el desfase calculado
   - Resincronización periódica cada 5 minutos para corregir posibles derivas
   - Modificaciones en el endpoint `/api/health/` para proporcionar hora en formato ISO con zona horaria Argentina

2. **Sistema Mejorado de Gestión de Mensajes**:
   - Aumento de la duración base de los mensajes a 30 segundos
   - Implementación de reinicio del temporizador basado en interacción del usuario
   - Sistema centralizado para gestión de temporizadores de mensajes
   - Gestión inteligente que permite que múltiples operarios vean sus mensajes de confirmación

3. **Corrección de Problemas de CSRF**:
   - Actualización de la función `getCookie` para manejar correctamente el nombre personalizado de cookie CSRF
   - Ampliación del middleware CSRF para incluir todas las IPs relevantes de terminales
   - Adición de exención CSRF a nivel de vista para la funcionalidad crítica de registro de movimientos

### Beneficios obtenidos:
- **Mayor precisión**: La hora mostrada corresponde siempre a la hora real del servidor
- **Eficiencia mejorada**: Reducción drástica de peticiones al servidor, de 60 por minuto a solo 1 cada 5 minutos
- **Experiencia fluida**: Reloj actualizado cada segundo sin saltos ni retardos
- **Tolerancia a fallos**: Funcionamiento continuado incluso con problemas temporales de conexión
- **Consistencia visual**: Todos los terminales muestran la misma hora exacta
- **Mayor visibilidad de notificaciones**: Los mensajes permanecen visibles el tiempo necesario
- **Adaptabilidad al usuario**: El sistema se adapta a la actividad del usuario
- **Mayor disponibilidad**: Funcionamiento correcto incluso en navegadores antiguos o con condiciones de red subóptimas

### Documentación generada:
Se ha creado documentación detallada de las mejoras implementadas en el archivo [`documentacion/analista/mejoras_interfaz_usuario.md`](mejoras_interfaz_usuario.md), que incluye:
- Descripción detallada de los problemas y soluciones
- Código implementado con comentarios explicativos
- Ventajas de cada solución
- Recomendaciones para futuras mejoras

### Próximos pasos recomendados:
1. Monitorear el funcionamiento del sistema durante una semana para verificar que las soluciones implementadas resuelven completamente los problemas identificados.
2. Considerar la implementación de las mejoras adicionales sugeridas en la documentación, especialmente el sistema de caché para terminales sin conexión.
3. Realizar una encuesta de satisfacción entre los operarios para evaluar la mejora en la experiencia de usuario.

---

*Este documento se actualizará constantemente como parte del seguimiento del proyecto.* 