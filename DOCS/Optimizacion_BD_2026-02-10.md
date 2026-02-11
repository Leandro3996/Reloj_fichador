# Informe de Optimización - Base de Datos Reloj Fichador

**Fecha:** 2026-02-10
**Autor:** Sistemas Hores (Teo / Leandro)
**Base de datos:** `docker_horesdb` (MySQL 8.x)
**Servidores:** Desarrollo (192.168.10.11), Producción (192.168.10.39:53306)

---

## 1. Estado actual de la base de datos

### Tablas principales

| Tabla | Filas | Data | Índices |
|-------|------:|-----:|--------:|
| `reloj_fichador_registrodiario` | 52,505 | 3.5 MB | 4.5 MB |
| `reloj_fichador_historicalregistrodiario` | 48,036 | 4.5 MB | 7.0 MB |
| `reloj_fichador_registroasistencia` | 22,171 | 1.5 MB | 4.9 MB |
| `reloj_fichador_horas_trabajadas` | 13,225 | 1.5 MB | 0.4 MB |
| `reloj_fichador_horas_extras` | 11,554 | 1.5 MB | 0.3 MB |
| `reloj_fichador_horas_totales` | 781 | 0.09 MB | 0.05 MB |
| `reloj_fichador_operario` | 330 | 0.05 MB | 0.05 MB |

**Total:** 45 tablas, ~15 MB datos + ~25 MB índices.

### Proyección de crecimiento

Con ~80 operarios fichando ~2 veces/día = ~160 registros diarios, ~58,000/año:

| Tabla | Hoy | 5 años | 10 años |
|-------|----:|-------:|--------:|
| `registrodiario` | 52K | ~340K | ~630K |
| `horas_trabajadas` | 13K | ~100K | ~200K |
| `historicalregistrodiario` | 48K | ~300K | ~600K |

---

## 2. Problemas detectados

### 2.1 Índices compuestos faltantes (PRIORIDAD ALTA)

Las queries más frecuentes filtran por **operario + rango de fecha**, pero no existe un
índice compuesto para esta combinación. MySQL tiene que hacer un index scan completo en
una columna y luego filtrar fila por fila en la otra.

**Tablas afectadas:**

- `registrodiario`: tiene índice en `hora_fichada` e índice en `operario_id` por separado,
  pero NO `(operario_id, hora_fichada)`.
- `horas_trabajadas`: solo tiene índice en `operario_id`, falta `(operario_id, fecha)`.
- `horas_totales`: solo tiene índice en `operario_id`, falta `(operario_id, mes_actual)`.

**Impacto:** A medida que la tabla crece, las queries con subqueries correlacionadas
(que buscan el registro anterior de un operario) se degradan significativamente porque
deben recorrer todos los registros del operario en lugar de buscar directamente por
el rango de fechas.

### 2.2 Índices duplicados (PRIORIDAD BAJA)

- `registrodiario` tiene **2 índices en `operario_id`**:
  - `reloj_fichador_regis_operario_id_75f4af8c_fk_reloj_fic` (FK automático)
  - `reloj_ficha_operari_7b299b_idx` (índice manual)
  - Uno es redundante y ralentiza cada INSERT/UPDATE.

- `operario` tiene **2 índices en `dni`**:
  - `dni` (unique constraint)
  - `reloj_ficha_dni_b631b6_idx` (índice manual)
  - Mismo problema: el segundo es redundante.

### 2.3 Subqueries correlacionadas en consultas Metabase (PRIORIDAD ALTA)

Las queries de Metabase 91 y 92 ("Registros Diarios - Con Filtros" y "Registro diario
con Totales") calculan el tiempo de descanso con una **subquery correlacionada ejecutada
2 veces por cada fila**:

```sql
-- Se ejecuta 2 VECES por cada fila de tipo 'entrada_transitoria'
(SELECT MAX(rd2.hora_fichada)
 FROM reloj_fichador_registrodiario rd2
 WHERE rd2.operario_id = rd.operario_id
   AND rd2.tipo_movimiento = 'salida_transitoria'
   AND rd2.hora_fichada < rd.hora_fichada
   AND rd2.valido = TRUE)
```

Esto significa que para cada registro de entrada transitoria, MySQL busca en toda
la tabla 2 veces. Con 630K filas en 10 años, esto será extremadamente lento.

**Solución aplicada en query 86:** Se reemplazó por un `LEFT JOIN LATERAL` que
ejecuta la búsqueda una sola vez:

```sql
LEFT JOIN LATERAL (
  SELECT rd2.hora_fichada
  FROM reloj_fichador_registrodiario rd2
  WHERE rd2.operario_id = rd.operario_id
    AND rd2.tipo_movimiento = 'salida_transitoria'
    AND rd2.hora_fichada < rd.hora_fichada
    AND rd2.valido = TRUE
  ORDER BY rd2.hora_fichada DESC
  LIMIT 1
) prev_st ON rd.tipo_movimiento = 'entrada_transitoria'
```

### 2.4 Consultas sin filtro de fecha (PRIORIDAD MEDIA)

| Query Metabase | Nombre | Problema |
|----------------|--------|----------|
| 85 | Reporte - Horas Trabajadas | Sin filtro de fecha, carga todos los registros |
| 87 | Reporte - Resumen del mes | Sin filtro, carga todos los meses históricos |

Sin filtros, estas queries cargan la totalidad de la tabla cada vez que se abren.
Con el crecimiento proyectado, serán cada vez más lentas.

---

## 3. Acciones recomendadas

### 3.1 Crear índices compuestos (inmediato)

```sql
-- El más importante: acelera todas las queries por operario + fecha
CREATE INDEX idx_rd_operario_fecha
  ON reloj_fichador_registrodiario (operario_id, hora_fichada);

-- Para reportes de horas trabajadas
CREATE INDEX idx_ht_operario_fecha
  ON reloj_fichador_horas_trabajadas (operario_id, fecha);

-- Para resumen mensual
CREATE INDEX idx_htot_operario_mes
  ON reloj_fichador_horas_totales (operario_id, mes_actual);
```

**Riesgo:** Ninguno. Los índices se crean en caliente y no afectan datos existentes.
Solo consumen un poco más de espacio en disco y ralentizan marginalmente los INSERTs.

### 3.2 Añadir filtros de fecha a queries 85 y 87

Agregar template tags `fecha_inicio` y `fecha_fin` para que no carguen todo el histórico.

### 3.3 Optimizar queries 91 y 92

Reemplazar las subqueries correlacionadas duplicadas por `LEFT JOIN LATERAL`
(mismo patrón que se aplicó en query 86).

### 3.4 Eliminar índices duplicados

```sql
-- En registrodiario (verificar cuál es el redundante)
DROP INDEX reloj_ficha_operari_7b299b_idx ON reloj_fichador_registrodiario;

-- En operario
DROP INDEX reloj_ficha_dni_b631b6_idx ON reloj_fichador_operario;
```

**Nota:** Verificar que el índice FK sigue existiendo antes de eliminar el manual.

### 3.5 Considerar particionado (a futuro, +500K filas)

Cuando `registrodiario` supere las 500K filas, considerar particionar por año:

```sql
ALTER TABLE reloj_fichador_registrodiario
PARTITION BY RANGE (YEAR(hora_fichada)) (
  PARTITION p2025 VALUES LESS THAN (2026),
  PARTITION p2026 VALUES LESS THAN (2027),
  -- agregar particiones por año
  PARTITION pmax VALUES LESS THAN MAXVALUE
);
```

Esto permite que MySQL solo escanee la partición relevante al filtrar por fecha.

---

## 4. Resumen de prioridades

| Prioridad | Acción | Impacto | Esfuerzo |
|-----------|--------|---------|----------|
| ALTA | Crear índices compuestos | Alto | Bajo (3 comandos SQL) |
| ALTA | Optimizar queries 91, 92 | Alto | Medio (reescribir SQL) |
| MEDIA | Filtros de fecha en queries 85, 87 | Medio | Bajo |
| BAJA | Eliminar índices duplicados | Bajo | Bajo |
| FUTURO | Particionado por año | Alto | Alto |
