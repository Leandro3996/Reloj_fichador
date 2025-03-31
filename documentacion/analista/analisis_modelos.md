# Análisis de Modelos de Datos - Reloj Fichador

## Estructura Principal de Modelos

Tras analizar el código del sistema, se han identificado los siguientes modelos principales que componen el núcleo del sistema:

### 1. Operario
Este modelo representa a los trabajadores cuya asistencia y horas se registran:

- **Identificador**: DNI (único)
- **Información personal**: Nombre, apellido, información adicional
- **Datos laborales**: Fecha de ingreso, áreas asignadas
- **Estado**: Activo/inactivo
- **Metadata**: Foto, descripción, título técnico

Este modelo mantiene un historial de cambios mediante `HistoricalRecords`, lo que permite auditar modificaciones a lo largo del tiempo.

### 2. Área
Representa las divisiones organizacionales donde pueden trabajar los operarios:

- **Nombre**: Identificador del área
- **Horarios**: Relación many-to-many con el modelo Horario

### 3. Horario
Define los horarios laborales asignables a distintas áreas:

- **Nombre**: Identificador del horario (ej. "Turno Mañana")
- **Hora inicio**: Hora de comienzo del turno
- **Hora fin**: Hora de finalización del turno

### 4. RegistroDiario
El modelo central para el control de asistencia. Registra cada entrada/salida:

- **Operario**: Relación al operario que ficha
- **Hora fichada**: Timestamp exacto de la marcación
- **Tipo movimiento**: Cuatro opciones: entrada, salida, entrada transitoria, salida transitoria
- **Validación**: Campos para marcar inconsistencias y mantener la integridad
- **Cálculos auxiliares**: Campos para almacenar diferencias entre entrada-salida

Este modelo también mantiene historial con `HistoricalRecords`.

### 5. Licencia
Gestiona los permisos y ausencias justificadas:

- **Operario**: Relación al operario que solicita la licencia
- **Fechas**: Período de la licencia (inicio, fin)
- **Documentación**: Archivo adjunto con validación de tipo
- **Descripción**: Detalles adicionales

### 6. Modelos de Cálculo de Horas

El sistema utiliza varios modelos para los distintos tipos de horas calculadas:

#### 6.1 Horas_trabajadas
- Registra horas normales, nocturnas y extras para un operario en una fecha específica
- Incluye un método de clase `calcular_horas_trabajadas()` para el cálculo automático

#### 6.2 Horas_feriado
- Registra horas trabajadas en días feriados
- Incluye método `sumar_horas_feriado()` para el cálculo

#### 6.3 Horas_extras
- Registra específicamente las horas extra trabajadas
- Implementa `calcular_horas_extras()` como método de cálculo

#### 6.4 Horas_totales
- Agrupa totales mensuales de todos los tipos de horas
- Implementa `calcular_horas_totales()` para consolidar información mensual

### 7. RegistroAsistencia
Modelo para el seguimiento general de asistencia:

- **Operario**: Relación al operario
- **Fecha**: Día específico
- **Estado**: Presente/Ausente
- **Justificación**: Indica si una ausencia está justificada
- **Descripción**: Detalles adicionales

## Funciones Clave para el Cálculo de Horas

El sistema implementa funciones críticas para el cálculo de horas trabajadas:

### 1. Redondeo de Horas

- **`redondear_entrada(dt)`**: Redondea la hora de entrada hacia arriba a la próxima hora completa
- **`redondear_salida(dt)`**: Redondea la hora de salida hacia abajo a la hora completa anterior

### 2. Cálculo por Franjas Horarias

- **`calcular_horas_por_franjas(inicio, fin, limites=None)`**: Función sofisticada que calcula:
  - Horas normales (6:00 - 20:00)
  - Horas nocturnas (20:00 - 6:00)

### 3. Cálculo de Diferencias

- **`calcular_diferencia_entrada_salida(entrada, salida)`**: Calcula el tiempo entre entrada y salida
- **`RegistroDiario.calcular_diferencia_entrada_salida()`**: Método que integra el cálculo de diferencias

## Relaciones Entre Modelos

El sistema presenta las siguientes relaciones clave:

1. **Operario a Área**: Relación muchos a muchos (un operario puede pertenecer a varias áreas)
2. **Área a Horario**: Relación muchos a muchos (un área puede tener varios horarios)
3. **Operario a RegistroDiario**: Relación uno a muchos (un operario tiene múltiples registros)
4. **Operario a Licencia**: Relación uno a muchos (un operario puede tener múltiples licencias)
5. **Operario a modelos de horas**: Relaciones uno a muchos para todos los cálculos de horas

## Observaciones y Recomendaciones

1. **Complejidad del Modelo**: El sistema presenta una estructura de datos compleja pero bien organizada, que refleja las complejas reglas de negocio.

2. **Oportunidad de Refactorización**: El código de cálculo de horas podría beneficiarse de una encapsulación en clases especializadas para mejorar la mantenibilidad.

3. **Optimización de Consultas**: Los métodos de cálculo realizan múltiples consultas a la base de datos que podrían optimizarse mediante:
   - Uso de anotaciones y agregaciones de Django
   - Implementación de caché para cálculos frecuentes

4. **Historial y Auditoría**: El uso de `HistoricalRecords` es una práctica excelente para mantener la trazabilidad, pero podría ampliarse a más modelos.

5. **Validación de Datos**: Se recomienda reforzar las validaciones en `clean()` de los modelos para garantizar la integridad de datos.

## Diagrama de Relaciones Simplificado

```
Operario <-----> Área <-----> Horario
   |
   |-----> RegistroDiario
   |-----> Licencia
   |-----> Horas_trabajadas
   |-----> Horas_feriado
   |-----> Horas_extras
   |-----> Horas_totales
   |-----> RegistroAsistencia
```

Este análisis inicial de modelos servirá como base para un estudio más profundo de las funcionalidades y posibles optimizaciones del sistema.

---

*Este documento es parte de la documentación técnica del proyecto y será actualizado conforme avance el análisis.* 