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

## 🔄 SINCRONIZACIÓN AUTOMÁTICA DE FERIADOS

### Sistema de Actualización Periódica

La sincronización de feriados desde la API ArgentinaDatos ahora funciona de dos formas:

#### 1️⃣ **Manual (Bajo Demanda)**

Ejecutar el comando Django manualmente cuando sea necesario:

```bash
# Sincronizar feriados del año actual
docker compose exec web python manage.py sincronizar_feriados

# Sincronizar feriados de un año específico
docker compose exec web python manage.py sincronizar_feriados 2026

# Aceptar automáticamente todas las sugerencias (sin revisión manual)
docker compose exec web python manage.py sincronizar_feriados --aceptar-todos

# Limpiar sugerencias pendientes antes de sincronizar
docker compose exec web python manage.py sincronizar_feriados --limpiar-pendientes
```

#### 2️⃣ **Automática (Celery Beat)**

La tarea Celery `sincronizar_feriados_api` se ejecuta automáticamente según la programación configurada:

**Configuración actual:**
- **Horario:** Todos los días a las 3:00 AM (Argentina)
- **Ubicación:** `mantenedor/celery.py` línea 38-44
- **Tarea:** `apps.reloj_fichador.tasks.sincronizar_feriados_api`

**Comportamiento:**
- ✅ Se conecta a ArgentinaDatos API
- ✅ Descarga feriados del año actual
- ✅ Crea sugerencias con estado "pendiente" (no auto-acepta)
- ✅ NO modifica sugerencias ya existentes
- ✅ Verifica si el feriado ya está aceptado en CalendarioLaboral
- ✅ Registra todo en logs (`logs/reloj_fichador.log`)

**Ejemplo de ejecución:**
```
2025-01-15 03:00:00 - Iniciando sincronización automática de feriados para 2025
2025-01-15 03:00:05 - Nueva sugerencia de feriado creada: 2025-02-17 - Carnaval
2025-01-15 03:00:06 - Sincronización completada: 5 nuevas sugerencias, 0 ya existentes, 15 ya aceptadas en calendario
```

### Personalización de la Programación

Para cambiar la frecuencia de sincronización, edita `mantenedor/celery.py`:

**Opciones comunes:**

```python
# Diariamente a las 3 AM (ACTUAL)
'schedule': crontab(hour=3, minute=0)

# Lunes a las 3 AM (una vez por semana)
'schedule': crontab(day_of_week=0, hour=3, minute=0)

# Primer día del mes a las 3 AM (mensual)
'schedule': crontab(day_of_month=1, hour=3, minute=0)

# Primer día de año a las 3 AM (anual)
'schedule': crontab(month=1, day=1, hour=3, minute=0)

# Cada 6 horas
'schedule': crontab(minute=0, hour='*/6')
```

### Flujo de Trabajo Recomendado

1. **Sincronización automática** (diaria) → Crea sugerencias pendientes
2. **Admin revisa** sugerencias en `/admin/reloj_fichador/sugerenciaferiado/`
3. **Admin acepta/rechaza** cada sugerencia según criterios de la empresa
4. Si se acepta → Se crea automáticamente en CalendarioLaboral
5. Si se rechaza → Se marca como rechazada con observaciones (opcional)

### Monitoreo de Sincronización

**Ver logs de Celery:**
```bash
docker compose logs -f celery
```

**Ver logs de la aplicación:**
```bash
docker compose exec web tail -f logs/reloj_fichador.log
```

**Buscar errores de sincronización:**
```bash
docker compose logs celery | grep -i "sincronizar"
```

**Verificar estado de Celery Beat:**
```bash
docker compose exec celery-beat celery -A mantenedor inspect active
```

### Requisitos para que Funcione

1. ✅ **Celery y Redis en funcionamiento**
   ```bash
   docker compose up -d celery celery-beat redis
   ```

2. ✅ **Conexión a Internet** (para la API ArgentinaDatos)
   ```bash
   curl https://api.argentinadatos.com/v1/feriados/2025
   ```

3. ✅ **Base de datos disponible**
   ```bash
   docker compose up -d db
   ```

### Troubleshooting

**La sincronización no se ejecuta:**
```bash
# Verificar que celery-beat está corriendo
docker compose ps celery-beat

# Reiniciar celery-beat
docker compose restart celery-beat

# Ver logs de celery-beat
docker compose logs celery-beat
```

**API no disponible:**
```bash
# Probando conectividad a la API
curl -I https://api.argentinadatos.com/v1/feriados/2025

# Si falla, revisar logs
docker compose logs web | grep -i "obtener_feriados_api"
```

**Sugerencias no aparecen en admin:**
```bash
# Verificar que la tarea se ejecutó
docker compose logs celery | grep "sincronizar_feriados_api"

# Contar sugerencias en la BD
docker compose exec db mysql -u root -p docker_horesdb -e "SELECT COUNT(*) FROM reloj_fichador_sugerenciaferiado;"
```

---

## ✅ CHECKLIST FINAL

- [x] Modelos creados y migrados
- [x] Funciones de validación implementadas
- [x] Admin customizado creado
- [x] Tarea Celery actualizada
- [x] Sincronización automática configurada
- [x] Tests pasados
- [x] Documentación completada
- [x] Sintaxis verificada
- [x] Imports correctos
- [x] Sin errores de migración

---

**Estado:** 🟢 LISTO PARA PRODUCCIÓN

