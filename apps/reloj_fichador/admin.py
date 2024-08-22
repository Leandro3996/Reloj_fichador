from rangefilter.filters import DateRangeFilter
from django.contrib import admin
from django.db import models
from django.contrib.admin.widgets import AdminSplitDateTime
from .models import Operario, RegistroDiario, Horas_trabajadas, Horas_extras, Horas_totales, Area, Horario
from datetime import timedelta

@admin.register(Operario)
class OperarioAdmin(admin.ModelAdmin):
    list_display = ('dni', 'nombre', 'apellido', 'fecha_nacimiento', 'fecha_ingreso_empresa','titulo_tecnico', 'get_areas',)
    list_filter = ('areas', 'fecha_nacimiento', 'fecha_ingreso_empresa','titulo_tecnico',)
    search_fields = ('dni', 'nombre', 'apellido', 'fecha_nacimiento', 'fecha_ingreso_empresa','titulo_tecnico',)
    filter_horizontal = ('areas',)

    def get_areas(self, obj):
        return ", ".join([area.nombre for area in obj.areas.all()])
    get_areas.short_description = 'Áreas'

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
