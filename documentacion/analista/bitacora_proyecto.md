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

---

*Este documento se actualizará constantemente como parte del seguimiento del proyecto.* 