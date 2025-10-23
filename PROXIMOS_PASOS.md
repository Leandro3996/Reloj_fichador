# 📋 Próximos Pasos - Reloj Fichador

**Fecha**: 23 de Octubre 2025
**Estado**: Planificación
**Prioridad**: ALTA

---

## 🎯 Objetivo Principal

Refinar el cálculo de horas de enfermedad para **excluir días no laborales** (domingos y feriados).

### Regla de Negocio Crítica

Cuando un operario tiene **licencia médica**:
- ✅ Se cuentan SOLO los **días laborales** (lunes a viernes, sin feriados)
- ❌ NO se cuentan los **domingos**
- ❌ NO se cuentan los **feriados** (días no laborables)
- 🔄 Los feriados se registran como **"horas_feriado"**, no como **"horas_enfermedad"**

**Ejemplo:**
```
Licencia médica: 5 días (Lunes 27 - Viernes 31 de Octubre)
├─ Lunes 27 (laboral)      → 8 horas enfermedad ✅
├─ Martes 28 (laboral)     → 8 horas enfermedad ✅
├─ Miércoles 29 (laboral)  → 8 horas enfermedad ✅
├─ Jueves 30 (laboral)     → 8 horas enfermedad ✅
└─ Viernes 31 (feriado)    → 8 horas feriado ❌ (NO enfermedad)
   Total: 32 horas enfermedad + 8 horas feriado
```

---

## 📊 Análisis Actual

### Estado Presente (Octubre 2025)

El sistema **actualmente cuenta ALL días** sin distinción:
- ❌ No diferencia entre días laborales y no laborales
- ❌ No considera feriados
- ❌ No considera domingos
- ✅ Fórmula simple: `dias × 8 horas` (en tasks.py:96-98)

**Ejemplo del error actual:**
```python
# Licencia: 5 días (incluye 1 domingo + 1 feriado)
duracion_dias = 5
horas_enfermedad_total = timedelta(hours=5 * 8)  # 40 horas ❌
# Debería ser: 24 horas (3 días laborales × 8)
```

---

## 🔧 Cambios Requeridos

### 1. **Crear Calendario Laboral** (Nueva Tabla)
**Ubicación**: `apps/reloj_fichador/models.py`

```python
class CalendarioLaboral(models.Model):
    """Define qué días son laborables y cuáles son feriados"""
    fecha = models.DateField(unique=True, db_index=True)
    es_laborable = models.BooleanField(
        default=True,
        help_text="True = día laboral, False = feriado/no laboral"
    )
    descripcion = models.CharField(
        max_length=200,
        blank=True,
        help_text="Ej: 'Día de Difuntos', 'Feriado Nacional'"
    )

    class Meta:
        verbose_name = "Día Laboral"
        verbose_name_plural = "Calendario Laboral"
        ordering = ['fecha']
        indexes = [
            models.Index(fields=['fecha', 'es_laborable']),
        ]

    def __str__(self):
        tipo = "Laboral" if self.es_laborable else "No Laboral"
        return f"{self.fecha} - {tipo} {self.descripcion}"
```

### 2. **Crear Función: `calcular_horas_enfermedad_laborales()`**
**Ubicación**: `apps/reloj_fichador/models.py` o `utils.py`

```python
def calcular_horas_enfermedad_laborales(fecha_inicio, fecha_fin):
    """
    Calcula horas de enfermedad contando SOLO días laborales.

    Args:
        fecha_inicio (date): Primer día de licencia
        fecha_fin (date): Último día de licencia

    Returns:
        timedelta: Horas enfermedad (solo días laborales)

    Lógica:
        1. Iterar cada día entre fecha_inicio y fecha_fin (inclusive)
        2. Excluir domingos (weekday() == 6)
        3. Consultar CalendarioLaboral para feriados
        4. Contar solo días que sean laborables
        5. Multiplicar por 8 horas
    """
    dias_laborales = 0
    fecha_actual = fecha_inicio

    while fecha_actual <= fecha_fin:
        # Excluir domingos (Sunday = 6)
        if fecha_actual.weekday() != 6:
            # Verificar si es feriado en CalendarioLaboral
            try:
                dia_calendario = CalendarioLaboral.objects.get(fecha=fecha_actual)
                if dia_calendario.es_laborable:
                    dias_laborales += 1
            except CalendarioLaboral.DoesNotExist:
                # Si no está en calendario, asumir que es laboral
                dias_laborales += 1

        fecha_actual += timedelta(days=1)

    return timedelta(hours=dias_laborales * 8)
```

### 3. **Actualizar `procesar_licencia_aprobada()` Task**
**Ubicación**: `apps/reloj_fichador/tasks.py:96-98`

**ANTES:**
```python
duracion_dias = (licencia.fecha_fin - licencia.fecha_inicio).days + 1
horas_enfermedad_total = timedelta(hours=duracion_dias * 8)
```

**DESPUÉS:**
```python
# Usar nueva función que solo cuenta días laborales
from .utils import calcular_horas_enfermedad_laborales
horas_enfermedad_total = calcular_horas_enfermedad_laborales(
    licencia.fecha_inicio,
    licencia.fecha_fin
)
```

### 4. **Actualizar Admin para CalendarioLaboral**
**Ubicación**: `apps/reloj_fichador/admin.py`

```python
@admin.register(CalendarioLaboral)
class CalendarioLaboralAdmin(UnfoldModelAdmin):
    list_display = ['fecha', 'es_laborable', 'descripcion']
    list_filter = ['es_laborable', 'fecha']
    search_fields = ['descripcion']
    date_hierarchy = 'fecha'

    fieldsets = (
        ('Información', {
            'fields': ('fecha', 'es_laborable')
        }),
        ('Descripción', {
            'fields': ('descripcion',)
        }),
    )
```

### 5. **Crear Migration**
```bash
docker compose exec web python manage.py makemigrations reloj_fichador
docker compose exec web python manage.py migrate
```

### 6. **Crear Management Command: `cargar_calendario_laboral.py`**
**Ubicación**: `apps/reloj_fichador/management/commands/cargar_calendario_laboral.py`

```python
"""
Carga el calendario laboral para un año específico.
Incluye feriados nacionales de Argentina.
"""

from django.core.management.base import BaseCommand
from apps.reloj_fichador.models import CalendarioLaboral
from datetime import date, timedelta

FERIADOS_ARGENTINA_2025 = {
    (1, 1): "Año Nuevo",
    (2, 10): "Día de los Mártires",
    (2, 17): "Carnaval",
    (2, 18): "Carnaval",
    (4, 2): "Malvinas",
    (5, 1): "Día del Trabajo",
    (5, 25): "Revolución de Mayo",
    (6, 20): "Día de la Bandera",
    (7, 9): "Independencia",
    (8, 17): "Muerte del Gral. San Martín",
    (10, 12): "Día de la Raza",
    (11, 17): "Muerte del Gral. Güemes",
    (12, 8): "Inmaculada Concepción",
    (12, 25): "Navidad",
}

class Command(BaseCommand):
    help = "Carga el calendario laboral (feriados) para Argentina"

    def add_arguments(self, parser):
        parser.add_argument('--year', type=int, default=2025)

    def handle(self, *args, **options):
        year = options['year']
        # Cargar todos los feriados...
        self.stdout.write(f"Cargados feriados para {year}")
```

---

## 🧪 Tests Requeridos

### Test 1: `test_horas_enfermedad_excluye_domingos`
```python
def test_horas_enfermedad_excluye_domingos(self):
    """
    Licencia de 5 días que incluye 1 domingo.
    Debe contar solo 4 días laborales = 32 horas.
    """
    # Lunes 27 - Viernes 31 de Octubre 2025
    # Incluye domingo 26 de octubre (fuera del rango)
    # Resultado: 5 días laborales = 40 horas ✓
```

### Test 2: `test_horas_enfermedad_excluye_feriados`
```python
def test_horas_enfermedad_excluye_feriados(self):
    """
    Licencia que incluye día de feriado.
    El feriado se registra como horas_feriado, NO horas_enfermedad.
    """
    # Licencia incluye 31 Oct (feriado de Día de Difuntos)
    # Debe contar solo días laborales
    # Debe registrar horas_feriado por separado
```

### Test 3: `test_horas_enfermedad_con_feriado_nacional`
```python
def test_horas_enfermedad_con_feriado_nacional(self):
    """
    Licencia médica que cruza feriado nacional (Día del Trabajo, etc).
    """
    # Mayo 1-5 (incluye 1 May = Día del Trabajo)
    # Debe contar: 4 días laborales = 32 horas enfermedad
    #              1 día feriado = 8 horas feriado
```

---

## 📋 Plan de Implementación

### Fase 1: Setup (1-2 horas)
- [ ] Crear modelo CalendarioLaboral
- [ ] Crear migration
- [ ] Crear admin para CalendarioLaboral

### Fase 2: Lógica (2-3 horas)
- [ ] Crear función `calcular_horas_enfermedad_laborales()`
- [ ] Actualizar `procesar_licencia_aprobada()` en tasks.py
- [ ] Manejar casos edge (domingos, feriados)

### Fase 3: Data (1 hora)
- [ ] Crear management command para cargar calendario
- [ ] Cargar feriados Argentina 2025-2026
- [ ] Verificar domingos automáticamente

### Fase 4: Testing (2 horas)
- [ ] Tests unitarios (3 tests mínimo)
- [ ] Verificar con datos reales
- [ ] Procesar licencias históricas nuevamente

### Fase 5: Verificación (1 hora)
- [ ] Ejecutar tests
- [ ] Verificar reportes actualizados
- [ ] Validar con casos reales (Pizarro, Morales)

---

## 🔄 Casos de Uso a Validar

### Caso 1: Licencia con Sunday
```
Licencia: Oct 27-31, 2025 (Lun-Vie)
Domingos en rango: Ninguno
Resultado: 5 días × 8h = 40h enfermedad ✓
```

### Caso 2: Licencia con Domingo
```
Licencia: Oct 25-31, 2025 (Sab-Vie)
├─ Sábado 25: No laboral (skip)
├─ Domingo 26: No laboral (skip)
├─ Lun-Vie 27-31: 5 días laborales
Resultado: 5 días × 8h = 40h enfermedad ✓
```

### Caso 3: Licencia con Feriado
```
Licencia: Apr 30 - May 5, 2025
├─ Mié 30: Laboral (8h enfermedad)
├─ Jue 1 (May): Feriado "Día del Trabajo" (8h feriado)
├─ Vie 2: Laboral (8h enfermedad)
├─ Sábado 3: No laboral
├─ Domingo 4: No laboral
├─ Lunes 5: Laboral (8h enfermedad)
Resultado: 24h enfermedad + 8h feriado ✓
```

### Caso 4: Licencia Larga con Múltiples Feriados
```
Licencia: 30 días (incluye múltiples domingos y 3 feriados)
Cálculo: Solo contar días laborales
Ejemplo: 22 días laborales = 176h enfermedad
```

---

## 📝 Notas Importantes

### Integración con Sistemas Existentes

1. **RegistroAsistencia**
   - Los domingos y feriados ya tienen registros de RegistroAsistencia
   - La licencia médica debe REEMPLAZAR esos registros
   - El estado_asistencia debe cambiar según el tipo de día

2. **Horas_totales**
   - Necesita campos separados para auditar:
     - `horas_enfermedad` (solo días laborales de licencia)
     - `horas_feriado` (días feriados durante licencia)
   - Total de licencia = horas_enfermedad + horas_feriado

3. **Retroactividad**
   - El algoritmo de retroactividad debe considerar:
     - Solo justificar ausencias en días laborales
     - No justificar ausencias en domingos/feriados

4. **Reportes**
   - Mostrar ambas columnas: "Horas Enfermedad" y "Horas Feriado"
   - Sumar correctamente en totales mensuales

---

## 🎓 Referencia de Código

### Detectar Domingos
```python
from datetime import date, timedelta

def es_domingo(fecha):
    """Retorna True si es domingo (weekday == 6)"""
    return fecha.weekday() == 6

# Uso
fecha = date(2025, 10, 26)
if es_domingo(fecha):
    print("Es domingo")  # True
```

### Iterar Rango de Fechas
```python
fecha_inicio = date(2025, 10, 27)
fecha_fin = date(2025, 10, 31)

fecha_actual = fecha_inicio
while fecha_actual <= fecha_fin:
    print(fecha_actual)  # Imprime cada día
    fecha_actual += timedelta(days=1)
```

### Nombres de Días
```python
DIAS_SEMANA = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo",
}

fecha = date(2025, 10, 26)
print(DIAS_SEMANA[fecha.weekday()])  # "Domingo"
```

---

## 📞 Contacto y Preguntas

**Preguntas a resolver antes de implementar:**

1. ¿Qué feriados se deben considerar?
   - [ ] Feriados nacionales de Argentina
   - [ ] Feriados provinciales específicos
   - [ ] Días no laborables personalizados

2. ¿Qué sucede si un operario tiene licencia en domingo?
   - ¿Se le descuenta el domingo?
   - ¿O se cuenta solo a partir del lunes?

3. ¿Los sábados se consideran laborales?
   - ¿O la mayoría de operarios trabaja Lun-Vie?

4. ¿Necesita retroactividad para las licencias históricas?
   - ¿Ejecutar `procesar_licencias_pendientes` de nuevo?

---

## ✅ Checklist Final

- [ ] Modelo CalendarioLaboral creado
- [ ] Migration aplicada
- [ ] Admin funcional para calendario
- [ ] Función calcular_horas_enfermedad_laborales() implementada
- [ ] tasks.py actualizado
- [ ] Tests pasados (3/3)
- [ ] Management command para cargar feriados
- [ ] Feriados cargados para 2025-2026
- [ ] Licencias históricas reprocesadas
- [ ] Reportes actualizados
- [ ] Documentación creada (IMPLEMENTACION_CALENDARIO_LABORAL.md)
- [ ] Verificación en producción

---

**Estado**: 📋 LISTO PARA IMPLEMENTACIÓN
**Estimado**: 8-10 horas de desarrollo
**Prioridad**: ALTA (Afecta cálculos de nómina)

