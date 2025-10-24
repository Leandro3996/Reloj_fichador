# 📋 Justificación Retroactiva de Licencias Médicas

**Fecha:** 23 de octubre de 2025
**Estado:** ✅ IMPLEMENTADO Y TESTEADO
**Versión:** 1.0

---

## 🎯 Propósito

Este documento describe cómo el sistema maneja el **escenario real de negocio** donde:

1. **Empleado falta** el día X (se crea `RegistroAsistencia` sin justificación)
2. **Empleado se reincorpora** el día Y con certificado médico
3. **Licencia se carga** y aprueba (posterior a las ausencias)
4. **Sistema retroactivamente justifica** la(s) ausencia(s) anterior(es)

---

## 📊 Escenario Real vs Sistema Anterior

### ❌ Problema Anterior
```
Día 1: Empleado falta → RegistroAsistencia (ausente, SIN justificación)
Día 2: Empleado falta → RegistroAsistencia (ausente, SIN justificación)
Día 3: Empleado falta → RegistroAsistencia (ausente, SIN justificación)
Día 5: Empleado se reincorpora con certificado
       → Se carga licencia para días 1-3
       → Se aprueba licencia
       ❌ Los registros de días 1-3 SIGUEN sin justificación
          (El sistema solo justificaba días coincidentes, no retroactivos)
```

### ✅ Solución Implementada
```
Día 1: Empleado falta → RegistroAsistencia (ausente, SIN justificación)
Día 2: Empleado falta → RegistroAsistencia (ausente, SIN justificación)
Día 3: Empleado falta → RegistroAsistencia (ausente, SIN justificación)
Día 5: Empleado se reincorpora con certificado
       → Se carga licencia para días 1-3
       → Se aprueba licencia
       ✅ Sistema AUTOMÁTICAMENTE:
          1. Busca registros sin justificación ANTES de la fecha de inicio
          2. Los justifica si están dentro de 30 días antes
          3. Los vincula a la licencia
          4. Registra en descripción: "Justificada retroactivamente"
```

---

## 🔄 Cómo Funciona

### Flujo de Ejecución

Cuando se **aprueba una licencia médica**, el sistema ejecuta `procesar_licencia_aprobada()`:

```python
# En apps/reloj_fichador/tasks.py (líneas 71-196)

@shared_task
def procesar_licencia_aprobada(licencia_id):
    """
    Procesa licencia aprobada con JUSTIFICACIÓN RETROACTIVA
    """
    licencia = Licencia.objects.get(pk=licencia_id)

    # PASO 1: ✅ RETROACTIVIDAD - Buscar ausencias ANTERIORES no justificadas
    registros_sin_justificacion_previos = RegistroAsistencia.objects.filter(
        operario=licencia.operario,
        fecha__lt=licencia.fecha_inicio,  # ANTES de la licencia
        estado_asistencia=RegistroAsistencia.ausente,
        estado_justificacion=False,  # SIN justificación
        licencia_relacionada__isnull=True  # Sin licencia vinculada
    ).order_by('-fecha')[:30]  # Últimos 30 días

    registros_justificados_previos = 0
    for registro_previo in registros_sin_justificacion_previos:
        # RESTRICCIÓN: Máximo 30 días de retroactividad
        dias_diferencia = (licencia.fecha_inicio - registro_previo.fecha).days
        if 0 < dias_diferencia <= 30:  # Entre 1 y 30 días antes
            # Justificar
            registro_previo.estado_justificacion = True
            registro_previo.licencia_relacionada = licencia
            registro_previo.descripcion = \
                f'Ausencia justificada retroactivamente por licencia (ID: {licencia.pk})'
            registro_previo.save()
            registros_justificados_previos += 1
            logger.info(f'Justificado retroactivamente: {registro_previo.fecha}')

    # PASO 2: Procesar días de la licencia
    # (Ver documentación IMPLEMENTACION_HORAS_ENFERMEDAD.md para detalles)

    # PASO 3: Crear/actualizar HorasEnfermedad
    # (Acumular horas de enfermedad)
```

### Restricciones y Límites

| Aspecto | Restricción | Razón |
|---------|-------------|-------|
| **Período retroactivo** | Máximo 30 días | Evitar abusos; una licencia no debería cubrir absencias de meses atrás |
| **Registros a justificar** | Solo los ANTERIORES a fecha_inicio | Licencias futuras no pueden justificar pasado más lejano |
| **Estado del registro** | Solo `ausente` + `sin justificación` | No toca registros que ya están justificados |
| **Vinculación** | Solo si `licencia_relacionada` es NULL | No cambia licencias ya vinculadas |
| **Cantidad búsqueda** | Últimos 30 días | Optimización de BD ([:30]) |

---

## 📋 Ejemplo Práctico: Luciano Morales

**Caso Real del Proyecto:**

| Fecha | Acción | Resultado |
|-------|--------|-----------|
| 2025-10-01 a 2025-10-30 | Luciano falta 30 días (enfermedad prolongada) | 30 RegistroAsistencia: `ausente, sin justificación` |
| 2025-11-01 | Se reincorpora con certificado médico | - |
| 2025-11-01 | Se carga/aprueba licencia: 2025-10-01 a 2025-10-30 | - |
| **Después** | ✅ Sistema procesa licencia | 30 registros → `ausente, JUSTIFICADO` |

**Validación en BD:**
```sql
-- Antes
SELECT COUNT(*) FROM reloj_fichador_registroasistencia
WHERE operario_id = 146
  AND estado_justificacion = 0;  -- 29 registros sin justificar

-- Después
SELECT COUNT(*) FROM reloj_fichador_registroasistencia
WHERE operario_id = 146
  AND licencia_relacionada_id = 30;  -- 30 registros justificados por licencia 30
```

---

## 🧪 Tests

### Test 1: Escenario Real (5 días)

**Ubicación:** `TEST/test_justificacion_retroactiva.py::TestJustificacionRetroactiva::test_escenario_real_ausencia_luego_licencia`

**Qué valida:**
- ✅ Crea 5 RegistroAsistencia sin justificación (simula ausencias)
- ✅ Crea Licencia aprobada después (simula carga de certificado)
- ✅ Procesa licencia
- ✅ Verifica que los 5 registros ahora están justificados
- ✅ Verifica que se crearon 40 horas de enfermedad (5 × 8h)
- ✅ Verifica vinculación a licencia

**Estado:** ✅ PASADO

```
TEST: Escenario Real: Ausencia → Licencia (Retroactiva)
  ✓ Registros retroactivamente justificados: 5/5
  ✓ Horas de enfermedad acumuladas: 40h
  ✓ Licencia vinculada: 1
```

### Test 2: Límite de 30 Días

**Ubicación:** `TEST/test_justificacion_retroactiva.py::TestJustificacionRetroactiva::test_justificacion_retroactiva_dentro_30_dias`

**Qué valida:**
- ✅ Crea registros a 1, 5, 15, 29, 30 días antes (DEBEN justificarse)
- ✅ Crea registros a 31, 50 días antes (NO DEBEN justificarse)
- ✅ Aprueba licencia
- ✅ Verifica que se justificaron los primeros 5+ registros
- ✅ Verifica que NO se justificaron los 2 últimos

**Estado:** ✅ PASADO

```
TEST: Límite de 30 días
  ✓ Registros justificados (dentro de 30 días): 6
  ✓ Registros SIN justificar (fuera de límite): 2
```

---

## 🚀 Ejecución de Tests

```bash
# Test del escenario real
docker compose exec -T web python manage.py test \
  TEST.test_justificacion_retroactiva.TestJustificacionRetroactiva.test_escenario_real_ausencia_luego_licencia \
  -v 2

# Test del límite de 30 días
docker compose exec -T web python manage.py test \
  TEST.test_justificacion_retroactiva.TestJustificacionRetroactiva.test_justificacion_retroactiva_dentro_30_dias \
  -v 2

# Ambos tests
docker compose exec -T web python manage.py test \
  TEST.test_justificacion_retroactiva \
  -v 2
```

---

## 📊 Integración con Otros Sistemas

### Interacción con `Horas_totales`

Cuando se justifican registros retroactivamente:

1. **No afecta** directamente `Horas_totales`
2. **Sí afecta** si la licencia es aprobada:
   - Se crean horas de enfermedad
   - Se actualiza `Horas_totales.horas_enfermedad`

```python
# En procesar_licencia_aprobada (líneas 169-189)
mes_periodo = licencia.fecha_inicio.strftime('%Y-%m')
horas_enfermedad_obj, created = HorasEnfermedad.objects.get_or_create(...)

# Recalcular horas del mes
Horas_totales.calcular_horas_totales(licencia.operario, mes_periodo)
```

### Reportes

Los registros justificados retroactivamente aparecen en:

- ✅ **Admin `RegistroAsistencia`:**
  - Filtro: `estado_justificacion = True`
  - Campo: `licencia_relacionada` (muestra ID de licencia)
  - Campo: `descripcion` (muestra "justificada retroactivamente")

- ✅ **Reportes `Horas_totales`:**
  - Columna: `horas_enfermedad` (suma todas las licencias del mes)

---

## ⚙️ Configuración

### Cambiar límite de 30 días

En `apps/reloj_fichador/tasks.py` línea 114:

```python
# Cambiar de:
if 0 < dias_diferencia <= 30:

# A (por ejemplo, 60 días):
if 0 < dias_diferencia <= 60:
```

### Deshabilitar retroactividad

Si necesitas deshabilitar esta característica (solo justificar días coincidentes):

```python
# Comentar o eliminar líneas 102-120 en tasks.py
```

---

## 📝 Logging y Auditoría

Cada justificación retroactiva se registra en logs:

```
INFO 2025-10-23 16:04:22 tasks
  Justificado retroactivamente registro anterior: González, Carlos en 2025-10-31

INFO 2025-10-23 16:04:22 tasks
  Licencia 1 procesada: 5/5 días justificados, 0 días retroactivos, 40h enfermedad
```

**Auditoría en BD:**
- Campo `descripcion` en `RegistroAsistencia` registra "Justificada retroactivamente"
- Campo `fecha_creacion` en `HorasEnfermedad` muestra cuándo se procesó

---

## 🔍 Verificación en Base de Datos

```sql
-- Ver registros justificados retroactivamente
SELECT
    ra.fecha,
    ra.estado_asistencia,
    ra.estado_justificacion,
    ra.licencia_relacionada_id,
    ra.descripcion
FROM reloj_fichador_registroasistencia ra
WHERE ra.descripcion LIKE '%retroactivamente%'
ORDER BY ra.fecha DESC
LIMIT 10;
```

---

## 🎓 Casos de Uso

### Caso 1: Licencia de 5 días (dentro del mismo rango)
```
Ausencias: Lun-Vie (5 registros sin justificación)
Licencia: Lun-Vie (aprobada)
Resultado: Los 5 se justifican
```

### Caso 2: Licencia con atraso (hasta 30 días)
```
Ausencias: Oct 1-5 (5 registros sin justificación)
Licencia cargada: Nov 1 (por Oct 1-5)
Resultado: Los 5 se justifican (dentro de 30 días)
```

### Caso 3: Licencia con atraso > 30 días (FUERA de límite)
```
Ausencias: Sep 1-5 (5 registros sin justificación)
Licencia cargada: Nov 1 (por Sep 1-5) - más de 60 días después
Resultado: Los 5 NO se justifican (fuera del límite de 30 días)
```

### Caso 4: Ausencia parcial
```
Ausencias: Oct 1, 3, 5 (3 registros sin justificación)
Licencia: Oct 1-5 (aprobada)
Resultado: Los 3 se justifican (dentro de rango y límite)
```

---

## 🐛 Troubleshooting

### ¿Por qué mis registros no se justificaron?

**Posibles causas:**

1. **Licencia rechazada:** Solo se procesan licencias con `estado='aprobada'`
2. **Fuera de 30 días:** Si la ausencia fue hace >30 días
3. **Ya justificados:** Si `estado_justificacion=True` ya
4. **Ya vinculados:** Si `licencia_relacionada` ya tiene valor

**Verificación:**
```python
# Ejecutar desde shell Django
python manage.py shell

from apps.reloj_fichador.models import RegistroAsistencia, Licencia
licencia = Licencia.objects.get(pk=...)  # Tu licencia
registros = RegistroAsistencia.objects.filter(
    operario=licencia.operario,
    fecha__lt=licencia.fecha_inicio,
    estado_asistencia=RegistroAsistencia.ausente,
    estado_justificacion=False,
    licencia_relacionada__isnull=True
)
print(f"Registros sin justificación previos: {registros.count()}")
for r in registros:
    dias_diff = (licencia.fecha_inicio - r.fecha).days
    print(f"  {r.fecha}: {dias_diff} días antes ({r.estado_justificacion=})")
```

### ¿Cómo recalcular manualmente?

Usa el management command:

```bash
docker compose exec -T web python manage.py \
  sincronizar_asistencias_con_licencias \
  --operario 146 \
  --verbose
```

---

## 📚 Referencias

- [IMPLEMENTACION_HORAS_ENFERMEDAD.md](IMPLEMENTACION_HORAS_ENFERMEDAD.md) - Sistema de horas de enfermedad
- [COMO_FUNCIONAN_LAS_LICENCIAS_MEDICAS.md](COMO_FUNCIONAN_LAS_LICENCIAS_MEDICAS.md) - Flujo general de licencias
- [apps/reloj_fichador/tasks.py](apps/reloj_fichador/tasks.py) - Código fuente (líneas 71-196)
- [TEST/test_justificacion_retroactiva.py](TEST/test_justificacion_retroactiva.py) - Tests

---

## ✅ Checklist de Implementación

- ✅ Lógica de justificación retroactiva implementada
- ✅ Límite de 30 días implementado
- ✅ Logging detallado agregado
- ✅ Tests unitarios creados y pasados
- ✅ Documentación completada
- ✅ Syntax validado (py_compile)
- ✅ Funciona en escenarios reales

---

**Fecha:** 23 de octubre de 2025
**Estado:** ✅ PRODUCCIÓN LISTO
