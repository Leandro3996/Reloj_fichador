# Análisis Técnico: Flujo Completo de Fichado

**Fecha:** 18 de Octubre de 2025
**Proyecto:** Sistema de Control de Asistencia - Reloj Fichador
**Versión del Sistema:** 2.0 (PostgreSQL + Django Unfold)

---

## 1. Resumen Ejecutivo

Este documento describe el flujo técnico completo de una fichada (registro de asistencia) desde que un operario presiona un botón en la interfaz hasta que el registro se persiste en la base de datos PostgreSQL y dispara todos los cálculos automáticos asociados.

### Alcance del Análisis
- **Entrada:** Operario presiona botón de fichado (ejemplo: "Q - Entrada")
- **Salida:** Registro almacenado en PostgreSQL + cálculo de horas trabajadas/extras/totales
- **Componentes analizados:**
  - Frontend (Templates + JavaScript)
  - Backend (Views + Models)
  - Validaciones de negocio
  - Signals y triggers automáticos

---

## 2. Arquitectura del Sistema de Fichado

### 2.1. Stack Tecnológico

| Componente | Tecnología | Ubicación |
|------------|-----------|-----------|
| Frontend | HTML5 + JavaScript (ES6) + jQuery | `templates/reloj_fichador/base.html` |
| Backend | Django 5.0.7 + Python 3.11 | `apps/reloj_fichador/views.py` |
| Base de Datos | PostgreSQL 15 | Docker container `db_postgres` |
| Validaciones | Django Models + Custom Validators | `apps/reloj_fichador/models.py` |
| Automatización | Django Signals | `apps/reloj_fichador/signals.py` |
| Zona Horaria | America/Argentina/Buenos_Aires (UTC-3) | Configurado en `settings.py` |

### 2.2. Modelos Principales Involucrados

1. **`Operario`**: Representa a cada empleado
2. **`RegistroDiario`**: Almacena cada fichada individual (entrada/salida/transitorias)
3. **`Horas_trabajadas`**: Calcula horas normales/nocturnas por día
4. **`Horas_extras`**: Calcula horas extraordinarias
5. **`Horas_totales`**: Totaliza horas mensuales
6. **`RegistroAsistencia`**: Marca asistencia/ausencia/justificación

---

## 3. Flujo Detallado de una Fichada Normal

### FASE 1: Interfaz de Usuario (Frontend)

#### 3.1.1. Carga Inicial de la Página
**Archivo:** `templates/reloj_fichador/base.html`

```javascript
// Líneas 79-126: Sistema de verificación de sesión 24/7
- Verifica sesión activa cada 2 horas
- Mantiene token CSRF válido continuamente
- Refresca sesión después de 30 min de inactividad
- Maneja eventos de recuperación de enfoque (tabs del navegador)
```

**Características de UI:**
- **Reloj sincronizado:** Líneas 390-442
  - Sincroniza con servidor vía `/api/health/` cada 5 minutos
  - Calcula latencia de red para ajustar offset
  - Actualiza display cada segundo sin consultar servidor

- **Widget de clima:** Líneas 444-461
  - API: OpenWeatherMap (Río Cuarto, Córdoba)
  - Actualización cada 10 minutos

- **Fondos rotativos:** Líneas 367-388
  - 9 imágenes que cambian cada 60 segundos

#### 3.1.2. Selección de Tipo de Movimiento
**Evento:** Usuario presiona botón o tecla de acceso rápido

```javascript
// Líneas 128-143: función setTipoMovimiento(tipo)
Acciones:
1. Remueve clase 'active' de todos los botones
2. Actualiza campo hidden 'tipo_movimiento' con valor seleccionado
3. Cambia la URL del formulario dinámicamente
4. Agrega efecto visual de elevación (300ms)
5. Marca botón como activo
```

**Atajos de teclado disponibles:** (Líneas 154-173)
- `Q` → Entrada
- `Z` → Salida Transitoria
- `M` → Entrada Transitoria
- `P` → Salida
- `ESC` → Limpiar campo DNI

#### 3.1.3. Ingreso de DNI y Envío
**Validación en tiempo real:** (Líneas 182-184)
```javascript
// Solo permite números, bloquea otros caracteres
dniInput.addEventListener('input', function () {
    this.value = this.value.replace(/[^0-9]/g, '');
});
```

**Comportamiento del foco:** (Líneas 175-179)
- Campo DNI siempre mantiene el foco
- Previene pérdida de foco accidental
- Facilita fichado rápido sin mouse

---

### FASE 2: Envío AJAX al Servidor

#### 3.2.1. Preparación de la Solicitud
**Archivo:** `templates/reloj_fichador/base.html` (Líneas 186-234)

```javascript
movimientoForm.addEventListener('submit', function (event) {
    event.preventDefault(); // Evita recarga de página

    // Validación básica
    if (!dni) {
        mostrarMensaje('error', 'Debe ingresar un DNI válido ⚠️');
        return;
    }

    // Preparar FormData
    const formData = new FormData(movimientoForm);

    // Envío AJAX
    fetch(movimientoForm.action, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData
    })
```

**Datos enviados:**
- `dni`: Número de documento del operario
- `tipo_movimiento`: entrada | salida | salida_transitoria | entrada_transitoria
- `csrfmiddlewaretoken`: Token de seguridad (cookie: `fichador_csrf`)

**Endpoint destino:**
```
POST /registrar_movimiento/<tipo_movimiento>/
Ejemplo: POST /registrar_movimiento/entrada/
```

---

### FASE 3: Procesamiento en el Backend

#### 3.3.1. Vista Principal: `registrar_movimiento_tipo()`
**Archivo:** `apps/reloj_fichador/views.py` (Líneas 25-103)

**Decoradores aplicados:**
```python
@csrf_exempt  # Manejo personalizado de CSRF
@require_POST  # Solo acepta método POST
```

**Flujo de ejecución:**

```
┌─────────────────────────────────────┐
│ 1. Verificación de solicitud AJAX  │
│    Línea 28-31                      │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 2. Obtención de parámetros          │
│    - dni (request.POST)             │
│    - inconsistency_override (bool)  │
│    Líneas 33-34                     │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 3. Búsqueda de operario             │
│    Operario.objects.get(dni=dni)    │
│    Líneas 40-46                     │
│    ❌ DoesNotExist → 404            │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 4. Obtención de hora actual         │
│    timezone.now() en zona Argentina │
│    Líneas 48-50                     │
└────────────┬────────────────────────┘
             │
             ▼
         ┌───┴───┐
         │ Override? │
         └───┬───┘
             │
      ┌──────┴──────┐
      │NO           │SÍ
      ▼             ▼
┌──────────┐  ┌──────────────┐
│ Validar  │  │ Guardar con  │
│ secuencia│  │ inconsistencia│
│ (FASE 4) │  │ = True       │
└──────────┘  └──────────────┘
```

#### 3.3.2. Ruta SIN Override (Primera Tentativa)
**Líneas 52-81**

```python
# Crear instancia temporal para validación
registro = RegistroDiario(
    operario=operario,
    tipo_movimiento=tipo_movimiento,
    hora_fichada=hora_actual,
)

try:
    registro.full_clean()  # ⚠️ Ejecuta todas las validaciones
    registro.save()        # ✅ Guarda en BD si pasa validaciones
    return JsonResponse({
        'success': True,
        'message': "REGISTRO EXITOSO: ..."
    })

except ValidationError as ve:
    # ❌ Inconsistencia detectada
    return JsonResponse({
        'success': False,
        'inconsistencia': True,
        'descripcion_inconsistencia': "...",
        'tipo_movimiento': tipo_movimiento
    }, status=400)
```

**Respuesta al frontend:**
- **Éxito:** `{'success': True, 'message': '...'}`
- **Inconsistencia:** `{'success': False, 'inconsistencia': True, 'descripcion_inconsistencia': '...'}`

#### 3.3.3. Ruta CON Override (Segunda Tentativa)
**Líneas 82-102**

Si el usuario acepta fichar a pesar de la inconsistencia:

```python
registro = RegistroDiario(
    operario=operario,
    tipo_movimiento=tipo_movimiento,
    hora_fichada=hora_actual,
    inconsistencia=True,  # Marcado explícitamente
    valido=True,          # Pero es válido para cálculos
)
registro.save()

# Actualizar descripción post-guardado
registro.descripcion_inconsistencia = f"El operario ... registró 2 veces el movimiento ..."
registro.save(update_fields=['descripcion_inconsistencia'])
```

---

### FASE 4: Validaciones de Negocio

#### 3.4.1. Método `clean()` del Modelo RegistroDiario
**Archivo:** `apps/reloj_fichador/models.py` (Líneas 431-549)

**Estructura de validaciones:**

```
┌─────────────────────────────────────────────┐
│ PRE-VALIDACIONES                            │
├─────────────────────────────────────────────┤
│ 1. Normalización de fecha con zona horaria │
│    Líneas 442-453                           │
│    - Si USE_TZ=True → Convertir a Argentina│
│    - Calcular fecha lógica (turnos nocturnos)│
│                                             │
│ 2. Bypass de validaciones                  │
│    Líneas 457-470                           │
│    - Si inconsistencia=True → Salir         │
│    - Si origen=Admin → Salir (correcciones) │
└─────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│ VALIDACIONES POR TIPO DE MOVIMIENTO        │
├─────────────────────────────────────────────┤
│ A) ENTRADA (Líneas 477-491)                 │
│    ✓ Debe venir después de SALIDA           │
│    ⚠️ Advertencia si hora <= última salida  │
│                                             │
│ B) SALIDA (Líneas 493-505)                  │
│    ✓ Debe existir ENTRADA en el mismo día   │
│                                             │
│ C) TRANSITORIAS (Líneas 507-519)            │
│    ✓ Debe existir ENTRADA previa válida     │
└─────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│ VALIDACIÓN DE SECUENCIA DE JORNADA         │
│ Líneas 522-549                              │
│                                             │
│ 1. Buscar última ENTRADA antes de ahora     │
│ 2. Obtener todos los movimientos desde esa  │
│    ENTRADA (jornada lógica actual)          │
│ 3. Validar secuencia permitida según reglas │
└─────────────────────────────────────────────┘
         │
         ▼
    Resultado:
    - Sin errores → Continúa a guardado
    - Con errores → raise ValidationError
```

#### 3.4.2. Cálculo de Fecha Lógica
**Método estático:** `RegistroDiario.calcular_fecha_logica()` (Líneas 342-380)

**Regla de negocio crítica:**

```python
hora_limite = 06:00

Si tipo_movimiento == 'entrada' AND hora < 06:00:
    fecha_logica = fecha_real  # Entrada temprana, día actual

Si tipo_movimiento != 'entrada' AND hora < 06:00:
    fecha_logica = fecha_real - 1 día  # Pertenece al día anterior

Si hora >= 06:00:
    fecha_logica = fecha_real
```

**Ejemplo práctico:**
```
Fichada: SALIDA a las 02:30 AM del 19/10/2025
→ Fecha lógica: 18/10/2025 (pertenece a la jornada del día anterior)

Fichada: ENTRADA a las 05:45 AM del 19/10/2025
→ Fecha lógica: 19/10/2025 (entrada temprana, día actual)
```

#### 3.4.3. Validación de Secuencias Permitidas
**Criterios implementados:**

**1. Secuencia normal de jornada completa:**
```
ENTRADA → SALIDA TRANSITORIA → ENTRADA TRANSITORIA → SALIDA
```

**2. Secuencia simple:**
```
ENTRADA → SALIDA
```

**3. Inconsistencias detectadas:**
```
❌ ENTRADA → ENTRADA (dos entradas seguidas)
❌ SALIDA sin ENTRADA previa en el día
❌ TRANSITORIA sin ENTRADA previa válida
❌ Hora de movimiento anterior a último registro válido
```

---

### FASE 5: Persistencia en Base de Datos

#### 3.5.1. Guardado del Registro
**Método:** `registro.save()`

**Tabla destino:** `reloj_fichador_registrodiario`

**Campos almacenados:**

| Campo | Tipo | Ejemplo | Observaciones |
|-------|------|---------|---------------|
| `id_registro` | AutoField | 12847 | PK autoincremental |
| `operario_id` | ForeignKey | 245 | Referencia a `reloj_fichador_operario` |
| `hora_fichada` | DateTimeField | 2025-10-18 08:15:23-03 | Timezone-aware (UTC almacenado) |
| `tipo_movimiento` | CharField | 'entrada' | Valores: entrada/salida/salida_transitoria/entrada_transitoria |
| `origen_fichada` | CharField | 'Auto' | Siempre 'Auto' desde template |
| `inconsistencia` | BooleanField | False | True solo si override aceptado |
| `valido` | BooleanField | True | Siempre True (histórico) |
| `descripcion_inconsistencia` | TextField | NULL | Solo si inconsistencia=True |
| `dif_entrada_salida` | DurationField | NULL | Calculado en salidas |
| `dif_entrada_salida2` | DurationField | NULL | Segundo ciclo si aplica |
| `dif_entrada_salida_total` | DurationField | NULL | Suma de diferencias |

**Índices de performance:**
```sql
CREATE INDEX idx_operario ON reloj_fichador_registrodiario(operario_id);
CREATE INDEX idx_hora_fichada ON reloj_fichador_registrodiario(hora_fichada);
```

#### 3.5.2. Auditoría Histórica
**Tabla:** `reloj_fichador_historicalregistrodiario`

Cada guardado también crea un registro histórico vía `django-simple-history`:

```python
history = HistoricalRecords()  # Definido en modelo
```

Almacena:
- Todos los campos del registro
- Usuario que hizo el cambio
- Timestamp del cambio
- Tipo de cambio: `+` (creación), `~` (modificación), `-` (eliminación)

---

### FASE 6: Triggers Automáticos (Signals)

#### 3.6.1. Signal: `post_save` de RegistroDiario
**Archivo:** `apps/reloj_fichador/signals.py` (Líneas 40-75)

**Receptor 1: `actualizar_horas_despues_de_guardar`**

```
Trigger: Cada vez que se guarda un RegistroDiario
Acción:
┌────────────────────────────────────────┐
│ 1. Calcular fecha lógica del registro │
│    (turnos nocturnos)                  │
└──────────────┬─────────────────────────┘
               ▼
┌────────────────────────────────────────┐
│ 2. Calcular Horas_trabajadas           │
│    - Horas normales (06:00-20:00)      │
│    - Horas nocturnas (20:00-06:00)     │
│    Línea 51                            │
└──────────────┬─────────────────────────┘
               ▼
┌────────────────────────────────────────┐
│ 3. Calcular Horas_extras               │
│    - Si total > 8h → Extras            │
│    - Redondeo a bloques de 30 min      │
│    Línea 54                            │
└──────────────┬─────────────────────────┘
               ▼
┌────────────────────────────────────────┐
│ 4. Recortar Horas_trabajadas a 8h max │
│    - Distribuir proporcionalmente      │
│    - normales/nocturnas según ratio    │
│    Líneas 57-71                        │
└──────────────┬─────────────────────────┘
               ▼
┌────────────────────────────────────────┐
│ 5. Calcular Horas_totales del mes      │
│    - Sumar todas las horas del mes     │
│    Línea 74                            │
└────────────────────────────────────────┘
```

**Receptor 2: `actualizar_asistencia`** (Líneas 13-26)

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
        registro_asistencia.verificar_asistencia()
```

**Marca asistencia como:**
- **Presente:** Si hay al menos una ENTRADA válida
- **Ausente:** Sin registros válidos en el día
- **Justificado:** Si existe Licencia aprobada

#### 3.6.2. Prevención de Recursión Infinita
**Mecanismo:** `suppress_signal()` context manager

```python
from .utils import suppress_signal

with suppress_signal():
    # Código que hace save() sin disparar señales
    registro.save(update_fields=['campo1', 'campo2'])
```

**Implementación:** Usa thread-local storage para marcar que está dentro de un signal.

---

### FASE 7: Respuesta al Frontend

#### 3.7.1. Escenario 1: Fichado Exitoso
**JSON Response:**
```json
{
    "success": true,
    "message": "REGISTRO EXITOSO: PÉREZ, JUAN - Entrada - 18/10/2025 08:15:23"
}
```

**Comportamiento en UI:** (Líneas 212-215)
```javascript
if (data.success) {
    mostrarMensaje('success', data.message);
    dniInput.value = '';  // Limpiar DNI
    dniInput.focus();     // Preparar para siguiente fichado
}
```

**Display del mensaje:**
- Clase CSS: `.success` (fondo verde)
- Duración: 30 segundos (se reinicia con interacción)
- Auto-ocultamiento: `setTimeout(30000)`

#### 3.7.2. Escenario 2: Inconsistencia Detectada
**JSON Response:**
```json
{
    "success": false,
    "inconsistencia": true,
    "descripcion_inconsistencia": "Inconsistencia: Su último movimiento fue <strong>Entrada</strong> <strong>18/10/2025 06:30:15</strong>",
    "tipo_movimiento": "entrada"
}
```

**Comportamiento en UI:** (Líneas 217-228)
```javascript
if (data.inconsistencia) {
    // Mostrar modal de confirmación
    inconsistencyMessage.innerHTML = `
        ${data.descripcion_inconsistencia}<br>
        ¿Desea fichar de todos modos?
    `;
    inconsistencyModal.style.display = 'flex';
    inconsistencyModal.dataset.tipoMovimiento = data.tipo_movimiento;
}
```

**Modal de inconsistencia:**
- Fondo oscuro semitransparente
- Botones: "Aceptar" | "Cancelar"
- Cierre: Click fuera del modal o ESC

#### 3.7.3. Escenario 3: Usuario Acepta Inconsistencia
**Evento:** Click en botón "Aceptar" del modal (Líneas 236-281)

```javascript
acceptModalButton.onclick = function () {
    const formData = new FormData();
    formData.append('dni', dni);
    formData.append('tipo_movimiento', tipoMovimiento);
    formData.append('inconsistency_override', 'True');  // ⚠️ Flag de override

    // Nueva petición AJAX con override
    fetch(..., {
        method: 'POST',
        body: formData
    })
    .then(data => {
        if (data.success) {
            mostrarMensaje('success', data.message);
            // Cerrar modal y limpiar
        }
    })
}
```

**Resultado:**
- Registro guardado con `inconsistencia=True`
- Descripción almacenada en `descripcion_inconsistencia`
- Aparece en reportes del admin con color de advertencia

---

## 4. Cálculos Automáticos Post-Fichado

### 4.1. Horas Trabajadas (Normal + Nocturnas)
**Modelo:** `Horas_trabajadas`
**Método:** `calcular_horas_trabajadas(operario, fecha)` (models.py:504-562)

**Algoritmo:**

```
1. Obtener todos los registros VÁLIDOS del operario en la fecha lógica

2. Filtrar por secuencia válida:
   - Buscar pares: ENTRADA → SALIDA
   - Ignorar transitorias en este cálculo

3. Para cada par Entrada-Salida:
   a. Redondear hora de ENTRADA (15 min configurable)
   b. Hora de SALIDA sin redondeo (hora exacta)
   c. Calcular diferencia: salida - entrada_redondeada

4. Calcular franjas horarias:
   - NORMAL: 06:00 a 20:00
   - NOCTURNA: 20:00 a 06:00 (día siguiente)

5. Sumar todas las franjas del día

6. Almacenar en tabla horas_trabajadas:
   - horas_normales: timedelta
   - horas_nocturnas: timedelta
```

**Ejemplo de cálculo:**
```
Entrada: 07:42 → Redondeada a 07:45
Salida: 17:30 → Sin redondeo

Diferencia: 17:30 - 07:45 = 9h 45min

Franjas:
- 07:45 a 17:30 → Todo en horario NORMAL (06:00-20:00)
- horas_normales = 9h 45min
- horas_nocturnas = 0h
```

**Caso con franja nocturna:**
```
Entrada: 18:15 → Redondeada a 18:15
Salida: 22:45 → Sin redondeo

Diferencia: 22:45 - 18:15 = 4h 30min

Franjas:
- 18:15 a 20:00 = 1h 45min (NORMAL)
- 20:00 a 22:45 = 2h 45min (NOCTURNA)

horas_normales = 1h 45min
horas_nocturnas = 2h 45min
```

### 4.2. Horas Extras
**Modelo:** `Horas_extras`
**Regla:** Todo lo que exceda 8 horas por día

**Algoritmo:**

```
1. Obtener horas_trabajadas del día
   total_dia = horas_normales + horas_nocturnas

2. Si total_dia > 8 horas:
   extras_brutas = total_dia - 8h

3. Redondear extras a bloques de 30 minutos:
   - 0-14 min → 0
   - 15-44 min → 30 min
   - 45-59 min → 1 hora

4. Guardar en horas_extras:
   - horas_extras_50: extras redondeadas
   - fecha: fecha lógica
```

**Ejemplo:**
```
Día trabajado: 10h 25min
Extras brutas: 10h 25min - 8h = 2h 25min
Redondeo (30 min): 2h 30min

horas_extras_50 = 2h 30min
```

### 4.3. Horas Totales Mensuales
**Modelo:** `Horas_totales`
**Método:** `calcular_horas_totales(operario, mes)` (formato: 'YYYY-MM')

**Agregación:**

```sql
SELECT
    SUM(horas_normales) as total_normales,
    SUM(horas_nocturnas) as total_nocturnas
FROM horas_trabajadas
WHERE operario_id = ?
  AND fecha >= '2025-10-01'
  AND fecha < '2025-11-01'
```

**Campos almacenados:**
- `total_horas_normales`
- `total_horas_nocturnas`
- `total_horas_extras` (suma de `horas_extras` del mes)
- `mes`: '2025-10'

---

## 5. Configuraciones de Redondeo

### 5.1. Redondeo de Entrada
**Función:** `redondear_entrada(hora_fichada)` (models.py:61-85)
**Modelo de configuración:** `ConfiguracionRedondeo`

**Valores por defecto:**
```python
intervalo_redondeo = 15  # minutos
redondear_hacia_arriba = False
```

**Algoritmo:**
```python
minutos_totales = hora.hour * 60 + hora.minute

if redondear_hacia_arriba:
    minutos_redondeados = ceil(minutos_totales / intervalo) * intervalo
else:
    # Redondeo al más cercano
    minutos_redondeados = round(minutos_totales / intervalo) * intervalo
```

**Ejemplos con intervalo=15:**
```
08:03 → 08:00 (más cercano)
08:08 → 08:15 (más cercano)
08:12 → 08:15 (más cercano)
08:22 → 08:15 (más cercano)
```

### 5.2. Redondeo de Salida
**Función:** `redondear_salida(hora_fichada)` (models.py:87-106)
**Modelo de configuración:** `ConfiguracionRedondeoSalida`

**Valor por defecto:**
```python
redondeo_minutos = 60  # Redondear a la hora
tipo_redondeo = 'floor'  # Hacia abajo
```

**Algoritmo:**
```python
if tipo_redondeo == 'floor':
    # Redondear hacia abajo a la hora completa
    return hora.replace(minute=0, second=0, microsecond=0)
```

**Ejemplos:**
```
17:58 → 17:00
18:15 → 18:00
18:45 → 18:00
19:59 → 19:00
```

---

## 6. Manejo de Inconsistencias

### 6.1. Tipos de Inconsistencias Detectadas

| Código | Descripción | Ejemplo | Permite Override |
|--------|-------------|---------|------------------|
| INC-001 | Doble entrada sin salida intermedia | ENTRADA → ENTRADA | ✅ Sí |
| INC-002 | Salida sin entrada en el día | Primera fichada es SALIDA | ✅ Sí |
| INC-003 | Transitoria sin entrada previa | SALIDA_TRANS sin ENTRADA | ✅ Sí |
| INC-004 | Hora anterior a último registro | Fichado retroactivo | ⚠️ Advertencia |

### 6.2. Flujo de Manejo de Inconsistencias

```
Usuario intenta fichar
        │
        ▼
┌───────────────────┐
│ Validar secuencia │
└────────┬──────────┘
         │
    ┌────┴────┐
    │Válido?  │
    └────┬────┘
         │
    ┌────┴────┐
    NO        SÍ
    │         │
    ▼         ▼
┌─────────┐  ┌──────────┐
│ Mostrar │  │ Guardar  │
│ Modal   │  │ directo  │
└────┬────┘  └──────────┘
     │
  ┌──┴──┐
  │Acepta?│
  └──┬──┘
     │
  ┌──┴──┐
  SÍ    NO
  │     │
  ▼     ▼
┌────────┐ ┌────────┐
│Guardar │ │Cancelar│
│con flag│ │        │
└────────┘ └────────┘
```

### 6.3. Registro de Inconsistencias

**Tabla:** `reloj_fichador_registrodiario`
**Campos específicos:**
- `inconsistencia = True`
- `descripcion_inconsistencia = "Detalle del problema"`
- `valido = True` (se incluye en cálculos)

**Ejemplo de descripción:**
```
"El operario PÉREZ, JUAN registró 2 veces el movimiento Entrada."
```

**Visualización en admin:**
- Filas con fondo amarillo claro
- Icono de advertencia (⚠️)
- Descripción en tooltip
- Filtro dedicado: "Con inconsistencias"

---

## 7. Seguridad y Prevención de Errores

### 7.1. Protección CSRF
**Cookie personalizada:** `fichador_csrf`

```python
# settings.py
CSRF_COOKIE_NAME = 'fichador_csrf'
CSRF_COOKIE_HTTPONLY = False  # Accesible desde JS
CSRF_COOKIE_SAMESITE = 'Strict'
```

**Validación en cada request:**
```javascript
headers: {
    'X-CSRFToken': getCookie('csrftoken')
}
```

### 7.2. Validación de DNI

**Frontend:**
```javascript
// Solo permite dígitos numéricos
this.value = this.value.replace(/[^0-9]/g, '');
```

**Backend:**
```python
try:
    operario = Operario.objects.get(dni=dni)
except Operario.DoesNotExist:
    return JsonResponse({
        'success': False,
        'message': "OPERARIO NO ENCONTRADO ⚠️"
    }, status=404)
```

### 7.3. Prevención de Inyección SQL
- **ORM de Django:** Todas las consultas usan QuerySet API
- **Parámetros preparados:** Automático en Django ORM
- **Escape de HTML:** Templates auto-escapan por defecto

### 7.4. Logging y Auditoría

**Logger configurado:** `apps.reloj_fichador`

```python
logger.info(f"Registro creado exitosamente: {success_message}")
logger.warning(f"Inconsistencia detectada: {descripcion}")
logger.error(f"Operario con DNI={dni} no encontrado.")
logger.exception(f"Excepción inesperada: {e}")
```

**Historial completo:**
```python
# django-simple-history
RegistroDiario.history.all()  # Todos los cambios históricos
```

---

## 8. Performance y Optimización

### 8.1. Consultas Optimizadas

**Evitar N+1 queries:**
```python
# En views.py
operarios = Operario.objects.prefetch_related('areas').all()
horas_trabajadas = Horas_trabajadas.objects.select_related('operario').all()
```

### 8.2. Índices de Base de Datos

```python
class Meta:
    indexes = [
        models.Index(fields=['operario']),
        models.Index(fields=['hora_fichada']),
        models.Index(fields=['operario', 'hora_fichada']),
    ]
```

### 8.3. Caché y Sincronización

**Reloj del cliente:**
- Sincroniza cada 5 minutos con servidor
- Calcula offset para compensar latencia
- Actualiza display localmente cada segundo (sin network)

**Clima:**
- Cache implícito: actualiza cada 10 minutos
- API externa: OpenWeatherMap

---

## 9. Diagrama de Flujo Completo

```
┌──────────────────────────────────────────────────────────────────┐
│                    INTERFAZ DE USUARIO                           │
│                                                                  │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐                │
│  │   Q    │  │   Z    │  │   M    │  │   P    │                │
│  │ Entrada│  │Sal.Tran│  │Ent.Tran│  │ Salida │                │
│  └───┬────┘  └───┬────┘  └───┬────┘  └───┬────┘                │
│      └───────────┴───────────┴───────────┘                      │
│                         │                                        │
│                         ▼                                        │
│              ┌──────────────────┐                                │
│              │  Ingreso de DNI  │                                │
│              └────────┬─────────┘                                │
│                       │                                          │
│                       ▼                                          │
│              ┌──────────────────┐                                │
│              │  Submit (AJAX)   │                                │
│              └────────┬─────────┘                                │
└───────────────────────┼──────────────────────────────────────────┘
                        │
                        │ POST /registrar_movimiento/<tipo>/
                        │ Headers: X-CSRFToken
                        │ Body: {dni, tipo_movimiento}
                        │
                        ▼
┌──────────────────────────────────────────────────────────────────┐
│                         BACKEND (Django)                         │
│                                                                  │
│  ┌────────────────────────────────────────────────────┐         │
│  │ views.registrar_movimiento_tipo()                  │         │
│  │                                                     │         │
│  │ 1. Verificar AJAX request                          │         │
│  │ 2. Obtener operario por DNI                        │         │
│  │ 3. Capturar hora actual (timezone Argentina)       │         │
│  │ 4. Crear instancia RegistroDiario                  │         │
│  └──────────────────────┬─────────────────────────────┘         │
│                         │                                        │
│                         ▼                                        │
│  ┌────────────────────────────────────────────────────┐         │
│  │ models.RegistroDiario.full_clean()                 │         │
│  │                                                     │         │
│  │ • Normalizar zona horaria                          │         │
│  │ • Calcular fecha lógica (turnos nocturnos)         │         │
│  │ • Validar secuencia de movimientos                 │         │
│  │ • Verificar inconsistencias                        │         │
│  └──────────────────────┬─────────────────────────────┘         │
│                         │                                        │
│                    ┌────┴────┐                                   │
│                    │ Válido? │                                   │
│                    └────┬────┘                                   │
│                         │                                        │
│                ┌────────┴────────┐                               │
│                │                 │                               │
│               SÍ                NO                               │
│                │                 │                               │
│                ▼                 ▼                               │
│  ┌──────────────────┐  ┌─────────────────────┐                 │
│  │ registro.save()  │  │ raise ValidationError│                 │
│  └────────┬─────────┘  └──────────┬──────────┘                 │
│           │                       │                              │
│           │                       ▼                              │
│           │            ┌──────────────────────┐                 │
│           │            │ JsonResponse(        │                 │
│           │            │   inconsistencia=True│                 │
│           │            │ )                    │                 │
│           │            └──────────┬───────────┘                 │
│           │                       │                              │
│           │                       │ Frontend muestra modal       │
│           │                       │                              │
│           │                       ▼                              │
│           │            ┌──────────────────────┐                 │
│           │            │ Usuario acepta?      │                 │
│           │            └──────────┬───────────┘                 │
│           │                       │                              │
│           │                  ┌────┴────┐                        │
│           │                  │         │                        │
│           │                 SÍ        NO                        │
│           │                  │         │                        │
│           │                  ▼         ▼                        │
│           │       ┌─────────────┐  ┌────────┐                  │
│           │       │save(        │  │Cancelar│                  │
│           │       │inconsistencia=True)  └────┘                │
│           │       └──────┬──────┘                               │
│           └──────────────┘                                      │
│                   │                                             │
└───────────────────┼─────────────────────────────────────────────┘
                    │
                    │ TRIGGERS (Django Signals)
                    │
                    ▼
┌──────────────────────────────────────────────────────────────────┐
│              CÁLCULOS AUTOMÁTICOS (signals.py)                   │
│                                                                  │
│  post_save(RegistroDiario)                                      │
│          │                                                       │
│          ├─► Signal 1: actualizar_asistencia()                  │
│          │   └─► RegistroAsistencia.verificar_asistencia()      │
│          │       └─► Marca: Presente/Ausente/Justificado        │
│          │                                                       │
│          └─► Signal 2: actualizar_horas_despues_de_guardar()    │
│              │                                                   │
│              ├─► 1. Horas_trabajadas.calcular_horas_trabajadas()│
│              │   └─► Calcula normales (06-20h) y nocturnas      │
│              │                                                   │
│              ├─► 2. Horas_extras.calcular_horas_extras()        │
│              │   └─► Si > 8h → Redondea a bloques de 30min      │
│              │                                                   │
│              ├─► 3. Recortar Horas_trabajadas a 8h max          │
│              │   └─► Distribuir proporcionalmente                │
│              │                                                   │
│              └─► 4. Horas_totales.calcular_horas_totales()      │
│                  └─► Suma mensual de todas las horas            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
                    │
                    │ Respuesta JSON
                    │
                    ▼
┌──────────────────────────────────────────────────────────────────┐
│                    RESPUESTA AL FRONTEND                         │
│                                                                  │
│  ┌────────────────────────────────────────────────────┐         │
│  │ JsonResponse({                                     │         │
│  │   'success': true,                                 │         │
│  │   'message': 'REGISTRO EXITOSO: PÉREZ, JUAN ...'  │         │
│  │ })                                                 │         │
│  └──────────────────────┬─────────────────────────────┘         │
│                         │                                        │
│                         ▼                                        │
│              ┌──────────────────────┐                           │
│              │ mostrarMensaje()     │                           │
│              │ - Fondo verde        │                           │
│              │ - Duración: 30s      │                           │
│              └──────────────────────┘                           │
│                         │                                        │
│                         ▼                                        │
│              ┌──────────────────────┐                           │
│              │ Limpiar campo DNI    │                           │
│              │ Preparar para nueva  │                           │
│              │ fichada              │                           │
│              └──────────────────────┘                           │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 10. Casos de Uso Documentados

### Caso 1: Jornada Normal Simple
```
Operario: PÉREZ, JUAN (DNI: 12345678)
Fecha: 18/10/2025

08:12 → ENTRADA
    Redondeada a: 08:15

17:45 → SALIDA
    Sin redondeo: 17:45

Cálculos:
- Horas trabajadas: 17:45 - 08:15 = 9h 30min
- Horas normales: 9h 30min (todo en franja 06:00-20:00)
- Horas nocturnas: 0h
- Horas extras: 9h 30min - 8h = 1h 30min (redondeado: 1h 30min)

Resultado BD:
RegistroDiario: 2 registros (entrada, salida)
Horas_trabajadas: horas_normales=9.5h, horas_nocturnas=0h
Horas_extras: horas_extras_50=1.5h
RegistroAsistencia: estado='presente'
```

### Caso 2: Turno Nocturno
```
Operario: GÓMEZ, MARÍA (DNI: 23456789)
Fecha lógica: 18/10/2025

18/10 22:15 → ENTRADA
    Redondeada a: 22:15

19/10 06:30 → SALIDA
    Sin redondeo: 06:30
    Fecha lógica: 18/10 (pertenece al día anterior)

Cálculos:
- Horas trabajadas: 06:30 - 22:15 = 8h 15min
- Horas normales: 0h
- Horas nocturnas: 8h 15min (franja 20:00-06:00)
- Horas extras: 8h 15min - 8h = 15min → Redondeado: 0h

Resultado BD:
Ambos registros con fecha_logica = 18/10/2025
Horas_trabajadas: horas_normales=0h, horas_nocturnas=8.25h
Horas_extras: horas_extras_50=0h
RegistroAsistencia (18/10): estado='presente'
```

### Caso 3: Jornada con Salida Transitoria
```
Operario: LÓPEZ, CARLOS (DNI: 34567890)
Fecha: 18/10/2025

08:05 → ENTRADA
    Redondeada a: 08:00

12:30 → SALIDA TRANSITORIA
    (Pausa para almuerzo)

13:45 → ENTRADA TRANSITORIA
    (Regreso de almuerzo)

17:15 → SALIDA
    Sin redondeo: 17:15

Cálculos:
- Ciclo 1: 12:30 - 08:00 = 4h 30min
- Ciclo 2: 17:15 - 13:45 = 3h 30min
- Total: 4h 30min + 3h 30min = 8h 0min
- Horas normales: 8h (todo en franja 06:00-20:00)
- Horas extras: 0h

Resultado BD:
RegistroDiario: 4 registros
Horas_trabajadas: horas_normales=8h, horas_nocturnas=0h
Horas_extras: horas_extras_50=0h
```

### Caso 4: Inconsistencia Detectada y Aceptada
```
Operario: MARTÍNEZ, ANA (DNI: 45678901)
Fecha: 18/10/2025

08:15 → ENTRADA (✅ OK)

08:45 → ENTRADA (❌ Inconsistencia)
    Mensaje: "Su último movimiento fue Entrada 08:15:00"
    Usuario: Acepta override

17:30 → SALIDA (✅ OK)

Cálculos:
- Ignora segunda ENTRADA en cálculo de horas
- Usa: 17:30 - 08:15 = 9h 15min
- Horas normales: 9h 15min
- Horas extras: 1h 15min → Redondeado: 1h 30min

Resultado BD:
RegistroDiario: 3 registros
  - #1: ENTRADA (inconsistencia=False)
  - #2: ENTRADA (inconsistencia=True, descripcion="...")
  - #3: SALIDA (inconsistencia=False)

Horas_trabajadas: Calcula usando solo #1 y #3
```

---

## 11. Puntos Críticos de Mejora Identificados

### 11.1. Rendimiento
- **Optimización de signals:** Actualmente dispara múltiples recalculos. Considerar batch processing.
- **Cache de configuraciones:** `ConfiguracionRedondeo` se consulta en cada fichado.

### 11.2. Validaciones
- **Fechas retroactivas:** Actualmente genera solo advertencias, considerar bloqueo configurable.
- **Límite de horas diarias:** No hay validación de jornadas extremadamente largas (>16h).

### 11.3. UX/UI
- **Confirmación visual:** Agregar sonido o vibración en dispositivos móviles al fichar exitosamente.
- **Historial inmediato:** Mostrar últimas 3 fichadas del operario después de fichar.

### 11.4. Seguridad
- **Rate limiting:** Implementar límite de intentos de fichado por minuto.
- **Verificación 2FA (opcional):** Para operarios con permisos especiales.

---

## 12. Tecnologías y Bibliotecas Utilizadas

| Componente | Tecnología | Versión | Uso |
|------------|-----------|---------|-----|
| Backend Framework | Django | 5.0.7 | Framework principal |
| Base de Datos | PostgreSQL | 15 | Persistencia |
| ORM | Django ORM | Built-in | Consultas y modelos |
| Zona Horaria | pytz | 2024.1 | Manejo de timezones |
| Auditoría | django-simple-history | 3.7.0 | Historial de cambios |
| Admin Interface | django-unfold | 0.42.0 | Interface moderna |
| Frontend | JavaScript ES6 + jQuery | 3.6.0 | Interactividad |
| HTTP Client | Fetch API | Nativo | Requests AJAX |
| Logging | Python logging | Built-in | Trazabilidad |

---

## 13. Conclusiones

El sistema de fichado implementado es robusto y cuenta con múltiples capas de validación y cálculo automático. Los puntos destacados son:

### Fortalezas
1. **Validación en múltiples niveles:** Frontend + Backend + Modelo
2. **Manejo de inconsistencias:** Permite override con registro de auditoría
3. **Cálculos automáticos:** Signals disparan recalculos en cascada
4. **Experiencia de usuario:** Interfaz simple, atajos de teclado, foco automático
5. **Auditoría completa:** django-simple-history registra todos los cambios
6. **Timezone-aware:** Manejo correcto de zonas horarias y turnos nocturnos

### Áreas de Mejora
1. **Performance de signals:** Optimizar cascada de recalculos
2. **Validaciones configurables:** Permitir ajustar restricciones por operario/área
3. **Cache estratégico:** Reducir consultas a configuraciones
4. **Tests automatizados:** Expandir cobertura de casos edge
5. **Documentación de API:** Generar especificación OpenAPI/Swagger

---

**Documento generado por:** Claude Code
**Basado en análisis de:**
- `templates/reloj_fichador/base.html`
- `templates/reloj_fichador/home.html`
- `apps/reloj_fichador/views.py`
- `apps/reloj_fichador/models.py`
- `apps/reloj_fichador/signals.py`

**Próxima revisión:** Al implementar cambios significativos en el flujo de fichado
