# Análisis Técnico: Movimiento SALIDA (Final)

**Tipo de Movimiento:** `salida`
**Secuencia:** #4 en la jornada laboral (FINAL)
**Atajo de Teclado:** `P`
**Fecha:** 18 de Octubre de 2025

---

## 1. Definición y Propósito

### 1.1. ¿Qué es una Salida Final?

La **Salida** (o Salida Final) es el movimiento que registra cuando un operario **finaliza su jornada laboral** y abandona el establecimiento sin intención de regresar el mismo día.

### 1.2. Importancia Crítica

Este es el movimiento **MÁS IMPORTANTE** del sistema porque:

1. **Cierra el ciclo de trabajo** del día
2. **Dispara todos los cálculos automáticos:**
   - Horas trabajadas (normales + nocturnas)
   - Horas extras
   - Horas totales mensuales
3. **Aplica redondeo de salida** (hacia abajo a la hora)
4. **Calcula diferencias entrada-salida** para reportes
5. **Actualiza asistencia** como "presente"

### 1.3. Diferencia con Salida Transitoria

| Característica | Salida Final | Salida Transitoria |
|----------------|--------------|-------------------|
| Fin de jornada | ✅ Sí | ❌ No (pausa) |
| Regreso esperado | ❌ No | ✅ Sí (mismo día) |
| Calcula horas | ✅ Sí (inmediato) | ❌ No (espera SALIDA final) |
| Redondeo aplicado | ✅ Sí (a la hora) | ❌ No (hora exacta) |
| Siguiente movimiento | ENTRADA (mañana) | ENTRADA_TRANSITORIA (hoy) |
| Triggers signals | 🔥 TODOS | Solo asistencia |

---

## 2. Posición en la Secuencia de Jornada

### 2.1. Secuencias Válidas

#### Jornada Simple (sin pausas)
```
1. ENTRADA → 4. SALIDA
```

#### Jornada Completa (con pausa)
```
1. ENTRADA → 2. SAL_TRANS → 3. ENT_TRANS → 4. SALIDA
```

### 2.2. Movimiento Anterior Permitido

**Puede venir después de:**
- `ENTRADA` (jornada simple)
- `ENTRADA_TRANSITORIA` (jornada con pausa)

**Validación aplicada:**
```python
# models.py líneas 493-505
if self.tipo_movimiento == 'salida':
    # Debe existir ENTRADA en el mismo día
    entrada_del_dia = RegistroDiario.objects.filter(
        operario=self.operario,
        tipo_movimiento='entrada',
        hora_fichada__date=movimiento_fecha,
        valido=True
    ).exists()

    if not entrada_del_dia:
        raise ValidationError(
            "Atención: Usted no ha registrado una ENTRADA el día de hoy."
        )
```

### 2.3. Movimiento Siguiente Esperado

**Próximo movimiento:** `ENTRADA` (al día siguiente o próxima jornada)

**Transiciones válidas:**
```python
# models.py línea 557
transiciones_validas = {
    'salida': [],  # No permite nada más en esta jornada
}

# Una nueva jornada siempre debe iniciar con ENTRADA
```

---

## 3. Flujo Técnico Específico

### FASE 1: Interacción del Usuario

#### 3.1.1. Selección del Movimiento
**Interfaz:** `templates/reloj_fichador/base.html`

```html
<!-- Línea 37 -->
<button class="menu-button" onclick="setTipoMovimiento('salida')">
    Salida (P)
</button>
```

**Atajo de teclado:**
```javascript
// Líneas 166-167
case 'P':
    setTipoMovimiento('salida');
    break;
```

**Acción del botón:**
```javascript
// Línea 134
document.getElementById('tipo_movimiento').value = 'salida';

// Línea 135
document.getElementById('movimientoForm').action =
    "/registrar_movimiento/salida/";
```

#### 3.1.2. Contexto de Uso Típico

**Escenario jornada simple:**
```
08:00 → Operario presiona "Q" (Entrada)
        Comienza jornada

[9 horas después]

17:00 → Operario presiona "P" (Salida) ◄── Este momento
        Ingresa DNI: 12345678
        Sistema calcula horas y finaliza jornada
```

**Escenario jornada con pausa:**
```
08:00 → ENTRADA (Q)
12:30 → SALIDA_TRANSITORIA (Z) - almuerzo
13:45 → ENTRADA_TRANSITORIA (M) - regreso
17:30 → SALIDA (P) ◄── Este momento - finaliza todo
```

---

### FASE 2: Validaciones Backend

#### 3.2.1. Vista Principal
**Archivo:** `apps/reloj_fichador/views.py` (líneas 25-103)

```python
@csrf_exempt
@require_POST
def registrar_movimiento_tipo(request, tipo_movimiento):
    # tipo_movimiento = 'salida'

    dni = request.POST.get('dni')
    operario = Operario.objects.get(dni=dni)

    argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
    hora_actual = timezone.now().astimezone(argentina_tz)

    # Crear instancia para validación
    registro = RegistroDiario(
        operario=operario,
        tipo_movimiento='salida',
        hora_fichada=hora_actual,
    )

    registro.full_clean()  # ← Ejecuta validaciones
    registro.save()  # ← Dispara signals y cálculos
```

#### 3.2.2. Validaciones del Modelo
**Archivo:** `apps/reloj_fichador/models.py` (método `clean()`)

**Validación 1: Existencia de ENTRADA en el día**
```python
# Líneas 493-505
if self.tipo_movimiento == 'salida':
    # Calcular fecha lógica (considera turnos nocturnos)
    movimiento_fecha = RegistroDiario.calcular_fecha_logica(
        hora_fichada_normalizada,
        self.tipo_movimiento
    )

    # Buscar ENTRADA en la misma fecha lógica
    entrada_del_dia = RegistroDiario.objects.filter(
        operario=self.operario,
        tipo_movimiento='entrada',
        hora_fichada__date=movimiento_fecha,
        valido=True
    ).exists()

    if not entrada_del_dia:
        raise ValidationError({
            'tipo_movimiento': [
                "<span style='color: orange;'>Atención: "
                "Usted no ha registrado una ENTRADA el día de hoy.</span>"
            ]
        })
```

**Explicación de fecha lógica:**
```python
# Ejemplo turno nocturno:
# ENTRADA: 18/10 22:00 → fecha_lógica = 18/10
# SALIDA: 19/10 06:00 → fecha_lógica = 18/10 (pertenece al día anterior)

# Ambos tienen la misma fecha_lógica → Validación pasa ✅
```

**Validación 2: Transición desde movimiento anterior**
```python
# Líneas 522-556
# Obtener última ENTRADA
ultima_entrada = RegistroDiario.objects.filter(
    operario=self.operario,
    tipo_movimiento='entrada',
    hora_fichada__lt=self.hora_fichada,
    valido=True
).order_by('-id_registro').first()

if ultima_entrada:
    # Obtener movimientos desde esa ENTRADA
    registros_jornada = RegistroDiario.objects.filter(
        operario=self.operario,
        id_registro__gt=ultima_entrada.id_registro,
        valido=True
    ).exclude(pk=self.pk).order_by('id_registro')

    movimientos_jornada = ['entrada'] + list(
        registros_jornada.values_list('tipo_movimiento', flat=True)
    )

    # Ejemplos válidos:
    # ['entrada'] → Permite SALIDA ✅
    # ['entrada', 'salida_transitoria', 'entrada_transitoria'] → Permite SALIDA ✅

    last_movement = movimientos_jornada[-1]

    transiciones_validas = {
        'entrada': ['salida', 'salida_transitoria'],  # SALIDA permitida
        'entrada_transitoria': ['salida'],             # SALIDA permitida
    }

    if self.tipo_movimiento not in transiciones_validas.get(last_movement, []):
        raise ValidationError("Secuencia de movimientos inválida")
```

**Resultado de validaciones:**
```
✅ VÁLIDO si:
   - Existe ENTRADA en la fecha lógica del día
   - Último movimiento = ENTRADA o ENTRADA_TRANSITORIA
   - Hora fichada > hora de último movimiento
   - No hay ya una SALIDA registrada para esta jornada

❌ INVÁLIDO si:
   - No existe ENTRADA en el día
   - Último movimiento = SALIDA_TRANSITORIA (falta ENT_TRANS)
   - Ya existe SALIDA para esta jornada (doble salida)
```

---

### FASE 3: Persistencia y Redondeo

#### 3.3.1. Aplicación de Redondeo

**Función:** `redondear_salida(dt)` (models.py:88-106)

```python
def redondear_salida(dt):
    """
    Redondea la hora de salida hacia abajo según la configuración.
    """
    argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
    dt_local = dt.astimezone(argentina_tz)

    # Obtener configuración
    config = ConfiguracionRedondeoSalida.objects.first()
    min_salida = config.minutos_redondeo_salida if config else 0
    # Por defecto: min_salida = 0 (redondeo a la hora completa)

    # Redondear hacia abajo
    fecha_base = dt_local.replace(minute=min_salida, second=0, microsecond=0)

    if dt_local.minute < min_salida:
        fecha_base -= timedelta(hours=1)

    return fecha_base
```

**Ejemplos de redondeo (configuración por defecto: min=0):**
```
17:58:45 → 17:00:00
18:15:30 → 18:00:00
18:45:00 → 18:00:00
18:59:59 → 18:00:00
19:00:00 → 19:00:00
```

**Justificación del redondeo hacia abajo:**
- Evita pagar minutos no trabajados
- Incentiva a los operarios a no retirarse antes de tiempo
- Simplifica cálculos (horas exactas)

#### 3.3.2. Registro en Base de Datos

**Tabla:** `reloj_fichador_registrodiario`

```sql
INSERT INTO reloj_fichador_registrodiario (
    operario_id,
    hora_fichada,
    tipo_movimiento,
    origen_fichada,
    inconsistencia,
    valido,
    dif_entrada_salida,
    dif_entrada_salida_total
) VALUES (
    245,                                    -- ID del operario
    '2025-10-18 17:45:00-03:00',           -- Hora REDONDEADA (si era 17:58 → 17:00)
    'salida',                               -- Tipo de movimiento
    'Auto',                                 -- Origen
    FALSE,                                  -- Sin inconsistencia
    TRUE,                                   -- Válido
    '09:45:00',                            -- Diferencia calculada (ver sección 4.2)
    '09:45:00'                             -- Total acumulado
);
```

#### 3.3.3. Campos Específicos de Salida

| Campo | Valor | Observación |
|-------|-------|-------------|
| `tipo_movimiento` | `'salida'` | Identificador clave |
| `hora_fichada` | Hora redondeada | ⚠️ SE APLICA REDONDEO |
| `dif_entrada_salida` | Duración del ciclo 1 | Calculado automáticamente |
| `dif_entrada_salida2` | Duración del ciclo 2 | Si hay pausas transitorias |
| `dif_entrada_salida_total` | Suma total | Total de todos los ciclos |

---

### FASE 4: Cálculo de Diferencias Entrada-Salida

#### 4.4.1. Método `calcular_diferencia_entrada_salida()`
**Archivo:** `models.py` (líneas 383-429)

```python
def calcular_diferencia_entrada_salida(self):
    """
    Calcula la diferencia entre entrada redondeada y salida,
    y la almacena en dif_entrada_salida.
    """
    if self.tipo_movimiento != 'salida':
        return None  # Solo aplica a salidas

    # Buscar última ENTRADA antes de esta salida
    ultima_entrada = RegistroDiario.objects.filter(
        operario=self.operario,
        tipo_movimiento='entrada',
        valido=True,
        hora_fichada__lt=self.hora_fichada
    ).order_by('-hora_fichada').first()

    if not ultima_entrada:
        logger.warning(f"No se encontró ENTRADA previa para {self.operario}")
        return None

    # Redondear la entrada
    entrada_redondeada = redondear_entrada(ultima_entrada.hora_fichada)

    # Calcular diferencia (la hora de salida YA está redondeada)
    diferencia = self.hora_fichada - entrada_redondeada

    # Guardar en campos correspondientes
    if not self.dif_entrada_salida:
        self.dif_entrada_salida = diferencia
    else:
        # Si ya existe dif_entrada_salida, usar dif_entrada_salida2
        self.dif_entrada_salida2 = diferencia

    # Calcular total acumulado
    acum = timedelta(0)
    if self.dif_entrada_salida:
        acum += self.dif_entrada_salida
    if self.dif_entrada_salida2:
        acum += self.dif_entrada_salida2

    self.dif_entrada_salida_total = acum

    # Guardar sin disparar signals (prevenir recursión)
    with suppress_signal():
        self.save(update_fields=[
            'dif_entrada_salida',
            'dif_entrada_salida2',
            'dif_entrada_salida_total'
        ])

    return diferencia
```

**Ejemplo de cálculo:**
```python
# Jornada simple
ENTRADA: 08:07 → Redondeada a 08:00
SALIDA: 17:58 → Redondeada a 17:00

diferencia = 17:00 - 08:00 = 9h 0min

dif_entrada_salida = 9h 0min
dif_entrada_salida2 = NULL
dif_entrada_salida_total = 9h 0min
```

---

### FASE 5: TRIGGERS CRÍTICOS (Signals)

#### 5.5.1. Signal 1: Actualizar Asistencia
**Archivo:** `signals.py` (líneas 13-26)

```python
@receiver(post_save, sender=RegistroDiario)
def actualizar_asistencia(sender, instance, created, **kwargs):
    if created:  # Solo en creación
        fecha_actual = instance.hora_fichada.date()
        operario = instance.operario

        # Crear o actualizar registro de asistencia
        registro_asistencia, _ = RegistroAsistencia.objects.get_or_create(
            operario=operario,
            fecha=fecha_actual
        )

        # Verificar asistencia
        registro_asistencia.verificar_asistencia()
        # → estado = 'presente' (hay ENTRADA válida)
```

#### 5.5.2. Signal 2: Calcular Horas Trabajadas 🔥
**Archivo:** `signals.py` (líneas 40-75)

```python
@receiver(post_save, sender=RegistroDiario)
def actualizar_horas_despues_de_guardar(sender, instance, **kwargs):
    operario = instance.operario
    fecha_logica = RegistroDiario.calcular_fecha_logica(
        instance.hora_fichada,
        instance.tipo_movimiento
    )
    mes_logico = fecha_logica.strftime('%Y-%m')

    with suppress_signal():  # Prevenir cascadas infinitas

        # 1) Calcular horas trabajadas (normales + nocturnas)
        Horas_trabajadas.calcular_horas_trabajadas(operario, fecha_logica)

        # 2) Calcular horas extras (si total > 8h)
        Horas_extras.calcular_horas_extras(operario, fecha_logica)

        # 3) Recortar Horas_trabajadas a máximo 8h
        try:
            ht = Horas_trabajadas.objects.get(operario=operario, fecha=fecha_logica)
            total_reales = ht.horas_normales + ht.horas_nocturnas
            limite_jornada = timedelta(hours=8)

            if total_reales > limite_jornada:
                # Distribuir proporcionalmente
                ratio_n = ht.horas_normales / total_reales if total_reales else 0
                ratio_noct = ht.horas_nocturnas / total_reales if total_reales else 0

                ht.horas_normales = limite_jornada * ratio_n
                ht.horas_nocturnas = limite_jornada * ratio_noct

            ht.save()
        except Horas_trabajadas.DoesNotExist:
            pass

        # 4) Calcular totales mensuales
        Horas_totales.calcular_horas_totales(operario, mes_logico)
```

---

## 4. Cálculo de Horas Trabajadas (Detallado)

### 4.1. Algoritmo Principal
**Método:** `Horas_trabajadas.calcular_horas_trabajadas(operario, fecha)`
**Archivo:** `models.py` (líneas 504-562)

```python
@classmethod
def calcular_horas_trabajadas(cls, operario, fecha):
    """
    Calcula las horas trabajadas para un operario en una fecha específica.
    Separa en horas normales (06:00-20:00) y nocturnas (20:00-06:00).
    """
    # 1. Obtener todos los registros VÁLIDOS del día
    registros = RegistroDiario.objects.filter(
        operario=operario,
        hora_fichada__date=fecha,
        valido=True
    ).order_by('hora_fichada')

    # 2. Agrupar en pares ENTRADA → SALIDA
    entradas = []
    salidas = []

    for registro in registros:
        if registro.tipo_movimiento == 'entrada':
            entradas.append(registro)
        elif registro.tipo_movimiento == 'salida':
            salidas.append(registro)
        # Nota: salida_transitoria y entrada_transitoria se usan
        #       para calcular ciclos intermedios

    # 3. Calcular diferencias por cada par
    horas_normales_total = timedelta(0)
    horas_nocturnas_total = timedelta(0)

    for i, entrada in enumerate(entradas):
        if i < len(salidas):
            salida = salidas[i]

            # Redondear entrada
            entrada_red = redondear_entrada(entrada.hora_fichada)

            # Salida ya viene redondeada desde el registro
            salida_red = salida.hora_fichada

            # Calcular franjas horarias
            horas_n, horas_noct = calcular_horas_por_franjas(
                entrada_red,
                salida_red
            )

            horas_normales_total += horas_n
            horas_nocturnas_total += horas_noct

    # 4. Guardar en BD
    ht, created = cls.objects.update_or_create(
        operario=operario,
        fecha=fecha,
        defaults={
            'horas_normales': horas_normales_total,
            'horas_nocturnas': horas_nocturnas_total,
        }
    )

    return ht
```

### 4.2. Cálculo de Franjas Horarias
**Función:** `calcular_horas_por_franjas(entrada, salida)` (models.py:108-140)

```python
def calcular_horas_por_franjas(entrada, salida):
    """
    Separa el tiempo trabajado en franjas normales (06:00-20:00)
    y nocturnas (20:00-06:00).
    """
    HORA_INICIO_NORMAL = time(6, 0)   # 06:00
    HORA_FIN_NORMAL = time(20, 0)     # 20:00

    horas_normales = timedelta(0)
    horas_nocturnas = timedelta(0)

    # Iterar hora por hora
    tiempo_actual = entrada

    while tiempo_actual < salida:
        tiempo_siguiente = min(
            tiempo_actual + timedelta(hours=1),
            salida
        )

        # Determinar si esta hora es normal o nocturna
        hora_actual = tiempo_actual.time()

        if HORA_INICIO_NORMAL <= hora_actual < HORA_FIN_NORMAL:
            # Franja normal (06:00-20:00)
            horas_normales += (tiempo_siguiente - tiempo_actual)
        else:
            # Franja nocturna (20:00-06:00)
            horas_nocturnas += (tiempo_siguiente - tiempo_actual)

        tiempo_actual = tiempo_siguiente

    return horas_normales, horas_nocturnas
```

**Ejemplo de cálculo:**
```python
# Caso 1: Jornada completa diurna
ENTRADA: 08:00
SALIDA: 17:00

Franjas:
- 08:00 → 17:00 (9 horas) → Todo en franja normal (06:00-20:00)

Resultado:
horas_normales = 9h 0min
horas_nocturnas = 0h


# Caso 2: Jornada que cruza límite nocturno
ENTRADA: 18:00
SALIDA: 22:00

Franjas:
- 18:00 → 20:00 (2 horas) → Normal (06:00-20:00)
- 20:00 → 22:00 (2 horas) → Nocturna (20:00-06:00)

Resultado:
horas_normales = 2h 0min
horas_nocturnas = 2h 0min


# Caso 3: Turno nocturno completo
ENTRADA: 22:00 (18/10)
SALIDA: 06:00 (19/10 pero fecha_lógica=18/10)

Franjas:
- 22:00 → 06:00 (8 horas) → Todo en franja nocturna

Resultado:
horas_normales = 0h
horas_nocturnas = 8h 0min
```

### 4.3. Cálculo de Horas Extras
**Método:** `Horas_extras.calcular_horas_extras(operario, fecha)`

```python
@classmethod
def calcular_horas_extras(cls, operario, fecha):
    """
    Calcula horas extras si el total trabajado > 8 horas.
    Redondea a bloques de 30 minutos.
    """
    # Obtener horas trabajadas del día
    try:
        ht = Horas_trabajadas.objects.get(operario=operario, fecha=fecha)
    except Horas_trabajadas.DoesNotExist:
        return None

    total_dia = ht.horas_normales + ht.horas_nocturnas
    limite_jornada = timedelta(hours=8)

    if total_dia > limite_jornada:
        # Calcular extras brutas
        extras_brutas = total_dia - limite_jornada

        # Redondear a bloques de 30 minutos
        minutos_extras = extras_brutas.total_seconds() / 60

        if minutos_extras < 15:
            extras_redondeadas = timedelta(0)  # 0-14 min → 0
        elif minutos_extras < 45:
            extras_redondeadas = timedelta(minutes=30)  # 15-44 min → 30
        else:
            # Redondeo al múltiplo de 30 más cercano
            bloques = round(minutos_extras / 30)
            extras_redondeadas = timedelta(minutes=bloques * 30)

        # Guardar en BD
        he, created = cls.objects.update_or_create(
            operario=operario,
            fecha=fecha,
            defaults={
                'horas_extras_50': extras_redondeadas,
            }
        )

        return he
    else:
        # No hay extras, eliminar si existía
        cls.objects.filter(operario=operario, fecha=fecha).delete()
        return None
```

**Ejemplos de redondeo de extras:**
```
Total: 8h 10min → Extras brutas: 0h 10min → Redondeado: 0h 0min
Total: 8h 20min → Extras brutas: 0h 20min → Redondeado: 0h 30min
Total: 8h 35min → Extras brutas: 0h 35min → Redondeado: 0h 30min
Total: 9h 50min → Extras brutas: 1h 50min → Redondeado: 2h 0min
Total: 10h 25min → Extras brutas: 2h 25min → Redondeado: 2h 30min
```

---

## 5. Casos de Uso Específicos

### Caso 1: Jornada Simple Estándar

```
Operario: PÉREZ, JUAN (DNI: 12345678)
Fecha: 18/10/2025

08:12 → ENTRADA
    Redondeada a: 08:15

17:58 → SALIDA ◄── Dispara todos los cálculos
    Redondeada a: 17:00

Cálculos automáticos:
1. Diferencia entrada-salida:
   - 17:00 - 08:15 = 8h 45min
   - dif_entrada_salida = 8h 45min

2. Horas trabajadas:
   - Todo en franja normal (06:00-20:00)
   - horas_normales = 8h 45min
   - horas_nocturnas = 0h

3. Horas extras:
   - Total: 8h 45min > 8h
   - Extras brutas: 0h 45min
   - Redondeado: 1h 0min (45 min → 1h)

4. Horas totales:
   - Actualiza acumulado mensual de octubre 2025

Resultado BD:
- RegistroDiario: 2 registros (entrada, salida)
- Horas_trabajadas: horas_normales=8.75h, horas_nocturnas=0h
- Horas_extras: horas_extras_50=1h
- Horas_totales: actualizado con += 8.75h normales
- RegistroAsistencia: estado='presente'
```

### Caso 2: Jornada con Pausa (Almuerzo)

```
Operario: LÓPEZ, CARLOS (DNI: 34567890)
Fecha: 18/10/2025

08:05 → ENTRADA
    Redondeada a: 08:00

12:30 → SALIDA TRANSITORIA
    Sin redondeo: 12:30

13:45 → ENTRADA TRANSITORIA
    Sin redondeo: 13:45

17:15 → SALIDA ◄── Dispara cálculos
    Redondeada a: 17:00

Cálculos automáticos:
1. Diferencia entrada-salida:
   - Ciclo 1: 12:30 - 08:00 = 4h 30min
   - Ciclo 2: 17:00 - 13:45 = 3h 15min
   - dif_entrada_salida = 4h 30min
   - dif_entrada_salida2 = 3h 15min
   - dif_entrada_salida_total = 7h 45min

2. Horas trabajadas:
   - Total: 4h 30min + 3h 15min = 7h 45min
   - Todo en franja normal
   - horas_normales = 7h 45min
   - horas_nocturnas = 0h

3. Horas extras:
   - Total: 7h 45min < 8h
   - No hay extras

4. Tiempo de pausa (informativo, no contabilizado):
   - 13:45 - 12:30 = 1h 15min

Resultado BD:
- RegistroDiario: 4 registros
- Horas_trabajadas: horas_normales=7.75h, horas_nocturnas=0h
- Horas_extras: NULL (no se crea registro)
- Horas_totales: actualizado con += 7.75h normales
```

### Caso 3: Turno Nocturno

```
Operario: GÓMEZ, MARÍA (DNI: 23456789)
Fecha lógica: 18/10/2025

18/10 22:15 → ENTRADA
    Redondeada a: 22:15

19/10 06:30 → SALIDA ◄── Fecha real 19/10, pero fecha_lógica=18/10
    Redondeada a: 06:00

Cálculos automáticos:
1. Diferencia entrada-salida:
   - 06:00 - 22:15 = 7h 45min

2. Horas trabajadas:
   - Franjas:
     * 22:15 → 06:00 (siguiente día) → Nocturna
   - horas_normales = 0h
   - horas_nocturnas = 7h 45min

3. Horas extras:
   - Total: 7h 45min < 8h
   - No hay extras

Resultado BD:
- Ambos registros con fecha_logica = 18/10/2025
- Horas_trabajadas (18/10): horas_normales=0h, horas_nocturnas=7.75h
- Horas_extras: NULL
- RegistroAsistencia (18/10): estado='presente'
```

### Caso 4: Salida sin Entrada (Inconsistencia)

```
Operario: MARTÍNEZ, ANA (DNI: 45678901)
Fecha: 18/10/2025

[No registra ENTRADA]

17:30 → SALIDA ❌
```

**Validación aplicada:**
```python
entrada_del_dia = RegistroDiario.objects.filter(
    operario=operario,
    tipo_movimiento='entrada',
    hora_fichada__date='2025-10-18',
    valido=True
).exists()

# False
→ raise ValidationError("No ha registrado una ENTRADA el día de hoy")
```

**Mensaje al usuario:**
```
"Atención: Usted no ha registrado una ENTRADA el día de hoy.
¿Desea fichar de todos modos?"
```

**Si acepta override:**
- Se guarda con `inconsistencia=True`
- `descripcion_inconsistencia = "Salida sin entrada previa en el día"`
- **NO se calculan horas** (no hay par ENTRADA-SALIDA)
- Requiere corrección manual en admin

---

## 6. Inconsistencias Comunes

### 6.1. Doble Salida sin Entrada Intermedia

**Escenario:**
```
08:00 → ENTRADA
17:00 → SALIDA ✅
18:00 → SALIDA ❌ (sin ENTRADA intermedia)
```

**Validación:**
```python
# La jornada ya cerró con la primera SALIDA
# Nueva SALIDA requiere nueva ENTRADA

ultimo_movimiento = 'salida'

transiciones_validas = {
    'salida': [],  # No permite nada más
}

→ Inconsistencia detectada
```

**Mensaje:**
```
"Inconsistencia: Su último movimiento fue Salida 17:00:00.
Para registrar una nueva salida, primero debe registrar una Entrada."
```

### 6.2. Salida después de Salida Transitoria

**Escenario:**
```
08:00 → ENTRADA
12:30 → SALIDA TRANSITORIA
17:00 → SALIDA ❌ (falta ENTRADA_TRANSITORIA)
```

**Validación:**
```python
movimientos_jornada = ['entrada', 'salida_transitoria']
last_movement = 'salida_transitoria'

transiciones_validas = {
    'salida_transitoria': ['entrada_transitoria'],  # Solo permite esto
}

'salida' NOT IN ['entrada_transitoria']
→ Inconsistencia
```

**Mensaje:**
```
"Inconsistencia: Su último movimiento fue Salida Transitoria 12:30:00.
Debe registrar Entrada Transitoria antes de la salida final."
```

### 6.3. Salida Retroactiva (hora anterior al último movimiento)

**Escenario:**
```
08:00 → ENTRADA
17:00 → [Usuario intenta fichar con hora manual: 16:30] ❌
```

**Validación:**
```python
if self.hora_fichada <= ultimo_valido.hora_fichada:
    logger.warning(f"Salida ({self.hora_fichada}) <= último registro ({ultimo_valido.hora_fichada})")
    # Solo advertencia, no bloquea
```

**Comportamiento:**
- Se permite (no es error crítico)
- Se loguea como advertencia
- Supervisor puede revisar en reportes de inconsistencias

---

## 7. Respuestas del Sistema

### 7.1. Respuesta Exitosa

**JSON Response:**
```json
{
    "success": true,
    "message": "REGISTRO EXITOSO: PÉREZ, JUAN - Salida - 18/10/2025 17:00:00"
}
```

**Procesamiento en background (inmediato):**
```
[Signal] actualizar_asistencia
   → estado = 'presente'

[Signal] actualizar_horas_despues_de_guardar
   → Horas_trabajadas calculadas
   → Horas_extras calculadas
   → Horas_trabajadas recortadas a 8h max
   → Horas_totales actualizadas

[Cálculo] calcular_diferencia_entrada_salida
   → dif_entrada_salida = 9h 0min
```

**Todo esto ocurre en < 500ms**

**Comportamiento en UI:**
```javascript
mostrarMensaje('success', data.message);
// Fondo verde, mensaje 30 segundos
dniInput.value = '';
dniInput.focus();
```

### 7.2. Respuesta con Inconsistencia

**JSON Response:**
```json
{
    "success": false,
    "inconsistencia": true,
    "descripcion_inconsistencia": "Atención: Usted no ha registrado una ENTRADA el día de hoy.",
    "tipo_movimiento": "salida"
}
```

**Modal mostrado:**
```html
<div id="inconsistency-modal">
    <p>Atención: Usted no ha registrado una ENTRADA el día de hoy.</p>
    <p>¿Desea fichar de todos modos?</p>
    <button id="accept-modal-button">Aceptar</button>
    <button id="cancel-modal-button">Cancelar</button>
</div>
```

---

## 8. Logging y Monitoreo

### 8.1. Logs Críticos

```python
# Al guardar SALIDA exitosamente
logger.info(
    f"Registro creado exitosamente: PÉREZ, JUAN - Salida - 17:00:00"
)

# Al calcular horas
logger.info(
    f"Horas calculadas para {operario.nombre} en {fecha}: "
    f"Normales={horas_normales}, Nocturnas={horas_nocturnas}"
)

# Al detectar inconsistencia
logger.warning(
    f"Inconsistencia detectada: Salida sin entrada previa para {operario.dni}"
)

# Al calcular extras
logger.info(
    f"Horas extras calculadas: {extras_redondeadas} "
    f"(brutas: {extras_brutas})"
)
```

### 8.2. Métricas de Performance

**Query para analizar tiempos de procesamiento:**
```sql
-- Tiempo promedio entre ENTRADA y SALIDA por operario
SELECT
    o.nombre,
    o.apellido,
    AVG(EXTRACT(EPOCH FROM (
        salida.hora_fichada - entrada.hora_fichada
    )) / 3600) as horas_promedio
FROM reloj_fichador_registrodiario entrada
JOIN reloj_fichador_registrodiario salida
    ON entrada.operario_id = salida.operario_id
    AND DATE(entrada.hora_fichada) = DATE(salida.hora_fichada)
    AND salida.hora_fichada > entrada.hora_fichada
JOIN reloj_fichador_operario o
    ON entrada.operario_id = o.id_operario
WHERE entrada.tipo_movimiento = 'entrada'
  AND salida.tipo_movimiento = 'salida'
  AND entrada.valido = TRUE
  AND salida.valido = TRUE
GROUP BY o.nombre, o.apellido
ORDER BY horas_promedio DESC;
```

---

## 9. Mejoras Sugeridas

### 9.1. Funcionalidad

1. **Confirmación de salida:**
   - Mostrar resumen antes de fichar:
     ```
     "Va a registrar SALIDA (17:58 → redondeado a 17:00)
     Tiempo trabajado hoy: ~9h 45min
     ¿Confirmar?"
     ```

2. **Detección de jornadas excesivas:**
   - Alertar si > 12 horas trabajadas
   - Requiere confirmación adicional

3. **Estadísticas inmediatas:**
   - Después de fichar SALIDA, mostrar:
     ```
     ✅ Jornada finalizada
     Tiempo trabajado: 9h 45min
     Horas extras: 1h 45min
     Total del mes: 180h 30min
     ```

### 9.2. Optimización

1. **Cálculo diferido para alta carga:**
   - Si hay > 50 fichados simultáneos
   - Encolar cálculos en Celery para procesamiento asíncrono

2. **Cache de configuraciones:**
   - `ConfiguracionRedondeoSalida` se consulta en cada salida
   - Cachear en Redis por 1 hora

3. **Índices compuestos:**
   ```sql
   CREATE INDEX idx_operario_fecha_tipo ON reloj_fichador_registrodiario(
       operario_id, hora_fichada, tipo_movimiento
   );
   ```

### 9.3. Auditoría

1. **Notificaciones a supervisores:**
   - Email diario con salidas con inconsistencias
   - Dashboard con jornadas incompletas

2. **Reportes automáticos:**
   - Generar PDF con horas del día al registrar SALIDA
   - Enviar por email al operario/supervisor

---

## 10. Preguntas Frecuentes

### ¿Por qué mi hora de salida se redondea hacia abajo?

Para simplificar cálculos y evitar pagar minutos no trabajados. Si fichas a las 17:58, se registra como 17:00.

### ¿Qué pasa si olvido fichar la salida?

El sistema marca el día como "presente" (porque hay ENTRADA), pero las horas trabajadas no se calculan. Un supervisor debe corregir manualmente.

### ¿Puedo registrar dos salidas en un día?

No directamente. Necesitas registrar una nueva ENTRADA entre dos SALIDAS. Cada salida cierra la jornada actual.

### ¿Cuánto tardan en calcularse las horas después de fichar salida?

Los cálculos son instantáneos (< 500ms). Los signals se ejecutan inmediatamente después de guardar el registro.

### ¿Las salidas transitorias también cierran el día?

No, solo la SALIDA final cierra la jornada y dispara cálculos. Las salidas transitorias solo marcan pausas.

---

## 11. Referencias Técnicas

### Archivos Involucrados

| Archivo | Líneas Clave | Función |
|---------|--------------|---------|
| `templates/reloj_fichador/base.html` | 37, 166-167 | Botón y atajo |
| `apps/reloj_fichador/views.py` | 25-103 | Endpoint de registro |
| `apps/reloj_fichador/models.py` | 88-106 | Redondeo de salida |
| `apps/reloj_fichador/models.py` | 383-429 | Cálculo de diferencias |
| `apps/reloj_fichador/models.py` | 493-505 | Validación de ENTRADA |
| `apps/reloj_fichador/models.py` | 504-562 | Cálculo de horas |
| `apps/reloj_fichador/signals.py` | 40-75 | Triggers automáticos |

### Modelos de Base de Datos Afectados

1. **reloj_fichador_registrodiario** (INSERT)
2. **reloj_fichador_horas_trabajadas** (INSERT/UPDATE)
3. **reloj_fichador_horas_extras** (INSERT/UPDATE/DELETE)
4. **reloj_fichador_horas_totales** (UPDATE)
5. **reloj_fichador_registroasistencia** (UPDATE)
6. **reloj_fichador_historicalregistrodiario** (INSERT - auditoría)

---

**Documento generado por:** Claude Code
**Fecha:** 18 de Octubre de 2025
**Versión:** 1.0
**Próxima revisión:** Al modificar algoritmos de cálculo de horas o redondeos
