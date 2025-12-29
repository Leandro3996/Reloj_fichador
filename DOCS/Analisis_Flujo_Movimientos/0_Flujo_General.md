# Análisis del Sistema de Fichado - Vista General

**Sistema:** Reloj Fichador - Control de Asistencia
**Versión:** 2.0 (PostgreSQL + django-admin-interface)
**Fecha:** 18 de Octubre de 2025

---

## Índice de Documentación

Este directorio contiene el análisis técnico completo del sistema de fichado, organizado por tipo de movimiento en orden secuencial:

### 📄 Documentos Disponibles

1. **[1_Entrada.md](1_Entrada.md)** - Movimiento de ENTRADA (atajo: Q)
   - Inicio de jornada laboral
   - Redondeo a 15 minutos
   - Validaciones de secuencia

2. **[2_Salida_Transitoria.md](2_Salida_Transitoria.md)** - Movimiento de SALIDA TRANSITORIA (atajo: Z)
   - Inicio de pausa durante la jornada
   - Sin redondeo (hora exacta)
   - Requiere ENTRADA previa

3. **[3_Entrada_Transitoria.md](3_Entrada_Transitoria.md)** - Movimiento de ENTRADA TRANSITORIA (atajo: M)
   - Fin de pausa, retorno al trabajo
   - Sin redondeo (hora exacta)
   - Requiere SALIDA_TRANSITORIA previa

4. **[4_Salida.md](4_Salida.md)** - Movimiento de SALIDA FINAL (atajo: P)
   - Fin de jornada laboral
   - Redondeo hacia abajo a la hora
   - Dispara TODOS los cálculos automáticos

---

## Resumen Ejecutivo

### ¿Qué es el Sistema de Fichado?

El sistema de fichado es la interfaz principal donde los operarios registran sus movimientos de entrada y salida del establecimiento. Cada "fichada" genera un registro en la base de datos que se usa para calcular horas trabajadas, horas extras y controlar asistencia.

### Tipos de Movimientos

| # | Movimiento | Atajo | Propósito | Redondeo | Siguiente Permitido |
|---|------------|-------|-----------|----------|---------------------|
| 1 | **Entrada** | Q | Inicio de jornada | ✅ 15 min | Salida o Sal.Trans |
| 2 | **Salida Transitoria** | Z | Inicio de pausa | ❌ No | Ent.Trans únicamente |
| 3 | **Entrada Transitoria** | M | Fin de pausa | ❌ No | Salida únicamente |
| 4 | **Salida** | P | Fin de jornada | ✅ A la hora ⬇️ | Entrada (próxima jornada) |

---

## Secuencias Válidas

### Jornada Simple (sin pausas)

```
┌───────────┐
│  ENTRADA  │ (Q)
│   08:00   │
└─────┬─────┘
      │
      │ [Trabajo continuo: 9 horas]
      │
      ▼
┌───────────┐
│  SALIDA   │ (P)
│   17:00   │
└───────────┘

Cálculo:
- Horas trabajadas: 9h
- Horas extras: 1h
```

### Jornada Completa (con pausa de almuerzo)

```
┌───────────┐
│  ENTRADA  │ (Q)
│   08:00   │
└─────┬─────┘
      │
      │ [Trabajo: 4h 30min]
      │
      ▼
┌─────────────────────┐
│ SALIDA TRANSITORIA  │ (Z)
│       12:30         │
└─────┬───────────────┘
      │
      │ [Pausa: 1h 15min - NO contabiliza]
      │
      ▼
┌──────────────────────┐
│ ENTRADA TRANSITORIA  │ (M)
│       13:45          │
└─────┬────────────────┘
      │
      │ [Trabajo: 3h 30min]
      │
      ▼
┌───────────┐
│  SALIDA   │ (P)
│   17:15   │
└───────────┘

Cálculo:
- Tiempo trabajado: 8h (4h30 + 3h30)
- Pausa: 1h15 (NO contabilizado)
- Horas extras: 0h
```

---

## Flujo General de una Fichada

```
┌─────────────────────────────────────┐
│   1. USUARIO PRESIONA BOTÓN         │
│      (Q, Z, M, o P)                 │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   2. INGRESA DNI                    │
│      Validación: solo números       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   3. ENVÍO AJAX AL SERVIDOR         │
│      POST /registrar_movimiento/    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   4. VALIDACIONES BACKEND           │
│      - DNI existe?                  │
│      - Secuencia válida?            │
│      - Hora lógica correcta?        │
└──────────────┬──────────────────────┘
               │
          ┌────┴────┐
          │ Válido? │
          └────┬────┘
               │
      ┌────────┴────────┐
      │                 │
     SÍ                NO
      │                 │
      ▼                 ▼
┌──────────┐    ┌───────────────┐
│ GUARDAR  │    │ MOSTRAR MODAL │
│ EN BD    │    │ ¿Continuar?   │
└────┬─────┘    └───────┬───────┘
     │                  │
     │            ┌─────┴─────┐
     │            │           │
     │           SÍ          NO
     │            │           │
     │    ┌───────┴───┐   ┌───┴────┐
     │    │ Guardar   │   │Cancelar│
     │    │ con flag  │   └────────┘
     │    └─────┬─────┘
     └──────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   5. TRIGGERS AUTOMÁTICOS           │
│      - Actualizar asistencia        │
│      - Calcular horas (si SALIDA)   │
│      - Calcular extras (si SALIDA)  │
│      - Totales mensuales            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   6. RESPUESTA AL USUARIO           │
│      Mensaje: "REGISTRO EXITOSO"    │
└─────────────────────────────────────┘
```

---

## Validaciones por Tipo de Movimiento

### ENTRADA (Q)

```
✅ Permitida si:
   - No hay registros previos (primer fichado del día)
   - Último movimiento = SALIDA (jornada anterior completa)

❌ Bloqueada si:
   - Último movimiento = ENTRADA (doble entrada)
   - Último movimiento = SALIDA_TRANSITORIA (falló registrar ENT_TRANS)
   - Último movimiento = ENTRADA_TRANSITORIA (debe cerrar con SALIDA)
```

### SALIDA TRANSITORIA (Z)

```
✅ Permitida si:
   - Existe ENTRADA previa en la jornada
   - Último movimiento = ENTRADA (inicio de primera pausa)

❌ Bloqueada si:
   - No existe ENTRADA previa
   - Último movimiento = SALIDA_TRANSITORIA (doble salida trans)
   - Último movimiento = ENTRADA_TRANSITORIA (debe cerrar con SALIDA)
   - Último movimiento = SALIDA (jornada ya cerrada)
```

### ENTRADA TRANSITORIA (M)

```
✅ Permitida si:
   - Existe ENTRADA inicial en la jornada
   - Último movimiento = SALIDA_TRANSITORIA (fin de pausa)

❌ Bloqueada si:
   - No existe ENTRADA inicial
   - Último movimiento = ENTRADA (debe registrar SAL_TRANS primero)
   - Último movimiento = ENTRADA_TRANSITORIA (doble entrada trans)
   - Último movimiento = SALIDA (jornada ya cerrada)
```

### SALIDA FINAL (P)

```
✅ Permitida si:
   - Existe ENTRADA en el día (fecha lógica)
   - Último movimiento = ENTRADA (jornada simple)
   - Último movimiento = ENTRADA_TRANSITORIA (jornada con pausa)

❌ Bloqueada si:
   - No existe ENTRADA en el día
   - Último movimiento = SALIDA_TRANSITORIA (falta ENT_TRANS)
   - Último movimiento = SALIDA (doble salida)
```

---

## Redondeos Aplicados

### Entrada (Q) - Redondeo a 15 minutos (al más cercano)

```
Configuración: intervalo_redondeo = 15 minutos

Ejemplos:
08:00 → 08:00
08:03 → 08:00
08:08 → 08:15
08:12 → 08:15
08:22 → 08:15
08:28 → 08:30
```

**Justificación:** Simplicidad administrativa y equidad (no penalizar por 2-3 minutos).

### Salida (P) - Redondeo hacia abajo a la hora

```
Configuración: redondeo_minutos = 60 (a la hora)
               tipo_redondeo = 'floor' (hacia abajo)

Ejemplos:
17:00 → 17:00
17:15 → 17:00
17:45 → 17:00
17:58 → 17:00
18:00 → 18:00
```

**Justificación:** Evitar pagar tiempo no trabajado, incentivar a no retirarse antes.

### Salida Transitoria (Z) y Entrada Transitoria (M) - SIN redondeo

```
Se usa hora exacta para calcular con precisión el tiempo de pausa.

Ejemplos:
12:30:45 → 12:30:45 (se guarda tal cual)
13:47:12 → 13:47:12 (se guarda tal cual)
```

---

## Cálculos Automáticos (Solo en SALIDA final)

### 1. Horas Trabajadas

```python
# Algoritmo simplificado
for cada par (ENTRADA, SALIDA):
    entrada_red = redondear_entrada(entrada.hora)
    salida_red = salida.hora  # Ya viene redondeada

    diferencia = salida_red - entrada_red

    # Separar en franjas
    horas_normales += tiempo_en_franja(06:00, 20:00)
    horas_nocturnas += tiempo_en_franja(20:00, 06:00)
```

**Ejemplos:**
```
Caso 1: 08:00 → 17:00
  - 9 horas → Todo normal (06:00-20:00)
  - Normales: 9h, Nocturnas: 0h

Caso 2: 18:00 → 22:00
  - 18:00→20:00: 2h normales
  - 20:00→22:00: 2h nocturnas
  - Normales: 2h, Nocturnas: 2h

Caso 3: 22:00 → 06:00 (siguiente día)
  - 8 horas → Todo nocturno
  - Normales: 0h, Nocturnas: 8h
```

### 2. Horas Extras

```python
total_dia = horas_normales + horas_nocturnas

if total_dia > 8 horas:
    extras_brutas = total_dia - 8h
    extras_redondeadas = redondear_a_bloques_30min(extras_brutas)
```

**Redondeo de extras:**
```
0-14 min → 0h
15-44 min → 30 min
45-59 min → 1h
60-89 min → 1h
90-119 min → 1h 30min
...
```

**Ejemplos:**
```
Total: 8h 10min → Extras: 0h (< 15min)
Total: 8h 25min → Extras: 30min
Total: 9h 50min → Extras: 2h
Total: 10h 20min → Extras: 2h 30min
```

### 3. Recorte de Horas Trabajadas

```python
# Después de calcular horas y extras, recortar a máximo 8h

if horas_trabajadas > 8h:
    # Distribuir proporcionalmente
    horas_normales = 8h * (normales / total)
    horas_nocturnas = 8h * (nocturnas / total)
```

**Ejemplo:**
```
Calculado inicial:
- Normales: 7h
- Nocturnas: 3h
- Total: 10h → Excede 8h

Recorte proporcional:
- Normales: 8h * (7/10) = 5h 36min
- Nocturnas: 8h * (3/10) = 2h 24min
- Total: 8h

Extras ya calculados: 2h (las que exceden 8h)
```

### 4. Totales Mensuales

```python
# Sumar todas las horas del mes
Horas_totales.update(
    total_normales += horas_normales_del_dia,
    total_nocturnas += horas_nocturnas_del_dia,
    total_extras += horas_extras_del_dia
)
```

---

## Fecha Lógica (Turnos Nocturnos)

### Concepto

Para turnos que cruzan medianoche, el sistema usa "fecha lógica" en lugar de fecha real:

```
Regla:
- Si hora < 06:00 y tipo = 'salida' → Fecha lógica = día anterior
- Si hora < 06:00 y tipo = 'entrada' → Fecha lógica = día actual
- Si hora >= 06:00 → Fecha lógica = día actual
```

### Ejemplos

```
Ejemplo 1: Turno nocturno
ENTRADA: 18/10 22:00 → fecha_lógica = 18/10
SALIDA:  19/10 06:00 → fecha_lógica = 18/10

Ambos pertenecen a la jornada del 18/10 ✅


Ejemplo 2: Entrada madrugada
ENTRADA: 19/10 05:00 → fecha_lógica = 19/10 (entrada temprana, día actual)
SALIDA:  19/10 14:00 → fecha_lógica = 19/10

Jornada completa del 19/10 ✅


Ejemplo 3: Salida madrugada (sin entrada nocturna previa)
ENTRADA: 18/10 08:00 → fecha_lógica = 18/10
SALIDA:  19/10 02:00 → fecha_lógica = 18/10 (hora < 06:00)

Jornada del 18/10 con salida a las 02:00 del 19 ✅
```

---

## Inconsistencias y Overrides

### ¿Qué es una Inconsistencia?

Es cuando el sistema detecta una secuencia de movimientos inválida pero permite continuar si el usuario acepta explícitamente.

### Proceso de Manejo

```
Usuario intenta fichar → Validación falla
                              ↓
                    ┌─────────────────┐
                    │ MOSTRAR MODAL   │
                    │                 │
                    │ "Inconsistencia │
                    │  detectada:     │
                    │  [mensaje]      │
                    │                 │
                    │ ¿Fichar igual?" │
                    └────┬───────┬────┘
                         │       │
                    [Aceptar] [Cancelar]
                         │       │
                         ▼       ▼
                    ┌────────┐ ┌────┐
                    │Guardar │ │ X  │
                    │ con    │ └────┘
                    │ flag   │
                    └────────┘
```

### Campos de Inconsistencia

```python
RegistroDiario(
    inconsistencia = True,  # Marca visual en admin
    valido = True,          # Sigue contando para cálculos
    descripcion_inconsistencia = "Detalle del problema detectado"
)
```

### Tipos Comunes

| Código | Descripción | Permite Override |
|--------|-------------|------------------|
| INC-E01 | Doble ENTRADA sin SALIDA | ✅ Sí |
| INC-E02 | ENTRADA con hora anterior al último registro | ⚠️ Advertencia |
| INC-S01 | SALIDA sin ENTRADA en el día | ✅ Sí |
| INC-ST01 | SALIDA_TRANS sin ENTRADA previa | ✅ Sí |
| INC-ST02 | Doble SALIDA_TRANS sin ENT_TRANS | ✅ Sí |
| INC-ET01 | ENT_TRANS sin SAL_TRANS previa | ✅ Sí |
| INC-ET02 | Doble ENT_TRANS sin SALIDA | ✅ Sí |

---

## Triggers Automáticos (Django Signals)

### Signal: `post_save(RegistroDiario)`

Ejecutado **inmediatamente** después de guardar cualquier fichada:

```python
@receiver(post_save, sender=RegistroDiario)
def actualizar_asistencia(sender, instance, created, **kwargs):
    """
    Marca al operario como 'presente' si existe ENTRADA válida en el día.
    """
    # EJECUTA EN: Todos los movimientos
    # TIEMPO: ~50ms

@receiver(post_save, sender=RegistroDiario)
def actualizar_horas_despues_de_guardar(sender, instance, **kwargs):
    """
    Calcula horas trabajadas, extras y totales.
    """
    # EJECUTA EN: Solo SALIDA final
    # TIEMPO: ~200-400ms
    # OPERACIONES:
    #   1. Horas_trabajadas.calcular_horas_trabajadas()
    #   2. Horas_extras.calcular_horas_extras()
    #   3. Recortar Horas_trabajadas a 8h max
    #   4. Horas_totales.calcular_horas_totales()
```

### Performance

```
Fichado ENTRADA:
  - Actualizar asistencia: 50ms
  - TOTAL: ~50ms

Fichado SALIDA:
  - Actualizar asistencia: 50ms
  - Calcular horas trabajadas: 150ms
  - Calcular horas extras: 50ms
  - Recortar horas: 20ms
  - Totales mensuales: 100ms
  - TOTAL: ~370ms
```

---

## Stack Tecnológico

### Frontend

```
- HTML5 + CSS3
- JavaScript ES6 (vanilla)
- jQuery 3.6.0 (para AJAX)
- Fetch API (requests)
- EventListener para atajos de teclado
```

### Backend

```
- Django 5.0.7
- Python 3.11
- PostgreSQL 15
- pytz (timezone handling)
- django-simple-history (auditoría)
- django-admin-interface (admin interface)
```

### Infraestructura

```
- Docker Compose
- Gunicorn (WSGI server)
- Nginx (reverse proxy)
- Celery + Redis (tareas asíncronas)
```

---

## Archivos Clave del Sistema

### Templates

```
templates/reloj_fichador/
├── base.html           → Interfaz principal de fichado
│                         (botones, reloj, modal, AJAX)
└── home.html           → Página de bienvenida
```

### Backend Python

```
apps/reloj_fichador/
├── models.py           → Modelos de datos y validaciones
│   ├── RegistroDiario (líneas 295-550)
│   ├── Horas_trabajadas (líneas 400-562)
│   ├── Horas_extras
│   └── redondear_entrada() / redondear_salida()
│
├── views.py            → Endpoints de API
│   └── registrar_movimiento_tipo() (líneas 25-103)
│
├── signals.py          → Triggers automáticos
│   ├── actualizar_asistencia() (líneas 13-26)
│   └── actualizar_horas_despues_de_guardar() (líneas 40-75)
│
└── admin.py            → Configuración Django Admin
    └── 15 ModelAdmins con django-admin-interface
```

### Configuración

```
mantenedor/
├── settings.py         → Configuración Django
│   ├── USE_TZ = True (timezone-aware)
│   ├── TIME_ZONE = 'America/Argentina/Buenos_Aires'
│   └── admin-interface (configuración del admin)
│
└── utils.py            → Utilidades para admin-interface
    ├── environment_callback()
    └── dashboard_callback()
```

---

## Tablas de Base de Datos

### Principales

```sql
reloj_fichador_registrodiario
  ├── id_registro (PK)
  ├── operario_id (FK)
  ├── hora_fichada (TIMESTAMP WITH TIMEZONE)
  ├── tipo_movimiento (VARCHAR)
  ├── inconsistencia (BOOLEAN)
  ├── valido (BOOLEAN)
  ├── dif_entrada_salida (INTERVAL)
  └── descripcion_inconsistencia (TEXT)

reloj_fichador_horas_trabajadas
  ├── id (PK)
  ├── operario_id (FK)
  ├── fecha (DATE)
  ├── horas_normales (INTERVAL)
  └── horas_nocturnas (INTERVAL)

reloj_fichador_horas_extras
  ├── id (PK)
  ├── operario_id (FK)
  ├── fecha (DATE)
  └── horas_extras_50 (INTERVAL)

reloj_fichador_horas_totales
  ├── id (PK)
  ├── operario_id (FK)
  ├── mes (VARCHAR YYYY-MM)
  ├── total_horas_normales (INTERVAL)
  ├── total_horas_nocturnas (INTERVAL)
  └── total_horas_extras (INTERVAL)

reloj_fichador_registroasistencia
  ├── id (PK)
  ├── operario_id (FK)
  ├── fecha (DATE)
  ├── estado (VARCHAR: presente/ausente/justificado)
  └── inconsistencia_asistencia (BOOLEAN)
```

### Auditoría

```sql
reloj_fichador_historicalregistrodiario
  ├── history_id (PK)
  ├── [todos los campos de RegistroDiario]
  ├── history_type ('+' create, '~' update, '-' delete)
  ├── history_date (TIMESTAMP)
  └── history_user_id (FK)
```

---

## Seguridad

### Protección CSRF

```python
# settings.py
CSRF_COOKIE_NAME = 'fichador_csrf'
CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_HTTPONLY = False  # Accesible desde JS

# En cada request AJAX
headers: {
    'X-CSRFToken': getCookie('fichador_csrf')
}
```

### Validación de Entrada

```javascript
// Frontend: Solo números
dniInput.value = dniInput.value.replace(/[^0-9]/g, '');

// Backend: Verificación de existencia
try:
    operario = Operario.objects.get(dni=dni)
except Operario.DoesNotExist:
    return 404
```

### Prevención de Inyección SQL

- **Django ORM:** Queries parametrizadas automáticamente
- **No raw SQL:** Todas las consultas usan QuerySet API
- **Escape automático:** Templates escapan HTML por defecto

---

## Monitoreo y Logging

### Niveles de Log

```python
logger.info()     # Operaciones exitosas
logger.warning()  # Inconsistencias, advertencias
logger.error()    # Operarios no encontrados
logger.exception() # Errores inesperados con traceback
```

### Ejemplos de Logs

```
INFO: Operario encontrado: PÉREZ, JUAN
INFO: Registro creado exitosamente: PÉREZ, JUAN - Entrada - 08:15:00
WARNING: Inconsistencia detectada: Doble entrada sin salida
ERROR: Operario con DNI=99999999 no encontrado
EXCEPTION: Error inesperado al calcular horas: [traceback]
```

### Métricas Disponibles

```sql
-- Fichados por hora
SELECT EXTRACT(HOUR FROM hora_fichada) as hora, COUNT(*)
FROM reloj_fichador_registrodiario
WHERE DATE(hora_fichada) = CURRENT_DATE
GROUP BY hora;

-- Tiempo promedio de procesamiento (desde logs)
-- Inconsistencias del día
-- Horas trabajadas por operario/área
```

---

## Mejoras Futuras Sugeridas

### UX/UI

1. **Confirmación visual mejorada:**
   - Sonido al fichar exitosamente
   - Vibración en dispositivos móviles
   - Animación de éxito más prominente

2. **Historial inmediato:**
   - Mostrar últimas 3 fichadas del operario
   - Tiempo trabajado parcial del día

3. **Estadísticas en tiempo real:**
   ```
   "Hoy llevas trabajadas: 4h 30min
   Tu jornada comenzó a las 08:00"
   ```

### Funcionalidad

1. **Pausas múltiples:**
   - Permitir más de un ciclo SAL_TRANS → ENT_TRANS
   - Ejemplo: almuerzo + gestión bancaria

2. **Validaciones configurables:**
   - Límite de horas diarias (alertar si > 12h)
   - Tiempo mínimo entre movimientos (evitar errores)

3. **Geolocalización (opcional):**
   - Registrar ubicación GPS al fichar
   - Validar que esté dentro del establecimiento

### Performance

1. **Cache de configuraciones:**
   - Redis para ConfiguracionRedondeo
   - Evitar consultas repetidas en cada fichado

2. **Cálculos asíncronos:**
   - Si > 50 fichados simultáneos
   - Usar Celery para cálculos en background

3. **Índices optimizados:**
   ```sql
   CREATE INDEX idx_operario_fecha_tipo
   ON reloj_fichador_registrodiario(operario_id, hora_fichada, tipo_movimiento);
   ```

### Reporting

1. **Reportes automáticos:**
   - PDF diario enviado por email al operario
   - Resumen semanal para supervisores

2. **Dashboard analytics:**
   - Tiempo promedio de pausas por área
   - Cumplimiento de horarios
   - Tendencias de horas extras

---

## Recursos y Enlaces

### Documentación Oficial

- **Django:** https://docs.djangoproject.com/
- **django-admin-interface:** https://github.com/admin-interfaceadmin/django-admin-interface
- **pytz:** https://pythonhosted.org/pytz/
- **PostgreSQL:** https://www.postgresql.org/docs/

### Documentación del Proyecto

- [Informe Ejecutivo](../Informe_Ejecutivo.md)
- [Configuración MCP PostgreSQL](../../CONFIGURACION_MCP_POSTGRESQL.md)
- [Setup PostgreSQL](../../POSTGRESQL_SETUP.md)
- [Manual django-admin-interface](../../documentacion/django-admin-interface-manual.md)

### Archivos de Referencia

```
DOCS/Analisis_Flujo_Movimientos/
├── 0_Flujo_General.md       ← ESTE DOCUMENTO
├── 1_Entrada.md
├── 2_Salida_Transitoria.md
├── 3_Entrada_Transitoria.md
└── 4_Salida.md
```

---

## Preguntas Frecuentes Generales

### ¿Qué pasa si se va la luz mientras estoy fichando?

El sistema usa transacciones de base de datos. Si falla a mitad del proceso, no se guarda nada (todo o nada). El usuario debe volver a fichar.

### ¿Puedo fichar desde el admin de Django?

Sí, pero el admin tiene validaciones más laxas para permitir correcciones manuales. Los registros creados desde admin pueden tener secuencias que no serían permitidas desde el template.

### ¿Cuánto tiempo se guardan los registros históricos?

Indefinidamente por defecto. `django-simple-history` guarda todos los cambios. Se recomienda archivar registros > 5 años.

### ¿El sistema funciona offline?

No, requiere conexión al servidor. Para entornos sin internet estable, considerar implementar service workers para queue de fichados pendientes.

### ¿Cómo se manejan los feriados?

Los feriados se marcan en el modelo `Horas_feriado`. Las horas trabajadas en feriados se calculan por separado y pueden tener recargo diferente (configuración pendiente).

---

## Contacto y Soporte

Para dudas técnicas sobre el sistema:
- Revisar esta documentación primero
- Consultar logs en `/logs/`
- Acceder al admin de Django para correcciones manuales
- Contactar al equipo de sistemas

---

**Documento generado por:** Claude Code
**Fecha:** 18 de Octubre de 2025
**Versión:** 1.0
**Última actualización:** Al crear análisis individuales de cada movimiento

---

## Navegación Rápida

**Inicio:** [Volver al índice](#índice-de-documentación)

**Documentos:**
- [1. ENTRADA →](1_Entrada.md)
- [2. SALIDA TRANSITORIA →](2_Salida_Transitoria.md)
- [3. ENTRADA TRANSITORIA →](3_Entrada_Transitoria.md)
- [4. SALIDA FINAL →](4_Salida.md)

**Proyecto:** [Volver a DOCS](../README.md)
