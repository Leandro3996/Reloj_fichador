# Mejoras en Exportación del Django Admin - Noviembre 2025

## 📅 Fecha de Implementación
**12 de Noviembre de 2025**

## 🎯 Problema Resuelto

**Problema anterior:** Al exportar datos desde el Django Admin usando `django-import-export`, los archivos Excel contenían IDs en lugar de nombres legibles:
- Operario: `23` ← (solo el ID)
- Tipo Movimiento: `entrada` ← (código interno)
- Válido: `True` ← (booleano en inglés)
- Fecha: `2025-11-12 08:30:00` ← (formato ISO)

**Solución implementada:** Ahora exporta datos en formato legible:
- Operario: `García, Juan Manuel` ← (nombre completo)
- Tipo Movimiento: `Entrada` ← (texto legible)
- Válido: `Sí` ← (español)
- Fecha: `12/11/2025 08:30:00` ← (formato español)

---

## 🛠️ Implementación Técnica

### 1. **Widgets Personalizados** (`export_widgets.py`)

Se creó un nuevo archivo con widgets reutilizables:

```python
# apps/reloj_fichador/export_widgets.py

class NombreCompletoWidget(ForeignKeyWidget):
    """Exporta "Apellido, Nombre" en vez de ID"""

class ChoiceDisplayWidget(Widget):
    """Exporta el texto legible de choices"""

class SiNoWidget(BooleanWidget):
    """Exporta "Sí"/"No" en vez de True/False"""

class FechaHoraWidget(DateTimeWidget):
    """Exporta fechas en formato dd/mm/yyyy hh:mm:ss"""

class FechaWidget(DateWidget):
    """Exporta fechas en formato dd/mm/yyyy"""

class TimeDeltaWidget(Widget):
    """Exporta timedelta en formato "08h 30m"""

class DecimalHorasWidget(Widget):
    """Exporta timedelta como decimal (8.50 horas)"""
```

**Ventajas:**
- ✅ Reutilizables en múltiples modelos
- ✅ Manejan exportación E importación automáticamente
- ✅ Código más limpio y mantenible

---

### 2. **Resources Mejorados**

Se crearon/mejoraron 3 Resources principales:

#### **RegistroDiarioResource**
```python
class RegistroDiarioResource(resources.ModelResource):
    operario = fields.Field(
        column_name='Operario',
        attribute='operario',
        widget=NombreCompletoWidget(Operario)
    )

    tipo_movimiento = fields.Field(
        column_name='Tipo de Movimiento',
        attribute='tipo_movimiento',
        widget=ChoiceDisplayWidget(RegistroDiario.TIPO_MOVIMIENTO)
    )

    hora_fichada = fields.Field(
        column_name='Fecha y Hora',
        attribute='hora_fichada',
        widget=FechaHoraWidget()
    )

    valido = fields.Field(
        column_name='Válido',
        attribute='valido',
        widget=SiNoWidget()
    )

    inconsistencia = fields.Field(
        column_name='Inconsistencia',
        attribute='inconsistencia',
        widget=SiNoWidget()
    )
```

#### **HorasTrabajadasResource**
```python
class HorasTrabajadasResource(resources.ModelResource):
    operario = fields.Field(
        column_name='Operario',
        attribute='operario',
        widget=NombreCompletoWidget(Operario)
    )

    fecha = fields.Field(
        column_name='Fecha',
        attribute='fecha',
        widget=FechaWidget()
    )

    horas_normales = fields.Field(
        column_name='Horas Normales',
        attribute='horas_normales',
        widget=TimeDeltaWidget()  # Exporta "08h 30m"
    )
```

#### **OperarioResource**
```python
class OperarioResource(resources.ModelResource):
    fecha_nacimiento = fields.Field(
        column_name='Fecha de Nacimiento',
        attribute='fecha_nacimiento',
        widget=FechaWidget()
    )

    activo = fields.Field(
        column_name='Activo',
        attribute='activo',
        widget=SiNoWidget()
    )

    area = fields.Field(
        column_name='Área',
        attribute='area',
        widget=NombreCompletoWidget(Area)
    )
```

---

### 3. **Integración en Django Admin**

Se cambió de `ExportMixin` a `ImportExportMixin` y se configuró `resource_class`:

```python
# Antes
@admin.register(Operario)
class OperarioAdmin(ExportMixin, SimpleHistoryAdmin, admin.ModelAdmin):
    pass

# Después
@admin.register(Operario)
class OperarioAdmin(ImportExportMixin, SimpleHistoryAdmin, admin.ModelAdmin):
    resource_class = OperarioResource
```

**Modelos con exportación mejorada:**
- ✅ `RegistroDiario` → Registros de entrada/salida
- ✅ `Horas_trabajadas` → Horas calculadas
- ✅ `Operario` → Datos de empleados

---

## 📊 Comparación Antes vs Después

### Exportación de RegistroDiario

**ANTES:**
| id | operario | tipo_movimiento | hora_fichada | valido |
|----|----------|----------------|--------------|--------|
| 1  | 23       | entrada        | 2025-11-12 08:30:00 | True |
| 2  | 23       | salida         | 2025-11-12 17:00:00 | True |

**DESPUÉS:**
| id | Operario | Tipo de Movimiento | Fecha y Hora | Válido |
|----|----------|-------------------|--------------|---------|
| 1  | García, Juan Manuel | Entrada | 12/11/2025 08:30:00 | Sí |
| 2  | García, Juan Manuel | Salida | 12/11/2025 17:00:00 | Sí |

### Exportación de Horas_trabajadas

**ANTES:**
| id | operario | fecha | horas_normales | horas_nocturnas |
|----|----------|-------|----------------|-----------------|
| 1  | 23       | 2025-11-12 | 0:08:30:00 | 0:00:00:00 |

**DESPUÉS:**
| id | Operario | Fecha | Horas Normales | Horas Nocturnas |
|----|----------|-------|----------------|-----------------|
| 1  | García, Juan Manuel | 12/11/2025 | 08h 30m | 00h 00m |

---

## 🎨 Características de los Widgets

### NombreCompletoWidget
- **Exportación:** Muestra "Apellido, Nombre"
- **Importación:** Acepta nombre completo, DNI o ID
- **Uso:** Para todos los campos ForeignKey de Operario, Area, etc.

### ChoiceDisplayWidget
- **Exportación:** Muestra el texto legible (display name)
- **Importación:** Acepta tanto el código como el texto (case insensitive)
- **Uso:** Para campos con choices (tipo_movimiento, estado, etc.)

### SiNoWidget
- **Exportación:** Muestra "Sí" o "No"
- **Importación:** Acepta múltiples variaciones:
  - Español: `Sí`, `Si`, `No`
  - Inglés: `Yes`, `True`, `False`
  - Números: `1`, `0`
- **Uso:** Para campos booleanos

### FechaHoraWidget
- **Exportación:** Formato `dd/mm/yyyy hh:mm:ss`
- **Importación:** Acepta múltiples formatos:
  - `dd/mm/yyyy hh:mm:ss`
  - `yyyy-mm-dd hh:mm:ss`
  - `dd-mm-yyyy hh:mm:ss`
- **Uso:** Para campos DateTime

### TimeDeltaWidget
- **Exportación:** Formato `XXh YYm` (ej: "08h 30m")
- **Importación:** Acepta:
  - `8h 30m`
  - `8:30`
  - `8.5` (decimal)
- **Uso:** Para campos de duración (horas trabajadas)

---

## 🚀 Cómo Usar la Nueva Funcionalidad

### Para Usuarios del Admin

#### Exportar Datos:
1. Ir al listado del modelo (ej: Registros Diarios)
2. Opcional: Aplicar filtros
3. Hacer clic en botón **"EXPORT"** (parte superior derecha)
4. Seleccionar formato (Excel recomendado)
5. Descargar archivo con datos legibles

#### Importar Datos:
1. Preparar archivo Excel con columnas exportadas
2. Hacer clic en botón **"IMPORT"** (parte superior derecha)
3. Seleccionar archivo
4. Revisar vista previa
5. Confirmar importación
6. El sistema recalcula automáticamente las horas

---

## 🔧 Para Desarrolladores

### Crear Resource para Nuevo Modelo

```python
from import_export import resources, fields
from .export_widgets import (
    NombreCompletoWidget, SiNoWidget, FechaWidget
)

class MiModeloResource(resources.ModelResource):
    # ForeignKey con nombre legible
    operario = fields.Field(
        column_name='Operario',
        attribute='operario',
        widget=NombreCompletoWidget(Operario)
    )

    # Booleano como Sí/No
    activo = fields.Field(
        column_name='Activo',
        attribute='activo',
        widget=SiNoWidget()
    )

    # Fecha en formato español
    fecha = fields.Field(
        column_name='Fecha',
        attribute='fecha',
        widget=FechaWidget()
    )

    class Meta:
        model = MiModelo
        fields = ('id', 'operario', 'activo', 'fecha')
        export_order = fields
```

### Agregar al Admin

```python
from import_export.admin import ImportExportMixin

@admin.register(MiModelo)
class MiModeloAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = MiModeloResource
    # ... resto de configuración
```

---

## 📁 Archivos Modificados

```
apps/reloj_fichador/
├── export_widgets.py         ← NUEVO: Widgets reutilizables
├── admin.py                  ← MODIFICADO: Resources mejorados
└── models.py                 ← Sin cambios

requirements.txt              ← Actualizado (django-import-export 4.3.13)
```

---

## ✅ Verificación de Funcionamiento

Se verificaron las siguientes funcionalidades:

1. ✅ **Exportación de RegistroDiario:**
   - Nombres de operarios en lugar de IDs
   - Tipos de movimiento legibles
   - Fechas en formato español
   - Sí/No en lugar de True/False

2. ✅ **Exportación de Horas_trabajadas:**
   - Nombres de operarios
   - Horas en formato legible (08h 30m)
   - Fechas en formato español

3. ✅ **Exportación de Operario:**
   - Fechas de nacimiento e ingreso legibles
   - Activo como Sí/No
   - Áreas con nombres en vez de IDs

4. ✅ **Importación:**
   - Acepta datos exportados
   - Acepta múltiples formatos de entrada
   - Validación y errores claros

---

## 🎯 Beneficios

### Para Usuarios
- ✅ Datos legibles sin necesidad de interpretar IDs
- ✅ Archivos Excel listos para compartir
- ✅ Formato familiar (español, Sí/No, fechas dd/mm/yyyy)
- ✅ Facilita auditorías y reportes

### Para Desarrolladores
- ✅ Código reutilizable y mantenible
- ✅ Fácil agregar nuevos modelos
- ✅ Widgets probados y documentados
- ✅ Reducción de código duplicado

### Para el Sistema
- ✅ Mantiene compatibilidad con django-import-export
- ✅ No rompe funcionalidad existente
- ✅ Importación/exportación más robusta
- ✅ Mejor experiencia de usuario

---

## 📚 Referencias

- **django-import-export:** https://django-import-export.readthedocs.io/
- **Documentación de widgets:** `apps/reloj_fichador/export_widgets.py`
- **Herramientas instaladas:** Ver `documentacion/ACTUALIZACION_HERRAMIENTAS_REPORTERIA_2025.md`

---

## 🔮 Mejoras Futuras Sugeridas

1. **Reportes con gráficos** usando xlsxwriter
2. **PDFs profesionales** desde templates HTML con weasyprint
3. **Exportación programada** vía Celery
4. **Dashboards interactivos** para ejecutivos
5. **Validaciones personalizadas** en importación

---

**Implementado por:** Claude Code
**Fecha:** 12 de Noviembre de 2025
**Versión django-import-export:** 4.3.13
