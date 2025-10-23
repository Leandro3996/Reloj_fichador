# 📅 IMPLEMENTACIÓN - CALENDARIO LABORAL Y GRUPOS DE SÁBADO

**Fecha de implementación:** 23 de Octubre de 2025
**Estado:** ✅ COMPLETADO

---

## 🎯 OBJETIVO

Resolver dos problemas críticos en el sistema de asistencia:

1. **Domingos marcados como ausencias:** Los domingos no debería generarse registros de asistencia
2. **Sábados sin flexibilidad:** No había forma de definir qué operarios trabajan cada sábado
3. **Feriados no contemplados:** No había manera de marcar días feriados, paros, o cambios de calendario

---

## 📋 SOLUCIÓN IMPLEMENTADA

### 1️⃣ **Modelo `CalendarioLaboral`**

Define días especiales (feriados, paros, mantenimiento, etc.). Por defecto, cualquier día NO registrado es laborable.

**Campos:**
- `fecha` (DateField, única): Fecha del evento
- `tipo_dia`: Opciones disponibles:
  - ✅ Día Laboral Normal
  - 🎉 Feriado Nacional
  - 📅 Feriado Movible
  - ✊ Paro/Conflicto Laboral
  - 🔧 Mantenimiento/Clausura
  - ❓ Otro
- `nombre`: Descripción del evento
- `descripcion`: Detalles adicionales
- `aplica_a_todas_areas`: Boolean (permite aplicar solo a áreas específicas)
- `areas`: ManyToMany (si aplica a áreas específicas)
- Auditoría: `creado_el`, `actualizado_el`

**Ubicación en admin:** Panel Reloj Fichador → Calendarios Laborales

---

### 2️⃣ **Modelo `GrupoSabado`**

Asigna operarios a grupos de sábado (A/B) con lógica de semanas pares/impares.

**Lógica de funcionamiento:**
- **Grupo A:** Trabaja en semanas **pares** de sábado (2, 4, 6, 8, etc.)
- **Grupo B:** Trabaja en semanas **impares** de sábado (1, 3, 5, 7, etc.)

**Campos:**
- `operario`: ForeignKey a Operario
- `grupo`: CharField ('A' o 'B')
- `fecha_inicio`: Fecha desde la que tiene efecto
- `fecha_fin`: Fecha hasta la que tiene efecto (NULL = indefinido)
- `descripcion`: Motivo del cambio (opcional)
- Auditoría: `creado_el`, `actualizado_el`

**Validaciones:**
- No puede haber dos grupos activos simultáneamente para el mismo operario
- Detecta y previene solapamientos automáticamente

**Ubicación en admin:** Panel Reloj Fichador → Grupos de Sábado

---

### 3️⃣ **Función `es_dia_laboral(fecha, operario=None)`**

Determina si una fecha es laboral considerando:

```
1. CalendarioLaboral (feriados, paros, etc.)
   ↓
2. Domingos → NUNCA son laborales
   ↓
3. Sábados → Solo si operario está en grupo A/B
   ↓
4. Lunes-viernes → SIEMPRE son laborales (salvo calendario)
```

**Ejemplos de uso:**

```python
from apps.reloj_fichador.utils import es_dia_laboral
from datetime import date

# Verificar si domingo es laboral
es_dia_laboral(date(2025, 10, 26))  # False (domingo)

# Verificar si sábado es laboral para un operario
es_dia_laboral(date(2025, 10, 18), operario=carlos)  # True/False según grupo

# Verificar día normal
es_dia_laboral(date(2025, 10, 20))  # True (lunes)

# Verificar con feriado registrado
es_dia_laboral(date(2025, 10, 22))  # False (feriado)
```

---

### 4️⃣ **Funciones Auxiliares**

#### `obtener_sabados_operario(operario, mes, año)`
Retorna lista de sábados que un operario trabaja en un mes.

```python
from apps.reloj_fichador.utils import obtener_sabados_operario

sabados = obtener_sabados_operario(operario, mes=10, año=2025)
# [date(2025, 10, 4), date(2025, 10, 18)]
```

#### `obtener_dias_laborales_mes(operario=None, mes=None, año=None)`
Retorna lista de todos los días laborales de un mes.

```python
dias_lab = obtener_dias_laborales_mes(operario=carlos, mes=10, año=2025)
# [date(2025, 10, 1), date(2025, 10, 2), ..., date(2025, 10, 31)]
```

#### `obtener_feriados_mes(mes=None, año=None)`
Retorna feriados del mes.

```python
feriados = obtener_feriados_mes(mes=10, año=2025)
# [(date(2025, 10, 22), "Feriado de Prueba", "🎉 Feriado Nacional")]
```

#### `horas_feriado_por_operario(operario, mes, año)`
Calcula horas perdidas por feriados (asume 8h/día lunes-viernes, 4h sábado).

```python
horas = horas_feriado_por_operario(carlos, 10, 2025)
# 8.0 (si hay un feriado en un día laboral)
```

---

### 5️⃣ **Modificación de `generar_registros_asistencia()`**

La tarea Celery ahora:

1. ✅ Verifica si hoy es día laboral GENERAL (excluye domingos y feriados)
2. ✅ Para cada operario, verifica si hoy es laboral PARA ESE OPERARIO
3. ✅ Solo crea registros si ambas condiciones son verdaderas
4. ✅ Registra logs de operarios que no trabajan hoy

**Cambio clave:**
```python
# ANTES: Creaba registro para TODOS los operarios, incluyendo domingos
if es_dia_laboral(hoy, operario):  # NUEVO: Valida día laboral
    registro, created = RegistroAsistencia.objects.get_or_create(...)
```

---

## 🎛️ ADMIN CUSTOMIZADO

### Calendario Laboral

**Vista de lista:**
- 📅 Fecha
- 🎨 Tipo de día (con color: verde/naranja/rojo/etc.)
- 📝 Nombre
- 🏢 Aplica a todas áreas
- 📅 Creado el

**Filtros:**
- Por tipo de día
- Por fecha (rango)
- Por aplicación a áreas

**Acciones masivas:**
- ✅ Marcar como Laborales
- 🎉 Marcar como Feriados
- ✊ Marcar como Paros

### Grupos de Sábado

**Vista de lista:**
- 👤 Operario
- 🔤 Grupo (A/B con colores)
- 📅 Fecha Inicio
- 📅 Fecha Fin (muestra "∞ Indefinido" si aplica)
- ✅ Estado (Activo/Inactivo)

**Filtros:**
- Por grupo (A/B)
- Por fecha de inicio
- Por estado de vigencia

---

## 📊 EJEMPLOS DE USO

### Crear un Feriado

**Via Admin:**
1. Ir a "Calendarios Laborales"
2. Hacer clic en "Agregar Calendario Laboral"
3. Llenar:
   - Fecha: 2025-11-17
   - Tipo: 🎉 Feriado Nacional
   - Nombre: Soberanía Nacional
   - Descripción: Feriado nacional
4. Guardar

**Via Python:**
```python
from apps.reloj_fichador.models import CalendarioLaboral
from datetime import date

CalendarioLaboral.objects.create(
    fecha=date(2025, 11, 17),
    tipo_dia='feriado',
    nombre='Soberanía Nacional',
    descripcion='Feriado nacional'
)
```

### Asignar Operario a Grupo

**Via Admin:**
1. Ir a "Grupos de Sábado"
2. Hacer clic en "Agregar Grupo de Sábado"
3. Llenar:
   - Operario: Carlos Martinez
   - Grupo: Grupo A (Semanas Pares)
   - Fecha Inicio: 2025-10-01
   - Fecha Fin: (dejar vacío para indefinido)
4. Guardar

**Via Python:**
```python
from apps.reloj_fichador.models import GrupoSabado, Operario
from datetime import date

operario = Operario.objects.get(nombre='Carlos', apellido='Martinez')
GrupoSabado.objects.create(
    operario=operario,
    grupo='A',
    fecha_inicio=date(2025, 10, 1),
    fecha_fin=None  # Indefinido
)
```

---

## 🧪 VERIFICACIÓN

**Test de domingos:**
```python
from apps.reloj_fichador.utils import es_dia_laboral
from datetime import date

assert not es_dia_laboral(date(2025, 10, 26))  # Domingo = False ✅
```

**Test de sábados con grupo:**
```python
from apps.reloj_fichador.models import Operario, GrupoSabado
from datetime import date

operario = Operario.objects.get(nombre='Carlos')
GrupoSabado.objects.create(
    operario=operario,
    grupo='A',
    fecha_inicio=date(2025, 10, 1)
)

# Semana 42 (par) = Grupo A trabaja
assert es_dia_laboral(date(2025, 10, 18), operario)  # True ✅

# Semana 43 (impar) = Grupo A no trabaja
assert not es_dia_laboral(date(2025, 10, 25), operario)  # False ✅
```

---

## 🔄 MIGRACIÓN

**Nombre de migración:** `0032_add_calendario_laboral_y_grupo_sabado`

**Tablas creadas:**
- `reloj_fichador_calendarlaboral`
- `reloj_fichador_gruposabado`
- `reloj_fichador_calendarlaboral_areas` (relación M2M)

**Para aplicar:**
```bash
python manage.py migrate reloj_fichador
```

---

## 🚀 IMPACTO EN OTRAS ÁREAS

### RegistroAsistencia
- No se generan registros para domingos
- No se generan registros para sábados no programados
- No se generan registros para feriados/paros

### RegistroDiario
- Sin cambios directos
- Los registros de entrada/salida se siguen capturando normalmente
- La validación ocurre en la capa de asistencia

### Celery
- `generar_registros_asistencia()`: Ahora más eficiente (menos registros innecesarios)

---

## 📈 PRÓXIMAS MEJORAS (Opcional)

1. **Vista de Calendario Mensual:**
   - Tabla interactiva para marcar feriados
   - Arrastrar/soltar para cambiar grupos
   - Miniatura de asistencia del mes

2. **Reportes:**
   - Horas de feriado por mes/año
   - Validación de grupos inconsistentes
   - Alertas de operarios sin grupo asignado

3. **Integraciones:**
   - Importar feriados nacionales automáticamente
   - API para cambios de grupo desde exterior

---

## ✅ CHECKLIST FINAL

- [x] Modelos creados y migrados
- [x] Funciones de validación implementadas
- [x] Admin customizado creado
- [x] Tarea Celery actualizada
- [x] Tests pasados
- [x] Documentación completada
- [x] Sintaxis verificada
- [x] Imports correctos
- [x] Sin errores de migración

---

**Estado:** 🟢 LISTO PARA PRODUCCIÓN

