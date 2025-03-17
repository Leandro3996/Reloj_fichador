# Guía de Pruebas Automatizadas - Reloj Fichador

Este documento explica cómo ejecutar las pruebas automatizadas para el proyecto Reloj Fichador.

## Estructura de Pruebas

Las pruebas están organizadas en varios archivos:

- `apps/reloj_fichador/tests/test_models.py`: Pruebas para los modelos
- `apps/reloj_fichador/tests/test_registro_diario.py`: Pruebas para el registro diario
- `apps/reloj_fichador/tests/test_calculo_horas.py`: Pruebas para el cálculo de horas
- `apps/reloj_fichador/tests/test_views.py`: Pruebas para las vistas
- `apps/reloj_fichador/tests/test_integracion.py`: Pruebas de integración

## Cómo Ejecutar las Pruebas

### Requisitos Previos

- Docker Desktop debe estar instalado y en ejecución
- Los contenedores del proyecto deben estar activos (se iniciarán automáticamente si no lo están)

### Forma Sencilla (Recomendada)

1. Ejecuta el script principal de pruebas haciendo doble clic en:
   ```
   run_tests.bat
   ```

2. Selecciona una opción del menú:
   - Opción 1: Ejecutar todas las pruebas
   - Opción 2: Ejecutar solo pruebas de modelos
   - Opción 3: Ejecutar solo pruebas de vistas
   - Opción 4: Ejecutar una prueba específica (deberás introducir la ruta)
   - Opción 5: Ejecutar pruebas con SQLite (local, sin Docker)
   - Opción 6: Salir

### Ejecución Manual

Las pruebas se ejecutan dentro del contenedor Docker para asegurar que todas las dependencias están disponibles:

```bash
# Ejecutar todas las pruebas de modelos
docker-compose exec web python manage.py test apps.reloj_fichador.tests.test_models -v 2

# Ejecutar una prueba específica
docker-compose exec web python manage.py test apps.reloj_fichador.tests.test_models.OperarioModelTest -v 2
```

### Ejecución Local (Alternativa)

Si prefieres ejecutar las pruebas fuera de Docker, necesitarás instalar las dependencias:

```bash
pip install django mysqlclient colorama
```

Y luego puedes ejecutar:

```bash
python manage.py test apps.reloj_fichador.tests.test_models
```

## Características Especiales

- Las pruebas se ejecutan dentro del contenedor Docker para garantizar el entorno adecuado
- Verificación automática de que Docker esté en ejecución y los contenedores estén activos
- Configuración de SQLite optimizada para pruebas rápidas
- Respeto a la configuración de zonas horarias del proyecto principal

## Trabajando con Fechas y Zonas Horarias

El proyecto incluye utilidades para manejar correctamente las fechas según la configuración del proyecto:

```python
from tests_utils.datetime_helpers import normalize_datetime, ensure_timezone_consistency, create_datetime

# Normalizar una fecha según la configuración del proyecto
fecha_normalizada = normalize_datetime(mi_fecha)

# Asegurar que dos fechas sean compatibles para comparación
fecha1, fecha2 = ensure_timezone_consistency(fecha1, fecha2)

# Crear una fecha con la configuración correcta de zona horaria
nueva_fecha = create_datetime(2024, 6, 15, 8, 30)
```

Estas utilidades aseguran que las fechas sean manejadas correctamente según el valor de `USE_TZ` en la configuración del proyecto.

## Solución de Problemas

### Errores comunes:

1. **Docker no está en ejecución**: 
   Inicia Docker Desktop y vuelve a intentarlo. El script intentará detectar si Docker está en ejecución.

2. **Error de módulo no encontrado**: 
   Si ves "ModuleNotFoundError: No module named 'django'", asegúrate de que estás ejecutando las pruebas dentro de Docker o que has instalado Django localmente.

3. **Problemas de permisos de base de datos**: 
   Las pruebas dentro de Docker utilizan la base de datos del contenedor, lo que evita problemas de permisos.

4. **Errores de zona horaria**:
   Si encuentras errores como "can't compare offset-naive and offset-aware datetimes", utiliza las funciones auxiliares de `datetime_helpers.py` para normalizar las fechas.

## Desarrollo de Nuevas Pruebas

Cuando desarrolles nuevas pruebas:

1. Colócalas en el directorio correspondiente según su propósito (models, views, etc.)
2. Sigue el patrón de nomenclatura: `test_[nombre_de_caracteristica].py`
3. Asegúrate de usar clases que hereden de `TestCase`
4. Los métodos de prueba deben comenzar con `test_`
5. Usa objetos mock cuando sea apropiado para aislar las pruebas
6. Utiliza las utilidades de fechas para evitar problemas de zonas horarias

Para más información consulta la documentación sobre pruebas en Django: https://docs.djangoproject.com/en/5.1/topics/testing/ 