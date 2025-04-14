# Guía de Configuración de MySQL 8.4.0 con Django

> **Fecha:** 12/04/2025  
> **Autor:** Analista de Sistemas  
> **Versión:** 1.0

## Introducción

Esta guía detalla la configuración óptima para usar MySQL 8.4.0 con Django en el sistema Reloj Fichador, abordando los problemas comunes de permisos y configuración que pueden surgir con esta versión específica de MySQL.

## Requisitos de privilegios

MySQL 8.4.0 implementa un sistema de privilegios más estricto que versiones anteriores, lo que puede afectar a aplicaciones Django que intentan modificar variables de sesión durante la conexión. Los privilegios mínimos requeridos son:

### Privilegios básicos:
- `SELECT`, `INSERT`, `UPDATE`, `DELETE` (operaciones CRUD)
- `CREATE`, `ALTER`, `DROP` (gestión de estructura)
- `INDEX` (creación/eliminación de índices)
- `REFERENCES` (restricciones de clave foránea)

### Privilegios adicionales para Django:
- `SYSTEM_VARIABLES_ADMIN` (permitir modificar variables del sistema)
- `SESSION_VARIABLES_ADMIN` (permitir modificar variables de sesión)

### Privilegios para backup:
- `RELOAD` (para operaciones como FLUSH)
- `LOCK TABLES` (para consistencia durante backups)
- `PROCESS` (monitoreo de procesos en curso)
- `SHOW VIEW` (para hacer backup de vistas)
- `EVENT` (para programar eventos)

## Configuración óptima en Django

La siguiente configuración para `settings.py` proporciona una compatibilidad óptima con MySQL 8.4.0:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'",
            'charset': 'utf8mb4',
            'connect_timeout': 30,
            'autocommit': True,
            'isolation_level': 'READ COMMITTED',
        },
    }
}
```

### Parámetros explicados:

1. **`init_command`**: Define el modo SQL a utilizar al iniciar cada conexión.
   - `STRICT_TRANS_TABLES`: Rechaza valores inválidos en transacciones
   - `NO_ZERO_IN_DATE`/`NO_ZERO_DATE`: Rechaza fechas con componentes cero o completamente cero
   - `ERROR_FOR_DIVISION_BY_ZERO`: Genera error al dividir por cero
   - `NO_ENGINE_SUBSTITUTION`: Evita sustitución automática de motores de almacenamiento

2. **`charset`**: Define la codificación de caracteres (`utf8mb4` soporta todos los caracteres Unicode, incluidos emojis).

3. **`connect_timeout`**: Tiempo máximo (en segundos) para establecer la conexión.

4. **`autocommit`**: Confirma automáticamente cada sentencia SQL.

5. **`isolation_level`**: Define cómo las transacciones afectan a otras transacciones concurrentes.
   - `READ COMMITTED`: Las lecturas dentro de una transacción solo ven datos confirmados.

## Configuración de usuario en MySQL

Para crear un usuario con los privilegios necesarios, ejecute los siguientes comandos en MySQL:

```sql
-- Crear el usuario con contraseña
CREATE USER 'sistemas'@'%' IDENTIFIED BY 'S1st3mas2024';

-- Otorgar privilegios generales
GRANT ALL PRIVILEGES ON *.* TO 'sistemas'@'%' WITH GRANT OPTION;

-- Otorgar privilegios específicos de sistema
GRANT SYSTEM_VARIABLES_ADMIN, SESSION_VARIABLES_ADMIN ON *.* TO 'sistemas'@'%';

-- Otorgar privilegios para backup
GRANT SELECT, RELOAD, LOCK TABLES, PROCESS, SHOW VIEW, EVENT ON *.* TO 'sistemas'@'%';

-- Aplicar los cambios
FLUSH PRIVILEGES;
```

## Solución a problemas comunes

### Error: Access denied for SYSTEM_VARIABLES_ADMIN

**Síntoma:**
```
Access denied; you need (at least one of) the SYSTEM_VARIABLES_ADMIN or SESSION_VARIABLES_ADMIN privilege(s) for this operation
```

**Solución:**
1. Otorgar los privilegios necesarios:
   ```sql
   GRANT SYSTEM_VARIABLES_ADMIN, SESSION_VARIABLES_ADMIN ON *.* TO 'usuario'@'%';
   FLUSH PRIVILEGES;
   ```
2. O modificar la configuración de Django para evitar establecer variables de sistema:
   ```python
   'OPTIONS': {
       'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'",
   }
   ```

### Error: Unknown variable 'defaults-file'

**Síntoma:**
```
mysqldump: [ERROR] unknown variable 'defaults-file=/path/to/file'
```

**Solución:**
Corregir la sintaxis del comando, separando el parámetro y su valor:
```bash
# Incorrecto
mysqldump defaults-file=/path/to/file

# Correcto
mysqldump --defaults-file=/path/to/file
```

O usar parámetros directos:
```bash
mysqldump -h host -u usuario -pcontraseña base_de_datos
```

## Consideraciones de seguridad

1. **Privilegios mínimos**: Aunque en esta guía otorgamos privilegios amplios para facilitar el diagnóstico, en un entorno de producción se recomienda limitar los privilegios al mínimo necesario.

2. **Contraseñas seguras**: Utilice contraseñas complejas (mínimo 12 caracteres, combinando mayúsculas, minúsculas, números y símbolos).

3. **Restricción de acceso**: Limite desde qué hosts puede conectarse el usuario (por ejemplo, `'usuario'@'localhost'` en lugar de `'usuario'@'%'`).

4. **Auditoría**: Implemente auditoría de acceso y cambios en la base de datos.

## Recomendaciones adicionales

1. **Monitoreo**: Configure alertas para detectar intentos de acceso fallidos o consumo anormal de recursos.

2. **Backups**: Realice backups periódicos y verifique que se pueden restaurar correctamente.

3. **Actualizaciones**: Manténgase al día con las actualizaciones de seguridad tanto de MySQL como de Django.

4. **Documentación**: Mantenga documentados todos los cambios de configuración y priviliegios. 