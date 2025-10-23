# 📋 Implementación: Horas de Enfermedad en Licencias Médicas

**Fecha:** 23 de octubre de 2025
**Estado:** ✅ COMPLETADO
**Requisito:** Cuando se aprueba una licencia médica, las horas deben sumarse al modelo `Horas_totales` como `horas_enfermedad`

---

## 📊 Resumen Ejecutivo

Se implementó un sistema completo de acumulación de horas de enfermedad que:

✅ **Calcula automáticamente** horas de enfermedad (días × 8 horas)
✅ **Crea registros de asistencia** justificados para cada día de licencia
✅ **Almacena auditoría completa** en el modelo `HorasEnfermedad`
✅ **Actualiza Horas_totales** con horas de enfermedad acumuladas
✅ **Procesa de forma asíncrona** sin bloquear la interfaz admin

---

## 🏗️ Arquitectura de Solución

### 1. Nuevos Modelos Creados

#### `HorasEnfermedad` (nuevo)
Modelo para registrar y auditar horas de enfermedad acumuladas por licencias médicas.

```python
class HorasEnfermedad(models.Model):
    operario = ForeignKey(Operario)  # Empleado
    licencia = ForeignKey(Licencia)  # Licencia que generó las horas
    horas_enfermedad = DurationField  # Total de horas (duracion × 8h)
    fecha_creacion = DateTimeField    # Cuándo se registró
    mes_periodo = CharField           # Mes (YYYY-MM) para agrupación

    # Índices para optimización
    - Index: operario + mes_periodo
    - Index: licencia (para auditoría)
```

**Propósito:**
- Mantener histórico completo de licencias y horas
- Permitir auditoría de cambios
- Rastrear qué licencia generó cada hora de enfermedad

#### `Horas_totales` (modificado)
Se agregó un nuevo campo:

```python
horas_enfermedad = DurationField(
    default=timedelta,
    help_text="Horas acumuladas por licencias médicas aprobadas"
)
```

---

## 🔄 Flujo Completo de Procesos

```
┌─────────────────────────────────────────────┐
│ Usuario aprueba Licencia en Admin           │
│ estado: pendiente → aprobada                │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│ Licencia.save() detecta cambio de estado    │
│ (Línea 259 en models.py)                    │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│ Dispara tarea Celery ASÍNCRONA:             │
│ procesar_licencia_aprobada.delay(pk)        │
│ (Línea 276 en models.py)                    │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│ CELERY - procesar_licencia_aprobada()       │
│ (tasks.py:72-178)                           │
│                                             │
│ 1. Calcula horas: duracion_días × 8        │
│ 2. Itera día por día                        │
│ 3. Por cada día:                            │
│    - Crea/actualiza RegistroAsistencia      │
│      (estado=ausente, justificado=True)     │
│ 4. Crea registro HorasEnfermedad            │
│    - Vincula licencia                       │
│    - Almacena mes_periodo                   │
│ 5. Recalcula Horas_totales del mes          │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│ RESULTADO FINAL:                            │
│ ✅ RegistroAsistencia: N registros          │
│ ✅ HorasEnfermedad: 1 registro              │
│ ✅ Horas_totales: Actualizado               │
└─────────────────────────────────────────────┘
```

---

## 📁 Archivos Modificados

### 1. `apps/reloj_fichador/models.py`

**Línea 689-714:** Nuevo modelo `HorasEnfermedad`
```python
class HorasEnfermedad(models.Model):
    operario = models.ForeignKey(Operario, on_delete=models.CASCADE)
    licencia = models.ForeignKey('Licencia', on_delete=models.SET_NULL, null=True, blank=True)
    horas_enfermedad = models.DurationField(default=timedelta, ...)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    mes_periodo = models.CharField(max_length=20, ...)
```

**Línea 751-752:** Campo agregado a `Horas_totales`
```python
horas_enfermedad = models.DurationField(
    default=timedelta,
    help_text="Horas acumuladas por licencias médicas aprobadas"
)
```

**Línea 787-790:** Método `calcular_horas_totales()` actualizado
```python
# Sumar horas de enfermedad acumuladas por licencias médicas
horas_enfermedad = HorasEnfermedad.objects.filter(
    operario=operario,
    mes_periodo=mes
).aggregate(total=Sum('horas_enfermedad'))['total'] or timedelta()
```

### 2. `apps/reloj_fichador/tasks.py`

**Línea 72-178:** Tarea `procesar_licencia_aprobada()` ampliada

Cambios principales:
- Calcula horas de enfermedad: `duracion_dias × 8`
- Línea 141-162: Crear/actualizar `HorasEnfermedad`
- Línea 161: Recalcula `Horas_totales` del mes
- Mejor logging para auditoría

```python
# Calcular duración en días y convertir a horas (8h por día)
duracion_dias = (licencia.fecha_fin - licencia.fecha_inicio).days + 1
horas_enfermedad_total = timedelta(hours=duracion_dias * 8)

# ... procesar días ...

# ✅ CREAR REGISTRO DE HORAS DE ENFERMEDAD
mes_periodo = licencia.fecha_inicio.strftime('%Y-%m')
horas_enfermedad_obj, created = HorasEnfermedad.objects.get_or_create(
    operario=licencia.operario,
    licencia=licencia,
    mes_periodo=mes_periodo,
    defaults={'horas_enfermedad': horas_enfermedad_total}
)

# ✅ RECALCULAR HORAS_TOTALES DEL MES
Horas_totales.calcular_horas_totales(licencia.operario, mes_periodo)
```

### 3. `apps/reloj_fichador/admin.py`

**Línea 20:** Import agregado
```python
HorasEnfermedad  # Agregado a los imports
```

**Línea 1634-1681:** Nuevo `HorasEnfermedadAdmin`
```python
@admin.register(HorasEnfermedad)
class HorasEnfermedadAdmin(UnfoldModelAdmin):
    # Lista de horas enfermedad con formateo legible
    # Campos read-only (sin edición manual)
    # Enlaces a licencias relacionadas
    # No permite agregar/eliminar manualmente
```

---

## 🗄️ Migrations Aplicadas

### Migration 0034: `add_horasenfermedade_model`

Aplicada correctamente a la BD real.

```bash
✓ Created table: reloj_fichador_horasenfermedad
✓ Added column: horas_enfermedad to horas_totales
✓ Created indexes for optimized queries
```

**Verificación en MySQL:**
```sql
DESCRIBE reloj_fichador_horasenfermedad;
SHOW COLUMNS FROM reloj_fichador_horas_totales LIKE 'horas_enfermedad';
```

---

## 🧪 Testing

### Test Unitario: `test_licencia_enfermedad.py`

Ubicación: `TEST/test_licencia_enfermedad.py`

**Tests Implementados:**

1. ✅ **test_licencia_medica_3_dias**
   - Valida: 3 días = 24 horas
   - Verifica: RegistroAsistencia creados
   - Verifica: HorasEnfermedad creado
   - Estado: PASADO

2. ✅ **test_licencia_medica_5_dias**
   - Valida: 5 días = 40 horas (semana laboral)
   - Estado: PASADO

3. ✅ **test_multiple_licencias_mismo_mes**
   - Valida: Múltiples licencias se suman correctamente
   - Licencia 1: 2 días = 16h
   - Licencia 2: 3 días = 24h
   - Total: 40h
   - Estado: PASADO

**Ejecución:**
```bash
docker compose exec -T web python manage.py test \
  TEST.test_licencia_enfermedad.TestLicenciaEnfermedad -v 2
```

---

## 📊 Ejemplo de Uso

### Escenario: Empleado toma licencia médica de 3 días

**Paso 1: Admin crea licencia**
```
Fecha inicio: 27/10/2025 (Lunes)
Fecha fin: 29/10/2025 (Miércoles)
Estado: Pendiente
Aplicar a asistencia: ✓ Sí
```

**Paso 2: Admin aprueba**
```
Estado: Aprobada ← Esto dispara la tarea Celery
```

**Paso 3: Sistema procesa automáticamente**

En la BD se crea:

**RegistroAsistencia (3 registros):**
| Fecha | Operario | Estado | Justificado | Licencia |
|-------|----------|--------|-------------|----------|
| 2025-10-27 | Juan | Ausente | ✓ | 1 |
| 2025-10-28 | Juan | Ausente | ✓ | 1 |
| 2025-10-29 | Juan | Ausente | ✓ | 1 |

**HorasEnfermedad (1 registro):**
| Operario | Licencia | Horas | Mes | Fecha Creación |
|----------|----------|-------|-----|----------------|
| Juan | 1 | 24:00 | 2025-10 | 2025-10-23 18:37:52 |

**Horas_totales (actualizado o creado):**
| Operario | Mes | Horas Normales | Horas Nocturnas | Horas Extras | Horas Feriado | **Horas Enfermedad** |
|----------|-----|----------------|-----------------|--------------|---------------|----------------------|
| Juan | 2025-10 | 160:00 | 0:00 | 0:00 | 0:00 | **24:00** |

---

## 🔍 Auditoría y Tracking

### ¿Cómo se audita?

1. **Django SimpleHistory** en modelo `Licencia`:
   - Registra todos los cambios de estado
   - Quién aprobó y cuándo

2. **Modelo `HorasEnfermedad`**:
   - Mantiene vínculo a la licencia original
   - Registra fecha_creacion (timestamp)
   - Permite rastrear cambios en admin

3. **Logs de Celery**:
   - Cada procesamiento se registra en logs
   - Errores capturados y registrados

### Visualización en Admin

**Panel de Horas Enfermedad:**
- URL: `/admin/reloj_fichador/horasenfermedad/`
- Filtros: Por mes, operario, fecha creación
- Búsqueda: Por nombre del operario
- Enlaces: Directos a la licencia relacionada

---

## ⚙️ Configuración y Personalización

### Cambiar horas por día (actualmente 8h)

En `tasks.py` línea 93:
```python
horas_enfermedad_total = timedelta(hours=duracion_dias * 8)  # ← Cambiar aquí
```

O hacer configurable en settings.

### Aplicar a asistencia (opcional)

Las licencias tienen un flag:
```python
licencia.aplicar_a_asistencia = True  # ← Controla si se generan HorasEnfermedad
```

---

## 🚀 Próximas Mejoras (Opcional)

1. **Portal de Empleados:**
   - Ver saldo de horas de enfermedad
   - Visualizar histórico de licencias

2. **Integración con Nómina:**
   - Exportar horas_enfermedad
   - Calcular bonificaciones/descuentos

3. **Reportes Avanzados:**
   - Tendencias de licencias por mes
   - Comparativas por área
   - Alertas de abuso

4. **Restricciones:**
   - Máximo de horas de enfermedad por año
   - Bloqueo automático después de X días

---

## 📌 Checklist de Implementación

- ✅ Modelo `HorasEnfermedad` creado
- ✅ Campo `horas_enfermedad` agregado a `Horas_totales`
- ✅ Tarea Celery actualizada
- ✅ Método `calcular_horas_totales()` mejorado
- ✅ Admin interface implementado
- ✅ Migrations creadas y aplicadas
- ✅ Tests unitarios creados y pasados
- ✅ Documentación completada
- ✅ Código en producción (Django real) ✓
- ✅ Código en tests (SQLite) ✓

---

## 🆘 Troubleshooting

### Error: "duplicate column name 'horas_enfermedad'"
**Solución:** Migration ya fue aplicada. Ejecutar `showmigrations` para verificar.

### Las horas no aparecen en Horas_totales
**Causa:** `calcular_horas_totales()` no fue llamado
**Solución:** Se llama automáticamente en `procesar_licencia_aprobada()`

### Celery no procesa la tarea
**Verificar:** `docker compose logs celery | grep procesar_licencia`
**Reiniciar:** `docker compose restart celery celery-beat`

---

## 📞 Soporte

Para preguntas o mejoras, contactar al desarrollador.

---

**Fecha de Implementación:** 23 de octubre de 2025
**Versión:** 1.0
**Estado:** ✅ Producción
