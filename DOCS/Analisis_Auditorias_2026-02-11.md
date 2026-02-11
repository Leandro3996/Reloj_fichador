# Análisis Comparativo de Auditorías - Reloj Fichador

**Fecha:** 2026-02-11
**Autor:** Sistemas Hores (Teo / Leandro)
**Fuentes analizadas:**
- `Auditoria_Codex.md` — Revisión estática por OpenAI Codex
- `Auditoria_Gemini.md` — Auditoría por Google Gemini
- `DOCS/Optimizacion_BD_2026-02-10.md` — Informe propio de optimización de BD
- Opiniones de expertos en Reddit (r/mysql, r/SQL, r/Database, r/django)

---

## 1. Coincidencias entre los tres análisis

Los tres documentos (informe propio, Codex, Gemini) coinciden en los puntos fundamentales:

- **Índices compuestos `(operario, fecha)` son críticos** en las tablas principales.
- **Existen índices redundantes** que ralentizan INSERTs/UPDATEs sin beneficio.
- **Las subqueries correlacionadas** en Metabase (queries 91/92) son un antipatrón de rendimiento.
- **Las queries sin filtro de fecha** (85, 87) cargan toda la tabla innecesariamente.

Esto refuerza que estas son las prioridades reales. Los expertos de Reddit también lo confirman unánimemente.

---

## 2. Aportes exclusivos de Codex

Codex fue más granular en el análisis de índices:

### 2.1 Más modelos sin índices
El informe propio solo cubría `registrodiario`, `horas_trabajadas` y `horas_totales`. Codex identificó correctamente que **`Horas_extras` y `Horas_feriado`** también necesitan índices compuestos `(operario, fecha)`.

### 2.2 Índices más específicos
Propone índices covering para patrones de query concretos:
- `(operario, tipo_movimiento, valido, hora_fichada)` — para búsquedas de último movimiento por tipo.
- `(operario, valido, id_registro)` — para `get_last_valid_record()`.

**Veredicto:** Buenos candidatos, pero de segunda prioridad. Implementar solo si se detectan queries lentas con estos patrones.

### 2.3 Problema de `__date` sobre DateTimeField
Hallazgo importante: cuando Django hace `hora_fichada__date=X`, genera `CAST(hora_fichada AS DATE) = X`, lo que **invalida el uso del índice** en `hora_fichada`. Alternativas:
- Agregar un campo `fecha_logica` (DateField) sincronizado.
- Usar índices funcionales si el motor lo soporta.

**Veredicto:** Problema real que hay que investigar después de implementar los índices compuestos.

### 2.4 Índices redundantes adicionales
Codex identificó más redundancias que el informe propio:
- `RegistroAsistencia(operario, fecha)` — redundante con `unique_together`.
- `CalendarioLaboral.fecha` — redundante con `unique=True`.
- `HorasEnfermedad.licencia` — redundante con ForeignKey.

---

## 3. Aportes exclusivos de Gemini

Gemini amplió el alcance más allá de la BD, abarcando código y arquitectura:

### 3.1 Persistir hora redondeada
Propone guardar `hora_fichada_redondeada` en el modelo para evitar recálculos.

**Veredicto:** Interesante pero **no prioritario**. Agrega complejidad de sincronización sin beneficio inmediato claro. Reconsiderar si el redondeo se convierte en cuello de botella.

### 3.2 Cálculos que cargan demasiado en memoria
Tanto Codex como Gemini detectan que `calcular_horas_trabajadas()` carga todos los registros del operario y filtra en Python. Con el crecimiento proyectado (630K filas en 10 años), esto será un problema.

**Veredicto:** Problema real pero que se mitiga parcialmente con los índices compuestos. Optimizar el filtrado en la query después.

### 3.3 Refactorizar lógica de `clean()`/`save()` a servicios
Recomendación de arquitectura válida para mejorar testabilidad y mantenibilidad.

**Veredicto:** No prioritario. El código funciona. Refactorizar sin necesidad concreta es over-engineering en este momento.

### 3.4 Auditoría de zonas horarias
Recomienda verificar consistencia en el manejo de `USE_TZ` y conversiones con `pytz`.

**Veredicto:** Buena práctica pero no urgente. El sistema funciona correctamente en producción.

---

## 4. Validación con expertos de Reddit

Se consultaron opiniones en r/mysql, r/SQL, r/Database y r/django:

| Tema | Opinión de expertos |
|---|---|
| Índices compuestos | **Unanimidad:** es la optimización #1, máximo impacto, mínimo riesgo |
| Subqueries correlacionadas | **Unanimidad:** antipatrón que "explodes runtime" — reemplazar por JOINs |
| Índices duplicados | **Consenso:** eliminar, pero verificar FKs antes |
| Particionado | **Consenso:** "keep it simple" hasta 500K+ filas; el mantenimiento de particiones puede causar bloqueos |
| Queries sin filtro | **Obvio:** nadie discute que es un problema |

**Cita destacada:** *"Carefully think out your indexes. These will be your biggest improvement (possibly enough on their own)."* — u/Ok-Kaleidoscope5627 (r/Database)

**Advertencia sobre particionado:** *"ALTER TABLE ADD PARTITION in MySQL isn't really online. It takes metadata locks."* — u/Timely-Business-982 (r/mysql). Un usuario reportó que una operación de partición colisionó con un SELECT y crasheó la aplicación.

---

## 5. Plan de acción priorizado

| Prioridad | Acción | Fuente | Estado |
|---|---|---|---|
| 1 - AHORA | Crear índices compuestos en 5 tablas | Todos coinciden | Pendiente |
| 2 - AHORA | Eliminar índices redundantes | Codex + informe | Pendiente |
| 3 - PRONTO | Optimizar queries 91/92 (LATERAL JOIN) | Informe + Gemini | Pendiente |
| 4 - PRONTO | Filtros de fecha en queries 85/87 | Informe + Gemini | Pendiente |
| 5 - DESPUÉS | Evaluar problema de `__date` en DateTimeField | Codex | Pendiente |
| 6 - DESPUÉS | Optimizar cálculos en memoria (calcular_horas_trabajadas) | Codex + Gemini | Pendiente |
| 7 - FUTURO | Refactorizar lógica de modelos | Gemini | Pendiente |
| 8 - FUTURO | Persistir hora redondeada | Gemini | Pendiente |
| 9 - FUTURO | Particionado por año (+500K filas) | Informe + Reddit | Pendiente |

---

## 6. Conclusión

Las tres auditorías son complementarias:
- **El informe propio** identificó correctamente las prioridades de BD.
- **Codex** fue más exhaustivo en índices y detectó el problema de `__date`.
- **Gemini** aportó visión de arquitectura y código, aunque algunas recomendaciones son prematuras.

La validación con Reddit confirmó que el orden de prioridades es correcto y que el particionado no debe apresurarse.
