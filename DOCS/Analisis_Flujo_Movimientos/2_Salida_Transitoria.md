# Análisis Técnico: Movimiento SALIDA TRANSITORIA

**Tipo de Movimiento:** `salida_transitoria`
**Secuencia:** #2 en la jornada laboral
**Atajo de Teclado:** `Z`
**Fecha:** 18 de Octubre de 2025

---

## 1. Definición y Propósito

### 1.1. ¿Qué es una Salida Transitoria?

La **Salida Transitoria** es un movimiento que registra cuando un operario **abandona temporalmente** su puesto de trabajo durante la jornada laboral, con la intención de regresar antes de finalizar el día.

### 1.2. Casos de Uso Comunes

- **Pausas para almuerzo/cena** (no contabilizan como tiempo trabajado)
- **Salidas por gestiones personales breves** (banco, trámites)
- **Descansos prolongados** fuera del establecimiento
- **Salidas por motivos médicos temporales** (retorna el mismo día)

### 1.3. Diferencia con Salida Final

| Característica | Salida Transitoria | Salida Final |
|----------------|-------------------|--------------|
| Regreso esperado | ✅ Sí, mismo día | ❌ No (fin de jornada) |
| Movimiento siguiente | Entrada Transitoria | Entrada (día siguiente) |
| Contabiliza horas | ❌ No (pausa) | ✅ Sí (cierre de ciclo) |
| Requiere par | ✅ Sí (E.Transitoria) | ⚠️ No obligatorio |

---

## 2. Posición en la Secuencia de Jornada

### 2.1. Secuencia Válida Completa

```
┌─────────────┐
│  1. ENTRADA │
└──────┬──────┘
       │
       ▼
┌──────────────────────┐
│ 2. SALIDA TRANSITORIA│  ◄─── ESTE DOCUMENTO
└──────┬───────────────┘
       │
       ▼
┌───────────────────────┐
│ 3. ENTRADA TRANSITORIA│
└──────┬────────────────┘
       │
       ▼
┌─────────────┐
│  4. SALIDA  │
└─────────────┘
```

### 2.2. Movimiento Anterior Obligatorio

**Debe existir:** `ENTRADA` (movimiento #1)

**Validación aplicada:**
```python
# models.py líneas 509-519
ultima_entrada = RegistroDiario.objects.filter(
    operario=self.operario,
    tipo_movimiento='entrada',
    valido=True,
    hora_fichada__lt=self.hora_fichada
).order_by('-id_registro').first()

if not ultima_entrada:
    raise ValidationError(
        "Atención: Los movimientos transitorios solo son válidos después de una ENTRADA."
    )
```

### 2.3. Movimiento Siguiente Esperado

**Debe continuar con:** `ENTRADA TRANSITORIA` (movimiento #3)

**Validación de transición:**
```python
# models.py líneas 553-556
transiciones_validas = {
    'salida_transitoria': ['entrada_transitoria'],
    # Solo permite entrada_transitoria después
}
```

---

## 3. Flujo Técnico Específico

### FASE 1: Interacción del Usuario

#### 3.1.1. Selección del Movimiento
**Interfaz:** `templates/reloj_fichador/base.html`

```html
<!-- Línea 33-34 -->
<button class="menu-button" onclick="setTipoMovimiento('salida_transitoria')">
    Salida Transitoria (Z)
</button>
```

**Atajo de teclado:**
```javascript
// Líneas 160-161
case 'Z':
    setTipoMovimiento('salida_transitoria');
    break;
```

**Acción del botón:**
```javascript
// Línea 134
document.getElementById('tipo_movimiento').value = 'salida_transitoria';

// Línea 135
document.getElementById('movimientoForm').action =
    "/registrar_movimiento/salida_transitoria/";
```

#### 3.1.2. Ingreso de DNI y Envío
```javascript
// Evento submit (líneas 187-234)
fetch('/registrar_movimiento/salida_transitoria/', {
    method: 'POST',
    headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: formData  // {dni: "12345678", tipo_movimiento: "salida_transitoria"}
})
```

---

### FASE 2: Validaciones Backend

#### 3.2.1. Vista Principal
**Archivo:** `apps/reloj_fichador/views.py` (líneas 25-103)

```python
@csrf_exempt
@require_POST
def registrar_movimiento_tipo(request, tipo_movimiento):
    # tipo_movimiento = 'salida_transitoria'

    dni = request.POST.get('dni')
    operario = Operario.objects.get(dni=dni)  # Puede lanzar DoesNotExist

    argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
    hora_actual = timezone.now().astimezone(argentina_tz)

    # Crear instancia para validación
    registro = RegistroDiario(
        operario=operario,
        tipo_movimiento='salida_transitoria',
        hora_fichada=hora_actual,
    )

    registro.full_clean()  # ← Ejecuta validaciones específicas
    registro.save()
```

#### 3.2.2. Validaciones del Modelo
**Archivo:** `apps/reloj_fichador/models.py` (método `clean()`)

**Validación 1: Existencia de ENTRADA previa**
```python
# Líneas 507-519
if self.tipo_movimiento in ['salida_transitoria', 'entrada_transitoria']:
    ultima_entrada = RegistroDiario.objects.filter(
        operario=self.operario,
        tipo_movimiento='entrada',
        valido=True,
        hora_fichada__lt=self.hora_fichada
    ).order_by('-id_registro').first()

    if not ultima_entrada:
        raise ValidationError({
            'tipo_movimiento': [
                "<span style='color: orange;'>Los movimientos transitorios "
                "solo son válidos después de una ENTRADA.</span>"
            ]
        })
```

**Validación 2: Transición desde movimiento anterior válido**
```python
# Líneas 522-556
# Obtener última ENTRADA
ultima_entrada = RegistroDiario.objects.filter(
    operario=self.operario,
    tipo_movimiento='entrada',
    hora_fichada__lt=self.hora_fichada,
    valido=True
).order_by('-id_registro').first()

# Obtener todos los movimientos desde esa ENTRADA
registros_jornada = RegistroDiario.objects.filter(
    operario=self.operario,
    id_registro__gt=ultima_entrada.id_registro,
    valido=True
).exclude(pk=self.pk).order_by('id_registro')

movimientos_jornada = ['entrada'] + list(
    registros_jornada.values_list('tipo_movimiento', flat=True)
)

# El último movimiento debe ser 'entrada' para permitir 'salida_transitoria'
last_movement = movimientos_jornada[-1]

transiciones_validas = {
    'entrada': ['salida', 'salida_transitoria'],  # ← Permitido
}

if last_movement not in transiciones_validas.get('entrada', []):
    raise ValidationError("Secuencia de movimientos inválida")
```

**Resultado de validaciones:**
```
✅ VÁLIDO si:
   - Existe ENTRADA previa en la jornada
   - No hay otro movimiento entre ENTRADA y esta SALIDA_TRANSITORIA
   - Hora fichada > hora de ENTRADA

❌ INVÁLIDO si:
   - No existe ENTRADA previa
   - Ya existe una SALIDA_TRANSITORIA sin su correspondiente ENTRADA_TRANSITORIA
   - Hora fichada < hora de última ENTRADA
```

---

### FASE 3: Persistencia en Base de Datos

#### 3.3.1. Registro en Tabla RegistroDiario

**Tabla:** `reloj_fichador_registrodiario`

```sql
INSERT INTO reloj_fichador_registrodiario (
    operario_id,
    hora_fichada,
    tipo_movimiento,
    origen_fichada,
    inconsistencia,
    valido
) VALUES (
    245,                                    -- ID del operario
    '2025-10-18 12:30:00-03:00',           -- Hora exacta con timezone
    'salida_transitoria',                   -- Tipo de movimiento
    'Auto',                                 -- Origen
    FALSE,                                  -- Sin inconsistencia
    TRUE                                    -- Válido
);
```

#### 3.3.2. Campos Específicos de Salida Transitoria

| Campo | Valor | Observación |
|-------|-------|-------------|
| `tipo_movimiento` | `'salida_transitoria'` | Identificador clave |
| `hora_fichada` | Hora exacta sin redondeo | No se aplica redondeo a salidas transitorias |
| `dif_entrada_salida` | `NULL` | No se calcula en transitorias |
| `dif_entrada_salida2` | `NULL` | Solo se calcula en SALIDA final |
| `descripcion_inconsistencia` | `NULL` | Solo si hay override |

---

### FASE 4: Triggers y Cálculos Automáticos

#### 4.4.1. Signal: post_save

**Archivo:** `apps/reloj_fichador/signals.py`

```python
@receiver(post_save, sender=RegistroDiario)
def actualizar_horas_despues_de_guardar(sender, instance, **kwargs):
    # instance.tipo_movimiento = 'salida_transitoria'

    operario = instance.operario
    fecha_logica = RegistroDiario.calcular_fecha_logica(
        instance.hora_fichada,
        instance.tipo_movimiento
    )

    # ⚠️ IMPORTANTE: Salida transitoria NO cierra ciclo de horas
    # Solo la SALIDA final (#4) dispara cálculo completo

    # NO se ejecuta:
    # - Horas_trabajadas.calcular_horas_trabajadas() ← Espera SALIDA final
    # - Horas_extras.calcular_horas_extras() ← Espera SALIDA final

    # SÍ se ejecuta:
    # - RegistroAsistencia.verificar_asistencia() ← Marca presencia
```

#### 4.4.2. Actualización de Asistencia

```python
@receiver(post_save, sender=RegistroDiario)
def actualizar_asistencia(sender, instance, created, **kwargs):
    if created:
        fecha_actual = instance.hora_fichada.date()
        operario = instance.operario

        registro_asistencia, _ = RegistroAsistencia.objects.get_or_create(
            operario=operario,
            fecha=fecha_actual
        )

        # Verifica si hay al menos una ENTRADA válida
        # La SALIDA_TRANSITORIA refuerza que el operario estuvo presente
        registro_asistencia.verificar_asistencia()
        # → estado = 'presente'
```

---

## 4. Cálculo de Horas Trabajadas

### 4.1. ¿Se Contabiliza la Salida Transitoria?

**Respuesta: NO directamente**

La salida transitoria **NO cierra un ciclo de horas trabajadas**. El sistema espera el movimiento completo:

```
ENTRADA (08:00)
    ↓
    [CICLO 1: NO CERRADO AÚN]
    ↓
SALIDA_TRANSITORIA (12:30) ← Solo marca pausa, no calcula horas
    ↓
    [PAUSA - NO CONTABILIZA]
    ↓
ENTRADA_TRANSITORIA (13:45) ← Retoma, no calcula horas
    ↓
    [CICLO 1: AÚN NO CERRADO]
    ↓
SALIDA (17:30) ← AQUÍ se calcula TODO el ciclo
```

### 4.2. Cálculo Real al Finalizar Jornada

**Cuando se registra la SALIDA final:**

```python
# models.py - Horas_trabajadas.calcular_horas_trabajadas()

# 1. Buscar ENTRADA inicial
entrada = RegistroDiario.objects.get(tipo_movimiento='entrada', ...)
# hora_entrada = 08:00

# 2. Buscar SALIDA_TRANSITORIA
salida_trans = RegistroDiario.objects.get(tipo_movimiento='salida_transitoria', ...)
# hora_salida_trans = 12:30

# 3. Buscar ENTRADA_TRANSITORIA
entrada_trans = RegistroDiario.objects.get(tipo_movimiento='entrada_transitoria', ...)
# hora_entrada_trans = 13:45

# 4. Buscar SALIDA final
salida = RegistroDiario.objects.get(tipo_movimiento='salida', ...)
# hora_salida = 17:30

# CÁLCULO:
ciclo_1 = salida_trans - entrada  # 12:30 - 08:00 = 4h 30min
ciclo_2 = salida - entrada_trans  # 17:30 - 13:45 = 3h 45min

total_trabajado = ciclo_1 + ciclo_2  # 4h 30min + 3h 45min = 8h 15min

# La pausa (13:45 - 12:30 = 1h 15min) NO se contabiliza
```

### 4.3. Aplicación de Redondeos

**Salida Transitoria:** ⚠️ **NO se redondea**

A diferencia de la SALIDA final que se redondea hacia abajo a la hora, las salidas transitorias usan la hora exacta para cálculos precisos del tiempo de pausa.

```python
# models.py - redondear_salida() NO se aplica a transitorias

if tipo_movimiento == 'salida_transitoria':
    # Usar hora exacta sin redondeo
    return hora_fichada  # 12:30:45 → 12:30:45
```

---

## 5. Casos de Uso Específicos

### Caso 1: Jornada con Almuerzo

```
Operario: LÓPEZ, CARLOS (DNI: 34567890)
Fecha: 18/10/2025

08:05 → ENTRADA
    Redondeada a: 08:00

12:30 → SALIDA TRANSITORIA ◄── Inicio de almuerzo
    Sin redondeo: 12:30

13:45 → ENTRADA TRANSITORIA ◄── Fin de almuerzo
    Sin redondeo: 13:45

17:15 → SALIDA
    Sin redondeo: 17:15

Cálculos (ejecutados al registrar SALIDA):
- Ciclo 1: 12:30 - 08:00 = 4h 30min
- Ciclo 2: 17:15 - 13:45 = 3h 30min
- Total trabajado: 8h 0min
- Tiempo de pausa: 13:45 - 12:30 = 1h 15min (NO contabilizado)

Resultado BD:
- RegistroDiario: 4 registros
- Horas_trabajadas: horas_normales=8h, horas_nocturnas=0h
- Horas_extras: horas_extras_50=0h (no excede 8h)
```

### Caso 2: Doble Pausa (Almuerzo + Gestión)

```
Operario: MARTÍNEZ, ANA (DNI: 45678901)
Fecha: 18/10/2025

08:15 → ENTRADA

12:00 → SALIDA TRANSITORIA (almuerzo)
13:30 → ENTRADA TRANSITORIA

15:00 → SALIDA TRANSITORIA (gestión bancaria) ❌ INCONSISTENCIA
```

**Validación aplicada:**
```
last_movement = 'entrada_transitoria'

transiciones_validas = {
    'entrada_transitoria': ['salida'],  # Solo permite SALIDA final
}

'salida_transitoria' NOT IN ['salida']
→ raise ValidationError("Secuencia inválida")
```

**Mensaje al usuario:**
```
"Inconsistencia: Su último movimiento fue Entrada Transitoria 13:30:00.
¿Desea fichar de todos modos?"
```

**Si acepta override:**
- Se guarda con `inconsistencia=True`
- El cálculo de horas puede ser incorrecto
- Requiere corrección manual en admin

### Caso 3: Salida Transitoria sin Retorno

```
Operario: PÉREZ, JUAN (DNI: 12345678)
Fecha: 18/10/2025

08:00 → ENTRADA
12:30 → SALIDA TRANSITORIA
[No registra ENTRADA_TRANSITORIA]
[No registra SALIDA]

Fin del día: ¿Qué sucede?
```

**Comportamiento del sistema:**

1. **Al finalizar el día (00:00):**
   - RegistroAsistencia marca: `estado='presente'` (hay ENTRADA)
   - Pero: `inconsistencia_asistencia=True` (secuencia incompleta)

2. **Cálculo de horas:**
   - `Horas_trabajadas`: **0 horas** (no hay par ENTRADA→SALIDA completo)
   - `Horas_extras`: **0 horas**

3. **Reportes del admin:**
   - Aparece con advertencia: "Jornada incompleta"
   - Operario: PRESENTE pero sin horas calculadas
   - Requiere intervención manual

4. **Corrección en admin:**
   - Supervisor puede agregar ENTRADA_TRANSITORIA y SALIDA retroactivas
   - Al guardar, signals recalculan automáticamente las horas

---

## 6. Inconsistencias Comunes

### 6.1. Salida Transitoria sin Entrada Previa

**Escenario:**
```
[Sin registros previos]
12:30 → SALIDA TRANSITORIA ❌
```

**Validación:**
```python
if not ultima_entrada:
    raise ValidationError(
        "Los movimientos transitorios solo son válidos después de una ENTRADA."
    )
```

**Mensaje al usuario:**
```
"Atención: Los movimientos transitorios solo son válidos después de una ENTRADA."
```

### 6.2. Doble Salida Transitoria

**Escenario:**
```
08:00 → ENTRADA
12:30 → SALIDA TRANSITORIA
14:00 → SALIDA TRANSITORIA ❌ (sin ENTRADA_TRANSITORIA intermedia)
```

**Validación:**
```python
last_movement = 'salida_transitoria'

transiciones_validas = {
    'salida_transitoria': ['entrada_transitoria'],
}

'salida_transitoria' NOT IN ['entrada_transitoria']
→ Inconsistencia
```

### 6.3. Salida Transitoria después de Salida Final

**Escenario:**
```
08:00 → ENTRADA
17:30 → SALIDA (final)
18:00 → SALIDA TRANSITORIA ❌ (jornada ya cerrada)
```

**Validación:**
```python
# Se considera inicio de nueva jornada
# Pero requiere ENTRADA previa

ultima_entrada antes de 18:00 = 08:00 (del mismo día)
ultimo_movimiento = 'salida'

# Se permite ENTRADA después de SALIDA
# Pero NO SALIDA_TRANSITORIA después de SALIDA

→ Inconsistencia detectada
```

---

## 7. Diferencias con Otros Movimientos

### 7.1. vs. ENTRADA

| Aspecto | ENTRADA | SALIDA TRANSITORIA |
|---------|---------|-------------------|
| Redondeo | ✅ Sí (15 min) | ❌ No (hora exacta) |
| Movimiento previo | SALIDA (o ninguno) | ENTRADA obligatoria |
| Cierra ciclo | ❌ No (inicia) | ❌ No (pausa) |
| Siguiente permitido | SALIDA o SAL_TRANS | ENTRADA_TRANS únicamente |

### 7.2. vs. SALIDA FINAL

| Aspecto | SALIDA TRANSITORIA | SALIDA FINAL |
|---------|-------------------|--------------|
| Redondeo | ❌ No | ✅ Sí (hacia abajo a hora) |
| Retorno esperado | ✅ Sí (ENT_TRANS) | ❌ No (fin de jornada) |
| Cálculo de horas | ❌ No (espera SALIDA) | ✅ Sí (inmediato) |
| Triggers signals | Solo asistencia | Todos (horas, extras, totales) |
| Siguiente movimiento | ENTRADA_TRANS | ENTRADA (día siguiente) |

### 7.3. vs. ENTRADA TRANSITORIA

| Aspecto | SALIDA TRANSITORIA | ENTRADA TRANSITORIA |
|---------|-------------------|---------------------|
| Secuencia | #2 | #3 |
| Inicia/Termina pausa | ✅ Inicia | ✅ Termina |
| Movimiento previo | ENTRADA | SALIDA_TRANSITORIA |
| Siguiente movimiento | ENTRADA_TRANSITORIA | SALIDA |

---

## 8. Respuestas del Sistema

### 8.1. Respuesta Exitosa

**JSON Response:**
```json
{
    "success": true,
    "message": "REGISTRO EXITOSO: LÓPEZ, CARLOS - Salida Transitoria - 18/10/2025 12:30:15"
}
```

**Comportamiento en UI:**
```javascript
// base.html líneas 212-215
mostrarMensaje('success', data.message);
// Fondo verde, duración 30 segundos
dniInput.value = '';  // Limpiar DNI
dniInput.focus();     // Preparar para siguiente fichado
```

### 8.2. Respuesta con Inconsistencia

**JSON Response:**
```json
{
    "success": false,
    "inconsistencia": true,
    "descripcion_inconsistencia": "Atención: Los movimientos transitorios solo son válidos después de una ENTRADA.",
    "tipo_movimiento": "salida_transitoria"
}
```

**Modal mostrado:**
```html
<div id="inconsistency-modal">
    <p>Atención: Los movimientos transitorios solo son válidos después de una ENTRADA.</p>
    <p>¿Desea fichar de todos modos?</p>
    <button id="accept-modal-button">Aceptar</button>
    <button id="cancel-modal-button">Cancelar</button>
</div>
```

---

## 9. Logging y Auditoría

### 9.1. Logs Generados

```python
# views.py

# Al buscar operario
logger.info(f"Operario encontrado: {operario.nombre} {operario.apellido}")

# Al validar exitosamente
logger.info(f"Registro creado exitosamente: LÓPEZ, CARLOS - Salida Transitoria - 12:30:15")

# Al detectar inconsistencia
logger.warning(f"Inconsistencia detectada: Los movimientos transitorios requieren ENTRADA previa")

# Al aceptar override
logger.info(f"Registro creado con inconsistencia: LÓPEZ, CARLOS - Salida Transitoria")
```

### 9.2. Historial de Cambios

**Tabla:** `reloj_fichador_historicalregistrodiario`

```sql
SELECT
    history_id,
    history_type,  -- '+' (creado), '~' (modificado), '-' (eliminado)
    history_date,
    history_user_id,
    tipo_movimiento,
    hora_fichada,
    inconsistencia
FROM reloj_fichador_historicalregistrodiario
WHERE operario_id = 245
  AND DATE(hora_fichada) = '2025-10-18'
  AND tipo_movimiento = 'salida_transitoria'
ORDER BY history_date DESC;
```

---

## 10. Configuración y Personalización

### 10.1. Configuraciones Aplicables

**NO aplican a Salida Transitoria:**
- `ConfiguracionRedondeo` (solo para ENTRADA)
- `ConfiguracionRedondeoSalida` (solo para SALIDA final)

**SÍ aplican:**
- Zona horaria: `America/Argentina/Buenos_Aires`
- Cálculo de fecha lógica (turnos nocturnos)
- Validaciones de secuencia

### 10.2. Personalización de Validaciones

Para modificar las transiciones permitidas:

```python
# models.py líneas 553-556
transiciones_validas = {
    'entrada': ['salida', 'salida_transitoria'],
    'salida_transitoria': ['entrada_transitoria'],  # ← Modificar aquí
    # Por ejemplo, permitir también SALIDA directa:
    # 'salida_transitoria': ['entrada_transitoria', 'salida'],
}
```

---

## 11. Mejoras Sugeridas

### 11.1. Funcionalidad

1. **Límite de tiempo de pausa:**
   - Alertar si pausa > 2 horas
   - Validar que ENTRADA_TRANSITORIA ocurra dentro del mismo día

2. **Pausas múltiples:**
   - Actualmente solo permite 1 pausa (sal_trans → ent_trans)
   - Considerar permitir múltiples pausas en jornadas extensas

3. **Estadísticas de pausas:**
   - Dashboard mostrando tiempo promedio de pausas por operario
   - Identificar patrones (ej: almuerzo siempre 12:00-13:00)

### 11.2. UX/UI

1. **Indicador visual:**
   - Mostrar estado actual del operario: "En pausa" después de SALIDA_TRANSITORIA
   - Color diferente en el botón si ya hay salida transitoria activa

2. **Confirmación automática:**
   - Si hora actual > 13:00 y hay SALIDA_TRANSITORIA sin retorno
   - Sugerir registrar ENTRADA_TRANSITORIA

3. **Historial inmediato:**
   - Después de fichar SALIDA_TRANSITORIA, mostrar:
     ```
     "Inicio de pausa: 12:30"
     "Su jornada comenzó a las 08:00"
     "Tiempo trabajado antes de pausa: 4h 30min"
     ```

---

## 12. Preguntas Frecuentes

### ¿Qué pasa si olvido registrar la entrada transitoria?

El sistema marca la jornada como incompleta. Las horas trabajadas **no se calculan** hasta que se complete la secuencia. Un supervisor debe corregir manualmente en el admin.

### ¿Puedo tener múltiples salidas transitorias en un día?

No directamente. La secuencia solo permite:
```
ENTRADA → SAL_TRANS → ENT_TRANS → SALIDA
```

Para múltiples pausas, se requeriría modificar las validaciones.

### ¿Se redondea la hora de salida transitoria?

No, se usa la hora exacta para calcular con precisión el tiempo de pausa.

### ¿Cuenta como asistencia si solo registro entrada y salida transitoria?

Sí, el sistema marca como **presente** porque hay una ENTRADA válida, pero las horas trabajadas serán **0** si no se completa la jornada.

---

## 13. Referencias Técnicas

### Archivos Involucrados

| Archivo | Líneas Relevantes | Descripción |
|---------|------------------|-------------|
| `templates/reloj_fichador/base.html` | 33-34, 160-161 | Botón y atajo de teclado |
| `apps/reloj_fichador/views.py` | 25-103 | Endpoint de registro |
| `apps/reloj_fichador/models.py` | 507-556 | Validaciones específicas |
| `apps/reloj_fichador/signals.py` | 13-26, 40-75 | Triggers automáticos |

### Modelos de Base de Datos

- `reloj_fichador_registrodiario`: Tabla principal
- `reloj_fichador_historicalregistrodiario`: Auditoría
- `reloj_fichador_registroasistencia`: Control de asistencia
- `reloj_fichador_horas_trabajadas`: Cálculo de horas (post-SALIDA)

---

**Documento generado por:** Claude Code
**Fecha:** 18 de Octubre de 2025
**Versión:** 1.0
**Próxima revisión:** Al modificar validaciones de movimientos transitorios
