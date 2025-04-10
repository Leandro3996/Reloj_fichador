# Scripts de Mantenimiento y Soporte

Este directorio contiene scripts útiles para el mantenimiento y la operación del Sistema Reloj Fichador en entornos Docker.

## Índice de scripts

| Script | Descripción | Uso |
|--------|-------------|-----|
| [`verificacion_docker.sh`](./verificacion_docker.sh) | Verifica el estado de contenedores Docker y detecta problemas comunes | `./verificacion_docker.sh [reiniciar]` |
| [`mantenimiento.sh`](./mantenimiento.sh) | Realiza tareas comunes de mantenimiento del sistema | `./mantenimiento.sh [opción]` |

## Script de Verificación

### Características principales

- Detecta automáticamente contenedores que no están funcionando
- Analiza los logs para identificar errores conocidos, especialmente en MySQL
- Proporciona soluciones a problemas comunes de configuración
- Ofrece la opción de reiniciar automáticamente los servicios con problemas
- Verifica la conectividad con la base de datos

### Uso común

```bash
# Solo verificar y mostrar problemas
./verificacion_docker.sh

# Verificar y reiniciar automáticamente los servicios con problemas
./verificacion_docker.sh reiniciar
```

### Documentación completa

Ver [documentación detallada](../documentacion_script_verificacion.md) para más información.

## Script de Mantenimiento

### Opciones disponibles

- `backup`: Crea una copia de seguridad de la base de datos
- `limpiar_logs`: Comprime y archiva logs antiguos
- `estado`: Muestra el estado actual de los contenedores
- `reiniciar`: Reinicia todos los servicios de Docker
- `actualizar`: Actualiza el código desde el repositorio
- `test`: Ejecuta las pruebas automatizadas
- `migrar`: Ejecuta migraciones pendientes de Django
- `staticfiles`: Recolecta archivos estáticos
- `ayuda`: Muestra información de ayuda

### Ejemplos de uso

```bash
# Crear un backup de la base de datos
./mantenimiento.sh backup

# Limpiar logs antiguos
./mantenimiento.sh limpiar_logs

# Verificar estado actual
./mantenimiento.sh estado

# Actualizar el sistema
./mantenimiento.sh actualizar
```

## Mejores prácticas

- Siempre asegúrate de tener permisos de ejecución (`chmod +x script.sh`)
- Ejecuta los scripts desde el directorio raíz del proyecto o usar rutas absolutas
- Revisa los logs generados para identificar posibles problemas
- Programa ejecuciones periódicas para mantenimiento preventivo

## Mejoras recientes

### 10/04/2025
- Corrección de problemas de compatibilidad con MySQL 8.4.0
- Optimización de scripts siguiendo mejores prácticas de seguridad
- Mejoras en manejo de errores y reporte de problemas

---

*Todos los scripts siguen las mejores prácticas de shell scripting y han sido optimizados para máxima robustez y claridad.* 