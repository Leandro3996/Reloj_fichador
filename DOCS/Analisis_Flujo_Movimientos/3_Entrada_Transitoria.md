# Análisis Técnico: Movimiento ENTRADA TRANSITORIA

**Tipo de Movimiento:** `entrada_transitoria`
**Secuencia:** #3 en la jornada laboral
**Atajo de Teclado:** `M`
**Fecha:** 18 de Octubre de 2025

---

## 1. Definición y Propósito

### 1.1. ¿Qué es una Entrada Transitoria?

La **Entrada Transitoria** es un movimiento que registra cuando un operario **regresa a su puesto de trabajo** después de haber salido temporalmente durante la jornada laboral.

### 1.2. Casos de Uso Comunes

- **Retorno de pausa para almuerzo/cena**
- **Regreso de gestiones personales breves**
- **Fin de descanso prolongado**
- **Reintegro después de atención médica temporal**

### 1.3. Relación con Salida Transitoria

| Característica | Salida Transitoria | Entrada Transitoria |
|----------------|-------------------|---------------------|
| Función | Inicio de pausa | Fin de pausa |
| Requiere movimiento previo | ENTRADA | SALIDA TRANSITORIA |
| Siguiente movimiento | ENTRADA TRANSITORIA | SALIDA (final) |
| Forma par | ✅ Sí, con ENT_TRANS | ✅ Sí, con SAL_TRANS |
| Contabiliza horas | ❌ No (marca pausa) | ❌ No (retoma trabajo) |

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
│ 2. SALIDA TRANSITORIA│
└──────┬───────────────┘
       │
       ▼
┌───────────────────────┐
│ 3. ENTRADA TRANSITORIA│  ◄─── ESTE DOCUMENTO
└──────┬────────────────┘
       │
       ▼
┌─────────────┐
│  4. SALIDA  │
└─────────────┘
```

### 2.2. Movimiento Anterior Obligatorio

**Debe existir:** `SALIDA TRANSITORIA` (movimiento #2)

**Validación aplicada:**
```python
# models.py líneas 553-556
transiciones_validas = {
    'salida_transitoria': ['entrada_transitoria'],  # Solo permite ENT_TRANS
}

# Si último movimiento != 'salida_transitoria'
# → raise ValidationError("Secuencia inválida")
```

**Además, debe existir ENTRADA inicial:**
```python
# models.py líneas 507-519
# Validación heredada de movimientos transitorios
ultima_entrada = RegistroDiario.objects.filter(
    operario=self.operario,
    tipo_movimiento='entrada',
    valido=True,
    hora_fichada__lt=self.hora_fichada
).order_by('-id_registro').first()

if not ultima_entrada:
    raise ValidationError(
        "Los movimientos transitorios solo son válidos después de una ENTRADA."
    )
```

### 2.3. Movimiento Siguiente Esperado

**Debe continuar con:** `SALIDA` (movimiento #4 - final)

**Validación de transición:**
```python
# models.py líneas 553-556
transiciones_validas = {
    'entrada_transitoria': ['salida'],  # Solo permite SALIDA final
}
```

---

## 3. Flujo Técnico Específico

### FASE 1: Interacción del Usuario

#### 3.1.1. Selección del Movimiento
**Interfaz:** `templates/reloj_fichador/base.html`

```html
<!-- Línea 35-36 -->
<button class="menu-button" onclick="setTipoMovimiento('entrada_transitoria')">
    Entrada Transitoria (M)
</button>
```

**Atajo de teclado:**
```javascript
// Líneas 163-164
case 'M':
    setTipoMovimiento('entrada_transitoria');
    break;
```

**Acción del botón:**
```javascript
// Línea 134
document.getElementById('tipo_movimiento').value = 'entrada_transitoria';

// Línea 135
document.getElementById('movimientoForm').action =
    "/registrar_movimiento/entrada_transitoria/";
```

#### 3.1.2. Contexto de Uso Típico

**Escenario esperado:**
```
11:45 → Operario presiona "Z" (Salida Transitoria)
        Sale a almorzar

[40-90 minutos después]

13:15 → Operario regresa y presiona "M" (Entrada Transitoria) ◄── Este momento
        Ingresa DNI: 12345678
        Sistema registra retorno
```

---

### FASE 2: Validaciones Backend

#### 3.2.1. Vista Principal
**Archivo:** `apps/reloj_fichador/views.py` (líneas 25-103)

```python
@csrf_exempt
@require_POST
def registrar_movimiento_tipo(request, tipo_movimiento):
    # tipo_movimiento = 'entrada_transitoria'

    dni = request.POST.get('dni')
    operario = Operario.objects.get(dni=dni)

    argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
    hora_actual = timezone.now().astimezone(argentina_tz)

    # Crear instancia para validación
    registro = RegistroDiario(
        operario=operario,
        tipo_movimiento='entrada_transitoria',
        hora_fichada=hora_actual,
    )

    registro.full_clean()  # ← Ejecuta validaciones específicas
    registro.save()
```

#### 3.2.2. Validaciones del Modelo
**Archivo:** `apps/reloj_fichador/models.py` (método `clean()`)

**Validación 1: Existencia de ENTRADA inicial**
```python
# Líneas 507-519
if self.tipo_movimiento in ['salida_transitoria', 'entrada_transitoria']:
    # Ambas transitorias requieren ENTRADA previa

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

**Validación 2: Secuencia desde SALIDA_TRANSITORIA**
```python
# Líneas 522-556
# Obtener última ENTRADA
ultima_entrada = RegistroDiario.objects.filter(
    operario=self.operario,
    tipo_movimiento='entrada',
    hora_fichada__lt=self.hora_fichada,
    valido=True
).order_by('-id_registro').first()

# Obtener movimientos desde esa ENTRADA
registros_jornada = RegistroDiario.objects.filter(
    operario=self.operario,
    id_registro__gt=ultima_entrada.id_registro,
    valido=True
).exclude(pk=self.pk).order_by('id_registro')

movimientos_jornada = ['entrada'] + list(
    registros_jornada.values_list('tipo_movimiento', flat=True)
)

# Ejemplo de movimientos_jornada:
# ['entrada', 'salida_transitoria']

last_movement = movimientos_jornada[-1]  # 'salida_transitoria'

# Validar transición
transiciones_validas = {
    'salida_transitoria': ['entrada_transitoria'],  # ← Debe coincidir
}

if self.tipo_movimiento not in transiciones_validas.get(last_movement, []):
    raise ValidationError({
        'tipo_movimiento': [
            f"Inconsistencia: Su último movimiento fue {last_movement}. "
            f"No puede registrar {self.tipo_movimiento}."
        ]
    })
```

**Validación 3: Orden cronológico**
```python
# Líneas 489-491 (advertencia, no bloqueante)
if self.hora_fichada <= ultimo_valido.hora_fichada:
    logger.warning(
        f"Advertencia: Entrada transitoria ({self.hora_fichada}) "
        f"<= última salida transitoria ({ultimo_valido.hora_fichada})"
    )
    # No se agrega a inconsistencias, solo log
```

**Resultado de validaciones:**
```
✅ VÁLIDO si:
   - Existe ENTRADA inicial en la jornada
   - Último movimiento = SALIDA_TRANSITORIA
   - Hora fichada > hora de SALIDA_TRANSITORIA
   - No hay otra ENTRADA_TRANSITORIA sin SALIDA posterior

❌ INVÁLIDO si:
   - No existe ENTRADA inicial
   - Último movimiento ≠ SALIDA_TRANSITORIA
   - Ya existe ENTRADA_TRANSITORIA sin SALIDA posterior
   - Hora fichada < hora de SALIDA_TRANSITORIA
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
    '2025-10-18 13:45:00-03:00',           -- Hora exacta con timezone
    'entrada_transitoria',                  -- Tipo de movimiento
    'Auto',                                 -- Origen
    FALSE,                                  -- Sin inconsistencia
    TRUE                                    -- Válido
);
```

#### 3.3.2. Campos Específicos de Entrada Transitoria

| Campo | Valor | Observación |
|-------|-------|-------------|
| `tipo_movimiento` | `'entrada_transitoria'` | Identificador clave |
| `hora_fichada` | Hora exacta sin redondeo | No se aplica redondeo |
| `dif_entrada_salida` | `NULL` | No se calcula en transitorias |
| `dif_entrada_salida2` | `NULL` | Solo en SALIDA final |
| `descripcion_inconsistencia` | `NULL` | Solo si hay override |

---

### FASE 4: Cálculo de Tiempo de Pausa

#### 4.4.1. Detección del Par Transitorio

Aunque la ENTRADA_TRANSITORIA no calcula horas trabajadas, sí permite calcular el **tiempo de pausa**:

```python
# Lógica conceptual (no implementada directamente, pero posible)

salida_trans = RegistroDiario.objects.filter(
    operario=operario,
    tipo_movimiento='salida_transitoria',
    hora_fichada__lt=entrada_trans.hora_fichada
).order_by('-hora_fichada').first()

tiempo_pausa = entrada_trans.hora_fichada - salida_trans.hora_fichada
# Ejemplo: 13:45 - 12:30 = 1h 15min
```

**Este tiempo NO se contabiliza como horas trabajadas.**

#### 4.4.2. Signal: post_save

**Archivo:** `apps/reloj_fichador/signals.py`

```python
@receiver(post_save, sender=RegistroDiario)
def actualizar_horas_despues_de_guardar(sender, instance, **kwargs):
    # instance.tipo_movimiento = 'entrada_transitoria'

    operario = instance.operario
    fecha_logica = RegistroDiario.calcular_fecha_logica(
        instance.hora_fichada,
        instance.tipo_movimiento
    )

    # ⚠️ IMPORTANTE: Entrada transitoria NO cierra ciclo
    # Solo marca fin de pausa y permite continuar jornada

    # NO se ejecuta:
    # - Horas_trabajadas.calcular_horas_trabajadas() ← Espera SALIDA final
    # - Horas_extras.calcular_horas_extras() ← Espera SALIDA final

    # SÍ se ejecuta:
    # - RegistroAsistencia.verificar_asistencia() ← Confirma presencia
```

#### 4.4.3. Actualización de Asistencia

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

        # Verifica si hay ENTRADA válida
        # La ENTRADA_TRANSITORIA refuerza estado='presente'
        registro_asistencia.verificar_asistencia()
        # → estado = 'presente'
```

---

## 4. Cálculo de Horas Trabajadas

### 4.1. Rol en el Cálculo Final

La ENTRADA_TRANSITORIA **marca el fin de una pausa** pero NO dispara cálculo de horas. El sistema espera la SALIDA final para calcular todo:

```
ENTRADA (08:00)
    ↓
    Ciclo 1 iniciado
    ↓
SALIDA_TRANSITORIA (12:30)
    ↓
    [Pausa iniciada - no contabiliza]
    ↓
ENTRADA_TRANSITORIA (13:45) ◄── Fin de pausa, NO calcula aún
    ↓
    Ciclo 1 retomado
    ↓
SALIDA (17:30) ◄── AQUÍ se calcula todo el día
```

### 4.2. Cálculo Completo al Registrar SALIDA

**Cuando finalmente se registra la SALIDA:**

```python
# models.py - Horas_trabajadas.calcular_horas_trabajadas()

# 1. Obtener todos los movimientos del día
registros = RegistroDiario.objects.filter(
    operario=operario,
    hora_fichada__date=fecha,
    valido=True
).order_by('hora_fichada')

# Ejemplo:
# - 08:00 ENTRADA
# - 12:30 SALIDA_TRANSITORIA
# - 13:45 ENTRADA_TRANSITORIA ◄── Este registro
# - 17:30 SALIDA

# 2. Agrupar en ciclos
ciclo_1_inicio = 08:00  # ENTRADA
ciclo_1_pausa = 12:30   # SALIDA_TRANSITORIA
ciclo_1_retorno = 13:45 # ENTRADA_TRANSITORIA
ciclo_1_fin = 17:30     # SALIDA

# 3. Calcular tiempo trabajado
trabajado_mañana = 12:30 - 08:00 = 4h 30min
trabajado_tarde = 17:30 - 13:45 = 3h 45min
total_trabajado = 4h 30min + 3h 45min = 8h 15min

# 4. Tiempo de pausa (NO contabilizado)
pausa = 13:45 - 12:30 = 1h 15min

# 5. Guardar en BD
Horas_trabajadas.objects.update_or_create(
    operario=operario,
    fecha=fecha,
    defaults={
        'horas_normales': timedelta(hours=8, minutes=15),
        'horas_nocturnas': timedelta(0),
    }
)
```

### 4.3. Redondeos Aplicados

**Entrada Transitoria:** ⚠️ **NO se redondea**

Se usa la hora exacta para calcular con precisión el tiempo de pausa:

```python
# NO se aplica redondear_entrada() a entrada_transitoria

hora_entrada_trans = 13:47:35
# Se usa tal cual: 13:47:35 (sin redondear a 13:45 o 14:00)
```

**Justificación:**
- Precisión en cálculo de pausas
- Equidad (no penalizar/beneficiar por segundos)
- Solo la ENTRADA inicial se redondea (15 min)

---

## 5. Casos de Uso Específicos

### Caso 1: Jornada Estándar con Almuerzo

```
Operario: LÓPEZ, CARLOS (DNI: 34567890)
Fecha: 18/10/2025

08:05 → ENTRADA
    Redondeada a: 08:00

12:30 → SALIDA TRANSITORIA
    Sin redondeo: 12:30 (inicio almuerzo)

13:45 → ENTRADA TRANSITORIA ◄── Retorno de almuerzo
    Sin redondeo: 13:45

17:15 → SALIDA
    Sin redondeo: 17:15

Cálculos (ejecutados al registrar SALIDA):
- Ciclo mañana: 12:30 - 08:00 = 4h 30min
- Ciclo tarde: 17:15 - 13:45 = 3h 30min
- Total trabajado: 8h 0min
- Tiempo de pausa: 1h 15min (NO contabilizado)

Resultado BD:
- RegistroDiario: 4 registros
- Horas_trabajadas: horas_normales=8h, horas_nocturnas=0h
- Horas_extras: horas_extras_50=0h
```

### Caso 2: Entrada Transitoria sin Salida Transitoria Previa

```
Operario: MARTÍNEZ, ANA (DNI: 45678901)
Fecha: 18/10/2025

08:15 → ENTRADA

13:45 → ENTRADA TRANSITORIA ❌ (sin SAL_TRANS previa)
```

**Validación aplicada:**
```python
# Movimientos de la jornada:
movimientos_jornada = ['entrada']  # Solo hay ENTRADA

last_movement = 'entrada'

transiciones_validas = {
    'entrada': ['salida', 'salida_transitoria'],  # NO incluye 'entrada_transitoria'
}

'entrada_transitoria' NOT IN ['salida', 'salida_transitoria']
→ raise ValidationError("Secuencia inválida")
```

**Mensaje al usuario:**
```
"Inconsistencia: Su último movimiento fue Entrada 08:15:00.
No puede registrar Entrada Transitoria directamente."
```

**Modal de override:**
```
¿Desea fichar de todos modos?
[Aceptar] [Cancelar]
```

**Si acepta:**
- Se guarda con `inconsistencia=True`
- `descripcion_inconsistencia = "Entrada transitoria sin salida transitoria previa"`
- Cálculo de horas puede ser incorrecto
- Requiere revisión en admin

### Caso 3: Doble Entrada Transitoria

```
Operario: PÉREZ, JUAN (DNI: 12345678)
Fecha: 18/10/2025

08:00 → ENTRADA
12:30 → SALIDA TRANSITORIA
13:45 → ENTRADA TRANSITORIA ✅
14:00 → ENTRADA TRANSITORIA ❌ (duplicada)
```

**Validación aplicada:**
```python
# Movimientos de la jornada:
movimientos_jornada = ['entrada', 'salida_transitoria', 'entrada_transitoria']

last_movement = 'entrada_transitoria'

transiciones_validas = {
    'entrada_transitoria': ['salida'],  # Solo permite SALIDA
}

'entrada_transitoria' NOT IN ['salida']
→ Inconsistencia detectada
```

**Mensaje:**
```
"Inconsistencia: Su último movimiento fue Entrada Transitoria 13:45:00.
Debe registrar Salida para finalizar la jornada."
```

### Caso 4: Entrada Transitoria antes de Salida Transitoria (orden invertido)

```
Operario: GÓMEZ, MARÍA (DNI: 23456789)
Fecha: 18/10/2025

08:00 → ENTRADA
12:30 → SALIDA TRANSITORIA (fichó, pero se olvidó)
12:32 → ENTRADA TRANSITORIA ❌ (registra antes de tiempo)
```

**Validación aplicada:**
```python
# Validación de hora (líneas 489-491)
ultimo_valido = RegistroDiario.objects.filter(...).first()
# ultimo_valido.hora_fichada = 12:30
# self.hora_fichada = 12:32

if self.hora_fichada <= ultimo_valido.hora_fichada:
    # 12:32 > 12:30 → No aplica esta validación

# Pero la secuencia ES válida:
last_movement = 'salida_transitoria'
transiciones_validas['salida_transitoria'] = ['entrada_transitoria']
# ✅ Permitido
```

**Resultado:** ✅ **Registro válido**
- Es una pausa muy corta (2 minutos)
- El sistema lo permite
- Supervisor puede revisar pausas sospechosamente cortas en reportes

---

## 6. Inconsistencias Comunes

### 6.1. Entrada Transitoria sin Salida Transitoria

**Escenario:**
```
08:00 → ENTRADA
13:00 → ENTRADA TRANSITORIA ❌
```

**Causa:** Operario olvidó registrar SALIDA_TRANSITORIA antes de salir a almorzar.

**Validación:**
```python
last_movement = 'entrada'
'entrada_transitoria' NOT IN transiciones_validas['entrada']
→ Inconsistencia
```

**Solución:**
- Usuario: Aceptar override y reportar a supervisor
- Supervisor: Corregir en admin agregando SALIDA_TRANSITORIA retroactiva

### 6.2. Entrada Transitoria después de Salida Final

**Escenario:**
```
08:00 → ENTRADA
12:30 → SALIDA TRANSITORIA
13:00 → SALIDA ❌ (registró SALIDA en lugar de ENTRADA_TRANSITORIA)
14:00 → ENTRADA TRANSITORIA ❌ (ahora intenta corregir)
```

**Validación:**
```python
last_movement = 'salida'  # Jornada ya cerrada

transiciones_validas = {
    'salida': [],  # No permite nada después (nueva jornada debe empezar con ENTRADA)
}

'entrada_transitoria' NOT IN []
→ Inconsistencia
```

**Mensaje:**
```
"Inconsistencia: Ya registró una Salida final.
Para continuar, debe registrar una nueva Entrada."
```

**Corrección necesaria:** Supervisor debe:
1. Eliminar la SALIDA incorrecta de las 13:00
2. Agregar ENTRADA_TRANSITORIA a las 13:00
3. Agregar SALIDA correcta al final de jornada

### 6.3. Entrada Transitoria sin Entrada Inicial

**Escenario:**
```
[Sin registros previos]
13:00 → ENTRADA TRANSITORIA ❌
```

**Validación:**
```python
# Líneas 509-519
ultima_entrada = RegistroDiario.objects.filter(
    tipo_movimiento='entrada',
    hora_fichada__lt=self.hora_fichada,
    ...
).first()

if not ultima_entrada:
    raise ValidationError(
        "Los movimientos transitorios solo son válidos después de una ENTRADA."
    )
```

**Mensaje:**
```
"Atención: Los movimientos transitorios solo son válidos después de una ENTRADA."
```

---

## 7. Diferencias con Otros Movimientos

### 7.1. vs. ENTRADA

| Aspecto | ENTRADA | ENTRADA TRANSITORIA |
|---------|---------|---------------------|
| Redondeo | ✅ Sí (15 min) | ❌ No (hora exacta) |
| Movimiento previo | SALIDA (o ninguno) | SALIDA_TRANSITORIA obligatoria |
| Inicia ciclo | ✅ Sí (ciclo completo) | ❌ No (retoma ciclo) |
| Siguiente permitido | SAL o SAL_TRANS | SALIDA únicamente |
| Secuencia | #1 | #3 |

### 7.2. vs. SALIDA TRANSITORIA

| Aspecto | SALIDA TRANSITORIA | ENTRADA TRANSITORIA |
|---------|-------------------|---------------------|
| Función | Inicio de pausa | Fin de pausa |
| Movimiento previo | ENTRADA | SALIDA_TRANSITORIA |
| Siguiente movimiento | ENTRADA_TRANSITORIA | SALIDA |
| Forma par | Sí (inicio) | Sí (cierre) |
| Secuencia | #2 | #3 |

### 7.3. vs. SALIDA FINAL

| Aspecto | ENTRADA TRANSITORIA | SALIDA FINAL |
|---------|---------------------|--------------|
| Redondeo | ❌ No | ✅ Sí (hacia abajo a hora) |
| Cierra jornada | ❌ No | ✅ Sí |
| Cálculo de horas | ❌ No (espera SALIDA) | ✅ Sí (inmediato) |
| Triggers signals | Solo asistencia | Todos (horas, extras, totales) |
| Siguiente movimiento | SALIDA | ENTRADA (día siguiente) |
| Secuencia | #3 | #4 |

---

## 8. Respuestas del Sistema

### 8.1. Respuesta Exitosa

**JSON Response:**
```json
{
    "success": true,
    "message": "REGISTRO EXITOSO: LÓPEZ, CARLOS - Entrada Transitoria - 18/10/2025 13:45:20"
}
```

**Comportamiento en UI:**
```javascript
// base.html líneas 212-215
mostrarMensaje('success', data.message);
// Mensaje verde con duración 30 segundos
dniInput.value = '';  // Limpiar campo DNI
dniInput.focus();     // Preparar para siguiente fichado
```

### 8.2. Respuesta con Inconsistencia

**JSON Response:**
```json
{
    "success": false,
    "inconsistencia": true,
    "descripcion_inconsistencia": "Inconsistencia: Su último movimiento fue Entrada 08:15:00. No puede registrar Entrada Transitoria sin una Salida Transitoria previa.",
    "tipo_movimiento": "entrada_transitoria"
}
```

**Modal mostrado:**
```html
<div id="inconsistency-modal">
    <p>Inconsistencia: Su último movimiento fue Entrada 08:15:00.
       No puede registrar Entrada Transitoria sin una Salida Transitoria previa.</p>
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

logger.info(
    f"Operario encontrado: {operario.nombre} {operario.apellido}"
)

logger.info(
    f"Registro creado exitosamente: LÓPEZ, CARLOS - "
    f"Entrada Transitoria - 13:45:20"
)

logger.warning(
    f"Inconsistencia detectada: Entrada transitoria sin salida "
    f"transitoria previa para operario {operario.dni}"
)

logger.info(
    f"Registro creado con inconsistencia: LÓPEZ, CARLOS - "
    f"Entrada Transitoria"
)
```

### 9.2. Consulta de Historial

**Ejemplo SQL:**
```sql
SELECT
    r.id_registro,
    r.tipo_movimiento,
    r.hora_fichada,
    r.inconsistencia,
    r.descripcion_inconsistencia
FROM reloj_fichador_registrodiario r
WHERE r.operario_id = 245
  AND DATE(r.hora_fichada) = '2025-10-18'
  AND r.valido = TRUE
ORDER BY r.hora_fichada;
```

**Resultado esperado:**
```
id | tipo_movimiento       | hora_fichada         | inconsistencia
---|----------------------|----------------------|---------------
1  | entrada              | 08:00:00             | FALSE
2  | salida_transitoria   | 12:30:00             | FALSE
3  | entrada_transitoria  | 13:45:00             | FALSE
4  | salida               | 17:30:00             | FALSE
```

---

## 10. Mejoras Sugeridas

### 10.1. Funcionalidad

1. **Límite de duración de pausa:**
   - Alertar si tiempo entre SAL_TRANS y ENT_TRANS > 2 horas
   - Configurar límites por área/horario

2. **Detección automática de olvidos:**
   - Si pasan > 90 min desde SAL_TRANS sin ENT_TRANS
   - Notificar a supervisor para verificación

3. **Estadísticas de pausas:**
   - Tiempo promedio de pausa por operario
   - Comparativa con promedio del área
   - Dashboard de cumplimiento de horarios de pausa

### 10.2. UX/UI

1. **Indicador de estado:**
   - Mostrar "En pausa desde las 12:30" al fichar ENT_TRANS
   - Tiempo transcurrido en pausa

2. **Sugerencias contextuales:**
   ```
   "Su última salida transitoria fue hace 1h 15min.
   Ahora está registrando su regreso."
   ```

3. **Resumen post-fichado:**
   ```
   ✅ Retorno registrado: 13:45
   Tiempo de pausa: 1h 15min
   Tiempo trabajado antes de pausa: 4h 30min
   Jornada actual: 4h 30min (pendiente de salida final)
   ```

### 10.3. Reportes y Analytics

1. **Informe de pausas:**
   - Duración promedio por día de la semana
   - Operarios con pausas fuera de rango esperado
   - Cumplimiento de horarios de almuerzo

2. **Alertas automáticas:**
   - Pausa > 2 horas → Email a supervisor
   - ENT_TRANS sin SAL_TRANS previa → Inconsistencia reportada

---

## 11. Preguntas Frecuentes

### ¿Qué pasa si registro entrada transitoria sin haber registrado salida transitoria?

El sistema detecta la inconsistencia y muestra un modal. Puedes aceptar el override, pero el registro quedará marcado y requerirá corrección manual por el supervisor.

### ¿Se redondea la hora de entrada transitoria?

No, se usa la hora exacta para calcular con precisión el tiempo de pausa.

### ¿Puedo registrar múltiples entradas transitorias en un día?

No directamente con la configuración actual. El flujo permite solo un par SAL_TRANS → ENT_TRANS por jornada.

### ¿Qué pasa si olvido registrar entrada transitoria después de la pausa?

El sistema queda esperando ENT_TRANS. Al intentar registrar SALIDA final, detectará la inconsistencia. Las horas no se calcularán correctamente hasta que se complete la secuencia.

### ¿La entrada transitoria cuenta para las horas trabajadas?

No directamente. Solo marca el fin de la pausa. Las horas se calculan al registrar la SALIDA final, restando automáticamente el tiempo de pausa.

---

## 12. Referencias Técnicas

### Archivos Involucrados

| Archivo | Líneas Relevantes | Descripción |
|---------|------------------|-------------|
| `templates/reloj_fichador/base.html` | 35-36, 163-164 | Botón y atajo de teclado |
| `apps/reloj_fichador/views.py` | 25-103 | Endpoint de registro |
| `apps/reloj_fichador/models.py` | 507-556 | Validaciones específicas |
| `apps/reloj_fichador/signals.py` | 13-26, 40-75 | Triggers de asistencia |

### Modelos de Base de Datos

- `reloj_fichador_registrodiario`: Almacenamiento principal
- `reloj_fichador_historicalregistrodiario`: Auditoría
- `reloj_fichador_registroasistencia`: Control de asistencia
- `reloj_fichador_horas_trabajadas`: Cálculo (post-SALIDA final)

### Transiciones Válidas

```python
# models.py línea 555
transiciones_validas = {
    'entrada': ['salida', 'salida_transitoria'],
    'salida_transitoria': ['entrada_transitoria'],  # ← Solo permite esto
    'entrada_transitoria': ['salida'],               # ← Este movimiento solo permite SALIDA
    'salida': [],  # Nueva jornada debe empezar con ENTRADA
}
```

---

**Documento generado por:** Claude Code
**Fecha:** 18 de Octubre de 2025
**Versión:** 1.0
**Próxima revisión:** Al modificar validaciones de movimientos transitorios
