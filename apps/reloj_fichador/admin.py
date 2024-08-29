from rangefilter.filters import DateRangeFilter
from django.contrib import admin
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.contrib.admin.widgets import AdminSplitDateTime
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.html import format_html
from .models import Operario, RegistroDiario, Horas_trabajadas, Horas_extras, Horas_totales, Area, Horario, Licencia, RegistroAsistencia
from django.urls import path, reverse
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from .forms import LicenciaForm
from .utils import generar_pdf, generar_excel


class Command(BaseCommand):
    help = 'Genera registros de asistencia para los operarios activos'

    def handle(self, *args, **kwargs):
        hoy = timezone.now().date()
        operarios_activos = Operario.objects.filter(activo=True)

        for operario in operarios_activos:
            registro, created = RegistroAsistencia.objects.get_or_create(
                operario=operario,
                fecha=hoy
            )
            registro.verificar_asistencia()
            self.stdout.write(self.style.SUCCESS(f'Registro generado para {operario}'))

class ActivoInactivoFilter(admin.SimpleListFilter):
    title = _('Activo/Inactivo')
    parameter_name = 'activo'

    def lookups(self, request, model_admin):
        return (
            ('1', _('Activo')),
            ('0', _('Inactivo')),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(activo=True)
        elif self.value() == '0':
            return queryset.filter(activo=False)
        return queryset

class LicenciaInline(admin.TabularInline):
    model = Licencia
    extra = 1
    fields = ['archivo', 'fecha_subida']
    readonly_fields = ['fecha_subida']


@admin.register(Operario)
class OperarioAdmin(admin.ModelAdmin):
    inlines = [LicenciaInline]  # Incluir el Inline de Licencias
    list_display = (
        'dni', 'nombre', 'apellido', 'fecha_nacimiento', 'fecha_ingreso_empresa', 'titulo_tecnico', 'get_areas', 'activo'
    )
    list_filter = ('areas', ('fecha_nacimiento', DateRangeFilter), ('fecha_ingreso_empresa', DateRangeFilter), 'titulo_tecnico', ActivoInactivoFilter)
    search_fields = ('dni', 'nombre', 'apellido', 'fecha_nacimiento', 'fecha_ingreso_empresa', 'titulo_tecnico')
    filter_horizontal = ('areas',)
    actions = ['asignar_area']

    def get_areas(self, obj):
        return ", ".join([area.nombre for area in obj.areas.all()])

    get_areas.short_description = 'Áreas'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset

    # Acción personalizada para asignar área
    def asignar_area(self, request, queryset):
        if 'apply' in request.POST:
            area_id = request.POST.get('area')
            if not area_id:
                self.message_user(request, "No se seleccionó ninguna área.", level='error')
                return

            try:
                area = Area.objects.get(id=area_id)
            except Area.DoesNotExist:
                self.message_user(request, "El área seleccionada no existe.", level='error')
                return

            for operario in queryset:
                operario.areas.add(area)  # Asignar el área seleccionada al operario
                operario.save()  # Guardar los cambios en la base de datos

            self.message_user(request, f"Área '{area.nombre}' asignada a {queryset.count()} operario(s).")
            return
        else:
            areas = Area.objects.all()
            return render(request, 'admin/asignar_area.html', {'operarios': queryset, 'areas': areas})

    asignar_area.short_description = "Asignar área a los operarios seleccionados"

@admin.register(RegistroDiario)
class RegistroDiarioAdmin(admin.ModelAdmin):
    list_display = ('operario', 'tipo_movimiento', 'formatted_hora_fichada', 'origen_fichada')
    list_filter = ('tipo_movimiento',)
    search_fields = ('operario__dni', 'operario__nombre', 'operario__apellido')
    fields = ('operario', 'tipo_movimiento', 'hora_fichada')
    actions = ['exportar_pdf', 'exportar_excel']

    HEADER_MAP = {
        'operario': 'Operario',
        'tipo_movimiento': 'Tipo Movimiento',
        'hora_fichada': 'Hora Fichada',
        'origen_fichada': 'Origen Fichada',
    }

    def exportar_pdf(self, request, queryset):
        campos = ['operario', 'tipo_movimiento', 'hora_fichada', 'origen_fichada']
        encabezados = [self.HEADER_MAP[campo] for campo in campos]
        return generar_pdf(self, request, queryset, campos, encabezados, "Reporte de Registro Diario")
    exportar_pdf.short_description = "Exportar a PDF"

    def exportar_excel(self, request, queryset):
        campos = ['operario', 'tipo_movimiento', 'hora_fichada', 'origen_fichada']
        encabezados = [self.HEADER_MAP[campo] for campo in campos]
        return generar_excel(self, request, queryset, campos, encabezados, "Reporte de Registro Diario")
    exportar_excel.short_description = "Exportar a Excel"

    def formatted_hora_fichada(self, obj):
        return obj.hora_fichada.strftime('%Y-%m-%d %H:%M:%S')
    formatted_hora_fichada.short_description = 'Hora Fichada'



@admin.register(Horas_trabajadas)
class HorasTrabajadasAdmin(admin.ModelAdmin):
    list_display = ('operario', 'fecha', 'get_horas_trabajadas', 'get_horas_nocturnas')
    search_fields = ('operario__dni', 'operario__nombre', 'operario__apellido')
    list_filter = ('fecha', ('fecha', DateRangeFilter))

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('operario')  # Optimiza la relación ForeignKey con operario

    def get_horas_trabajadas(self, obj):
        total_seconds = obj.horas_trabajadas.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        return f"{hours}h {minutes}m {seconds}s"

    get_horas_trabajadas.short_description = 'Horas Trabajadas'

    def get_horas_nocturnas(self, obj):
        total_seconds = obj.horas_nocturnas.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        return f"{hours}h {minutes}m {seconds}s"

    get_horas_nocturnas.short_description = 'Horas Nocturnas'

    def recalcular_horas_trabajadas(self, request, queryset):
        for obj in queryset:
            Horas_trabajadas.calcular_horas_trabajadas(obj.operario, obj.fecha)
        self.message_user(request, "Horas trabajadas recalculadas con éxito.")

    recalcular_horas_trabajadas.short_description = "Recalcular horas trabajadas seleccionadas"

@admin.register(Horas_extras)
class HorasExtrasAdmin(admin.ModelAdmin):
    list_display = ('operario', 'fecha', 'get_horas_extras')
    search_fields = ('operario__dni', 'operario__nombre', 'operario__apellido')
    list_filter = ('fecha', ('fecha', DateRangeFilter))

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('operario')  # Optimiza la relación ForeignKey con operario

    def get_horas_extras(self, obj):
        total_seconds = obj.horas_extras.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

    get_horas_extras.short_description = 'Horas Extras'

@admin.register(Horas_totales)
class HorasTotalesAdmin(admin.ModelAdmin):
    list_display = ('get_dni', 'operario', 'get_horas_normales', 'get_horas_nocturnas', 'get_horas_extras', 'get_horas_feriado')
    search_fields = ('operario__dni', 'operario__nombre', 'operario__apellido')
    list_filter = ('mes_actual',)

    def get_dni(self, obj):
        return obj.operario.dni
    get_dni.short_description = 'DNI'

    def get_horas_normales(self, obj):
        total_seconds = obj.horas_normales.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return f"{hours}h {minutes}m"
    get_horas_normales.short_description = 'Horas Normales'

    def get_horas_nocturnas(self, obj):
        total_seconds = obj.horas_nocturnas.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return f"{hours}h {minutes}m"
    get_horas_nocturnas.short_description = 'Horas Nocturnas'

    def get_horas_extras(self, obj):
        total_seconds = obj.horas_extras.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return f"{hours}h {minutes}m"
    get_horas_extras.short_description = 'Horas Extras'

    def get_horas_feriado(self, obj):
        total_seconds = obj.horas_feriado.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return f"{hours}h {minutes}m"
    get_horas_feriado.short_description = 'Horas Feriado'

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'hora_inicio', 'hora_fin')
    search_fields = ('nombre',)

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'mostrar_horarios')
    search_fields = ('nombre',)
    filter_horizontal = ('horarios',)

    def mostrar_horarios(self, obj):
        return ", ".join([f"{horario.nombre}: {horario.hora_inicio.strftime('%H:%M')} - {horario.hora_fin.strftime('%H:%M')}" for horario in obj.horarios.all()])
    mostrar_horarios.short_description = 'Horarios'


@admin.register(RegistroAsistencia)
class RegistroAsistenciaAdmin(admin.ModelAdmin):
    list_display = (
        'operario', 'fecha', 'estado_asistencia', 'estado_justificacion_selector', 'descripcion', 'acciones'
    )
    list_filter = ('estado_asistencia', 'estado_justificacion', 'fecha')
    search_fields = ('operario__dni', 'operario__nombre', 'operario__apellido')
    actions = ['marcar_justificado', 'marcar_no_justificado']

    def estado_justificacion_selector(self, obj):
        return '✅' if obj.estado_justificacion else '❌'
    estado_justificacion_selector.short_description = 'Justificación'

    def marcar_justificado(self, request, queryset):
        queryset.update(estado_justificacion=True)
        self.message_user(request, "Las ausencias seleccionadas han sido marcadas como justificadas.")

    def marcar_no_justificado(self, request, queryset):
        queryset.update(estado_justificacion=False)
        self.message_user(request, "Las ausencias seleccionadas han sido marcadas como no justificadas.")

    def acciones(self, obj):
        return format_html(
            '<a class="button" href="{}">Cargar Licencia</a>',
            reverse('admin:cargar_licencia', args=[obj.pk])
        )
    acciones.short_description = 'Acciones'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('cargar-licencia/<int:pk>/', self.cargar_licencia, name='cargar_licencia'),
        ]
        return custom_urls + urls

    def cargar_licencia(self, request, pk):
        registro_asistencia = get_object_or_404(RegistroAsistencia, pk=pk)

        if request.method == 'POST':
            form = LicenciaForm(request.POST, request.FILES)
            if form.is_valid():
                licencia = form.save(commit=False)
                licencia.operario = registro_asistencia.operario
                licencia.save()
                registro_asistencia.estado_justificacion = True
                registro_asistencia.descripcion = form.cleaned_data['descripcion']
                registro_asistencia.save()
                return redirect('admin:reloj_fichador_registroasistencia_changelist')
        else:
            form = LicenciaForm()

        return render(request, 'admin/cargar_licencia.html', {'form': form, 'registro_asistencia': registro_asistencia})

