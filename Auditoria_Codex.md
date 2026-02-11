# Auditoria de modelos - Reloj Fichador

Fecha: 2026-02-11
Alcance: Revision estatica de `apps/reloj_fichador/models.py` buscando mejoras de rendimiento y consistencia en el modelo de datos. No se hicieron cambios.

## Resumen ejecutivo
- Hay varias oportunidades claras de indices compuestos en tablas grandes (especialmente `RegistroDiario`, `Horas_trabajadas`, `Horas_extras`, `Horas_totales`).
- Existen indices redundantes creados manualmente sobre campos que ya tienen indice por `unique` o por `ForeignKey`.
- Hay metodos que cargan demasiados registros en memoria por falta de filtros de fecha o por usar `__date` sobre `DateTimeField` sin un indice efectivo.

## Hallazgos por modelo

### Operario
- `dni` es `unique=True` y ademas se declara `models.Index(fields=['dni'])`. Esto es redundante porque el indice unico ya existe.
- `apellido` tiene indice y es razonable si se filtra/ordena frecuentemente.

### RegistroDiario
- Solo hay indices simples en `operario` y `hora_fichada`. Para las queries reales se usan filtros combinados y orden por fecha.
- Mejoras de indices recomendadas (segun patrones en el propio modelo):
  - `(operario, hora_fichada)` para filtros por operario y rango de fechas.
  - `(operario, tipo_movimiento, valido, hora_fichada)` para consultas que buscan ultimo movimiento por tipo y validez.
  - `(operario, valido, id_registro)` para `get_last_valid_record()` que ordena por `id_registro`.
- El indice simple en `operario` es redundante porque los `ForeignKey` ya indexan por defecto. Solo conviene si se elimina y se reemplaza por compuestos.
- `calcular_horas_trabajadas()` carga todos los registros del operario y filtra en memoria por fecha logica. Esto escala mal. Requiere algun filtro de fecha a nivel DB (campo derivado o columna auxiliar).
- Filtros frecuentes con `hora_fichada__date=...` pueden evitar indices efectivos sobre `hora_fichada`.

### Horas_trabajadas
- No tiene indices. Se consulta por `operario` y `fecha` en varias partes del codigo.
- Recomendado indice compuesto `(operario, fecha)` y posiblemente `unique_together` si no se desean duplicados por dia.

### Horas_extras
- No tiene indices. Se consulta por `operario` y `fecha`.
- Recomendado indice compuesto `(operario, fecha)` y `unique_together` si corresponde.

### Horas_totales
- No tiene indices. Se consulta por `operario` y `mes_actual`.
- Recomendado indice compuesto `(operario, mes_actual)` y `unique_together` si corresponde.

### Horas_feriado
- Sin indices. Se consulta por `operario` y `fecha`.
- Recomendado indice compuesto `(operario, fecha)` si se filtra por estos campos.

### Licencia
- Tiene indices en `(operario, fecha_inicio)` y `estado`. Los filtros comunes incluyen `operario`, `estado`, `fecha_inicio`, `fecha_fin`.
- Posible mejora: indice compuesto `(operario, estado, fecha_inicio, fecha_fin)` para verificar solapamientos y licencias aprobadas por rango.

### RegistroAsistencia
- `unique_together = ('operario', 'fecha')` ya crea un indice unico. El indice adicional `models.Index(fields=['operario', 'fecha'])` es redundante.
- Filtros por `estado_asistencia` y `estado_justificacion` ya tienen indice compuesto. OK.

### CalendarioLaboral
- `fecha` es `unique=True`, por lo que el indice extra sobre `fecha` es redundante.

### GrupoSabado
- Indices en `(operario, fecha_inicio)` y `grupo`. Razonable.

### HorasEnfermedad
- Indice en `licencia` es redundante porque `ForeignKey` ya indexa por defecto. Mantener el compuesto `(operario, mes_periodo)`.

### SugerenciaFeriado
- `unique_together = ('fecha', 'fuente')` no cubre busquedas solo por `fecha`, por lo que el indice en `fecha` puede ser util. OK.

## Hallazgos transversales
- Varios `ForeignKey` tienen indices explicitos redundantes. En Django, los `ForeignKey` ya crean indice por defecto.
- Si se filtra por fecha en `DateTimeField` usando `__date`, un indice convencional en `hora_fichada` no suele ser suficiente. Alternativas:
  - Agregar un campo `fecha_logica` o `fecha_calculada` (DateField) y mantenerlo sincronizado.
  - Usar funciones/indices funcionales si el motor lo soporta.
- Uso intensivo de `HistoricalRecords` incrementa tablas historicas. Si se hacen reportes sobre historicos, evaluar indices alli tambien.

## Lista de ajustes prioritarios (sin implementar)
- RegistroDiario: indices compuestos para `operario + hora_fichada` y `operario + tipo_movimiento + valido + hora_fichada`.
- Horas_trabajadas / Horas_extras / Horas_totales / Horas_feriado: indices compuestos por operario y fecha/mes.
- Limpieza de indices redundantes: `Operario.dni`, `RegistroAsistencia(operario, fecha)`, `CalendarioLaboral.fecha`, `RegistroDiario.operario`, `HorasEnfermedad.licencia`.

