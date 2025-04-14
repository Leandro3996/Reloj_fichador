# Guía de Reinstalación del Sistema Reloj Fichador

## Introducción

Esta guía explica los pasos para reinstalar el sistema Reloj Fichador con el nuevo usuario superusuario "sistemas" en la base de datos MySQL. Este proceso soluciona problemas de permisos que impedían el correcto funcionamiento de los servicios.

## Requisitos previos

- Docker y Docker Compose instalados y funcionando
- Acceso a terminal con permisos para ejecutar scripts
- Los scripts deben tener permisos de ejecución (`chmod +x nombre_script.sh`)

## Proceso de reinstalación

### 1. Preparación

Asegúrate de estar en el directorio raíz del proyecto:

```bash
cd /ruta/al/proyecto/Reloj_fichador
```

Verifica que los scripts tienen permisos de ejecución:

```bash
chmod +x create_mysql_superuser.sh restart_with_new_user.sh
```

### 2. Ejecución del script de reinicio

Ejecuta el script de reinicio:

```bash
./restart_with_new_user.sh
```

Este script realizará automáticamente las siguientes acciones:
1. Detener todos los contenedores en ejecución
2. Iniciar solo el contenedor de la base de datos
3. Esperar a que la base de datos esté disponible
4. Crear el usuario superusuario "sistemas"
5. Iniciar el resto de los contenedores
6. Mostrar el estado de los contenedores

### 3. Verificación del sistema

Para verificar que el sistema está funcionando correctamente, revisa los logs:

```bash
docker-compose logs -f
```

Los servicios deberían iniciar sin errores relacionados con permisos de MySQL.

### 4. Acceso a la aplicación

Una vez que todos los servicios están en ejecución, puedes acceder a la aplicación en:

- Aplicación web: http://localhost:5080
- Reportes BIRT: http://localhost:6003/birt

### 5. Solución de problemas

Si encuentras algún problema durante el proceso:

1. **Problemas con la base de datos:**
   ```bash
   docker-compose logs db
   ```

2. **Problemas con la aplicación web:**
   ```bash
   docker-compose logs web
   ```

3. **Problemas con Celery:**
   ```bash
   docker-compose logs celery celery-beat
   ```

Si necesitas reiniciar un servicio específico:
```bash
docker-compose restart nombre_servicio
```

## Cambios realizados

Este proceso ha implementado las siguientes mejoras:

1. Creación de un usuario "sistemas" con todos los privilegios necesarios
2. Corrección de errores en el servicio de backup
3. Optimización de la configuración de conexión a MySQL
4. Actualización de los archivos de configuración

## Contacto para soporte

Si encuentras problemas durante el proceso, contacta al equipo de soporte técnico en:
- Email: soporte@empresa.com
- Teléfono: (123) 456-7890 