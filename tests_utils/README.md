# Utilidades para Pruebas - Reloj Fichador

Este directorio contiene herramientas para ejecutar las pruebas automatizadas del sistema Reloj Fichador de manera eficiente y sin problemas de permisos de base de datos.

## Características

- **Uso de SQLite en memoria**: Las pruebas se ejecutan con SQLite en memoria, evitando problemas de permisos y acelerando la ejecución.
- **Scripts formativos**: Los resultados se muestran con colores para facilitar la interpretación.
- **Opciones flexibles**: Permite ejecutar pruebas específicas o todas las pruebas.

## Archivos disponibles

- `sqlite_settings.py`: Configuración de Django para usar SQLite en memoria durante las pruebas.
- `run_model_tests.py`: Script principal para ejecutar todas las pruebas de modelos.
- `run_specific_test.py`: Script para ejecutar una prueba específica.
- `run_all_tests.bat`: Script de Windows para ejecutar todas las pruebas de forma rápida.
- `run_specific_test.bat`: Script de Windows para ejecutar una prueba específica.

## Cómo utilizar

### Ejecutar todas las pruebas de modelos

Simplemente haz doble clic en `run_all_tests.bat` o ejecuta:

```bash
python tests_utils/run_model_tests.py
```

### Ejecutar una prueba específica

Utiliza el script `run_specific_test.bat` pasando la ruta del test:

```bash
run_specific_test.bat apps.reloj_fichador.tests.test_models.OperarioModelTest
```

O directamente con Python:

```bash
python tests_utils/run_specific_test.py apps.reloj_fichador.tests.test_views.ReporteViewTest
```

### Opciones avanzadas

Para opciones más avanzadas, puedes usar el script run_specific_test.py con argumentos:

```bash
python tests_utils/run_specific_test.py -v 3 apps.reloj_fichador.tests.test_models.OperarioModelTest.test_campos_max_length
```

## Requisitos

El único requisito externo es la biblioteca `colorama` para mostrar colores en la consola, que se instalará automáticamente al usar los scripts .bat.

## Estructura recomendada de pruebas

- **tests_models.py**: Pruebas para los modelos
- **tests_views.py**: Pruebas para las vistas
- **tests_forms.py**: Pruebas para los formularios
- **tests_utils.py**: Pruebas para las utilidades
- **tests_api.py**: Pruebas para la API (si existe) 