# Auditoría de Modelos - Reloj Fichador

Este documento detalla los hallazgos y las potenciales mejoras identificadas tras la revisión de los modelos de la aplicación "Reloj Fichador" y el análisis de optimización de la base de datos proporcionado.

## 1. Índices

### Hallazgos
*   **registrodiario:**
    *   **Faltante:** Índice compuesto `(operario_id, hora_fichada)`. El informe de rendimiento lo identifica como crítico, ya que la mayoría de las consultas filtran por operario y rango de fechas.
    *   **Duplicado:** Un índice en `operario_id`. Existe el índice automático de la ForeignKey y otro manual. Uno de ellos es redundante.
*   **horas_trabajadas:**
    *   **Faltante:** Índice compuesto `(operario_id, fecha)`. Necesario para consultas que filtran por operario y rango de fechas.
*   **horas_totales:**
    *   **Faltante:** Índice compuesto `(operario_id, mes_actual)`. Recomendado para optimizar el acceso a los totales por operario y mes.
*   **operario:**
    *   **Duplicado:** Un índice en `dni`. Existe la restricción `unique=True` (que crea un índice automáticamente) y un índice manual adicional. Uno de ellos es redundante.
*   **Licencia:**
    *   **Existente:** `(operario, fecha_inicio)` y `estado`. Estos índices parecen adecuados para las consultas de licencias.
*   **RegistroAsistencia:**
    *   **Existente:** `(operario, fecha)` y `(estado_asistencia, estado_justificacion)`. Aparentemente correctos.
*   **CalendarioLaboral:**
    *   **Existente:** `fecha` y `tipo_dia`. Adecuados.
*   **GrupoSabado:**
    *   **Existente:** `(operario, fecha_inicio)` y `grupo`. Adecuados.
*   **SugerenciaFeriado:**
    *   **Existente:** `fecha`, `estado`, `fuente`. Adecuados.

### Impacto
Los índices faltantes son la causa principal de la degradación del rendimiento en consultas frecuentes, especialmente a medida que la base de datos crece. Los índices duplicados no afectan la lectura, pero ralentizan las operaciones de `INSERT`/`UPDATE`.

### Acciones Recomendadas
1.  **Crear índices compuestos:**
    *   `reloj_fichador_registrodiario`: `(operario_id, hora_fichada)`
    *   `reloj_fichador_horas_trabajadas`: `(operario_id, fecha)`
    *   `reloj_fichador_horas_totales`: `(operario_id, mes_actual)`
2.  **Eliminar índices duplicados:**
    *   `registrodiario`: Eliminar el índice manual en `operario_id`.
    *   `operario`: Eliminar el índice manual en `dni`.

## 2. Optimización de Consultas (Queries)

### Hallazgos
*   **Queries 85 - Horas Trabajadas y 87 - Resumen del mes:** Según el informe, estas consultas cargan todos los datos sin un filtro de fecha adecuado.
*   **Queries 91 - Registros con filtros y 92 - Registro con totales:** Utilizan un patrón de subquery correlacionada duplicada que es ineficiente y se degrada con el volumen de datos.

### Impacto
Estas consultas se volverán extremadamente lentas a medida que la base de datos crezca, impactando directamente la experiencia del usuario y el rendimiento del servidor.

### Acciones Recomendadas
1.  **Añadir filtros de fecha:** Implementar filtros de fecha en las queries 85 y 87 para que solo carguen los datos relevantes según el período de tiempo solicitado (ej. mes actual, año actual).
2.  **Optimizar subqueries correlacionadas:** Reescribir las queries 91 y 92 para utilizar `LEFT JOIN LATERAL` u otra técnica más eficiente, similar a cómo se corrigió la query 86 (según el informe). Esto eliminará las ejecuciones duplicadas de la subconsulta.

## 3. Redondeo de Horas

### Hallazgos
*   La lógica de redondeo (`redondear_entrada`, `redondear_salida`) se aplica de forma dinámica. El valor redondeado de `hora_fichada` no se persiste directamente en el modelo `RegistroDiario`.
*   La función `calcular_horas_por_franjas` utiliza una lógica "simplificada" que podría no cubrir todos los escenarios complejos de turnos nocturnos o turnos que cruzan la medianoche de forma más granular.

### Impacto
No persistir la `hora_fichada` redondeada puede llevar a cálculos repetitivos y a una menor eficiencia en consultas o procesos que necesiten los valores redondeados. Cualquier cambio en la lógica de redondeo afectaría retroactivamente los cálculos históricos si no se persisten los valores.

### Acciones Recomendadas
1.  **Persistir horas redondeadas:** Añadir campos `hora_fichada_redondeada` (o similar) a `RegistroDiario` y almacenar el resultado de `redondear_entrada` o `redondear_salida` al momento de guardar el registro. Esto optimizaría futuras consultas y cálculos.
2.  **Revisar `calcular_horas_por_franjas`:** Evaluar si la lógica "simplificada" es suficiente para todos los requisitos del negocio o si necesita una implementación más robusta que maneje escenarios de turnos más complejos (ej. turnos que empiezan un día y terminan al día siguiente, pero que tienen tramos nocturnos intermedios).

## 4. Eficiencia de Cálculos en Modelos

### Hallazgos
*   **`RegistroDiario.calcular_diferencia_entrada_salida`:** Realiza una consulta para obtener el `ultima_entrada` y luego guarda el propio registro, lo que implica una operación de base de datos doble.
*   **`Horas_trabajadas.calcular_horas_trabajadas`:** Filtra todos los registros del operario y luego itera para encontrar los del día específico. El filtrado inicial podría ser más restrictivo para reducir la carga.
*   **`Horas_totales.calcular_horas_totales`:** Realiza múltiples consultas de agregación a diferentes modelos (`Horas_trabajadas`, `Horas_extras`, `Horas_feriado`, `HorasEnfermedad`) para un mes específico.

### Impacto
Los métodos de cálculo actuales pueden volverse costosos en términos de recursos (CPU, I/O de base de datos) a medida que el volumen de datos y la frecuencia de cálculo aumentan.

### Acciones Recomendadas
1.  **Optimizar `calcular_diferencia_entrada_salida`:** Considerar si este cálculo puede integrarse mejor en el `save()` del modelo o si los campos `dif_entrada_salida` pueden calcularse como parte de un proceso batch o asíncrono para reducir la carga transaccional.
2.  **Optimizar `Horas_trabajadas.calcular_horas_trabajadas`:** Ajustar la consulta inicial de `registros` para que sea más específica a la `fecha` requerida, reduciendo así el conjunto de datos sobre el que se itera.
3.  **Optimizar `Horas_totales.calcular_horas_totales`:** Evaluar el uso de `select_related`/`prefetch_related` si es posible, o explorar la creación de vistas materializadas o tablas de resumen pre-calculadas si la consulta es muy frecuente. La generación de estos totales podría delegarse a tareas de Celery.

## 5. Proyección a 10 años

### Hallazgos
*   `registrodiario`, `horas_trabajadas`, `historicalregistrodiario` se proyecta que alcanzarán entre 200K y 630K filas en 10 años.

### Impacto
Sin las optimizaciones de índices y consultas, el rendimiento se degradará gravemente con estos volúmenes de datos.

### Acciones Recomendadas
1.  **Priorizar la implementación:** Las acciones recomendadas en los puntos 1 y 2 (índices y optimización de queries) son críticas y deben implementarse lo antes posible.
2.  **Planificar particionamiento:** Cuando `registrodiario` se acerque a 500K filas, investigar y planificar el particionamiento de la tabla por año.

## 6. Recomendaciones Adicionales

### Hallazgos
*   **Lógica de Negocio en `clean()` y `save()`:** Los métodos `clean()` y `save()` de `RegistroDiario` y `Licencia` contienen lógica de negocio compleja (validaciones de secuencia, verificación de solapamientos, procesamiento de licencias, etc.).
*   **Manejo de Zonas Horarias:** El uso de `pytz` y `timezone.now()` se observa en varias funciones.

### Impacto
*   La lógica de negocio compleja dentro de `clean()` y `save()` puede hacer que los modelos sean más difíciles de probar, mantener y reutilizar. Además, puede introducir acoplamiento y dificultar la escalabilidad si estas operaciones se vuelven intensivas.
*   Un manejo inconsistente o incorrecto de las zonas horarias puede llevar a errores sutiles pero críticos en los cálculos de tiempo.

### Acciones Recomendadas
1.  **Refactorizar lógica de negocio:** Considerar mover parte de la lógica compleja de `clean()` y `save()` a "servicios" o funciones utilitarias externas. Esto mejoraría la separación de responsabilidades, la testabilidad y la legibilidad del código del modelo.
2.  **Auditoría de Zonas Horarias:** Realizar una auditoría exhaustiva de cómo se manejan las zonas horarias en toda la aplicación para asegurar que `USE_TZ` en `settings.py` y las conversiones de `pytz` se apliquen de manera uniforme y correcta en todos los puntos donde se manejan fechas y horas.
3.  **Persistencia del redondeo:** Como se mencionó en la sección 3, hacer persistentes los valores redondeados de las horas de fichada en el modelo `RegistroDiario` para simplificar la lógica de consulta y cálculo.
