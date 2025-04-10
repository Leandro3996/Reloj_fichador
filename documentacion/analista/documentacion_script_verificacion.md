# Documentación: Script de Verificación de Servicios Docker

## Descripción General

El script `verificacion_docker.sh` es una herramienta de diagnóstico para verificar y resolver problemas comunes en los contenedores Docker del proyecto Reloj Fichador. Proporciona información detallada sobre el estado de los servicios y ofrece soluciones automatizadas para problemas conocidos.

## Ubicación

```
documentacion/analista/scripts/verificacion_docker.sh
```

## Requisitos

- Docker instalado y en ejecución
- Docker Compose instalado (ya sea como comando independiente o como plugin de Docker)
- Permisos de ejecución en el script (`chmod +x verificacion_docker.sh`)

## Uso

```bash
./verificacion_docker.sh [reiniciar]
```

### Parámetros

- `reiniciar` (opcional): Si se proporciona, el script reiniciará automáticamente los contenedores que no estén funcionando correctamente.

## Funcionalidades

El script realiza las siguientes acciones:

1. **Verificación de prerrequisitos**:
   - Comprueba que Docker esté instalado y en ejecución
   - Identifica la versión correcta de Docker Compose disponible en el sistema

2. **Análisis de estado**:
   - Muestra el estado actual de todos los contenedores
   - Compara el número total de contenedores con los que están en ejecución

3. **Diagnóstico de problemas**:
   - Analiza los logs de los contenedores que no están en ejecución
   - Identifica errores específicos conocidos en la configuración de MySQL:
     - Problemas con `default-authentication-plugin` (obsoleto en MySQL 8.4.0)
     - Valor inválido en `authentication_policy`

4. **Corrección automática** (con parámetro `reiniciar`):
   - Detiene todos los contenedores con `docker-compose down`
   - Inicia todos los contenedores con `docker-compose up -d`
   - Verifica nuevamente el estado después del reinicio

5. **Validación de conectividad**:
   - Comprueba la conexión a la base de datos MySQL utilizando las credenciales del archivo `.env`

## Salida

El script proporciona mensajes detallados con códigos de colores para facilitar la lectura:

- **VERDE**: Mensajes informativos (INFO)
- **AMARILLO**: Advertencias (WARN)
- **ROJO**: Errores críticos (ERROR)

Cada mensaje incluye una marca de tiempo para facilitar el seguimiento de las acciones realizadas.

## Estructura del Código

El script está organizado de forma modular y sigue las mejores prácticas de shell scripting:

1. **Funciones de utilidad**:
   - `log()`: Gestiona la salida formateada con colores y marcas de tiempo

2. **Verificaciones iniciales**:
   - Comprobación de dependencias
   - Validación de la estructura del proyecto

3. **Análisis de estado**:
   - Verificación de contenedores
   - Detección de problemas específicos

4. **Acciones correctivas**:
   - Reinicio de servicios (cuando se solicita)
   - Validación post-reinicio

5. **Verificaciones adicionales**:
   - Comprobación de conectividad a bases de datos

## Mejoras Implementadas

Se han aplicado varias optimizaciones al script para aumentar su robustez:

1. **Correcciones de seguridad**:
   - Uso de comillas dobles en todas las variables para prevenir problemas de expansión
   - Manejo seguro de comandos y argumentos

2. **Optimizaciones de rendimiento**:
   - Uso de `grep -c` en lugar de `grep | wc -l` para conteos más eficientes

3. **Mejoras de legibilidad**:
   - Separación clara de funcionalidades
   - Comentarios descriptivos para facilitar el mantenimiento

## Casos de Uso

### Verificación Rutinaria

Para comprobar el estado de los contenedores sin realizar cambios:

```bash
./verificacion_docker.sh
```

### Solución Automática de Problemas

Para diagnosticar y resolver problemas automáticamente:

```bash
./verificacion_docker.sh reiniciar
```

## Solución de Problemas

Si el script reporta errores, las acciones recomendadas son:

1. Verificar los mensajes específicos de error en los logs
2. Comprobar la configuración en `docker-compose.yml`
3. Asegurar que el archivo `.env` contenga las credenciales correctas

## Mantenimiento

El script está diseñado para ser fácilmente extensible. Para añadir detección de nuevos problemas:

1. Identificar el patrón de error en los logs
2. Añadir una nueva condición en la sección de verificación de logs
3. Proporcionar un mensaje claro con la solución recomendada

## Historial de Cambios

- **10/04/2025**: Versión inicial con detección de problemas de autenticación en MySQL 8.4.0
- **10/04/2025**: Optimización con correcciones de ShellCheck para mayor robustez
- **10/04/2025**: Documentación completa del script 