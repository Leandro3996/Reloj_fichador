# 🔍 ANÁLISIS: ¿QUÉ SUCEDE CUANDO SE ACEPTA UN FERIADO?

**Fecha de análisis:** 23 de Octubre de 2025
**Pregunta:** ¿Se suma como horas_feriado en horastotales? ¿RegistroAsistencia lo toma como ausencia? ¿Queda justificado?

---

## 📋 RESPUESTA RÁPIDA

Cuando se **acepta un feriado** en `SugerenciaFeriado`:

| Aspecto | Resultado | Detalles |
|--------|-----------|---------|
| **¿Se suma en horas_feriado?** | ✅ **SÍ** | Se calcula en `horas_feriado_por_operario()` |
| **¿RegistroAsistencia como ausencia?** | ❌ **NO se crea** | No se genera si es feriado (validado en generar_registros_asistencia) |
| **¿Se marca como justificado?** | 🟡 **N/A** | No existe RegistroAsistencia para no justificar |

---

## 🔄 FLUJO COMPLETO PASO A PASO

### PASO 1: Usuario acepta feriado en Admin

**Archivo:** `apps/reloj_fichador/models.py:1131-1149`

```python
def aceptar(self, usuario=None):
    """Acepta la sugerencia y crea CalendarioLaboral"""

    # 1. Cambiar estado
    self.estado = 'aceptado'
    self.usuario_aprobador = usuario
    self.fecha_aprobacion = timezone.now()
    self.save()

    # 2. Crear entrada en CalendarioLaboral
    CalendarioLaboral.objects.get_or_create(
        fecha=self.fecha,
        defaults={
            'tipo_dia': 'feriado',
            'nombre': self.nombre,
            'aplica_a_todas_areas': True
        }
    )
```

**Resultado:** Se crea un registro en `CalendarioLaboral` con `tipo_dia='feriado'`

---

### PASO 2: Sistema valida si es día laboral (es_dia_laboral)

**Archivo:** `apps/reloj_fichador/utils.py:597-670`

```python
def es_dia_laboral(fecha, operario=None):
    """
    Verifica si una fecha es día laboral considerando:
    1. CalendarioLaboral (primero)
    2. Domingo (siempre no-laboral)
    3. Sábado con GrupoSabado (flexible)
    4. Lunes-viernes (siempre laborales)
    """

    # LÍNEA 615-617: VALIDACIÓN DE CALENDARIO LABORAL
    try:
        calendario = CalendarioLaboral.objects.get(fecha=fecha)
        if calendario.es_no_laboral():  # tipo_dia != 'laboral'
            return False  # ❌ NO es día laboral
    except CalendarioLaboral.DoesNotExist:
        pass
```

**Resultado:** `es_dia_laboral(fecha_feriado)` retorna `False`

---

### PASO 3: Generación de RegistroAsistencia (Celery)

**Archivo:** `apps/reloj_fichador/tasks.py:10-50`

```python
@shared_task
def generar_registros_asistencia():
    hoy = timezone.now().date()
    operarios_activos = Operario.objects.filter(activo=True)

    # VALIDACIÓN 1: ¿Es día laboral globally?
    if not es_dia_laboral(hoy):
        logger.info(f"Hoy ({hoy}) no es día laboral. No se generan registros.")
        return  # ❌ NO se crea nada si es feriado

    # Si pasa la validación global, verificar por operario
    for operario in operarios_activos:
        if not es_dia_laboral(hoy, operario):
            continue  # ❌ Saltar si operario no labora hoy

        # ✅ Solo crear si pasó ambas validaciones
        registro, created = RegistroAsistencia.objects.get_or_create(
            operario=operario,
            fecha=hoy
        )
```

**Resultado:**
- ✅ Si es feriado: **NO se crea RegistroAsistencia**
- ✅ No hay ausencia que registrar
- ✅ No hay nada que justificar

---

### PASO 4: Cálculo de horas_feriado en Horas_totales

**Archivo:** `apps/reloj_fichador/utils.py:778-813`

```python
def horas_feriado_por_operario(operario, mes, año):
    """
    Calcula horas de feriado perdidas por operario en el mes

    Retorna: float (horas)
    - Lunes-viernes: 8 horas por feriado
    - Sábado: 4 horas por feriado
    """

    horas_total = 0
    for dia in range(1, ultimo_dia + 1):
        fecha = date(año, mes, dia)

        # VALIDACIÓN: ¿Existe en CalendarioLaboral?
        try:
            cal = CalendarioLaboral.objects.get(fecha=fecha)
            if cal.es_no_laboral():  # tipo_dia != 'laboral'
                # CONTAR COMO HORAS PERDIDAS/FERIADO
                if fecha.weekday() == 5:  # Sábado
                    horas_total += 4  # Medio día
                else:  # Lunes-viernes
                    horas_total += 8  # Día completo
        except CalendarioLaboral.DoesNotExist:
            pass

    return horas_total  # ✅ Se suma a horas_feriado
```

**Resultado:**
- ✅ Se calcula automáticamente
- ✅ Se suma en `Horas_totales.horas_feriado`
- ✅ 8 horas si es lunes-viernes
- ✅ 4 horas si es sábado

---

## 📊 DIAGRAMA DE FLUJO

```
┌─────────────────────────────────────────┐
│  Admin ACEPTA sugerencia de feriado     │
└──────────────────┬──────────────────────┘
                   │
                   ↓
       ┌───────────────────────┐
       │ SugerenciaFeriado     │
       │ .aceptar()            │
       │ - estado → 'aceptado' │
       │ - crea CalendarioLaboral
       └───────────┬───────────┘
                   │
                   ↓
       ┌───────────────────────┐
       │ CalendarioLaboral     │
       │ fecha = 2025-02-17    │
       │ tipo_dia = 'feriado'  │
       └───────────┬───────────┘
                   │
        ┌──────────┴──────────┐
        ↓                     ↓
    CADA DÍA:            CÁLCULO MENSUAL:

    generar_registros_   horas_feriado_
    asistencia()         por_operario()
         │                     │
         ↓                     ↓
    es_dia_laboral()     CalendarioLaboral
    (valida Calendar)    .objects.filter()
         │                     │
         ↓                     ↓
    retorna FALSE        ¿es_no_laboral()?
    (NO es laboral)             │
         │                      ↓
         ↓                  Sí → suma +8h
    ❌ NO crea              o +4h(sábado)
    RegistroAsistencia          │
                                ↓
                        Horas_totales
                        .horas_feriado
                        += horas sumadas
```

---

## 📈 RESUMEN DEL IMPACTO

### Para cada feriado aceptado:

| Componente | Cambio | Efecto |
|-----------|--------|--------|
| **CalendarioLaboral** | ✅ Se crea | Marca fecha como no-laboral |
| **RegistroAsistencia** | ❌ No se crea | No hay "ausencia" que registrar |
| **Horas_feriado** | ✅ +8 o +4 | Se suma automáticamente en cálculo mensual |
| **Horas_normales** | ❌ No afecta | Operario no trabaja, no hay horas |
| **Horas_extras** | ❌ No afecta | Operario no trabaja, no hay extras |
| **Estado de justificación** | N/A | No aplica (no hay registro) |

---

## 💡 IMPLICACIONES IMPORTANTES

### 1. El operario NO tiene registro de ausencia
```
❌ Feriado aceptado ≠ "Ausencia en RegistroAsistencia"

El feriado previene la creación del registro, no lo crea y lo justifica.
```

### 2. Las horas de feriado SÍ se cuentan en el salario
```
✅ En liquidación salarial:
   - Horas_totales.horas_feriado se SUMA
   - Operario cobra el feriado como si hubiese trabajado
   - En Argentina: ley de feriados pagos
```

### 3. Impacto en reportes
```
Operario en día de feriado:
├─ NO aparece en "Ausentes del día" (sin RegistroAsistencia)
├─ SÍ aparece en "Días laborales: X feriados"
├─ SÍ afecta cálculo de "horas adeudadas" (no trabaja)
└─ SÍ aparece en "Horas de feriado" en nómina
```

---

## 🔧 VERIFICACIÓN TÉCNICA

### Para verificar el flujo en producción:

```python
# 1. Aceptar feriado
feriado = SugerenciaFeriado.objects.get(fecha='2025-02-17')
feriado.aceptar()

# 2. Verificar que se creó en CalendarioLaboral
cal = CalendarioLaboral.objects.get(fecha='2025-02-17')
print(f"Tipo: {cal.tipo_dia}")  # Será 'feriado'
print(f"Es no laboral: {cal.es_no_laboral()}")  # Será True

# 3. Verificar que NO se crea RegistroAsistencia
from datetime import date
registros = RegistroAsistencia.objects.filter(fecha=date(2025, 2, 17))
print(f"Registros para feriado: {registros.count()}")  # Será 0

# 4. Verificar que se suma en horas_feriado
from apps.reloj_fichador.utils import horas_feriado_por_operario
horas = horas_feriado_por_operario(operario, 2, 2025)
print(f"Horas de feriado en febrero: {horas}")  # Sumará 8 horas
```

---

## 📋 CASOS PRÁCTICOS

### Caso 1: Operario en feriado nacional aceptado

**Fecha:** 17 de febrero de 2025 (Carnaval - feriado movible)
**Estado:** Aceptado en CalendarioLaboral

**Resultado:**
- ❌ No hay RegistroAsistencia para ese día
- ✅ Se suma 8 horas a horas_feriado (es martes)
- ✅ En nómina: cobra como si hubiese trabajado
- ❌ No aparece como "ausente"
- ✅ Afecta cálculo de "días disponibles para trabajo"

---

### Caso 2: Operario en sábado de feriado aceptado

**Fecha:** 15 de noviembre de 2025 (Sábado)
**Estado:** Aceptado en CalendarioLaboral

**Resultado:**
- ❌ No hay RegistroAsistencia para ese día
- ✅ Se suma 4 horas a horas_feriado (es sábado = medio día)
- ✅ En nómina: cobra 4 horas
- ❌ No aparece como "ausente"
- ✅ GrupoSabado no se consulta (es no-laboral de todos modos)

---

### Caso 3: Feriado RECHAZADO

**Fecha:** 17 de febrero de 2025
**Estado:** Rechazado (no entra en CalendarioLaboral)

**Resultado:**
- ✅ SÍ se crea RegistroAsistencia (es día laboral)
- ❌ No se suma en horas_feriado
- ✅ Si no hay registro de entrada: marcado como ausente
- ❌ Si hay entrada: marcado como presente
- ✅ Puede ser justificado si hay licencia

---

## 🎯 CONCLUSIÓN

**Cuando se acepta un feriado:**

1. ✅ **Sí se suma como horas_feriado en Horas_totales**
   - 8 horas para lunes-viernes
   - 4 horas para sábados
   - Función: `horas_feriado_por_operario()`

2. ❌ **NO crea RegistroAsistencia como "ausencia"**
   - No hay registro que crear
   - No hay ausencia que justificar
   - Función `generar_registros_asistencia()` valida con `es_dia_laboral()`

3. 🟡 **No aplica el concepto de "justificado"**
   - El feriado PREVIENE el registro
   - No es una ausencia justificada
   - Es un día que directamente no se labora

---

## 🔗 REFERENCIAS DE CÓDIGO

| Función | Ubicación | Responsabilidad |
|---------|-----------|-----------------|
| `SugerenciaFeriado.aceptar()` | models.py:1131 | Crear CalendarioLaboral |
| `es_dia_laboral()` | utils.py:597 | Validar si es laboral |
| `generar_registros_asistencia()` | tasks.py:10 | Crear registros (evita feriados) |
| `horas_feriado_por_operario()` | utils.py:778 | Calcular horas perdidas |
| `CalendarioLaboral.es_no_laboral()` | models.py:910 | Verificar si es no-laboral |
| `RegistroAsistencia.verificar_asistencia()` | models.py:1074 | Verificar asistencia |

---

**Status:** ✅ ANÁLISIS COMPLETADO
**Verificado:** 23 de Octubre de 2025

