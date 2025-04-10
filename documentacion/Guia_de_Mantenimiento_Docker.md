# Guía de Mantenimiento de Contenedores Docker

## Introducción

Este documento proporciona información detallada sobre el mantenimiento y gestión de los contenedores Docker en el Sistema Reloj Fichador. Se incluyen herramientas, scripts, problemas comunes y sus soluciones, así como recomendaciones para un correcto funcionamiento del entorno.

## Índice de Contenidos

1. [Arquitectura de Contenedores](#arquitectura-de-contenedores)
2. [Scripts de Mantenimiento](#scripts-de-mantenimiento)
3. [Problemas Comunes y Soluciones](#problemas-comunes-y-soluciones)
4. [Buenas Prácticas](#buenas-prácticas)
5. [Monitorización y Verificación](#monitorización-y-verificación)
6. [Respaldos y Recuperación](#respaldos-y-recuperación)

---

## Arquitectura de Contenedores

El sistema Reloj Fichador está compuesto por los siguientes servicios en contenedores:

| Servicio | Imagen | Puerto | Descripción |
|----------|--------|--------|-------------|
| `db` | mysql:8.4.0 | 53306:3306 | Base de datos MySQL |
| `web` | (personalizada) | 58000:58000 | Aplicación Django con Gunicorn |
| `celery` | (personalizada) | - | Procesamiento asíncrono de tareas |
| `celery-beat` | (personalizada) | - | Programación de tareas periódicas |
| `redis` | redis:alpine | 6381:6379 | Broker para Celery |
| `nginx` | nginx:latest | 5080:80 | Servidor web y proxy inverso |
| `backup` | mysql:8.4.0 | - | Servicio de respaldo automático |
| `birt` | tomcat:9.0 | 6003:8088 | Generación de informes |

Los servicios están definidos en el archivo `docker-compose.yml` y están configurados para trabajar en la red `app_network_fichador`.

## Scripts de Mantenimiento

El sistema cuenta con dos scripts principales para el mantenimiento:

### 1. Script de Verificación (verificacion_docker.sh)

Ubicación: `documentacion/analista/scripts/verificacion_docker.sh`

Este script verifica el estado de todos los contenedores y detecta problemas comunes, especialmente relacionados con la configuración de MySQL.

**Uso:**
```bash
./verificacion_docker.sh [reiniciar]
```

**Características principales:**
- Detección automática de contenedores que no están en ejecución
- Análisis de logs para identificar errores conocidos
- Solución asistida para problemas de configuración en MySQL
- Capacidad de reinicio automático de contenedores
- Verificación de conectividad a la base de datos

[Documentación completa del script de verificación](documentacion/analista/documentacion_script_verificacion.md)

### 2. Script de Mantenimiento (mantenimiento.sh)

Ubicación: `documentacion/analista/scripts/mantenimiento.sh`

Este script proporciona múltiples funciones para tareas comunes de mantenimiento del sistema.

**Uso:**
```bash
./mantenimiento.sh [opción]
```

**Opciones disponibles:**
- `backup`: Crea una copia de seguridad de la base de datos
- `limpiar_logs`: Comprime y archiva logs antiguos
- `estado`: Muestra el estado actual de los contenedores
- `reiniciar`: Reinicia todos los servicios de Docker
- `actualizar`: Actualiza el código desde el repositorio
- `test`: Ejecuta las pruebas automatizadas
- `migrar`: Ejecuta migraciones pendientes de Django
- `staticfiles`: Recolecta archivos estáticos
- `ayuda`: Muestra información de ayuda

El script implementa medidas de seguridad como backups automáticos antes de actualizaciones y validación de acciones destructivas.

## Problemas Comunes y Soluciones

### Problema 1: Error de Configuración en MySQL 8.4.0

**Síntomas:**
- El contenedor de MySQL no arranca correctamente
- Aparece en los logs: `unknown variable 'default-authentication-plugin=mysql_native_password'`

**Causa:**
MySQL 8.4.0 ha eliminado la opción `default-authentication-plugin` que era válida en versiones anteriores.

**Solución:**
Modificar el comando en `docker-compose.yml`:
```yaml
command: >
  --authentication_policy='*,,' --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci --explicit_defaults_for_timestamp=1
```

### Problema 2: Valor Inválido en authentication_policy

**Síntomas:**
- El contenedor de MySQL no arranca correctamente
- Aparece en los logs: `Option --authentication-policy is set to an invalid value`

**Causa:**
El formato del parámetro `authentication_policy` es incorrecto. Este parámetro espera un formato específico con una lista delimitada por comas.

**Solución:**
La configuración correcta es `--authentication_policy='*,,'` donde:
- El primer asterisco (`*`) permite todos los métodos de autenticación para el primer factor
- Las comas vacías indican que no se requieren segundo y tercer factores

### Problema 3: Servicios Dependientes No Inician

**Síntomas:**
- Servicios como `web`, `celery` o `celery-beat` no arrancan
- Errores de conexión a la base de datos en los logs

**Causa:**
Los servicios intentan conectarse a la base de datos antes de que esté completamente iniciada.

**Solución:**
El script `wait-for-it.sh` ya está configurado para gestionar estas dependencias. Si persisten los problemas:
1. Ejecutar `docker-compose down` para detener todos los servicios
2. Ejecutar `docker-compose up -d db` para iniciar solo la base de datos
3. Esperar 30 segundos para asegurar que la base de datos esté completamente iniciada
4. Ejecutar `docker-compose up -d` para iniciar el resto de servicios

## Buenas Prácticas

### Actualización de Imágenes

1. **Verificar compatibilidad**: Revisar las notas de la versión antes de actualizar imágenes base
2. **Entorno de pruebas**: Probar actualizaciones en un entorno aislado antes de aplicarlas en producción
3. **Backups previos**: Siempre realizar respaldos antes de actualizar imágenes o configuraciones
4. **Actualización progresiva**: Actualizar un servicio a la vez para facilitar la identificación de problemas

### Seguridad

1. **No exponer puertos innecesarios**: Revisar regularmente los mapeos de puertos
2. **Rotación de credenciales**: Cambiar periódicamente las contraseñas de la base de datos
3. **Limitar acceso a volúmenes**: Proteger los volúmenes con datos sensibles
4. **Verificar configuración**: Validar que no hay valores predeterminados o inseguros

### Optimización de Rendimiento

1. **Limpieza regular**: Ejecutar `docker system prune` para eliminar recursos no utilizados
2. **Monitoreo de recursos**: Verificar regularmente el uso de CPU, memoria y disco
3. **Optimización de volúmenes**: Considerar volúmenes con rendimiento optimizado para bases de datos
4. **Ajuste de configuración**: Optimizar parámetros de Gunicorn, Nginx y MySQL según carga

## Monitorización y Verificación

### Verificación Proactiva

Se recomienda programar ejecuciones periódicas del script de verificación:

```bash
# Ejemplo de programación en crontab
0 8 * * * /ruta/absoluta/a/verificacion_docker.sh > /ruta/a/logs/verificacion_$(date +\%Y\%m\%d).log 2>&1
```

### Monitorización con Herramientas Externas

Para una monitorización más avanzada, considerar la implementación de:
- Prometheus + Grafana para métricas y visualización
- Alertmanager para notificaciones automáticas
- ELK Stack (Elasticsearch, Logstash, Kibana) para análisis centralizado de logs

## Respaldos y Recuperación

### Estrategia de Respaldos

El sistema implementa dos niveles de respaldo:

1. **Respaldos automáticos**: El contenedor `backup` realiza copias de seguridad periódicas
2. **Respaldos manuales**: El script `mantenimiento.sh` permite crear respaldos bajo demanda

### Recomendaciones para Respaldos

1. **Diversificar ubicaciones**: Almacenar respaldos en múltiples ubicaciones
2. **Verificar integridad**: Probar regularmente la restauración de respaldos
3. **Rotación**: Implementar políticas de retención para optimizar espacio
4. **Cifrado**: Considerar el cifrado de respaldos con datos sensibles

### Procedimiento de Recuperación

1. Detener los servicios: `docker-compose down`
2. Restaurar el respaldo:
   ```bash
   gunzip -c backups/backup_YYYYMMDD_HHMMSS.sql.gz | docker-compose exec -T db mysql -u root -p"$MYSQL_ROOT_PASSWORD" docker_horesdb
   ```
3. Reiniciar los servicios: `docker-compose up -d`
4. Verificar la integridad de los datos

---

## Historial de Actualizaciones

| Fecha | Versión | Descripción |
|-------|---------|-------------|
| 10/04/2025 | 1.0 | Documentación inicial con estructura básica |
| 10/04/2025 | 1.1 | Incorporación de solución para problemas de authentication_policy en MySQL 8.4.0 |
| 10/04/2025 | 1.2 | Adición de scripts de mantenimiento y verificación |

---

## Referencias

- [Documentación oficial de Docker](https://docs.docker.com/)
- [Documentación de MySQL 8.4](https://dev.mysql.com/doc/relnotes/mysql/8.4/en/)
- [Bitácora del proyecto](documentacion/analista/bitacora_proyecto.md)
- [Recomendaciones Docker](documentacion/analista/recomendaciones_docker.md) 