from rangefilter.filters import DateRangeFilter
from django.contrib import admin
from django.shortcuts import render
from django.db import models
from django.contrib.admin.widgets import AdminSplitDateTime
from .models import Operario, RegistroDiario, Horas_trabajadas, Horas_extras, Horas_totales, Area, Horario
from django.urls import path
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

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

@admin.register(Operario)
class OperarioAdmin(admin.ModelAdmin):
    list_display = (
    'dni', 'nombre', 'apellido', 'fecha_nacimiento', 'fecha_ingreso_empresa', 'titulo_tecnico', 'get_areas', 'activo')
    list_filter = ('areas',('fecha_nacimiento', DateRangeFilter), ('fecha_ingreso_empresa',DateRangeFilter), 'titulo_tecnico', ActivoInactivoFilter)
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
                print(f"Área seleccionada: {area.nombre}")  # Depuración: confirmar el área seleccionada
            except Area.DoesNotExist:
                self.message_user(request, "El área seleccionada no existe.", level='error')
                return

            for operario in queryset:
                print(f"Asignando área a operario: {operario.nombre}")  # Depuración: confirmación de operario
                operario.areas.add(area)  # Asignar el área seleccionada al operario
                operario.save()  # Guardar los cambios en la base de datos
                print(f"Área '{area.nombre}' asignada a {operario.nombre}")  # Depuración: confirmación de asignación

            self.message_user(request, f"Área '{area.nombre}' asignada a {queryset.count()} operario(s).")
            return
        else:
            areas = Area.objects.all()
            return render(request, 'admin/asignar_area.html', {'operarios': queryset, 'areas': areas})

    asignar_area.short_description = "Asignar área a los operarios seleccionados"

@admin.register(RegistroDiario)
class RegistroDiarioAdmin(admin.ModelAdmin):
    list_display = ('operario', 'tipo_movimiento', 'hora_fichada','origen_fichada')
    list_filter = ('tipo_movimiento',)
    search_fields = ('operario__dni', 'operario__nombre', 'operario__apellido')
    fields = ('operario', 'tipo_movimiento', 'hora_fichada')
    def save_model(self, request, obj, form, change):
        if not change:  # Si es una nueva instancia
            obj.origen_fichada = 'Manual'
        super().save_model(request, obj, form, change)

    formfield_overrides = {
        models.DateTimeField: {'widget': AdminSplitDateTime},
    }

@admin.register(Horas_trabajadas)
class HorasTrabajadasAdmin(admin.ModelAdmin):
    list_display = ('operario', 'fecha', 'get_horas_trabajadas')
    search_fields = ('operario__dni', 'operario__nombre', 'operario__apellido')
    list_filter = ('fecha',('fecha', DateRangeFilter))

    def get_horas_trabajadas(self, obj):
        # Convertir timedelta a formato horas y minutos
        total_seconds = obj.horas_trabajadas.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

    get_horas_trabajadas.short_description = 'Horas Trabajadas'

    def recalcular_horas_trabajadas(self, request, queryset):
        for obj in queryset:
            Horas_trabajadas.calcular_horas_trabajadas(obj.operario, obj.fecha)
        self.message_user(request, "Horas trabajadas recalculadas con éxito.")

    recalcular_horas_trabajadas.short_description = "Recalcular horas trabajadas seleccionadas"

@admin.register(Horas_extras)
class HorasExtrasAdmin(admin.ModelAdmin):
    list_display = ('operario', 'fecha', 'get_horas_extras')
    search_fields = ('operario__dni', 'operario__nombre', 'operario__apellido')
    list_filter = ('fecha',('fecha', DateRangeFilter))

    def get_horas_extras(self, obj):
        # Convertir timedelta a formato horas y minutos
        total_seconds = obj.horas_extras.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

    get_horas_extras.short_description = 'Horas Extras'

@admin.register(Horas_totales)
class HorasTotalesAdmin(admin.ModelAdmin):
    list_display = ('operario', 'mes_actual', 'horas_totales')
    search_fields = ('operario__dni', 'operario__nombre', 'operario__apellido')
    list_filter = ('mes_actual',)

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
