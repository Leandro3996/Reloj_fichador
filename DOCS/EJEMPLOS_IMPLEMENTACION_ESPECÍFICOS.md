# 💻 EJEMPLOS ESPECÍFICOS DE IMPLEMENTACIÓN

**Ejemplos Prácticos para Modelos del Proyecto Reloj Fichador**

---

## 📌 TABLA DE CONTENIDOS

1. [Operario - Modelo Base](#operario)
2. [RegistroDiario - Con Crispy Forms](#registrodiario)
3. [RegistroAsistencia - Con Template Override](#registroasistencia)
4. [Horas_trabajadas - Con Fieldset Tabs](#horas_trabajadas)
5. [Licencia - Con Widgets Mejorados](#licencia)

---

## 🔵 OPERARIO

### Estado Actual (Admin Básico)

```python
# apps/reloj_fichador/admin.py - ANTES
@admin.register(Operario)
class OperarioAdmin(ExportMixin, SimpleHistoryAdmin, UnfoldModelAdmin):
    list_display = ('dni', 'nombre', 'apellido', 'fecha_nacimiento',
                    'fecha_ingreso_empresa', 'titulo_tecnico', 'get_areas', 'activo')
    search_fields = ('dni', 'nombre', 'apellido')
    # Campos sin estructura
```

### Implementación Mejorada (Herramientas Nativas)

```python
# apps/reloj_fichador/admin.py - DESPUÉS
from django.db import models
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

@admin.register(Operario)
class OperarioAdmin(ExportMixin, SimpleHistoryAdmin, UnfoldModelAdmin):
    # ✅ PASO 1: Organizar con fieldsets claros
    fieldsets = (
        (_("Información Personal"), {
            "description": _("Datos personales e identificación del operario"),
            "fields": (
                ("dni", "nombre"),
                ("apellido", "fecha_nacimiento"),
                "foto",
            ),
        }),
        (_("Información Laboral"), {
            "description": _("Datos relacionados con el empleo y asignación"),
            "fields": (
                ("areas", "titulo_tecnico"),
                ("fecha_ingreso_empresa", "activo"),
            ),
        }),
        (_("Contacto y Dirección"), {
            "classes": ("collapse",),  # Colapsable por defecto
            "fields": (
                "email",
                "telefono",
                ("calle", "numero"),
                ("ciudad", "codigo_postal"),
            ),
        }),
        (_("Notas"), {
            "classes": ("collapse",),
            "fields": ("observaciones",),
        }),
    )

    # ✅ PASO 2: Widgets mejorados
    formfield_overrides = {
        models.TextField: {"widget": WysiwygWidget},
    }

    # ✅ PASO 3: Búsqueda y lista mejorada
    list_display = (
        'dni',
        'nombre',
        'apellido',
        'get_areas_display',
        'get_estado_badge',
        'fecha_ingreso_empresa',
    )

    search_fields = ('dni', 'nombre', 'apellido', 'email')

    # ✅ PASO 4: Filtros
    list_filter = (
        'activo',
        ('fecha_ingreso_empresa', DateRangeFilter),
        'areas',
        'titulo_tecnico',
    )

    # ✅ PASO 5: Campos de solo lectura en edición
    readonly_fields = ('fecha_creacion', 'fecha_modificacion', 'foto_preview')

    # ✅ PASO 6: Métodos para display mejorado
    def get_areas_display(self, obj):
        areas = obj.areas.all()
        return format_html(
            '<div class="space-y-1">{}</div>',
            ''.join([
                f'<span class="inline-block bg-primary-100 text-primary-800 px-2 py-1 rounded text-sm">{area.nombre}</span>'
                for area in areas
            ]) or '-'
        )
    get_areas_display.short_description = _("Áreas")

    def get_estado_badge(self, obj):
        color = 'bg-green-100 text-green-800' if obj.activo else 'bg-red-100 text-red-800'
        text = _("Activo") if obj.activo else _("Inactivo")
        return format_html(
            f'<span class="{color} px-3 py-1 rounded-full text-sm font-medium">{text}</span>'
        )
    get_estado_badge.short_description = _("Estado")

    def foto_preview(self, obj):
        if obj.foto:
            return format_html(
                '<img src="{}" style="max-width: 200px; height: auto;" />',
                obj.foto.url
            )
        return '-'
    foto_preview.short_description = _("Vista Previa de Foto")

    # ✅ PASO 7: Inlines para relaciones
    inlines = [LicenciaInline]
```

**Resultado Visual**:
- ✅ Formulario dividido en 4 secciones claras
- ✅ "Contacto" colapsable (menos clutter)
- ✅ Descripción en cada sección
- ✅ Widgets mejorados para TextFields
- ✅ Listado con badges de estado
- ✅ Vista previa de foto
- ✅ Búsqueda mejorada

---

## 🔴 REGISTRODIARIO

### Estado Actual

```python
# ANTES - Sin estructura clara
list_display = ('get_dni', 'get_nombre', 'tipo_movimiento',
                'formatted_hora_fichada', 'origin_fichada',
                'mostrar_inconsistencia', 'mostrar_valido')
```

### Implementación Mejorada (Nativa + Crispy)

#### Opción A: Solo Herramientas Nativas (Recomendado)

```python
@admin.register(RegistroDiario)
class RegistroDiarioAdmin(ImportExportMixin, SimpleHistoryAdmin, UnfoldModelAdmin):
    # ✅ Fieldsets organizados
    fieldsets = (
        (_("Información del Registro"), {
            "description": _("Datos básicos del fichaje"),
            "fields": (
                "operario",
                ("tipo_movimiento", "origen_fichada"),
                "hora_fichada",
            ),
        }),
        (_("Validación"), {
            "description": _("Estado y validación del registro"),
            "fields": (
                ("valido", "inconsistencia"),
                "descripcion_inconsistencia",
            ),
        }),
    )

    # ✅ Campos condicionales
    conditional_fields = {
        "descripcion_inconsistencia": {
            "__all__": ["inconsistencia"],
            "inconsistencia": True,  # Solo visible si hay inconsistencia
        }
    }

    # ✅ Búsqueda y filtros mejorados
    list_display = (
        'get_dni_badge',
        'get_nombre_completo',
        'get_tipo_movimiento_badge',
        'formatted_hora_fichada',
        'get_estado_badge',
    )

    list_filter = (
        ('hora_fichada', DateRangeFilter),
        'tipo_movimiento',
        'inconsistencia',
        'valido',
        'origen_fichada',
    )

    search_fields = (
        'operario__dni',
        'operario__nombre',
        'operario__apellido',
    )

    readonly_fields = ('hora_fichada_tz', 'operario_info')

    # ✅ Métodos para display con estilos
    def get_dni_badge(self, obj):
        return format_html(
            '<code class="bg-base-100 px-2 py-1 rounded font-mono text-sm">{}</code>',
            obj.operario.dni
        )
    get_dni_badge.short_description = _("DNI")

    def get_nombre_completo(self, obj):
        return f"{obj.operario.nombre} {obj.operario.apellido}"
    get_nombre_completo.short_description = _("Nombre")

    def get_tipo_movimiento_badge(self, obj):
        colores = {
            'entrada': 'bg-green-100 text-green-800',
            'salida': 'bg-red-100 text-red-800',
            'entrada_transitoria': 'bg-yellow-100 text-yellow-800',
            'salida_transitoria': 'bg-orange-100 text-orange-800',
        }
        etiquetas = {
            'entrada': '↗️ Entrada',
            'salida': '↙️ Salida',
            'entrada_transitoria': '↗️ Entrada Temp.',
            'salida_transitoria': '↙️ Salida Temp.',
        }
        color = colores.get(obj.tipo_movimiento, 'bg-base-100')
        texto = etiquetas.get(obj.tipo_movimiento, obj.get_tipo_movimiento_display())
        return format_html(
            f'<span class="{color} px-2 py-1 rounded text-sm font-medium">{texto}</span>'
        )
    get_tipo_movimiento_badge.short_description = _("Tipo")

    def get_estado_badge(self, obj):
        if obj.inconsistencia:
            return format_html(
                '<span class="bg-red-100 text-red-800 px-2 py-1 rounded text-sm">⚠️ Inconsistencia</span>'
            )
        elif not obj.valido:
            return format_html(
                '<span class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-sm">❌ No Válido</span>'
            )
        else:
            return format_html(
                '<span class="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">✅ Válido</span>'
            )
    get_estado_badge.short_description = _("Estado")

    def hora_fichada_tz(self, obj):
        """Mostrar la hora en zona horaria de Argentina"""
        from django.utils import timezone
        import pytz

        argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
        hora_arg = obj.hora_fichada.astimezone(argentina_tz)
        return formato_hora(hora_arg)
    hora_fichada_tz.short_description = _("Hora (Zona ARG)")

    def operario_info(self, obj):
        """Información del operario en el formulario"""
        return format_html(
            '<div class="space-y-2">'
            '<p><strong>{}</strong></p>'
            '<p class="text-sm text-base-500">DNI: {}</p>'
            '<p class="text-sm text-base-500">Activo: {}</p>'
            '</div>',
            f"{obj.operario.nombre} {obj.operario.apellido}",
            obj.operario.dni,
            _("Sí") if obj.operario.activo else _("No"),
        )
    operario_info.short_description = _("Información del Operario")
```

#### Opción B: Con Crispy Forms (Si quieres layout de 2 columnas)

```python
# forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset

class RegistroDiarioForm(forms.ModelForm):
    class Meta:
        model = RegistroDiario
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("operario", css_class="form-group col-md-8"),
                Column("tipo_movimiento", css_class="form-group col-md-4"),
            ),
            Row(
                Column("hora_fichada", css_class="form-group col-md-6"),
                Column("origen_fichada", css_class="form-group col-md-6"),
            ),
            Fieldset(
                _("Validación"),
                Row(
                    Column("valido", css_class="form-group col-md-6"),
                    Column("inconsistencia", css_class="form-group col-md-6"),
                ),
                "descripcion_inconsistencia",
            ),
        )

# admin.py
@admin.register(RegistroDiario)
class RegistroDiarioAdmin(ImportExportMixin, SimpleHistoryAdmin, UnfoldModelAdmin):
    form = RegistroDiarioForm  # Asignar formulario crispy
    # ... resto de config
```

---

## 🟠 REGISTROASISTENCIA

### Con Template Override

```python
# admin.py
@admin.register(RegistroAsistencia)
class RegistroAsistenciaAdmin(ExportMixin, UnfoldModelAdmin):
    fieldsets = (
        (_("Información de Asistencia"), {
            "fields": (
                "operario",
                ("estado_asistencia", "estado_justificacion"),
                "descripcion",
            ),
        }),
        (_("Período"), {
            "fields": ("fecha",),
            "classes": ("collapse",),
        }),
    )

    list_display = (
        'operario',
        'get_fecha_display',
        'get_asistencia_badge',
        'get_justificacion_badge',
    )

    def get_fecha_display(self, obj):
        return obj.fecha.strftime('%d/%m/%Y')
    get_fecha_display.short_description = _("Fecha")

    def get_asistencia_badge(self, obj):
        colores = {
            'presente': 'bg-green-100 text-green-800',
            'ausente': 'bg-red-100 text-red-800',
            'tarde': 'bg-yellow-100 text-yellow-800',
        }
        textos = {
            'presente': '✅ Presente',
            'ausente': '❌ Ausente',
            'tarde': '⚠️ Tarde',
        }
        color = colores.get(obj.estado_asistencia, 'bg-base-100')
        texto = textos.get(obj.estado_asistencia, obj.get_estado_asistencia_display())
        return format_html(f'<span class="{color} px-2 py-1 rounded text-sm">{texto}</span>')
    get_asistencia_badge.short_description = _("Asistencia")

    def get_justificacion_badge(self, obj):
        colores = {
            'sin_justificacion': 'bg-red-100 text-red-800',
            'pendiente': 'bg-yellow-100 text-yellow-800',
            'justificado': 'bg-green-100 text-green-800',
        }
        textos = {
            'sin_justificacion': '❌ Sin Justificación',
            'pendiente': '⏳ Pendiente',
            'justificado': '✅ Justificado',
        }
        color = colores.get(obj.estado_justificacion, 'bg-base-100')
        texto = textos.get(obj.estado_justificacion, obj.get_estado_justificacion_display())
        return format_html(f'<span class="{color} px-2 py-1 rounded text-sm">{texto}</span>')
    get_justificacion_badge.short_description = _("Justificación")
```

```html
<!-- templates/admin/reloj_fichador/registroasistencia/change_form.html -->
{% extends "unfold/change_form.html" %}
{% load i18n %}

{% block after_field_sets %}
    {{ block.super }}

    {% if original %}
        <div class="mt-8 border-t border-base-200 pt-6 dark:border-base-800">
            <h2 class="text-lg font-semibold text-base-900 dark:text-white">
                {% trans "Información Relacionada" %}
            </h2>

            <div class="mt-4 grid grid-cols-1 gap-6 lg:grid-cols-2">
                <!-- Licencias del operario -->
                <div class="border border-base-200 rounded-lg p-4 dark:border-base-800">
                    <h3 class="text-sm font-medium text-base-900 dark:text-white mb-3">
                        {% trans "Licencias Activas" %}
                    </h3>
                    {% if original.operario.licencia_set.all %}
                        <ul class="space-y-2">
                        {% for licencia in original.operario.licencia_set.all %}
                            <li class="text-sm text-base-600 dark:text-base-400">
                                {{ licencia.get_tipo_display }}: {{ licencia.fecha_inicio }} - {{ licencia.fecha_fin }}
                            </li>
                        {% endfor %}
                        </ul>
                    {% else %}
                        <p class="text-sm text-base-500 dark:text-base-400">{% trans "Sin licencias" %}</p>
                    {% endif %}
                </div>

                <!-- Registros recientes -->
                <div class="border border-base-200 rounded-lg p-4 dark:border-base-800">
                    <h3 class="text-sm font-medium text-base-900 dark:text-white mb-3">
                        {% trans "Últimos 5 Registros" %}
                    </h3>
                    {% if original.operario.registrodiario_set.all %}
                        <ul class="space-y-2">
                        {% for registro in original.operario.registrodiario_set.all|slice:":5" %}
                            <li class="text-sm text-base-600 dark:text-base-400">
                                {{ registro.get_tipo_movimiento_display }}: {{ registro.hora_fichada|date:"d/m/Y H:i" }}
                            </li>
                        {% endfor %}
                        </ul>
                    {% else %}
                        <p class="text-sm text-base-500 dark:text-base-400">{% trans "Sin registros" %}</p>
                    {% endif %}
                </div>
            </div>
        </div>
    {% endif %}
{% endblock %}
```

---

## 🟡 HORASTRABAJADAS

### Con Fieldset Tabs

```python
@admin.register(Horas_trabajadas)
class HorasTrabajadasAdmin(ExportMixin, UnfoldModelAdmin):
    # ✅ Usar fieldsets con formato "tabs"
    fieldsets = (
        ("tabs", {
            "fields": (
                (_("Información General"), {
                    "fields": (
                        ("operario", "fecha"),
                        "descripcion",
                    ),
                }),
                (_("Horas Normales"), {
                    "fields": (
                        ("horas_normales_dia", "horas_normales_noche"),
                        "total_horas_normales",
                    ),
                }),
                (_("Horas Especiales"), {
                    "fields": (
                        "horas_extras",
                        "horas_feriado",
                        "horas_enfermedad",
                    ),
                }),
                (_("Resumen"), {
                    "fields": (
                        "total_horas",
                    ),
                }),
            ),
        }),
    )

    list_display = (
        'operario',
        'fecha',
        'get_horas_normales_display',
        'get_horas_nocturnas_display',
        'get_horas_extras_display',
        'get_total_display',
    )

    list_filter = (
        ('fecha', DateRangeFilter),
        'operario__area',
    )

    search_fields = (
        'operario__dni',
        'operario__nombre',
        'operario__apellido',
    )

    readonly_fields = (
        'total_horas_normales',
        'total_horas',
        'operario_info',
        'fecha_calculo',
    )

    def get_horas_normales_display(self, obj):
        horas = obj.horas_normales_dia.total_seconds() / 3600 if obj.horas_normales_dia else 0
        return format_html(f'<span class="font-mono">{horas:.2f}h</span>')
    get_horas_normales_display.short_description = _("Horas Normales")

    def get_horas_nocturnas_display(self, obj):
        horas = obj.horas_normales_noche.total_seconds() / 3600 if obj.horas_normales_noche else 0
        return format_html(f'<span class="font-mono text-primary-600 dark:text-primary-400">{horas:.2f}h</span>')
    get_horas_nocturnas_display.short_description = _("Horas Nocturnas")

    def get_horas_extras_display(self, obj):
        horas = obj.horas_extras.total_seconds() / 3600 if obj.horas_extras else 0
        color = 'text-red-600' if horas > 0 else 'text-base-400'
        return format_html(f'<span class="font-mono {color}">{horas:.2f}h</span>')
    get_horas_extras_display.short_description = _("Horas Extras")

    def get_total_display(self, obj):
        horas = obj.total_horas.total_seconds() / 3600 if obj.total_horas else 0
        return format_html(f'<span class="font-mono font-bold">{horas:.2f}h</span>')
    get_total_display.short_description = _("Total")

    def operario_info(self, obj):
        return format_html(
            '<div class="bg-base-50 dark:bg-base-900 p-3 rounded border border-base-200 dark:border-base-800">'
            '<p class="font-medium">{} {}</p>'
            '<p class="text-sm text-base-600 dark:text-base-400">DNI: {}</p>'
            '<p class="text-sm text-base-600 dark:text-base-400">Área: {}</p>'
            '</div>',
            obj.operario.nombre,
            obj.operario.apellido,
            obj.operario.dni,
            ', '.join([area.nombre for area in obj.operario.areas.all()]) or '—'
        )
    operario_info.short_description = _("Operario")

    def fecha_calculo(self, obj):
        return obj.fecha_modificacion.strftime('%d/%m/%Y %H:%M') if obj.fecha_modificacion else '—'
    fecha_calculo.short_description = _("Calculado el")
```

---

## 🟢 LICENCIA

### Con Widgets Mejorados

```python
@admin.register(Licencia)
class LicenciaAdmin(SimpleHistoryAdmin, UnfoldModelAdmin):
    fieldsets = (
        (_("Información de la Licencia"), {
            "description": _("Detalles sobre el tipo y período de licencia"),
            "fields": (
                "operario",
                "tipo",
                ("fecha_inicio", "fecha_fin"),
                "dias_totales",
            ),
        }),
        (_("Documentación"), {
            "description": _("Archivo y fecha de carga"),
            "fields": (
                "archivo",
                "archivo_preview",
                "fecha_subida",
            ),
        }),
        (_("Notas Internas"), {
            "classes": ("collapse",),
            "fields": ("observaciones",),
        }),
    )

    formfield_overrides = {
        models.TextField: {"widget": WysiwygWidget},
    }

    readonly_fields = (
        'dias_totales',
        'archivo_preview',
        'fecha_subida',
        'operario_info',
    )

    list_display = (
        'get_operario_display',
        'get_tipo_badge',
        'get_periodo_display',
        'get_archivo_badge',
        'get_dias_display',
    )

    list_filter = (
        'tipo',
        ('fecha_inicio', DateRangeFilter),
        'operario__area',
    )

    search_fields = (
        'operario__dni',
        'operario__nombre',
        'operario__apellido',
    )

    def get_operario_display(self, obj):
        return format_html(
            '<div class="space-y-1">'
            '<p class="font-medium">{} {}</p>'
            '<p class="text-sm text-base-500">{}</p>'
            '</div>',
            obj.operario.nombre,
            obj.operario.apellido,
            obj.operario.dni,
        )
    get_operario_display.short_description = _("Operario")

    def get_tipo_badge(self, obj):
        colores = {
            'vacaciones': 'bg-blue-100 text-blue-800',
            'enfermedad': 'bg-red-100 text-red-800',
            'licencia_matrimonio': 'bg-pink-100 text-pink-800',
            'duelo': 'bg-gray-100 text-gray-800',
        }
        color = colores.get(obj.tipo, 'bg-base-100 text-base-800')
        return format_html(
            f'<span class="{color} px-2 py-1 rounded text-sm font-medium">'
            f'{obj.get_tipo_display()}'
            f'</span>'
        )
    get_tipo_badge.short_description = _("Tipo")

    def get_periodo_display(self, obj):
        return f"{obj.fecha_inicio.strftime('%d/%m/%Y')} - {obj.fecha_fin.strftime('%d/%m/%Y')}"
    get_periodo_display.short_description = _("Período")

    def get_archivo_badge(self, obj):
        if obj.archivo:
            return format_html(
                '<a href="{}" class="text-primary-600 hover:text-primary-700 dark:text-primary-400" target="_blank">'
                '📄 Ver Archivo'
                '</a>',
                obj.archivo.url
            )
        return format_html('<span class="text-base-400">—</span>')
    get_archivo_badge.short_description = _("Archivo")

    def get_dias_display(self, obj):
        dias = (obj.fecha_fin - obj.fecha_inicio).days + 1
        return format_html(
            '<span class="font-mono font-bold text-lg">{} días</span>',
            dias
        )
    get_dias_display.short_description = _("Duración")

    def archivo_preview(self, obj):
        if not obj.archivo:
            return format_html('<p class="text-base-400">{% trans "No hay archivo cargado" %}</p>')

        ext = obj.archivo.name.split('.')[-1].lower()

        if ext == 'pdf':
            return format_html(
                '<div class="border border-base-200 rounded p-4 dark:border-base-800">'
                '<a href="{}" target="_blank" class="text-primary-600 hover:underline">'
                '📄 Descargar PDF'
                '</a>'
                '</div>',
                obj.archivo.url
            )
        elif ext in ['jpg', 'jpeg', 'png', 'gif']:
            return format_html(
                '<div class="border border-base-200 rounded p-4 dark:border-base-800">'
                '<img src="{}" style="max-width: 300px; height: auto;" />'
                '<p class="text-sm text-base-500 mt-2"><a href="{}" target="_blank" download>Descargar imagen</a></p>'
                '</div>',
                obj.archivo.url,
                obj.archivo.url
            )
        else:
            return format_html(
                '<div class="border border-base-200 rounded p-4 dark:border-base-800">'
                '<a href="{}" target="_blank" class="text-primary-600 hover:underline">'
                '📥 Descargar Archivo'
                '</a>'
                '</div>',
                obj.archivo.url
            )
    archivo_preview.short_description = _("Vista Previa del Archivo")

    def operario_info(self, obj):
        return format_html(
            '<div class="bg-base-50 dark:bg-base-900 p-3 rounded">'
            '<p class="font-medium">{} {}</p>'
            '<p class="text-sm text-base-600 dark:text-base-400">DNI: {}</p>'
            '<p class="text-sm text-base-600 dark:text-base-400">Activo: {}</p>'
            '</div>',
            obj.operario.nombre,
            obj.operario.apellido,
            obj.operario.dni,
            _("Sí") if obj.operario.activo else _("No"),
        )
    operario_info.short_description = _("Información del Operario")
```

---

## ✅ PASOS DE VALIDACIÓN

Para cada modelo mejorado:

```bash
# 1. Verificar sintaxis Python
python manage.py check

# 2. Verificar migraciones
python manage.py makemigrations --dry-run

# 3. Probar en shell
python manage.py shell
from apps.reloj_fichador.admin import OperarioAdmin
# Debe cargar sin errores

# 4. Compilar static files
python manage.py collectstatic --noinput

# 5. Probar en navegador (http://localhost:5080/admin/)
# - ✅ Formularios cargan sin errores
# - ✅ Estilos se aplican
# - ✅ Campos se agrupan correctamente
# - ✅ Fieldsets tabs funcionan
# - ✅ Modo claro/oscuro funciona
```

---

## 📝 NOTAS IMPORTANTES

1. **Siempre usar `UnfoldModelAdmin`**, nunca `admin.ModelAdmin`
2. **Siempre extender desde `unfold/change_form.html`**, nunca de `admin/change_form.html`
3. **Usar `format_html()` para contenido HTML** en métodos display
4. **Probar en AMBOS modos**: claro y oscuro
5. **Documentar cambios** en docstrings y comentarios

---

**Ejemplos Preparados**: 2025-10-24
**Estado**: Listos para Copiar y Adaptar
**Complejidad**: Media
