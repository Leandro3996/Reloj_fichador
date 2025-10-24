# 🤖 Cálculo Automático: Conversión de Días a Horas

**Fecha:** 23 de octubre de 2025
**Estado:** ✅ FUNCIONANDO AUTOMÁTICAMENTE

---

## 📊 ¿Cómo Funciona?

**SÍ, el cálculo de conversión "días a horas" se hace COMPLETAMENTE AUTOMÁTICO.**

Cuando se aprueba una licencia médica, el sistema automáticamente:

1. ✅ **Calcula la duración en días** (fecha_fin - fecha_inicio + 1)
2. ✅ **Convierte a horas** (duración_días × 8)
3. ✅ **Almacena como DurationField** (timedelta en segundos)
4. ✅ **Muestra en admin** (formateado como "Xh Ym")

---

## 🔧 Código de Cálculo Automático

**Ubicación:** `apps/reloj_fichador/tasks.py` líneas 96-98

```python
# Calcular duración en días y convertir a horas (8h por día)
duracion_dias = (licencia.fecha_fin - licencia.fecha_inicio).days + 1
horas_enfermedad_total = timedelta(hours=duracion_dias * 8)
```

### Desglose del Código:

| Paso | Código | Qué Hace | Ejemplo |
|------|--------|----------|---------|
| 1️⃣ | `licencia.fecha_fin - licencia.fecha_inicio` | Calcula diferencia en días | 2025-06-18 - 2025-06-17 = 1 día |
| 2️⃣ | `.days + 1` | Suma 1 para incluir ambos días | 1 + 1 = 2 días |
| 3️⃣ | `duracion_dias * 8` | Multiplica por 8 horas/día | 2 × 8 = 16 horas |
| 4️⃣ | `timedelta(hours=...)` | Convierte a DurationField | timedelta(hours=16) |

---

## 📈 Ejemplos de Cálculo Automático

### Ejemplo 1: Licencia Corta (2 días)

**Licencia de Pizarro:**
- Fecha inicio: `2025-06-17`
- Fecha fin: `2025-06-18`

**Cálculo automático:**
```
Días: (2025-06-18 - 2025-06-17).days + 1 = 1 + 1 = 2 días
Horas: 2 × 8 = 16 horas
DurationField: timedelta(hours=16)
Total segundos: 16 × 3600 = 57,600 segundos
Mostrado en admin: "16h 0m" ✅
```

### Ejemplo 2: Licencia Mediana (5 días)

**Licencia hipotética:**
- Fecha inicio: `2025-05-01`
- Fecha fin: `2025-05-05`

**Cálculo automático:**
```
Días: (2025-05-05 - 2025-05-01).days + 1 = 4 + 1 = 5 días
Horas: 5 × 8 = 40 horas
DurationField: timedelta(hours=40)
Total segundos: 40 × 3600 = 144,000 segundos
Mostrado en admin: "40h 0m" ✅
```

### Ejemplo 3: Licencia Larga (30 días)

**Licencia de Morales:**
- Fecha inicio: `2025-06-01`
- Fecha fin: `2025-06-30`

**Cálculo automático:**
```
Días: (2025-06-30 - 2025-06-01).days + 1 = 29 + 1 = 30 días
Horas: 30 × 8 = 240 horas
DurationField: timedelta(hours=240)
Total segundos: 240 × 3600 = 864,000 segundos
Mostrado en admin: "240h 0m" ✅
```

### Ejemplo 4: Licencia de 1 Día

**Licencia hipotética:**
- Fecha inicio: `2025-07-15`
- Fecha fin: `2025-07-15`

**Cálculo automático:**
```
Días: (2025-07-15 - 2025-07-15).days + 1 = 0 + 1 = 1 día
Horas: 1 × 8 = 8 horas
DurationField: timedelta(hours=8)
Total segundos: 8 × 3600 = 28,800 segundos
Mostrado en admin: "8h 0m" ✅
```

---

## 🔄 Flujo Completo Automático

```
┌─────────────────────────────────────┐
│  Usuario aprueba licencia en admin  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Django signal dispara save() evento  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Licencia.save() llama:              │
│ procesar_licencia_aprobada(id)      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Calcular duración:                  │
│ duracion_dias =                     │
│   (fecha_fin - fecha_inicio).days+1 │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Convertir a horas:                  │
│ duracion_dias * 8                   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Crear timedelta:                    │
│ timedelta(hours=duracion_dias * 8)  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Guardar en HorasEnfermedad          │
│ (almacena como segundos)            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Actualizar Horas_totales            │
│ (suma HorasEnfermedad)              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ En admin: get_horas_enfermedad()    │
│ Convierte a "Xh Ym"                │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Mostrar en tabla: "240h 0m"         │
│ ✅ COMPLETADO                       │
└─────────────────────────────────────┘
```

---

## 💾 Almacenamiento en Base de Datos

El sistema guarda las horas como `DurationField` (internamente como segundos):

```sql
-- Tabla: reloj_fichador_horas_enfermedad
CREATE TABLE reloj_fichador_horas_enfermedad (
    id INT PRIMARY KEY,
    operario_id INT,
    licencia_id INT,
    horas_enfermedad BIGINT,  -- Almacena segundos
    mes_periodo VARCHAR(20),
    fecha_creacion DATETIME,
    FOREIGN KEY (operario_id) REFERENCES reloj_fichador_operario(id),
    FOREIGN KEY (licencia_id) REFERENCES reloj_fichador_licencia(id)
);

-- Ejemplos de datos:
-- Pizarro (2 días): horas_enfermedad = 57600 (16 × 3600)
-- Morales (30 días): horas_enfermedad = 864000 (240 × 3600)
```

---

## 🎯 Configuración Clave

### Fórmula Automatizada

```python
Horas de Enfermedad = (Días de Licencia) × 8 horas/día
```

### Dónde Se Define

- **Archivo:** `apps/reloj_fichador/tasks.py`
- **Líneas:** 96-98
- **Función:** `procesar_licencia_aprobada()`

### ¿Se Puede Cambiar?

**SÍ, se puede cambiar el valor de 8 horas por día.**

Para cambiar a, por ejemplo, 7 horas por día:

```python
# En tasks.py línea 98, cambiar:
horas_enfermedad_total = timedelta(hours=duracion_dias * 8)  # ← 8 horas

# A:
horas_enfermedad_total = timedelta(hours=duracion_dias * 7)  # ← 7 horas
```

---

## ✅ Verificación de Cálculos

Para verificar que el cálculo es correcto en cualquier momento:

```bash
docker compose exec -T web python manage.py shell

# En el shell:
from apps.reloj_fichador.models import HorasEnfermedad, Operario

# Buscar registros de enfermedad
for he in HorasEnfermedad.objects.all()[:5]:
    horas = int(he.horas_enfermedad.total_seconds() / 3600)
    dias = horas / 8
    print(f"{he.operario.apellido}: {horas}h ({dias:.0f} días)")
```

---

## 📊 Tabla de Conversiones Automáticas

| Días | Fórmula | Horas | DurationField | En Admin |
|------|---------|-------|---------------|----------|
| 1 | 1 × 8 | 8 | 8:00:00 | 8h 0m |
| 2 | 2 × 8 | 16 | 16:00:00 | 16h 0m |
| 3 | 3 × 8 | 24 | 1 day, 0:00:00 | 24h 0m |
| 5 | 5 × 8 | 40 | 1 day, 16:00:00 | 40h 0m |
| 10 | 10 × 8 | 80 | 3 days, 8:00:00 | 80h 0m |
| 30 | 30 × 8 | 240 | 10 days, 0:00:00 | 240h 0m |

---

## 🔍 Cómo Verificar que Funciona

### 1. Crear una Licencia de Prueba

1. Ir a admin: http://localhost:5080/admin/reloj_fichador/licencia/
2. Crear licencia: 3 días (debería calcular 24 horas)
3. Marcar "Aprobada"
4. Guardar

### 2. Verificar en Horas_totales

```bash
# En shell:
from apps.reloj_fichador.models import Horas_totales, HorasEnfermedad

# Ver horas enfermedad creadas
for he in HorasEnfermedad.objects.filter(operario__dni=XXXXX).order_by('-fecha_creacion')[:1]:
    horas = int(he.horas_enfermedad.total_seconds() / 3600)
    print(f"HorasEnfermedad: {horas}h")

# Ver Horas_totales actualizado
ht = Horas_totales.objects.filter(operario__dni=XXXXX).latest('mes_actual')
print(f"Horas_totales enfermedad: {int(ht.horas_enfermedad.total_seconds() / 3600)}h")
```

### 3. Verificar en Admin

Ir a: http://localhost:5080/admin/reloj_fichador/horas_totales/
Buscar al operario y verificar columna "Horas Enfermedad" muestre el valor correcto.

---

## 🚀 Proceso Completamente Automático

**No necesitas hacer nada manualmente.** El sistema automáticamente:

1. ✅ Calcula días de la licencia
2. ✅ Convierte a horas (× 8)
3. ✅ Guarda en HorasEnfermedad
4. ✅ Actualiza Horas_totales
5. ✅ Muestra en admin con formato correcto

**Todo sucede en tiempo real cuando apruebas una licencia.**

---

## 📝 Resumen

| Aspecto | Detalles |
|---------|----------|
| **¿Automático?** | ✅ SÍ, completamente automático |
| **Cálculo** | Días × 8 horas/día |
| **Dónde se calcula** | `procesar_licencia_aprobada()` en tasks.py |
| **Se puede cambiar** | ✅ SÍ, línea 98 de tasks.py |
| **Almacenamiento** | DurationField (segundos en BD) |
| **Mostrado en admin** | "Xh Ym" formato legible |

---

**Status:** ✅ **COMPLETAMENTE AUTOMATIZADO Y FUNCIONANDO**

El cálculo de "1 día = 8 horas" ocurre automáticamente cada vez que se aprueba una licencia médica.

