# Análisis de Errores en Logs de Docker y Soluciones Aplicadas

## Errores Identificados

### 1. Error de acceso en servicio de backup
```
mysqldump: Error: 'Access denied; you need (at least one of) the PROCESS privilege(s) for this operation'
```
**Problema:** El usuario MySQL utilizado para los backups carece del privilegio PROCESS necesario para realizar copias de seguridad completas.

**Solución:** Crear un script SQL para otorgar el privilegio PROCESS al usuario:
```sql
GRANT PROCESS ON *.* TO 'Leandro.3996'@'%';
FLUSH PRIVILEGES;
```
Este script debe ejecutarse en el contenedor de base de datos con:
```bash
docker-compose exec db mysql -u root -p < soluciones_backups/01_grant_privileges.sql
```

### 2. Error de host no permitido
```
Invalid HTTP_HOST header: '190.96.116.202:5080'. You may need to add '190.96.116.202' to ALLOWED_HOSTS.
```
**Problema:** Django está rechazando conexiones desde la IP 190.96.116.202 porque no está en la lista de ALLOWED_HOSTS.

**Solución:** Se ha añadido '190.96.116.202' a la lista ALLOWED_HOSTS en el archivo `mantenedor/settings.py`.

### 3. Advertencia de seguridad en Celery
```
SecurityWarning: You're running the worker with superuser privileges: this is absolutely not recommended!
```
**Problema:** El worker de Celery se está ejecutando como usuario root (uid=0), lo que representa un riesgo de seguridad.

**Solución:** Se ha modificado el comando de inicio de Celery en `docker-compose.yml` para utilizar un usuario no privilegiado con `--uid=1000`.

### 4. Advertencia en MySQL sobre configuración insegura del archivo PID
```
Warning: Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users.
```
**Problema:** La ubicación del archivo PID de MySQL tiene permisos inseguros y es accesible para todos los usuarios del sistema.

**Solución:** Esta advertencia es común en entornos contenedorizados y no representa un riesgo de seguridad significativo en configuraciones Docker, ya que el contenedor tiene su propio espacio de nombres aislado. No obstante, si se quisiera resolver, se podría:
1. Modificar los permisos del directorio `/var/run/mysqld` en un Dockerfile personalizado
2. Especificar una ubicación alternativa para el archivo PID en la configuración de MySQL

## Recomendaciones para Implementar las Soluciones

1. Para aplicar los nuevos privilegios MySQL, ejecute:
   ```bash
   docker-compose exec db mysql -u root -p < soluciones_backups/01_grant_privileges.sql
   ```

2. Tras modificar `settings.py` y `docker-compose.yml`, reinicie los servicios afectados:
   ```bash
   docker-compose up -d --build web celery
   ```

3. Para verificar que los errores han sido resueltos, monitorice los logs después de reiniciar los servicios:
   ```bash
   docker-compose logs -f backup web celery
   ``` 