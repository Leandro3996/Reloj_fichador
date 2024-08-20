from django.contrib import admin
from .models import Operario, RegistroDiario, Horas_trabajadas, Horas_feriado, Horas_extras, Horas_totales, Area, Horario

@admin.register(Operario)
class OperarioAdmin(admin.ModelAdmin):
    list_display = ('dni', 'nombre', 'apellido', 'get_areas')
    list_filter = ('areas',)
    search_fields = ('dni', 'nombre', 'apellido')
    filter_horizontal = ('areas',)

    def get_areas(self, obj):
        return ", ".join([area.nombre for area in obj.areas.all()])
    get_areas.short_description = 'Áreas'

@admin.register(RegistroDiario)
class RegistroDiarioAdmin(admin.ModelAdmin):
    list_display = ('operario', 'tipo_movimiento', 'hora_fichada')
    list_filter = ('tipo_movimiento',)
    search_fields = ('operario__dni', 'operario__nombre', 'operario__apellido')

@admin.register(Horas_trabajadas)
class HorasTrabajadasAdmin(admin.ModelAdmin):
    list_display = ('operario', 'fecha', 'horas_trabajadas')
    search_fields = ('operario__dni', 'operario__nombre', 'operario__apellido')
    list_filter = ('fecha',)

@admin.register(Horas_feriado)
class HorasFeriadoAdmin(admin.ModelAdmin):
    list_display = ('operario', 'fecha', 'horas_feriado')
    search_fields = ('operario__dni', 'operario__nombre', 'operario__apellido')
    list_filter = ('fecha',)

@admin.register(Horas_extras)
class HorasExtrasAdmin(admin.ModelAdmin):
    list_display = ('operario', 'mes', 'horas_extras')
    search_fields = ('operario__dni', 'operario__nombre', 'operario__apellido')
    list_filter = ('mes',)

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
