import json

from rangefilter.filters import DateRangeFilter
from django.contrib import admin, messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.contrib.admin.widgets import AdminSplitDateTime
from django.contrib.admin.models import LogEntry
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.html import format_html

# Imports de Unfold
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from .models import (
    Operario, RegistroDiario, Horas_trabajadas, Horas_extras,
    Horas_totales, Area, Horario, Licencia, RegistroAsistencia,
    Horas_feriado, HistoricalOperario, HistoricalRegistroDiario, ConfiguracionRedondeo, ConfiguracionRedondeoSalida, Reporte,
    CalendarioLaboral, GrupoSabado, SugerenciaFeriado
)

# Importar el modelo histórico de Licencia
from apps.reloj_fichador.models import Licencia
HistoricalLicencia = Licencia.history.model
from django.urls import path, reverse
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from .forms import LicenciaForm
from .utils import generar_pdf, generar_excel
from import_export.admin import ExportMixin, ImportExportMixin
from import_export import resources, fields
from datetime import datetime
from django.http import HttpResponse
import os
from django.conf import settings
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin as BaseGroupAdmin
from django.http import HttpResponseRedirect
import pytz
from .signals import actualizar_horas_despues_de_guardar


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

def exportar_pdf(modeladmin, request, queryset, calculate_hours_total=None):
    """
    Función genérica para exportar cualquier modelo a PDF.
    Determina automáticamente los campos y encabezados basados en el ModelAdmin
    
    Args:
        calculate_hours_total: Si es None, autodetecta. Si es True, fuerza el cálculo de totales.
                           Si es False, no calcula totales.
    """
    # Obtener lista de campos a mostrar del list_display del ModelAdmin
    if hasattr(modeladmin, 'list_display'):
        # Excluir el campo view_history_button de la lista de campos
        campos = [field for field in modeladmin.list_display if field != 'view_history_button']
    else:
        # Si no tiene list_display, usamos los campos definidos en el modelo
        campos = [field.name for field in modeladmin.model._meta.fields]
    
    # Generar los encabezados a partir de los nombres cortos de los campos o del HEADER_MAP si existe
    encabezados = []
    for campo in campos:
        if hasattr(modeladmin, 'HEADER_MAP') and campo in modeladmin.HEADER_MAP:
            encabezados.append(modeladmin.HEADER_MAP[campo])
        else:
            # Intentar obtener el verbose_name o short_description
            try:
                # Si es un método con short_description
                if hasattr(getattr(modeladmin, campo), 'short_description'):
                    encabezados.append(getattr(modeladmin, campo).short_description)
                # Si es un campo del modelo
                elif campo in [field.name for field in modeladmin.model._meta.fields]:
                    encabezados.append(modeladmin.model._meta.get_field(campo).verbose_name)
                else:
                    # Usar el nombre del campo capitalizado como fallback
                    encabezados.append(campo.replace('_', ' ').capitalize())
            except:
                # Si todo falla, usar el nombre del campo
                encabezados.append(campo.replace('_', ' ').capitalize())
    
    # Obtener el título del reporte basado en el verbose_name_plural del modelo
    titulo = f"Reporte de {modeladmin.model._meta.verbose_name_plural.capitalize()}"
    
    # Generar el PDF usando la función generar_pdf
    return generar_pdf(modeladmin, request, queryset, campos, encabezados, titulo, calculate_hours_total=calculate_hours_total)

exportar_pdf.short_description = "Exportar seleccionados a PDF"

# Mixin para añadir la acción de exportar a PDF
class ExportarPDFMixin:
    actions = ['exportar_pdf']
    
    def exportar_pdf(self, request, queryset):
        return exportar_pdf(self, request, queryset)
    exportar_pdf.short_description = "Exportar seleccionados a PDF"

@admin.register(Operario)
class OperarioAdmin(ExportMixin, SimpleHistoryAdmin, UnfoldModelAdmin):
    inlines = [LicenciaInline]
    list_display = (
        'dni', 'nombre', 'apellido', 'fecha_nacimiento', 'fecha_ingreso_empresa', 'titulo_tecnico', 'get_areas', 'activo', 'view_history_button'
    )
    list_filter = ('areas', ('fecha_nacimiento', DateRangeFilter), ('fecha_ingreso_empresa', DateRangeFilter), 'titulo_tecnico', ActivoInactivoFilter)
    search_fields = ('dni', 'nombre', 'apellido', 'fecha_nacimiento', 'fecha_ingreso_empresa', 'titulo_tecnico')
    filter_horizontal = ('areas',)
    actions = ['asignar_area', 'generar_reporte', 'exportar_excel', 'exportar_pdf']

    readonly_fields = ('foto_tag', 'get_areas')

    def get_areas(self, obj):
        return ", ".join([area.nombre for area in obj.areas.all()])
    get_areas.short_description = 'Áreas'

    def foto_tag(self, obj):
        if obj.foto:
            return format_html(f'<img src="{obj.foto.url}" style="max-width: 150px; height: auto;" />')
        return "(Sin foto)"
    foto_tag.short_description = 'Foto del operario'

    def view_history_button(self, obj):
        """Mostrar un botón para ver el historial del operario"""
        if obj.pk:
            url = reverse('admin:reloj_fichador_historicaloperario_changelist') + f"?id={obj.pk}"
            return format_html(
                '<a class="button" href="{}">Ver Historial</a>',
                url
            )
        return ""
    view_history_button.short_description = "Historial"

    def generar_reporte(self, request, queryset):
        registros = list(queryset)
        total_registros = Operario.objects.count()
        items_por_pagina = 30

        encabezados = ['DNI', 'Nombre', 'Apellido', 'Fecha Nacimiento', 'Fecha Ingreso',]

        filas = []
        for registro in registros:
            fila = [
                registro.dni,
                registro.nombre,
                registro.apellido,
                registro.fecha_nacimiento.strftime('%d/%m/%Y'),
                registro.fecha_ingreso_empresa.strftime('%d/%m/%Y'),               
            ]
            filas.append(fila)

        page_filas = [filas[i:i + items_por_pagina] for i in range(0, len(filas), items_por_pagina)]
        total_pages = len(page_filas)

        # Definir el título dinámico
        titulo_reporte = "Reporte de Operarios"

        context = {
            'encabezados': encabezados,
            'page_filas': page_filas,
            'num_columnas': len(encabezados),
            'current_date': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'current_page': 1,
            'total_pages': total_pages,
            'num_items_filtrados': len(registros),
            'total_items': total_registros,
            'titulo_reporte': titulo_reporte

        }

        return render(request, 'reloj_fichador/reporte.html', context)

    def exportar_excel(self, request, queryset):
        import openpyxl
        from django.http import HttpResponse

        registros = list(queryset)
        encabezados = ['DNI', 'Nombre', 'Apellido', 'Fecha Nacimiento', 'Fecha Ingreso',]

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Reporte de Operarios"
        sheet.append(encabezados)

        for registro in registros:
            fila = [
                registro.dni,
                registro.nombre,
                registro.apellido,
                registro.fecha_nacimiento.strftime('%d/%m/%Y'),
                registro.fecha_ingreso_empresa.strftime('%d/%m/%Y'),
            ]
            sheet.append(fila)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="Reporte_de_Operarios.xlsx"'
        workbook.save(response)

        return response

    exportar_excel.short_description = "Exportar a Excel"


# Resource para importación/exportación de RegistroDiario
class RegistroDiarioResource(resources.ModelResource):
    """
    Resource para manejar importación/exportación de RegistroDiario
    
    GUÍA RÁPIDA PARA USUARIOS:
    
    ✅ EXPORTAR REGISTROS:
    - Haga clic en "EXPORT" en la parte superior del listado
    - Seleccione el formato (Excel recomendado para usuarios básicos)
    - Descargue el archivo con todos los registros
    
    ✅ IMPORTAR REGISTROS:
    - Prepare un archivo Excel con estas columnas:
      * operario__dni: DNI del empleado (ej: 12345678)
      * tipo_movimiento: "entrada" o "salida" 
      * hora_fichada: Fecha y hora (ej: 2025-06-26 08:00:00)
      * valido: "True" o "False"
    
    - Haga clic en "IMPORT" en la parte superior
    - Seleccione su archivo Excel
    - Revise la vista previa antes de confirmar
    - El sistema recalculará automáticamente las horas
    """
    
    # Campos personalizados para exportación/importación
    operario__dni = resources.Field(
        column_name='operario__dni',
        attribute='operario__dni',
        readonly=False
    )
    
    operario__nombre = resources.Field(
        column_name='operario__nombre',
        attribute='operario__nombre',
        readonly=True
    )
    
    operario__apellido = resources.Field(
        column_name='operario__apellido', 
        attribute='operario__apellido',
        readonly=True
    )
    
    class Meta:
        model = RegistroDiario
        fields = ('operario__dni', 'operario__nombre', 'operario__apellido', 
                 'tipo_movimiento', 'hora_fichada', 'valido', 'inconsistencia', 
                 'descripcion_inconsistencia', 'origen_fichada')
        export_order = fields
        # Para determinar si un registro es nuevo o actualización, usar combinación única
        # Nota: Como operario__dni se mapea a operario durante la importación,
        # usaremos campos reales del modelo para identificación
        import_id_fields = []  # Vacío para que siempre cree nuevos registros
        skip_unchanged = True
        report_skipped = True
    
    def dehydrate_operario__dni(self, obj):
        """Exportar el DNI del operario en lugar del ID"""
        return obj.operario.dni if obj.operario else ''
    
    def dehydrate_operario__nombre(self, obj):
        """Exportar el nombre del operario"""
        return obj.operario.nombre if obj.operario else ''
    
    def dehydrate_operario__apellido(self, obj):
        """Exportar el apellido del operario"""
        return obj.operario.apellido if obj.operario else ''
    
    def dehydrate_tipo_movimiento(self, obj):
        """Convertir tipos complejos a tipos simples para importación"""
        # Convertir tipos complejos del sistema a tipos simples
        tipo_map = {
            'entrada_transitoria': 'entrada',
            'salida_transitoria': 'salida',
            'entrada': 'entrada',
            'salida': 'salida'
        }
        return tipo_map.get(obj.tipo_movimiento, obj.tipo_movimiento)
    
    def dehydrate_valido(self, obj):
        """Exportar como True/False string"""
        return 'True' if obj.valido else 'False'
    
    def dehydrate_inconsistencia(self, obj):
        """Exportar como True/False string"""
        return 'True' if obj.inconsistencia else 'False'
    
    def before_import_row(self, row, **kwargs):
        """Procesamiento antes de importar cada fila"""
        # Primero verificar que hay datos válidos en la fila
        if not any(value for value in row.values() if value):
            # Fila vacía, saltarla
            return
        
        # Buscar operario por DNI y asignar el ID
        dni_field = None
        for key in row.keys():
            if 'dni' in str(key).lower():
                dni_field = key
                break
        
        if dni_field and row[dni_field]:
            # Limpiar el DNI (remover espacios y caracteres no numéricos excepto guiones)
            dni = str(row[dni_field]).strip().replace('-', '').replace('.', '').replace(' ', '')
            
            try:
                # Buscar operario por DNI
                operario = Operario.objects.get(dni=dni)
                # Asignar el ID del operario encontrado al campo correcto para la base de datos
                row['operario_id'] = operario.id
                
                # Remover campos de DNI y otros campos de solo exportación
                if dni_field in row:
                    del row[dni_field]
                    
            except Operario.DoesNotExist:
                # Mensaje de error amigable con sugerencias
                raise ValueError(f"❌ Error: No se encontró un operario con DNI '{dni}'. "
                               f"Verifique que:\n"
                               f"• El operario esté registrado en el sistema\n"
                               f"• El DNI esté escrito correctamente\n"
                               f"• No haya espacios o caracteres adicionales")
            except Operario.MultipleObjectsReturned:
                raise ValueError(f"❌ Error: Se encontraron múltiples operarios con DNI '{dni}'. "
                               f"Por favor contacte al administrador para resolver esta duplicación.")
        else:
            # Si no hay DNI, verificar si hay ID de operario directo
            if 'operario_id' not in row or not row['operario_id']:
                raise ValueError("❌ Error: Debe proporcionar el DNI del operario (operario__dni) o el ID del operario.")
        
        # Validar y convertir tipo de movimiento
        if 'tipo_movimiento' in row and row['tipo_movimiento']:
            tipo_original = str(row['tipo_movimiento']).lower().strip()
            
            # Mapear tipos simples a tipos del sistema
            tipo_map = {
                'entrada': 'entrada',
                'salida': 'salida',
                'entrada_transitoria': 'entrada_transitoria',
                'salida_transitoria': 'salida_transitoria'
            }
            
            if tipo_original in tipo_map:
                row['tipo_movimiento'] = tipo_map[tipo_original]
            else:
                raise ValueError(f"❌ Error: '{row['tipo_movimiento']}' no es un tipo válido. "
                               f"Use uno de: 'entrada', 'salida', 'entrada_transitoria' o 'salida_transitoria'.")
        else:
            raise ValueError("❌ Error: El campo 'tipo_movimiento' es obligatorio.")
        
        # Validar formato de fecha
        if 'hora_fichada' in row and row['hora_fichada']:
            try:
                # Intentar parsear la fecha
                from datetime import datetime
                if isinstance(row['hora_fichada'], str):
                    # Intentar varios formatos comunes
                    formatos_fecha = [
                        '%Y-%m-%d %H:%M:%S',
                        '%d/%m/%Y %H:%M:%S',
                        '%d-%m-%Y %H:%M:%S',
                        '%Y-%m-%d %H:%M',
                        '%d/%m/%Y %H:%M',
                        '%d-%m-%Y %H:%M'
                    ]
                    
                    fecha_parseada = None
                    for formato in formatos_fecha:
                        try:
                            fecha_parseada = datetime.strptime(row['hora_fichada'], formato)
                            # Convertir al formato estándar
                            row['hora_fichada'] = fecha_parseada.strftime('%Y-%m-%d %H:%M:%S')
                            break
                        except ValueError:
                            continue
                    
                    if not fecha_parseada:
                        raise ValueError("Formato no reconocido")
                        
            except ValueError:
                raise ValueError(f"❌ Error: Formato de fecha incorrecto '{row['hora_fichada']}'. "
                               f"Use uno de estos formatos:\n"
                               f"• YYYY-MM-DD HH:MM:SS (ej: 2025-06-26 08:30:00)\n"
                               f"• DD/MM/YYYY HH:MM:SS (ej: 26/06/2025 08:30:00)\n"
                               f"• DD-MM-YYYY HH:MM:SS (ej: 26-06-2025 08:30:00)")
        else:
            raise ValueError("❌ Error: El campo 'hora_fichada' es obligatorio.")
        
        # Convertir strings de booleanos
        for field in ['valido', 'inconsistencia']:
            if field in row and row[field] is not None and row[field] != '':
                if isinstance(row[field], str):
                    value = str(row[field]).lower().strip()
                    if value in ['true', '1', 'sí', 'si', 'verdadero', 'yes']:
                        row[field] = True
                    elif value in ['false', '0', 'no', 'falso', 'false']:
                        row[field] = False
                    else:
                        # Dejar el valor por defecto
                        if field == 'valido':
                            row[field] = True  # Por defecto válido
                        else:
                            row[field] = False  # Por defecto sin inconsistencias
                elif row[field] == '':
                    # Campo vacío
                    if field == 'valido':
                        row[field] = True
                    else:
                        row[field] = False
        
        # Limpiar campos que son solo para exportación
        campos_readonly = ['operario__nombre', 'operario__apellido', 'id', 'ID']
        for campo in campos_readonly:
            if campo in row:
                del row[campo]
        
        # Asegurar que descripcion_inconsistencia tenga un valor por defecto si está vacío
        if 'descripcion_inconsistencia' in row and not row['descripcion_inconsistencia']:
            row['descripcion_inconsistencia'] = ''

    def get_or_init_instance(self, instance_loader, row):
        """
        Buscar instancia existente o crear nueva basándose en operario y hora_fichada
        """
        try:
            # Si tenemos operario_id y hora_fichada, buscar registro existente
            if 'operario_id' in row and 'hora_fichada' in row:
                operario_id = row['operario_id']
                hora_fichada = row['hora_fichada']
                
                # Convertir hora_fichada a datetime si es string
                if isinstance(hora_fichada, str):
                    from datetime import datetime
                    hora_fichada = datetime.strptime(hora_fichada, '%Y-%m-%d %H:%M:%S')
                
                try:
                    # Buscar registro existente
                    instance = RegistroDiario.objects.get(
                        operario_id=operario_id,
                        hora_fichada=hora_fichada
                    )
                    return instance, False  # Existente, no es nuevo
                except RegistroDiario.DoesNotExist:
                    # No existe, crear nuevo
                    pass
                except RegistroDiario.MultipleObjectsReturned:
                    # Si hay múltiples, tomar el primero y continuar
                    instance = RegistroDiario.objects.filter(
                        operario_id=operario_id,
                        hora_fichada=hora_fichada
                    ).first()
                    return instance, False
        except Exception:
            # Si hay cualquier error, crear nueva instancia
            pass
        
        # Crear nueva instancia
        return self._meta.model(), True
    
    def after_import_instance(self, instance, new, row_dict=None, **kwargs):
        """Procesamiento después de importar cada instancia"""
        # Asegurar que tenemos un origen_fichada para registros nuevos importados
        if new and not instance.origen_fichada:
            instance.origen_fichada = 'Importado'
        
        # Asegurar valores por defecto
        if instance.valido is None:
            instance.valido = True
        if instance.inconsistencia is None:
            instance.inconsistencia = False
        if not instance.descripcion_inconsistencia:
            instance.descripcion_inconsistencia = ''
    
    def after_save_instance(self, instance, using_transactions, dry_run):
        """Después de guardar, recalcular horas si no es dry_run"""
        if not dry_run:
            # Recalcular horas trabajadas para este registro
            actualizar_horas_despues_de_guardar(sender=RegistroDiario, instance=instance)
    
    def get_import_headers(self):
        """Personalizar encabezados de importación con explicaciones"""
        headers = super().get_import_headers()
        return [
            'operario__dni (DNI del empleado - solo números)',
            'tipo_movimiento (entrada o salida)',
            'hora_fichada (YYYY-MM-DD HH:MM:SS)',
            'valido (True o False)',
            'descripcion_inconsistencia (opcional)',
        ]


@admin.register(RegistroDiario)
class RegistroDiarioAdmin(ImportExportMixin, SimpleHistoryAdmin, UnfoldModelAdmin):
    resource_class = RegistroDiarioResource
    list_display = ('get_dni', 'get_nombre', 'get_apellido', 'tipo_movimiento', 'formatted_hora_fichada', 
                    'origen_fichada', 'mostrar_inconsistencia', 'mostrar_valido', 'view_history_button')
    list_filter = ('inconsistencia','valido','tipo_movimiento', ('hora_fichada', DateRangeFilter),'origen_fichada',)
    search_fields = ('operario__dni', 'operario__nombre', 'operario__apellido')
    fields = ('operario', 'tipo_movimiento', 'hora_fichada', 'valido','descripcion_inconsistencia',)
    actions = ['generar_reporte', 'exportar_excel', 'exportar_pdf', 'recalcular_horas']

    HEADER_MAP = {
        'get_dni': 'DNI',
        'get_nombre': 'Nombre',
        'get_apellido': 'Apellido',
        'tipo_movimiento': 'Tipo Movimiento',
        'formatted_hora_fichada': 'Hora Fichada',
        'origen_fichada': 'Origen Fichada',
    }

    def get_dni(self, obj):
        return obj.operario.dni
    get_dni.short_description = 'DNI'

    def get_nombre(self, obj):
        return obj.operario.nombre
    get_nombre.short_description = 'Nombre'

    def get_apellido(self, obj):
        return obj.operario.apellido
    get_apellido.short_description = 'Apellido'

    def formatted_hora_fichada(self, obj):
        if obj.hora_fichada:
            # Convertir a la zona horaria de Argentina
            argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
            hora_local = obj.hora_fichada
            if hora_local.tzinfo is not None:  # Si la fecha tiene zona horaria
                hora_local = hora_local.astimezone(argentina_tz)
            return hora_local.strftime('%d/%m/%Y %H:%M:%S')
        return ''
    formatted_hora_fichada.short_description = 'Hora Fichada'

    def save_model(self, request, obj, form, change):
        if not change:  # Solo si es un nuevo registro
            obj.origen_fichada = 'Manual'
        obj.save()

    def mostrar_inconsistencia(self, obj):
        if obj.inconsistencia:
            return format_html('<span style="color: red; font-weight: bold;">Sí</span>')
        else:
            return format_html('<span style="color: green;">No</span>')
    mostrar_inconsistencia.short_description = 'Inconsistencia'
    mostrar_inconsistencia.admin_order_field = 'inconsistencia'

    def mostrar_valido(self, obj):
        if obj.valido:
            return format_html('<span style="color: green; font-weight: bold;">Sí</span>')
        else:
            return format_html('<span style="color: red;">No</span>')
    mostrar_valido.short_description = 'Válido'
    mostrar_valido.admin_order_field = 'valido'

    def view_history_button(self, obj):
        """Mostrar un botón para ver el historial del registro"""
        if obj.pk:
            url = reverse('admin:reloj_fichador_historicalregistrodiario_changelist') + f"?id={obj.pk}"
            return format_html(
                '<a class="button" href="{}">Ver Historial</a>',
                url
            )
        return ""
    view_history_button.short_description = "Historial"

    def generar_reporte(self, request, queryset):
        registros = list(queryset)  # Convertir a lista para poder trabajar con slicing
        total_registros = RegistroDiario.objects.count()  # Total sin filtrar
        items_por_pagina = 30  # Limitar a 30 ítems por página

        # Definir los encabezados manualmente
        encabezados = ['DNI', 'Nombre', 'Apellido','Hora Fichada', 'Tipo Movimiento', 'Origen Fichada']

        # Preparar zona horaria de Argentina
        argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')

        # Filas con valores de cada campo
        filas = []
        for registro in registros:
            # Convertir hora a zona horaria de Argentina
            hora_local = registro.hora_fichada
            if hora_local.tzinfo is not None:
                hora_local = hora_local.astimezone(argentina_tz)
            
            fila = [
                registro.operario.dni,
                registro.operario.nombre,
                registro.operario.apellido,
                hora_local.strftime('%d/%m/%Y %H:%M:%S'),
                registro.tipo_movimiento.replace('_', ' ').capitalize(),
                registro.origen_fichada.capitalize(),
            ]
            filas.append(fila)

        # Dividir las filas en páginas de 30 ítems
        page_filas = [filas[i:i + items_por_pagina] for i in range(0, len(filas), items_por_pagina)]
        total_pages = len(page_filas)

        # Definir el título dinámico
        titulo_reporte = "Reporte de Registro Diario"

        # Obtener hora actual en Argentina para el reporte
        hora_actual = timezone.now().astimezone(argentina_tz)

        # Renderizar el template HTML con los datos dinámicos
        context = {
            'encabezados': encabezados,
            'page_filas': page_filas,  # Pasamos las filas ya divididas por páginas
            'num_columnas': len(encabezados),
            'current_date': hora_actual.strftime('%d/%m/%Y %H:%M'),
            'current_page': 1,  # Este valor se puede manejar mejor dentro del template
            'total_pages': total_pages,  # Total de páginas
            'num_items_filtrados': len(registros),  # Número de registros filtrados
            'total_items': total_registros,
            'titulo_reporte': titulo_reporte          # Número total de registros
        }

        return render(request, 'reloj_fichador/reporte.html', context)


    def exportar_excel(self, request, queryset):
        import openpyxl
        from django.http import HttpResponse

        registros = list(queryset)  # Convertir a lista para trabajar fácilmente
        total_registros = RegistroDiario.objects.count()  # Total sin filtrar
        
        # Definir los encabezados manualmente
        encabezados = ['DNI', 'Nombre', 'Apellido', 'Hora Fichada', 'Tipo Movimiento', 'Origen Fichada']
        
        # Preparar zona horaria de Argentina
        argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
        
        # Crear un nuevo archivo Excel
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Reporte de Registro Diario"
        
        # Escribir los encabezados en la primera fila
        sheet.append(encabezados)
        
        # Filas con valores de cada campo
        for registro in registros:
            # Convertir hora a zona horaria de Argentina
            hora_local = registro.hora_fichada
            if hora_local.tzinfo is not None:
                hora_local = hora_local.astimezone(argentina_tz)
                
            fila = [
                registro.operario.dni,
                registro.operario.nombre,
                registro.operario.apellido,
                hora_local.strftime('%d/%m/%Y %H:%M:%S'),
                registro.tipo_movimiento.replace('_', ' ').capitalize(),
                registro.origen_fichada.capitalize(),
            ]
            sheet.append(fila)  # Añadir cada fila al archivo Excel
        
        # Preparar la respuesta HTTP para la descarga del archivo Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="Reporte_de_Registro_Diario.xlsx"'
        
        # Guardar el archivo Excel en la respuesta
        workbook.save(response)
        
        return response

    exportar_excel.short_description = "Exportar a Excel"

    def recalcular_horas(self, request, queryset):
        for registro in queryset:
            # Ejecutar la función de signals manualmente para cada registro
            actualizar_horas_despues_de_guardar(sender=RegistroDiario, instance=registro)
        
        self.message_user(request, f"Se han recalculado las horas para {queryset.count()} registros.")
    
    recalcular_horas.short_description = "Recalcular horas trabajadas para estos registros"
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:registro_id>/recalcular/', self.admin_site.admin_view(self.recalcular_registro), 
                name='reloj_fichador_registrodiario_recalcular'),
        ]
        return custom_urls + urls
    
    def recalcular_registro(self, request, registro_id):
        registro = self.get_object(request, registro_id)
        if registro:
            actualizar_horas_despues_de_guardar(sender=RegistroDiario, instance=registro)
            self.message_user(request, f"Se han recalculado las horas para el registro de {registro.operario}.")
        return HttpResponseRedirect(reverse('admin:reloj_fichador_registrodiario_change', args=[registro_id]))
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_recalcular_button'] = True
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def recalcular_todas_horas(self, request):
        from .models import Operario, RegistroDiario, Horas_extras
        import datetime

        operarios = Operario.objects.filter(activo=True)
        contador = 0

        for operario in operarios:
            registros = RegistroDiario.objects.filter(
                operario=operario,
                valido=True
            ).order_by('hora_fichada')

            fechas = set()
            for registro in registros:
                # Recalcula horas trabajadas (incluye extras en Horas_trabajadas)
                actualizar_horas_despues_de_guardar(sender=RegistroDiario, instance=registro)
                fechas.add(registro.hora_fichada.date())
                contador += 1

            # Ahora recalcula Horas_extras para cada fecha de ese operario
            for fecha in fechas:
                Horas_extras.calcular_horas_extras(operario, fecha)

        self.message_user(request, f"Se han recalculado las horas para {contador} registros y horas extras asociadas.")
        return HttpResponseRedirect(reverse('admin:reloj_fichador_horas_trabajadas_changelist'))

    def recalcular_horas_trabajadas(self, request, queryset):
        from .models import RegistroDiario
        for ht in queryset:
            # Buscar registros de ese operario en esa fecha
            registros = RegistroDiario.objects.filter(
                operario=ht.operario,
                hora_fichada__date=ht.fecha
            ).order_by('hora_fichada')
            
            if registros.exists():
                # Tomar el primer registro como muestra para recalcular
                registro = registros.first()
                actualizar_horas_despues_de_guardar(sender=RegistroDiario, instance=registro)
                
        self.message_user(request, f"Se han recalculado las horas para {queryset.count()} registros.")
    
    recalcular_horas_trabajadas.short_description = "Recalcular horas seleccionadas"

@admin.register(Horas_trabajadas)
class HorasTrabajadasAdmin(ExportMixin, UnfoldModelAdmin):
    list_display = ('operario', 'fecha', 'get_horas_normales', 'get_horas_nocturnas')
    search_fields = ('operario__dni', 'operario__nombre', 'operario__apellido')
    list_filter = ('fecha', ('fecha', DateRangeFilter))
    actions = ['generar_reporte', 'exportar_excel', 'exportar_pdf', 'recalcular_horas_trabajadas']
    change_list_template = 'admin/reloj_fichador/horas_trabajadas/change_list.html'

    def get_queryset(self, request):
        """
        Optimiza la consulta con select_related.
        Ya no filtramos los registros con 0 horas para mostrar todos los operarios.
        """
        return super().get_queryset(request).select_related('operario')

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

    def generar_reporte(self, request, queryset):
        registros = list(queryset)
        total_registros = Horas_trabajadas.objects.count()
        items_por_pagina = 30

        encabezados = ['DNI', 'Nombre', 'Apellido', 'Fecha', 'Horas Trabajadas', 'Horas Nocturnas']
        filas = []
        for registro in registros:
            fila = [
                registro.operario.dni,
                registro.operario.nombre,
                registro.operario.apellido,
                registro.fecha.strftime('%d/%m/%Y'),
                self.get_horas_normales(registro),
                self.get_horas_nocturnas(registro),
            ]
            filas.append(fila)

        # Dividir las filas en páginas de 30 ítems
        page_filas = [filas[i:i + items_por_pagina] for i in range(0, len(filas), items_por_pagina)]
        total_pages = len(page_filas)

        # Definir el título dinámico
        titulo_reporte = "Reporte de Horas Trabajadas"

        context = {
            'encabezados': encabezados,
            'page_filas': page_filas,
            'num_columnas': len(encabezados),
            'current_date': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'current_page': 1,
            'total_pages': total_pages,
            'num_items_filtrados': len(registros),
            'total_items': total_registros,
            'titulo_reporte': titulo_reporte
        }

        return render(request, 'reloj_fichador/reporte.html', context)

    def exportar_excel(self, request, queryset):
        import openpyxl
        from django.http import HttpResponse

        registros = list(queryset)
        encabezados = ['DNI', 'Nombre', 'Apellido', 'Fecha', 'Horas Trabajadas', 'Horas Nocturnas']
        
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Reporte de Horas Trabajadas"
        sheet.append(encabezados)
        
        for registro in registros:
            fila = [
                registro.operario.dni,
                registro.operario.nombre,
                registro.operario.apellido,
                registro.fecha.strftime('%d/%m/%Y'),
                self.get_horas_normales(registro),
                self.get_horas_nocturnas(registro),
            ]
            sheet.append(fila)
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="Reporte_Horas_Trabajadas.xlsx"'
        workbook.save(response)
        
        return response

    exportar_excel.short_description = "Exportar a Excel"

    def exportar_pdf(self, request, queryset):
        # Usar la función generar_pdf con cálculo automático de totales de horas
        return exportar_pdf(self, request, queryset, calculate_hours_total=True)

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:horas_id>/recalcular/', self.admin_site.admin_view(self.recalcular_horas), 
                name='reloj_fichador_horas_trabajadas_recalcular'),
            path('recalcular-todas/', self.admin_site.admin_view(self.recalcular_todas_horas), 
                name='reloj_fichador_horas_trabajadas_recalcular_todas'),
        ]
        return custom_urls + urls
    
    def recalcular_horas(self, request, horas_id):
        from .models import RegistroDiario
        horas = self.get_object(request, horas_id)
        if horas:
            # Buscar registros de ese operario en esa fecha
            registros = RegistroDiario.objects.filter(
                operario=horas.operario,
                hora_fichada__date=horas.fecha
            ).order_by('hora_fichada')
            
            if registros.exists():
                # Tomar el primer registro como muestra para recalcular
                registro = registros.first()
                actualizar_horas_despues_de_guardar(sender=RegistroDiario, instance=registro)
                self.message_user(request, f"Se han recalculado las horas para {horas.operario} en la fecha {horas.fecha}.")
        
        return HttpResponseRedirect(reverse('admin:reloj_fichador_horas_trabajadas_change', args=[horas_id]))
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_recalcular_button'] = True
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def recalcular_todas_horas(self, request):
        from .models import Operario, RegistroDiario
        import datetime
        
        # Obtener todos los operarios activos
        operarios = Operario.objects.filter(activo=True)
        contador = 0
        
        for operario in operarios:
            # Buscar registros de este operario
            registros = RegistroDiario.objects.filter(
                operario=operario,
                valido=True
            ).order_by('hora_fichada')
            
            if registros.exists():
                # Tomar el registro más reciente
                registro = registros.last()
                # Recalcular horas para este operario
                actualizar_horas_despues_de_guardar(sender=RegistroDiario, instance=registro)
                contador += 1
        
        self.message_user(request, f"Se han recalculado las horas para {contador} operarios.")
        return HttpResponseRedirect(reverse('admin:reloj_fichador_horas_trabajadas_changelist'))


@admin.register(Horas_extras)
class HorasExtrasAdmin(ExportMixin, UnfoldModelAdmin):
    list_display = ('operario', 'fecha', 'get_horas_extras')
    search_fields = ('operario__dni', 'operario__nombre', 'operario__apellido')
    list_filter = ('fecha', ('fecha', DateRangeFilter))
    actions = ['generar_reporte', 'exportar_excel', 'exportar_pdf']

    def get_queryset(self, request):
        """
        Filtra los registros para ocultar aquellos con 0 horas extras.
        Optimiza la consulta con select_related.
        """
        queryset = super().get_queryset(request).select_related('operario')
        return queryset.exclude(horas_extras=timedelta(0))


    def get_horas_extras(self, obj):
        total_seconds = obj.horas_extras.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

    get_horas_extras.short_description = 'Horas Extras'

    def generar_reporte(self, request, queryset):
        registros = list(queryset)
        total_registros = Horas_extras.objects.count()
        items_por_pagina = 30

        encabezados = ['DNI', 'Nombre', 'Apellido', 'Fecha', 'Horas Extras']
        filas = []
        for registro in registros:
            fila = [
                registro.operario.dni,
                registro.operario.nombre,
                registro.operario.apellido,
                registro.fecha.strftime('%d/%m/%Y'),
                self.get_horas_extras(registro),
            ]
            filas.append(fila)

        # Dividir las filas en páginas de 30 ítems
        page_filas = [filas[i:i + items_por_pagina] for i in range(0, len(filas), items_por_pagina)]
        total_pages = len(page_filas)

         # Definir el título dinámico
        titulo_reporte = "Reporte de Horas Extras"

        context = {
            'encabezados': encabezados,
            'page_filas': page_filas,
            'num_columnas': len(encabezados),
            'current_date': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'current_page': 1,
            'total_pages': total_pages,
            'num_items_filtrados': len(registros),
            'total_items': total_registros,
            'titulo_reporte': titulo_reporte
        }

        return render(request, 'reloj_fichador/reporte.html', context)

    def exportar_excel(self, request, queryset):
        import openpyxl
        from django.http import HttpResponse

        registros = list(queryset)
        encabezados = ['DNI', 'Nombre', 'Apellido', 'Fecha', 'Horas Extras']
        
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Reporte de Horas Extras"
        sheet.append(encabezados)
        
        for registro in registros:
            fila = [
                registro.operario.dni,
                registro.operario.nombre,
                registro.operario.apellido,
                registro.fecha.strftime('%d/%m/%Y'),
                self.get_horas_extras(registro),
            ]
            sheet.append(fila)
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="Reporte_Horas_Extras.xlsx"'
        workbook.save(response)
        
        return response

    exportar_excel.short_description = "Exportar a Excel"

    def exportar_pdf(self, request, queryset):
        # Usar la función generar_pdf con cálculo automático de totales de horas
        return exportar_pdf(self, request, queryset, calculate_hours_total=True)



@admin.register(Horas_totales)
class HorasTotalesAdmin(ExportMixin, UnfoldModelAdmin):
    list_display = ('get_dni', 'operario','get_mes', 'get_horas_normales', 'get_horas_nocturnas', 'get_horas_extras', 'get_horas_feriado')
    search_fields = ('operario__dni', 'operario__nombre', 'operario__apellido')
    list_filter = ('mes_actual',)
    actions = ['generar_reporte', 'exportar_excel', 'exportar_pdf']
    change_list_template = 'admin/reloj_fichador/horas_totales/change_list.html'

    def get_queryset(self, request):
        """
        Optimiza la consulta con select_related.
        Ya no filtramos los registros con 0 horas para mostrar todos los operarios.
        """
        return super().get_queryset(request).select_related('operario')
    
    def get_mes(self, obj):
        try:
            anio, mes = obj.mes_actual.split('-')
            return f"{mes}/{anio}"
        except Exception as e:
            return obj.mes_actual
    get_mes.short_description = 'Mes'
        

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

    def generar_reporte(self, request, queryset):
        registros = list(queryset)
        total_registros = Horas_totales.objects.count()
        items_por_pagina = 30

        encabezados = ['DNI', 'Nombre', 'Apellido', 'Horas Normales', 'Horas Nocturnas', 'Horas Extras', 'Horas Feriado']
        filas = []
        for registro in registros:
            fila = [
                registro.operario.dni,
                registro.operario.nombre,
                registro.operario.apellido,
                self.get_horas_normales(registro),
                self.get_horas_nocturnas(registro),
                self.get_horas_extras(registro),
                self.get_horas_feriado(registro),
            ]
            filas.append(fila)

        # Dividir las filas en páginas de 30 ítems
        page_filas = [filas[i:i + items_por_pagina] for i in range(0, len(filas), items_por_pagina)]
        total_pages = len(page_filas)

        # Definir el título dinámico
        titulo_reporte = "Reporte de Horas Extras"

        context = {
            'encabezados': encabezados,
            'page_filas': page_filas,
            'num_columnas': len(encabezados),
            'current_date': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'current_page': 1,
            'total_pages': total_pages,
            'num_items_filtrados': len(registros),
            'total_items': total_registros,
            'titulo_reporte': titulo_reporte
        }

        return render(request, 'reloj_fichador/reporte.html', context)

    def exportar_excel(self, request, queryset):
        import openpyxl
        from django.http import HttpResponse

        registros = list(queryset)
        encabezados = ['DNI', 'Nombre', 'Apellido', 'Horas Normales', 'Horas Nocturnas', 'Horas Extras', 'Horas Feriado']
        
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Reporte de Horas Totales"
        sheet.append(encabezados)
        
        for registro in registros:
            fila = [
                registro.operario.dni,
                registro.operario.nombre,
                registro.operario.apellido,
                self.get_horas_normales(registro),
                self.get_horas_nocturnas(registro),
                self.get_horas_extras(registro),
                self.get_horas_feriado(registro),
            ]
            sheet.append(fila)
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="Reporte_Horas_Totales.xlsx"'
        workbook.save(response)
        
        return response

    exportar_excel.short_description = "Exportar a Excel"

    def exportar_pdf(self, request, queryset):
        # Usar la función generar_pdf con cálculo automático de totales de horas
        return exportar_pdf(self, request, queryset, calculate_hours_total=True)

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('recalcular-todas/', self.admin_site.admin_view(self.recalcular_todas_horas), 
                name='reloj_fichador_horas_totales_recalcular_todas'),
        ]
        return custom_urls + urls
    
    def recalcular_todas_horas(self, request):
        from .models import Operario, RegistroDiario
        import datetime
        
        # Obtener todos los operarios activos
        operarios = Operario.objects.filter(activo=True)
        contador = 0
        
        # Obtener mes actual en formato YYYY-MM
        mes_actual = datetime.datetime.now().strftime('%Y-%m')
        
        for operario in operarios:
            # Buscar registros de este operario
            registros = RegistroDiario.objects.filter(
                operario=operario,
                valido=True
            ).order_by('hora_fichada')
            
            if registros.exists():
                # Tomar el registro más reciente
                registro = registros.last()
                # Recalcular horas para este operario
                actualizar_horas_despues_de_guardar(sender=RegistroDiario, instance=registro)
                contador += 1
        
        self.message_user(request, f"Se han recalculado las horas para {contador} operarios.")
        return HttpResponseRedirect(reverse('admin:reloj_fichador_horas_trabajadas_changelist'))


@admin.register(RegistroAsistencia)
class RegistroAsistenciaAdmin(ExportMixin, UnfoldModelAdmin):
    list_display = (
        'operario', 'fecha', 'estado_asistencia', 'estado_justificacion_selector', 'descripcion', 'acciones'
    )
    list_filter = ('estado_asistencia', 'estado_justificacion', 'fecha')
    search_fields = ('operario__dni', 'operario__nombre', 'operario__apellido')
    actions = ['marcar_justificado', 'marcar_no_justificado', 'generar_reporte', 'exportar_excel', 'exportar_pdf']

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

    def generar_reporte(self, request, queryset):
        registros = list(queryset)
        total_registros = RegistroAsistencia.objects.count()
        items_por_pagina = 20

        encabezados = ['Operario', 'Fecha', 'Estado Asistencia', 'Justificación', 'Descripción']

        filas = []
        for registro in registros:
            fila = [
                registro.operario,
                registro.fecha.strftime('%d/%m/%Y'),
                registro.estado_asistencia.capitalize(),
                '✅' if registro.estado_justificacion else '❌',
                registro.descripcion or ''
            ]
            filas.append(fila)

        # Dividir las filas en páginas de 30 ítems
        page_filas = [filas[i:i + items_por_pagina] for i in range(0, len(filas), items_por_pagina)]
        total_pages = len(page_filas)

        # Definir el título dinámico
        titulo_reporte = "Reporte de Asistencias"

        context = {
            'encabezados': encabezados,
            'page_filas': page_filas,
            'num_columnas': len(encabezados),
            'current_date': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'current_page': 1,
            'total_pages': total_pages,
            'num_items_filtrados': len(registros),
            'total_items': total_registros,
            'titulo_reporte': titulo_reporte
        }

        return render(request, 'reloj_fichador/reporte.html', context)

    def exportar_excel(self, request, queryset):
        import openpyxl
        from django.http import HttpResponse

        registros = list(queryset)
        encabezados = ['Operario', 'Fecha', 'Estado Asistencia', 'Justificación', 'Descripción']

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Reporte de Registro de Asistencia"
        sheet.append(encabezados)

        for registro in registros:
            fila = [
                str(registro.operario),
                registro.fecha.strftime('%d/%m/%Y'),
                registro.estado_asistencia.capitalize(),
                '✅' if registro.estado_justificacion else '❌',
                registro.descripcion or ''
            ]
            sheet.append(fila)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="Reporte_de_Registro_Asistencia.xlsx"'
        workbook.save(response)

        return response

    exportar_excel.short_description = "Exportar a Excel"

    def exportar_pdf(self, request, queryset):
        # Usar la función generar_pdf con cálculo automático de totales de horas
        return exportar_pdf(self, request, queryset, calculate_hours_total=True)

@admin.register(Horario)
class HorarioAdmin(ExportarPDFMixin, UnfoldModelAdmin):
    list_display = ('nombre', 'hora_inicio', 'hora_fin')
    search_fields = ('nombre',)

@admin.register(Area)
class AreaAdmin(ExportarPDFMixin, UnfoldModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    filter_horizontal = ('horarios',)

@admin.register(Horas_feriado)
class HorasFeriadoAdmin(ExportMixin, UnfoldModelAdmin):
    list_display = ('operario', 'fecha', 'horas_feriado')
    search_fields = ('operario__dni', 'operario__nombre', 'operario__apellido')
    list_filter = ('fecha', ('fecha', DateRangeFilter))
    actions = ['exportar_pdf', 'exportar_excel']

    def exportar_pdf(self, request, queryset):
        # Usar la función generar_pdf con cálculo automático de totales de horas
        return exportar_pdf(self, request, queryset, calculate_hours_total=True)

@admin.register(LogEntry)
class LogEntryAdmin(ExportarPDFMixin, UnfoldModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message')
    list_filter = ('action_flag', 'user', 'content_type')
    search_fields = ('object_repr', 'change_message', 'user__username')
    readonly_fields = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message')
    
    def has_add_permission(self, request):
        return False  # Evita que se puedan añadir nuevos registros desde el admin
    
    def has_change_permission(self, request, obj=None):
        return False  # Evita cambios en los registros

    def has_delete_permission(self, request, obj=None):
        return False  # Evita eliminación de registros

    def action_flag(self, obj):
        """
        Muestra una representación más amigable de las acciones.
        """
        if obj.action_flag == 1:
            return format_html('<span style="color:green;">Creación</span>')
        elif obj.action_flag == 2:
            return format_html('<span style="color:orange;">Edición</span>')
        elif obj.action_flag == 3:
            return format_html('<span style="color:red;">Eliminación</span>')
        return obj.action_flag

    action_flag.short_description = 'Acción'

# Registro de modelos históricos
@admin.register(HistoricalOperario)
class HistoricalOperarioAdmin(UnfoldModelAdmin):
    list_display = ('dni', 'nombre', 'apellido', 'activo', 'history_date', 'history_user', 'history_type')
    list_filter = ('history_date', 'history_type', 'activo')
    search_fields = ('dni', 'nombre', 'apellido', 'history_user__username')
    readonly_fields = ('dni', 'nombre', 'apellido', 'history_date', 'history_user', 'history_type')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(HistoricalRegistroDiario)
class HistoricalRegistroDiarioAdmin(UnfoldModelAdmin):
    list_display = ('get_operario', 'tipo_movimiento', 'formatted_hora_fichada', 'valido', 'inconsistencia', 'history_date', 'history_user', 'history_type')
    list_filter = ('history_date', 'history_type', 'tipo_movimiento', 'valido', 'inconsistencia')
    search_fields = ('operario__dni', 'operario__nombre', 'operario__apellido', 'history_user__username')
    readonly_fields = ('tipo_movimiento', 'hora_fichada', 'valido', 'inconsistencia', 'history_date', 'history_user', 'history_type')
    
    def formatted_hora_fichada(self, obj):
        if obj.hora_fichada:
            # Convertir a la zona horaria de Argentina
            argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
            hora_local = obj.hora_fichada
            if hora_local.tzinfo is not None:  # Si la fecha tiene zona horaria
                hora_local = hora_local.astimezone(argentina_tz)
            return hora_local.strftime('%d/%m/%Y %H:%M:%S')
        return ''
    formatted_hora_fichada.short_description = 'Hora Fichada'
    
    def get_operario(self, obj):
        return f"{obj.operario}" if obj.operario else '—'
    get_operario.short_description = 'Operario'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(HistoricalLicencia)
class HistoricalLicenciaAdmin(UnfoldModelAdmin):
    list_display = ('get_operario', 'descripcion_corta', 'estado', 'fecha_inicio', 'fecha_fin', 'history_date', 'history_user', 'history_type')
    list_filter = ('history_date', 'history_type', 'estado', 'aplicar_a_asistencia')
    search_fields = ('operario__dni', 'operario__nombre', 'operario__apellido', 'descripcion', 'history_user__username')
    readonly_fields = ('operario', 'descripcion', 'estado', 'fecha_inicio', 'fecha_fin', 'archivo', 
                      'aplicar_a_asistencia', 'aprobada_por', 'observaciones', 
                      'history_date', 'history_user', 'history_type')
    
    def get_operario(self, obj):
        return f"{obj.operario}" if obj.operario else '—'
    get_operario.short_description = 'Operario'
    
    def descripcion_corta(self, obj):
        if obj.descripcion:
            texto = obj.descripcion[:50]
            if len(obj.descripcion) > 50:
                texto += '...'
            return texto
        return '-'
    descripcion_corta.short_description = 'Descripción'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

# Asignar la función exportar_pdf a cada clase
OperarioAdmin.exportar_pdf = exportar_pdf
RegistroDiarioAdmin.exportar_pdf = exportar_pdf  # Usar la versión sin cálculo de totales
HorarioAdmin.exportar_pdf = exportar_pdf
AreaAdmin.exportar_pdf = exportar_pdf
LogEntryAdmin.exportar_pdf = exportar_pdf
RegistroAsistenciaAdmin.exportar_pdf = exportar_pdf

# Personalizar exportar_pdf para añadir totales en reportes de horas
def exportar_pdf_con_totales(modeladmin, request, queryset):
    """Función específica para exportar reportes con totales de horas"""
    return exportar_pdf(modeladmin, request, queryset, calculate_hours_total=True)

exportar_pdf_con_totales.short_description = "Exportar seleccionados a PDF (con totales)"

# Asignar la función personalizada SOLO a las clases de horas
HorasTrabajadasAdmin.exportar_pdf = exportar_pdf_con_totales
HorasExtrasAdmin.exportar_pdf = exportar_pdf_con_totales
HorasTotalesAdmin.exportar_pdf = exportar_pdf_con_totales
HorasFeriadoAdmin.exportar_pdf = exportar_pdf_con_totales

# Personalizar el admin de User para limitar permisos
class RestrictedUserAdmin(UserAdmin, UnfoldModelAdmin):
    """
    Administrador personalizado para User que restringe la edición
    de usuarios de manera que los usuarios staff solo puedan editar
    su propio perfil, mientras que los superusuarios pueden editar cualquiera.

    Integrado con Unfold para una interfaz moderna.
    """

    # Formularios de Unfold para User
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    def has_change_permission(self, request, obj=None):
        # Si el usuario es superusuario, tiene permiso completo
        if request.user.is_superuser:
            return True
        
        # Si estamos comprobando permisos generales (sin objeto específico)
        if obj is None:
            return True
        
        # Los usuarios solo pueden modificar sus propios datos
        return obj == request.user
    
    def get_list_filter(self, request):
        # Mostrar filtros solo a superusuarios
        if request.user.is_superuser:
            return super().get_list_filter(request)
        return []
    
    def get_queryset(self, request):
        # Superusuarios ven todos los usuarios, el resto solo se ve a sí mismo
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(pk=request.user.pk)
    
    def changelist_view(self, request, extra_context=None):
        # Si el usuario no es superusuario, redirigir directamente a su página de edición
        if not request.user.is_superuser:
            return HttpResponseRedirect(
                reverse('admin:auth_user_change', args=(request.user.id,))
            )
        return super().changelist_view(request, extra_context)
    
    def has_module_permission(self, request):
        # Todos los usuarios staff pueden ver el módulo
        return request.user.is_staff
    
    def has_add_permission(self, request):
        # Solo superusuarios pueden añadir usuarios
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        # Solo superusuarios pueden eliminar usuarios
        return request.user.is_superuser
    
    def get_fieldsets(self, request, obj=None):
        # Definir los campos visibles según el tipo de usuario
        if not obj:
            return super().get_fieldsets(request, obj)
        
        # Si es superusuario, mostrar todos los campos
        if request.user.is_superuser:
            return super().get_fieldsets(request, obj)
        
        # Para usuarios normales, limitar los campos visibles
        # Eliminar campos de permisos para usuarios no superusuarios
        return [
            (None, {'fields': ('username', 'password')}),
            ('Información personal', {'fields': ('first_name', 'last_name', 'email')}),
        ]


# Clase personalizada para Group con Unfold
class GroupAdmin(BaseGroupAdmin, UnfoldModelAdmin):
    """
    Admin para el modelo Group integrado con Unfold.
    """
    pass

# =============================================================================
# CONFIGURACIÓN DE REDONDEO
# =============================================================================

@admin.register(ConfiguracionRedondeo)
class ConfiguracionRedondeoAdmin(UnfoldModelAdmin):
    """
    Admin para ConfiguracionRedondeo con Unfold.
    """
    list_display = ['id', 'minutos_redondeo_baja', 'minutos_redondeo_media']
    fieldsets = (
        ('Configuración de Redondeo de Entrada', {
            'fields': ('minutos_redondeo_baja', 'minutos_redondeo_media'),
            'description': 'Configura los minutos de redondeo para las entradas de los operarios.'
        }),
    )
    
    def has_add_permission(self, request):
        # Solo permitir un registro
        return not ConfiguracionRedondeo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # No permitir eliminación
        return False


@admin.register(ConfiguracionRedondeoSalida)
class ConfiguracionRedondeoSalidaAdmin(UnfoldModelAdmin):
    """
    Admin para ConfiguracionRedondeoSalida con Unfold.
    """
    list_display = ['id', 'minutos_redondeo_salida']
    fieldsets = (
        ('Configuración de Redondeo de Salida', {
            'fields': ('minutos_redondeo_salida',),
            'description': 'Configura los minutos de redondeo para las salidas de los operarios.'
        }),
    )
    
    def has_add_permission(self, request):
        # Solo permitir un registro
        return not ConfiguracionRedondeoSalida.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # No permitir eliminación
        return False


# Desregistrar los modelos predeterminados y registrar con Unfold
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, RestrictedUserAdmin)
admin.site.register(Group, GroupAdmin)


# =============================================================================
# SECCIÓN DE REPORTES
# =============================================================================

class ReporteManager:
    """Gestor de reportes personalizado"""
    
    @staticmethod
    def generar_reporte_asistencia(fecha_inicio=None, fecha_fin=None, operarios=None):
        """Genera reporte de asistencia por período con resumen de horas"""
        from django.db.models import Q, Sum, Count
        from datetime import datetime, date
        
        # Filtros base para registros
        filtros = Q(valido=True)
        
        if fecha_inicio:
            filtros &= Q(hora_fichada__date__gte=fecha_inicio)
        if fecha_fin:
            filtros &= Q(hora_fichada__date__lte=fecha_fin)
        if operarios:
            filtros &= Q(operario__in=operarios)
            
        registros = RegistroDiario.objects.filter(filtros).select_related('operario').order_by('operario__apellido', 'hora_fichada')
        
        # Agrupar por operario
        reporte_data = {}
        operarios_en_reporte = set()
        
        for registro in registros:
            operario = registro.operario
            operarios_en_reporte.add(operario)
            if operario not in reporte_data:
                reporte_data[operario] = {
                    'registros': [],
                    'resumen_horas': None,
                    'horas_por_fecha': {}  # Para almacenar horas trabajadas por fecha
                }
            reporte_data[operario]['registros'].append(registro)
        
        # Calcular resumen de horas trabajadas para el período
        filtros_horas = Q()
        if fecha_inicio:
            filtros_horas &= Q(fecha__gte=fecha_inicio)
        if fecha_fin:
            filtros_horas &= Q(fecha__lte=fecha_fin)
        if operarios:
            filtros_horas &= Q(operario__in=operarios)
        else:
            # Si no se especificaron operarios, usar solo los que aparecen en el reporte
            filtros_horas &= Q(operario__in=operarios_en_reporte)
            
        # Obtener horas trabajadas agrupadas por operario
        from django.db.models import DurationField
        from django.db.models.functions import Coalesce
        
        horas_resumen = Horas_trabajadas.objects.filter(filtros_horas).values(
            'operario',
            'operario__apellido', 
            'operario__nombre',
            'operario__dni'
        ).annotate(
            total_horas_normales=Sum('horas_normales'),
            total_horas_nocturnas=Sum('horas_nocturnas'), 
            total_horas_extras=Sum('horas_extras'),
            dias_trabajados=Count('fecha')  # Contar los días únicos trabajados
        ).order_by('operario__apellido')
        
        # Agregar resumen al reporte_data
        for resumen in horas_resumen:
            operario_id = resumen['operario']
            
            # Buscar el operario en reporte_data
            operario_obj = None
            for op in reporte_data.keys():
                if op.id == operario_id:
                    operario_obj = op
                    break
            
            if operario_obj:
                reporte_data[operario_obj]['resumen_horas'] = resumen
        
        # Obtener horas trabajadas detalladas por fecha para cada operario
        horas_detalladas = Horas_trabajadas.objects.filter(filtros_horas).select_related('operario')
        
        from datetime import timedelta
        
        for hora in horas_detalladas:
            # Buscar el operario en reporte_data
            operario_obj = None
            for op in reporte_data.keys():
                if op.id == hora.operario.id:
                    operario_obj = op
                    break
            
            if operario_obj:
                fecha_str = hora.fecha.strftime('%Y-%m-%d')
                
                # Calcular total sumando los campos que SÍ existen en el modelo
                total_trabajadas = timedelta(0)
                if hora.horas_normales:
                    total_trabajadas += hora.horas_normales
                if hora.horas_nocturnas:
                    total_trabajadas += hora.horas_nocturnas
                # Las horas extras NO se incluyen en el total trabajado
                
                reporte_data[operario_obj]['horas_por_fecha'][fecha_str] = {
                    'horas_normales': hora.horas_normales,
                    'horas_nocturnas': hora.horas_nocturnas,
                    'horas_extras': hora.horas_extras,
                    'total_trabajadas': total_trabajadas if total_trabajadas.total_seconds() > 0 else None
                }
        
        return reporte_data
    
    @staticmethod
    def generar_reporte_horas(mes=None, año=None, operarios=None):
        """Genera reporte de horas trabajadas por mes"""
        from django.db.models import Q
        from datetime import datetime, date
        
        if not mes or not año:
            hoy = date.today()
            mes = mes or hoy.month
            año = año or hoy.year
            
        # Filtros
        filtros = Q(fecha__month=mes, fecha__year=año)
        if operarios:
            filtros &= Q(operario__in=operarios)
            
        horas_trabajadas = Horas_trabajadas.objects.filter(filtros).select_related('operario').order_by('operario__apellido')
        
        return horas_trabajadas, mes, año
    
    @staticmethod
    def generar_reporte_inconsistencias(fecha_inicio=None, fecha_fin=None):
        """Genera reporte de inconsistencias por período"""
        from django.db.models import Q
        from datetime import datetime, date
        
        # Filtros base - registros con inconsistencias o no válidos
        filtros = Q(inconsistencia=True) | Q(valido=False)
        
        if fecha_inicio:
            filtros &= Q(hora_fichada__date__gte=fecha_inicio)
        if fecha_fin:
            filtros &= Q(hora_fichada__date__lte=fecha_fin)
            
        inconsistencias = RegistroDiario.objects.filter(filtros).select_related('operario').order_by('-hora_fichada')
        
        return inconsistencias


@admin.register(Reporte)
class ReporteAdmin(UnfoldModelAdmin):
    """Admin personalizado para la generación de reportes"""
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def changelist_view(self, request, extra_context=None):
        """Vista personalizada para mostrar las opciones de reportes"""
        from django.shortcuts import render
        
        context = {
            'title': 'Centro de Reportes',
            'has_add_permission': False,
            'has_change_permission': False,
            'has_delete_permission': False,
        }
        
        if extra_context:
            context.update(extra_context)
            
        return render(request, 'admin/reportes/centro_reportes.html', context)
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('asistencia/', self.admin_site.admin_view(self.reporte_asistencia), name='reporte_asistencia'),
            path('horas/', self.admin_site.admin_view(self.reporte_horas), name='reporte_horas'),
            path('inconsistencias/', self.admin_site.admin_view(self.reporte_inconsistencias), name='reporte_inconsistencias'),
            
            # Exportaciones
            path('horas/exportar-excel/', self.admin_site.admin_view(self.exportar_horas_excel), name='exportar_horas_excel'),
            path('horas/exportar-pdf/', self.admin_site.admin_view(self.exportar_horas_pdf), name='exportar_horas_pdf'),
            path('asistencia/exportar-excel/', self.admin_site.admin_view(self.exportar_asistencia_excel), name='exportar_asistencia_excel'),
            path('asistencia/exportar-pdf/', self.admin_site.admin_view(self.exportar_asistencia_pdf), name='exportar_asistencia_pdf'),
            path('inconsistencias/exportar-excel/', self.admin_site.admin_view(self.exportar_inconsistencias_excel), name='exportar_inconsistencias_excel'),
            path('inconsistencias/exportar-pdf/', self.admin_site.admin_view(self.exportar_inconsistencias_pdf), name='exportar_inconsistencias_pdf'),
        ]
        return custom_urls + urls
    
    def reporte_asistencia(self, request):
        """Vista para generar reporte de asistencia"""
        from django.shortcuts import render
        from datetime import datetime, date, timedelta
        
        # Valores por defecto
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        operario_ids = request.GET.getlist('operarios')
        
        # Convertir fechas si se proporcionaron
        if fecha_inicio:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            except:
                fecha_inicio = None
        
        if fecha_fin:
            try:
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            except:
                fecha_fin = None
        
        # Si no hay fechas, usar la última semana
        if not fecha_inicio and not fecha_fin:
            fecha_fin = date.today()
            fecha_inicio = fecha_fin - timedelta(days=7)
        
        # Operarios seleccionados
        operarios = None
        if operario_ids:
            operarios = Operario.objects.filter(id__in=operario_ids)
        
        # Generar reporte
        reporte_data = None
        if 'generar' in request.GET:
            reporte_data = ReporteManager.generar_reporte_asistencia(fecha_inicio, fecha_fin, operarios)
        
        context = {
            'title': 'Reporte de Asistencia',
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'operarios_disponibles': Operario.objects.filter(activo=True).order_by('apellido'),
            'operarios_seleccionados': operarios,
            'reporte_data': reporte_data,
        }
        
        return render(request, 'admin/reportes/reporte_asistencia.html', context)
    
    def reporte_horas(self, request):
        """Vista para generar reporte de horas trabajadas"""
        from django.shortcuts import render
        from datetime import datetime, date, timedelta
        
        # Parámetros
        mes = request.GET.get('mes')
        año = request.GET.get('año')
        operario_ids = request.GET.getlist('operarios')
        
        # Convertir a enteros
        try:
            mes = int(mes) if mes else date.today().month
            año = int(año) if año else date.today().year
        except:
            mes = date.today().month
            año = date.today().year
        
        # Operarios seleccionados
        operarios = None
        if operario_ids:
            operarios = Operario.objects.filter(id__in=operario_ids)
        
        # Generar reporte
        horas_trabajadas = None
        horas_agrupadas = None
        totales = None
        if 'generar' in request.GET:
            horas_trabajadas, mes, año = ReporteManager.generar_reporte_horas(mes, año, operarios)
            
            # Agrupar por operario y calcular subtotales
            if horas_trabajadas:
                from collections import OrderedDict
                horas_agrupadas = OrderedDict()
                total_normales = timedelta()
                total_nocturnas = timedelta()
                total_extras = timedelta()
                
                for hora in horas_trabajadas:
                    operario_key = f"{hora.operario.apellido}, {hora.operario.nombre}"
                    
                    if operario_key not in horas_agrupadas:
                        horas_agrupadas[operario_key] = {
                            'operario': hora.operario,
                            'registros': [],
                            'subtotal_normales': timedelta(),
                            'subtotal_nocturnas': timedelta(),
                            'subtotal_extras': timedelta(),
                        }
                    
                    # Obtener movimientos de entrada y salida para esta fecha (solo principales, no transitorios)
                    registros_dia = RegistroDiario.objects.filter(
                        operario=hora.operario,
                        hora_fichada__date=hora.fecha,
                        tipo_movimiento__in=['entrada', 'salida'],
                        valido=True
                    ).order_by('hora_fichada')
                    
                    entradas = []
                    salidas = []
                    
                    for registro in registros_dia:
                        if registro.tipo_movimiento == 'entrada':
                            entradas.append(registro.hora_fichada)
                        elif registro.tipo_movimiento == 'salida':
                            salidas.append(registro.hora_fichada)
                    
                    # Crear pares entrada/salida y generar filas separadas
                    max_movimientos = max(len(entradas), len(salidas))
                    
                    if max_movimientos == 0:
                        # No hay movimientos, crear una fila vacía
                        hora_con_movimientos = {
                            'hora': hora,
                            'entrada': None,
                            'salida': None
                        }
                        horas_agrupadas[operario_key]['registros'].append(hora_con_movimientos)
                    else:
                        # Crear una fila por cada par entrada/salida
                        for i in range(max_movimientos):
                            entrada = entradas[i] if i < len(entradas) else None
                            salida = salidas[i] if i < len(salidas) else None
                            
                            hora_con_movimientos = {
                                'hora': hora,
                                'entrada': entrada,
                                'salida': salida,
                                'es_primera_fila': i == 0  # Para mostrar horas solo en la primera fila
                            }
                            horas_agrupadas[operario_key]['registros'].append(hora_con_movimientos)
                    
                    # Sumar a subtotales del operario
                    if hora.horas_normales:
                        horas_agrupadas[operario_key]['subtotal_normales'] += hora.horas_normales
                        total_normales += hora.horas_normales
                    if hora.horas_nocturnas:
                        horas_agrupadas[operario_key]['subtotal_nocturnas'] += hora.horas_nocturnas
                        total_nocturnas += hora.horas_nocturnas
                    if hora.horas_extras:
                        horas_agrupadas[operario_key]['subtotal_extras'] += hora.horas_extras
                        total_extras += hora.horas_extras
                
                # Calcular total general para cada operario
                for operario_data in horas_agrupadas.values():
                    operario_data['subtotal_general'] = (
                        operario_data['subtotal_normales'] + 
                        operario_data['subtotal_nocturnas'] + 
                        operario_data['subtotal_extras']
                    )
                
                totales = {
                    'total_normales': total_normales,
                    'total_nocturnas': total_nocturnas,
                    'total_extras': total_extras,
                    'total_general': total_normales + total_nocturnas + total_extras
                }
        
        # Nombres de meses en español
        meses_es = [
            (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
            (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
            (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
        ]
        
        context = {
            'title': 'Reporte de Horas Trabajadas',
            'mes': mes,
            'año': año,
            'meses': meses_es,
            'años': list(range(2020, date.today().year + 2)),
            'operarios_disponibles': Operario.objects.filter(activo=True).order_by('apellido'),
            'operarios_seleccionados': operarios,
            'horas_trabajadas': horas_trabajadas,
            'horas_agrupadas': horas_agrupadas,
            'totales': totales,
        }
        
        return render(request, 'admin/reportes/reporte_horas.html', context)
    
    def reporte_inconsistencias(self, request):
        """Vista para generar reporte de inconsistencias"""
        from django.shortcuts import render
        from datetime import datetime, date, timedelta
        
        # Parámetros
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        
        # Convertir fechas
        if fecha_inicio:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            except:
                fecha_inicio = None
        
        if fecha_fin:
            try:
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            except:
                fecha_fin = None
        
        # Si no hay fechas, usar el último mes
        if not fecha_inicio and not fecha_fin:
            fecha_fin = date.today()
            fecha_inicio = fecha_fin - timedelta(days=30)
        
        # Generar reporte
        inconsistencias = None
        if 'generar' in request.GET:
            inconsistencias = RegistroDiario.objects.filter(
                inconsistencia=True,
                hora_fichada__date__range=[fecha_inicio, fecha_fin]
            ).select_related('operario').order_by('-hora_fichada')
        
        context = {
            'title': 'Reporte de Inconsistencias',
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'inconsistencias': inconsistencias,
        }
        
        return render(request, 'admin/reportes/reporte_inconsistencias.html', context)
    
    # ===== FUNCIONES DE EXPORTACIÓN =====
    
    def exportar_horas_excel(self, request):
        """Exportar reporte de horas a Excel"""
        import openpyxl
        from django.http import HttpResponse
        from django.utils import timezone
        from datetime import datetime, date, timedelta
        from openpyxl.styles import Font, PatternFill, Border, Side
        import pytz
        
        # Obtener los mismos parámetros que en reporte_horas
        mes = request.GET.get('mes')
        año = request.GET.get('año')
        operario_ids = request.GET.getlist('operarios')
        
        try:
            mes = int(mes) if mes else date.today().month
            año = int(año) if año else date.today().year
        except:
            mes = date.today().month
            año = date.today().year
        
        operarios = None
        if operario_ids:
            operarios = Operario.objects.filter(id__in=operario_ids)
        
        # Generar los datos
        horas_trabajadas, mes, año = ReporteManager.generar_reporte_horas(mes, año, operarios)
        
        # Agrupar por operario y calcular subtotales
        horas_agrupadas = None
        total_normales = timedelta()
        total_nocturnas = timedelta()
        total_extras = timedelta()
        
        if horas_trabajadas:
            from collections import OrderedDict
            horas_agrupadas = OrderedDict()
            
            for hora in horas_trabajadas:
                operario_key = f"{hora.operario.apellido}, {hora.operario.nombre}"
                
                if operario_key not in horas_agrupadas:
                    horas_agrupadas[operario_key] = {
                        'operario': hora.operario,
                        'registros': [],
                        'subtotal_normales': timedelta(),
                        'subtotal_nocturnas': timedelta(),
                        'subtotal_extras': timedelta(),
                    }
                
                # Obtener movimientos de entrada y salida para esta fecha (solo principales, no transitorios)
                registros_dia = RegistroDiario.objects.filter(
                    operario=hora.operario,
                    hora_fichada__date=hora.fecha,
                    tipo_movimiento__in=['entrada', 'salida'],
                    valido=True
                ).order_by('hora_fichada')
                
                entradas = []
                salidas = []
                
                for registro in registros_dia:
                    if registro.tipo_movimiento == 'entrada':
                        entradas.append(registro.hora_fichada)
                    elif registro.tipo_movimiento == 'salida':
                        salidas.append(registro.hora_fichada)
                
                # Crear pares entrada/salida y generar filas separadas
                max_movimientos = max(len(entradas), len(salidas))
                
                if max_movimientos == 0:
                    # No hay movimientos, crear una fila vacía
                    hora_con_movimientos = {
                        'hora': hora,
                        'entrada': None,
                        'salida': None
                    }
                    horas_agrupadas[operario_key]['registros'].append(hora_con_movimientos)
                else:
                    # Crear una fila por cada par entrada/salida
                    for i in range(max_movimientos):
                        entrada = entradas[i] if i < len(entradas) else None
                        salida = salidas[i] if i < len(salidas) else None
                        
                        hora_con_movimientos = {
                            'hora': hora,
                            'entrada': entrada,
                            'salida': salida,
                            'es_primera_fila': i == 0  # Para mostrar horas solo en la primera fila
                        }
                        horas_agrupadas[operario_key]['registros'].append(hora_con_movimientos)
                
                # Sumar a subtotales del operario
                if hora.horas_normales:
                    horas_agrupadas[operario_key]['subtotal_normales'] += hora.horas_normales
                    total_normales += hora.horas_normales
                if hora.horas_nocturnas:
                    horas_agrupadas[operario_key]['subtotal_nocturnas'] += hora.horas_nocturnas
                    total_nocturnas += hora.horas_nocturnas
                if hora.horas_extras:
                    horas_agrupadas[operario_key]['subtotal_extras'] += hora.horas_extras
                    total_extras += hora.horas_extras
            
            # Calcular total general para cada operario
            for operario_data in horas_agrupadas.values():
                operario_data['subtotal_general'] = (
                    operario_data['subtotal_normales'] + 
                    operario_data['subtotal_nocturnas'] + 
                    operario_data['subtotal_extras']
                )
        
        # Nombres de meses en español
        meses_es = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                   'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        # Crear workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = f"Horas {meses_es[mes]} {año}"
        
        # Headers
        headers = ['Empleado', 'Fecha Entrada', 'Fecha Salida', 'Horas Normales', 'Horas Nocturnas', 'Horas Extras', 'Total Diario']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color='417690', end_color='417690', fill_type='solid')
            cell.font = Font(bold=True, color='FFFFFF')
        
        # Datos agrupados por operario
        row = 2
        if horas_agrupadas:
            # Estilos para headers de operarios
            fill_operario = PatternFill(start_color='17A2B8', end_color='17A2B8', fill_type='solid')
            font_operario = Font(bold=True, color='FFFFFF')
            
            # Estilos para subtotales
            fill_subtotal = PatternFill(start_color='E8F4FD', end_color='E8F4FD', fill_type='solid')
            font_subtotal = Font(bold=True, italic=True)
            border_subtotal = Border(
                top=Side(border_style='thin', color='17A2B8'),
                bottom=Side(border_style='thin', color='17A2B8')
            )
            
            for operario_nombre, operario_data in horas_agrupadas.items():
                # Header del operario
                header_cell = ws.cell(row=row, column=1, value=f"{operario_nombre}")
                ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=7)
                header_cell.fill = fill_operario
                header_cell.font = font_operario
                row += 1
                
                # Registros del operario
                for registro in operario_data['registros']:
                    hora = registro['hora']
                    
                    # Formatear entrada y salida individual
                    dias_es = {
                        'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
                        'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
                    }
                    
                    entrada_text = "-"
                    if registro['entrada']:
                        # Convertir de UTC a timezone de Argentina
                        if timezone.is_aware(registro['entrada']):
                            argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
                            entrada_local = registro['entrada'].astimezone(argentina_tz)
                        else:
                            entrada_local = registro['entrada']
                        dia_en = entrada_local.strftime('%A')
                        dia_es = dias_es.get(dia_en, dia_en)
                        entrada_text = f"{dia_es} - {entrada_local.strftime('%d/%m/%Y - %H:%M:%S')}"
                    
                    salida_text = "-"
                    if registro['salida']:
                        # Convertir de UTC a timezone de Argentina
                        if timezone.is_aware(registro['salida']):
                            argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
                            salida_local = registro['salida'].astimezone(argentina_tz)
                        else:
                            salida_local = registro['salida']
                        dia_en = salida_local.strftime('%A')
                        dia_es = dias_es.get(dia_en, dia_en)
                        salida_text = f"{dia_es} - {salida_local.strftime('%d/%m/%Y - %H:%M:%S')}"
                    
                    ws.cell(row=row, column=1, value=f"    {hora.operario.apellido}, {hora.operario.nombre}")
                    ws.cell(row=row, column=2, value=entrada_text)
                    ws.cell(row=row, column=3, value=salida_text)
                    
                    # Solo mostrar horas en la primera fila de cada día
                    if registro.get('es_primera_fila', True):
                        horas_normales_num = hora.horas_normales.total_seconds() / 3600 if hora.horas_normales else 0
                        horas_nocturnas_num = hora.horas_nocturnas.total_seconds() / 3600 if hora.horas_nocturnas else 0
                        horas_extras_num = hora.horas_extras.total_seconds() / 3600 if hora.horas_extras else 0
                        total_diario = horas_normales_num + horas_nocturnas_num + horas_extras_num
                        
                        ws.cell(row=row, column=4, value=f"{horas_normales_num:.1f}h")
                        ws.cell(row=row, column=5, value=f"{horas_nocturnas_num:.1f}h")
                        ws.cell(row=row, column=6, value=f"{horas_extras_num:.1f}h")
                        ws.cell(row=row, column=7, value=f"{total_diario:.1f}h")
                    else:
                        ws.cell(row=row, column=4, value="-")
                        ws.cell(row=row, column=5, value="-")
                        ws.cell(row=row, column=6, value="-")
                        ws.cell(row=row, column=7, value="-")
                    
                    row += 1
                
                # Subtotal del operario
                subtotal_normales = operario_data['subtotal_normales'].total_seconds() / 3600
                subtotal_nocturnas = operario_data['subtotal_nocturnas'].total_seconds() / 3600
                subtotal_extras = operario_data['subtotal_extras'].total_seconds() / 3600
                subtotal_general = operario_data['subtotal_general'].total_seconds() / 3600
                
                subtotal_data = [
                    f"Subtotal {operario_nombre}", '', '',
                    f"{subtotal_normales:.1f}h",
                    f"{subtotal_nocturnas:.1f}h",
                    f"{subtotal_extras:.1f}h",
                    f"{subtotal_general:.1f}h"
                ]
                
                for col, value in enumerate(subtotal_data, 1):
                    cell = ws.cell(row=row, column=col, value=value)
                    cell.fill = fill_subtotal
                    cell.font = font_subtotal
                    cell.border = border_subtotal
                
                row += 2  # Espacio entre operarios
        
        # Agregar fila de totales
        if horas_agrupadas:
            # Fila vacía de separación
            row += 1
            
            # Fila de totales
            totales_normales = total_normales.total_seconds() / 3600
            totales_nocturnas = total_nocturnas.total_seconds() / 3600
            totales_extras = total_extras.total_seconds() / 3600
            total_general = totales_normales + totales_nocturnas + totales_extras
            
            # Estilos para la fila de totales
            fill_totales = PatternFill(start_color='F8F9FA', end_color='F8F9FA', fill_type='solid')
            font_totales = Font(bold=True)
            border_totales = Border(
                top=Side(border_style='thick', color='417690'),
                bottom=Side(border_style='thick', color='417690'),
                left=Side(border_style='thin'),
                right=Side(border_style='thin')
            )
            
            # Datos de totales
            totales_data = [
                'TOTALES', '', '', 
                f"{totales_normales:.1f}h",
                f"{totales_nocturnas:.1f}h", 
                f"{totales_extras:.1f}h",
                f"{total_general:.1f}h"
            ]
            
            for col, value in enumerate(totales_data, 1):
                cell = ws.cell(row=row, column=col, value=value)
                cell.fill = fill_totales
                cell.font = font_totales
                cell.border = border_totales
        
        # Respuesta HTTP
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="Reporte_Horas_{meses_es[mes]}_{año}.xlsx"'
        wb.save(response)
        return response
    
    def exportar_horas_pdf(self, request):
        """Exportar reporte de horas a PDF"""
        from django.http import HttpResponse
        from django.template.loader import get_template
        from django.utils import timezone
        from weasyprint import HTML
        from datetime import datetime, date, timedelta
        import tempfile
        
        # Obtener los mismos parámetros que en reporte_horas
        mes = request.GET.get('mes')
        año = request.GET.get('año')
        operario_ids = request.GET.getlist('operarios')
        
        try:
            mes = int(mes) if mes else date.today().month
            año = int(año) if año else date.today().year
        except:
            mes = date.today().month
            año = date.today().year
        
        operarios = None
        if operario_ids:
            operarios = Operario.objects.filter(id__in=operario_ids)
        
        # Generar los datos
        horas_trabajadas, mes, año = ReporteManager.generar_reporte_horas(mes, año, operarios)
        
        # Agrupar por operario y calcular subtotales (misma lógica que HTML)
        horas_agrupadas = None
        totales = None
        if horas_trabajadas:
            from collections import OrderedDict
            horas_agrupadas = OrderedDict()
            total_normales = timedelta()
            total_nocturnas = timedelta()
            total_extras = timedelta()
            
            for hora in horas_trabajadas:
                operario_key = f"{hora.operario.apellido}, {hora.operario.nombre}"
                
                if operario_key not in horas_agrupadas:
                    horas_agrupadas[operario_key] = {
                        'operario': hora.operario,
                        'registros': [],
                        'subtotal_normales': timedelta(),
                        'subtotal_nocturnas': timedelta(),
                        'subtotal_extras': timedelta(),
                    }
                
                # Obtener movimientos de entrada y salida para esta fecha (excluyendo transitorios)
                registros_dia = RegistroDiario.objects.filter(
                    operario=hora.operario,
                    hora_fichada__date=hora.fecha,
                    tipo_movimiento__in=['entrada', 'salida']
                ).order_by('hora_fichada')
                
                # Separar entradas y salidas
                entradas = [r for r in registros_dia if r.tipo_movimiento == 'entrada']
                salidas = [r for r in registros_dia if r.tipo_movimiento == 'salida']
                
                # Crear pares entrada/salida y generar filas separadas
                max_movimientos = max(len(entradas), len(salidas)) if (entradas or salidas) else 1
                
                for i in range(max_movimientos):
                    entrada = entradas[i] if i < len(entradas) else None
                    salida = salidas[i] if i < len(salidas) else None
                    
                    hora_con_movimientos = {
                        'hora': hora,
                        'entrada': entrada.hora_fichada if entrada else None,
                        'salida': salida.hora_fichada if salida else None,
                        'es_primera_fila': i == 0
                    }
                    horas_agrupadas[operario_key]['registros'].append(hora_con_movimientos)
                
                # Sumar a subtotales del operario (solo una vez por día)
                if hora.horas_normales:
                    horas_agrupadas[operario_key]['subtotal_normales'] += hora.horas_normales
                    total_normales += hora.horas_normales
                if hora.horas_nocturnas:
                    horas_agrupadas[operario_key]['subtotal_nocturnas'] += hora.horas_nocturnas
                    total_nocturnas += hora.horas_nocturnas
                if hora.horas_extras:
                    horas_agrupadas[operario_key]['subtotal_extras'] += hora.horas_extras
                    total_extras += hora.horas_extras
            
            # Calcular total general para cada operario
            for operario_data in horas_agrupadas.values():
                operario_data['subtotal_general'] = (
                    operario_data['subtotal_normales'] + 
                    operario_data['subtotal_nocturnas'] + 
                    operario_data['subtotal_extras']
                )
            
            totales = {
                'total_normales': total_normales,
                'total_nocturnas': total_nocturnas,
                'total_extras': total_extras,
                'total_general': total_normales + total_nocturnas + total_extras
            }
        
        # Nombres de meses en español
        meses_es = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                   'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        # Contexto para el template
        context = {
            'horas_trabajadas': horas_trabajadas,
            'horas_agrupadas': horas_agrupadas,
            'totales': totales,
            'mes_nombre': meses_es[mes],
            'año': año,
            'fecha_generacion': timezone.now().astimezone(timezone.get_default_timezone()).strftime('%d/%m/%Y %H:%M'),
            'operarios_filtro': operarios.count() if operarios else 'Todos los operarios',
        }
        
        # Renderizar template
        template = get_template('admin/reportes/pdf/reporte_horas_pdf.html')
        html_string = template.render(context)
        
        # Generar PDF
        html = HTML(string=html_string)
        pdf = html.write_pdf()
        
        # Respuesta HTTP
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Reporte_Horas_{meses_es[mes]}_{año}.pdf"'
        return response
    
    def exportar_asistencia_excel(self, request):
        """Exportar reporte de asistencia a Excel"""
        import openpyxl
        from django.http import HttpResponse
        from datetime import datetime, date, timedelta
        
        # Obtener parámetros
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        operario_ids = request.GET.getlist('operarios')
        
        # Convertir fechas
        if fecha_inicio:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            except:
                fecha_inicio = None
        
        if fecha_fin:
            try:
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            except:
                fecha_fin = None
        
        if not fecha_inicio and not fecha_fin:
            fecha_fin = date.today()
            fecha_inicio = fecha_fin - timedelta(days=7)
        
        operarios = None
        if operario_ids:
            operarios = Operario.objects.filter(id__in=operario_ids)
        
        # Generar datos
        reporte_data = ReporteManager.generar_reporte_asistencia(fecha_inicio, fecha_fin, operarios)
        
        # Crear workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Reporte Asistencia"
        
        # Headers
        headers = ['Empleado', 'DNI', 'Fecha', 'Hora', 'Tipo Movimiento', 'Origen', 'Horas Trabajadas', 'Horas Extras']
        for col, header in enumerate(headers, 1):
            ws.cell(row=1, column=col, value=header)
        
        # Datos de registros
        row = 2
        for operario, data in reporte_data.items():
            for registro in data['registros']:
                ws.cell(row=row, column=1, value=f"{operario.apellido}, {operario.nombre}")
                ws.cell(row=row, column=2, value=operario.dni)
                ws.cell(row=row, column=3, value=registro.hora_fichada.strftime('%d/%m/%Y'))
                ws.cell(row=row, column=4, value=registro.hora_fichada.strftime('%H:%M:%S'))
                ws.cell(row=row, column=5, value=registro.tipo_movimiento.replace('_', ' ').title())
                ws.cell(row=row, column=6, value=registro.origen_fichada)
                
                # Agregar horas trabajadas y extras solo para salidas
                if registro.tipo_movimiento == 'salida':
                    fecha_str = registro.hora_fichada.strftime('%Y-%m-%d')
                    horas_fecha = data.get('horas_por_fecha', {}).get(fecha_str)
                    
                    if horas_fecha:
                        # Horas trabajadas totales del día
                        if horas_fecha.get('total_trabajadas'):
                            horas_trabajadas = horas_fecha['total_trabajadas'].total_seconds() / 3600
                            ws.cell(row=row, column=7, value=f"{horas_trabajadas:.1f}h")
                        else:
                            ws.cell(row=row, column=7, value="0h")
                        
                        # Horas extras del día
                        if horas_fecha.get('horas_extras'):
                            horas_extras = horas_fecha['horas_extras'].total_seconds() / 3600
                            ws.cell(row=row, column=8, value=f"{horas_extras:.1f}h")
                        else:
                            ws.cell(row=row, column=8, value="0h")
                    else:
                        ws.cell(row=row, column=7, value="-")
                        ws.cell(row=row, column=8, value="-")
                else:
                    ws.cell(row=row, column=7, value="-")
                    ws.cell(row=row, column=8, value="-")
                
                row += 1
        
        # Agregar resumen de horas en una nueva hoja
        ws_resumen = wb.create_sheet(title="Resumen Horas")
        headers_resumen = ['Empleado', 'DNI', 'Horas Normales', 'Horas Nocturnas', 'Horas Extras', 'Días Trabajados', 'Total Horas']
        for col, header in enumerate(headers_resumen, 1):
            ws_resumen.cell(row=1, column=col, value=header)
        
        row_resumen = 2
        for operario, data in reporte_data.items():
            if data['resumen_horas']:
                resumen = data['resumen_horas']
                # Convertir timedelta a horas
                horas_normales = resumen['total_horas_normales'].total_seconds() / 3600 if resumen['total_horas_normales'] else 0
                horas_nocturnas = resumen['total_horas_nocturnas'].total_seconds() / 3600 if resumen['total_horas_nocturnas'] else 0
                horas_extras = resumen['total_horas_extras'].total_seconds() / 3600 if resumen['total_horas_extras'] else 0
                total_horas = horas_normales + horas_nocturnas + horas_extras
                
                ws_resumen.cell(row=row_resumen, column=1, value=f"{operario.apellido}, {operario.nombre}")
                ws_resumen.cell(row=row_resumen, column=2, value=operario.dni)
                ws_resumen.cell(row=row_resumen, column=3, value=f"{horas_normales:.1f}h")
                ws_resumen.cell(row=row_resumen, column=4, value=f"{horas_nocturnas:.1f}h")
                ws_resumen.cell(row=row_resumen, column=5, value=f"{horas_extras:.1f}h")
                ws_resumen.cell(row=row_resumen, column=6, value=resumen['dias_trabajados'] or 0)
                ws_resumen.cell(row=row_resumen, column=7, value=f"{total_horas:.1f}h")
                row_resumen += 1
        
        # Respuesta HTTP
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        fecha_str = f"{fecha_inicio.strftime('%d-%m-%Y')}_al_{fecha_fin.strftime('%d-%m-%Y')}"
        response['Content-Disposition'] = f'attachment; filename="Reporte_Asistencia_{fecha_str}.xlsx"'
        wb.save(response)
        return response
    
    def exportar_asistencia_pdf(self, request):
        """Exportar reporte de asistencia a PDF"""
        from django.http import HttpResponse
        from django.template.loader import get_template
        from weasyprint import HTML
        from datetime import datetime, date, timedelta
        
        # Obtener parámetros (mismo código que exportar_asistencia_excel)
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        operario_ids = request.GET.getlist('operarios')
        
        if fecha_inicio:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            except:
                fecha_inicio = None
        
        if fecha_fin:
            try:
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            except:
                fecha_fin = None
        
        if not fecha_inicio and not fecha_fin:
            fecha_fin = date.today()
            fecha_inicio = fecha_fin - timedelta(days=7)
        
        operarios = None
        if operario_ids:
            operarios = Operario.objects.filter(id__in=operario_ids)
        
        # Generar datos
        reporte_data = ReporteManager.generar_reporte_asistencia(fecha_inicio, fecha_fin, operarios)
        
        # Contexto para el template
        context = {
            'reporte_data': reporte_data,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'fecha_generacion': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'operarios_filtro': operarios.count() if operarios else 'Todos los operarios',
        }
        
        # Renderizar template
        template = get_template('admin/reportes/pdf/reporte_asistencia_pdf.html')
        html_string = template.render(context)
        
        # Generar PDF
        html = HTML(string=html_string)
        pdf = html.write_pdf()
        
        # Respuesta HTTP
        response = HttpResponse(pdf, content_type='application/pdf')
        fecha_str = f"{fecha_inicio.strftime('%d-%m-%Y')}_al_{fecha_fin.strftime('%d-%m-%Y')}"
        response['Content-Disposition'] = f'attachment; filename="Reporte_Asistencia_{fecha_str}.pdf"'
        return response
    
    def exportar_inconsistencias_excel(self, request):
        """Exportar reporte de inconsistencias a Excel"""
        import openpyxl
        from django.http import HttpResponse
        from datetime import datetime, date, timedelta
        
        # Obtener parámetros
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        
        # Convertir fechas
        if fecha_inicio:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            except:
                fecha_inicio = None
        
        if fecha_fin:
            try:
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            except:
                fecha_fin = None
        
        if not fecha_inicio and not fecha_fin:
            fecha_fin = date.today()
            fecha_inicio = fecha_fin - timedelta(days=7)
        
        # Generar datos
        inconsistencias = ReporteManager.generar_reporte_inconsistencias(fecha_inicio, fecha_fin)
        
        # Crear workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Inconsistencias"
        
        # Headers
        headers = ['Empleado', 'DNI', 'Fecha', 'Hora', 'Tipo Movimiento', 'Descripción', 'Válido']
        for col, header in enumerate(headers, 1):
            ws.cell(row=1, column=col, value=header)
        
        # Datos
        row = 2
        for inconsistencia in inconsistencias:
            ws.cell(row=row, column=1, value=f"{inconsistencia.operario.apellido}, {inconsistencia.operario.nombre}")
            ws.cell(row=row, column=2, value=inconsistencia.operario.dni)
            ws.cell(row=row, column=3, value=inconsistencia.hora_fichada.strftime('%d/%m/%Y'))
            ws.cell(row=row, column=4, value=inconsistencia.hora_fichada.strftime('%H:%M:%S'))
            ws.cell(row=row, column=5, value=inconsistencia.tipo_movimiento.replace('_', ' ').title())
            ws.cell(row=row, column=6, value=inconsistencia.descripcion_inconsistencia or "Sin descripción")
            ws.cell(row=row, column=7, value="Sí" if inconsistencia.valido else "No")
            row += 1
        
        # Respuesta HTTP
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        fecha_str = f"{fecha_inicio.strftime('%d-%m-%Y')}_al_{fecha_fin.strftime('%d-%m-%Y')}"
        response['Content-Disposition'] = f'attachment; filename="Reporte_Inconsistencias_{fecha_str}.xlsx"'
        wb.save(response)
        return response
    
    def exportar_inconsistencias_pdf(self, request):
        """Exportar reporte de inconsistencias a PDF"""
        from django.http import HttpResponse
        from django.template.loader import get_template
        from weasyprint import HTML
        from datetime import datetime, date, timedelta
        
        # Obtener parámetros
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        
        if fecha_inicio:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            except:
                fecha_inicio = None
        
        if fecha_fin:
            try:
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            except:
                fecha_fin = None
        
        if not fecha_inicio and not fecha_fin:
            fecha_fin = date.today()
            fecha_inicio = fecha_fin - timedelta(days=7)
        
        # Generar datos
        inconsistencias = ReporteManager.generar_reporte_inconsistencias(fecha_inicio, fecha_fin)
        
        # Contexto para el template
        context = {
            'inconsistencias': inconsistencias,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'fecha_generacion': datetime.now().strftime('%d/%m/%Y %H:%M'),
        }
        
        # Renderizar template
        template = get_template('admin/reportes/pdf/reporte_inconsistencias_pdf.html')
        html_string = template.render(context)
        
        # Generar PDF
        html = HTML(string=html_string)
        pdf = html.write_pdf()
        
        # Respuesta HTTP
        response = HttpResponse(pdf, content_type='application/pdf')
        fecha_str = f"{fecha_inicio.strftime('%d-%m-%Y')}_al_{fecha_fin.strftime('%d-%m-%Y')}"
        response['Content-Disposition'] = f'attachment; filename="Reporte_Inconsistencias_{fecha_str}.pdf"'
        return response


# ===============================================================================
# ADMIN INDEPENDIENTE PARA LICENCIAS
# ===============================================================================

class EstadoLicenciaFilter(admin.SimpleListFilter):
    title = _('Estado de Licencia')
    parameter_name = 'estado'

    def lookups(self, request, model_admin):
        return [
            ('pendiente', _('⏳ Pendientes')),
            ('aprobada', _('✅ Aprobadas')),
            ('rechazada', _('❌ Rechazadas')),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(estado=self.value())
        return queryset


class LicenciasPorAprobarFilter(admin.SimpleListFilter):
    title = _('Licencias por Aprobar')
    parameter_name = 'por_aprobar'

    def lookups(self, request, model_admin):
        return [
            ('si', _('🔍 Solo pendientes de aprobación')),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'si':
            return queryset.filter(estado='pendiente')
        return queryset


@admin.register(Licencia)
class LicenciaAdmin(SimpleHistoryAdmin, UnfoldModelAdmin):
    list_display = [
        'get_operario_info', 'descripcion_corta', 'periodo_licencia', 
        'duracion_dias', 'estado_display', 'fecha_subida', 'aprobada_por', 
        'aplicar_a_asistencia', 'acciones_licencia'
    ]
    
    list_filter = [
        EstadoLicenciaFilter,
        LicenciasPorAprobarFilter,
        'aplicar_a_asistencia',
        ('fecha_inicio', DateRangeFilter),
        ('fecha_subida', DateRangeFilter),
        'aprobada_por',
    ]
    
    search_fields = [
        'operario__dni',
        'operario__nombre', 
        'operario__apellido',
        'descripcion',
        'observaciones'
    ]
    
    readonly_fields = [
        'fecha_subida', 'fecha_aprobacion', 'duracion_display', 'historia_cambios'
    ]
    
    fieldsets = (
        ('📋 Información Básica', {
            'fields': ('operario', 'descripcion', 'archivo')
        }),
        ('📅 Período de Licencia', {
            'fields': ('fecha_inicio', 'fecha_fin', 'duracion_display')
        }),
        ('⚙️ Configuración', {
            'fields': ('estado', 'aplicar_a_asistencia')
        }),
        ('✅ Aprobación', {
            'fields': ('aprobada_por', 'fecha_aprobacion', 'observaciones'),
            'classes': ('collapse',)
        }),
        ('📊 Metadatos', {
            'fields': ('fecha_subida', 'historia_cambios'),
            'classes': ('collapse',)
        })
    )
    
    ordering = ['-fecha_subida', '-fecha_inicio']
    
    list_per_page = 25
    
    actions = ['aprobar_licencias_masivo', 'rechazar_licencias_masivo', 'exportar_excel_licencias']

    def get_operario_info(self, obj):
        """Información completa del operario"""
        return format_html(
            '<strong>{}, {}</strong><br><small>DNI: {}</small>',
            obj.operario.apellido,
            obj.operario.nombre,
            obj.operario.dni
        )
    get_operario_info.short_description = '👤 Operario'
    get_operario_info.admin_order_field = 'operario__apellido'

    def descripcion_corta(self, obj):
        """Descripción truncada"""
        if obj.descripcion:
            texto = obj.descripcion[:50]
            if len(obj.descripcion) > 50:
                texto += '...'
            return texto
        return '-'
    descripcion_corta.short_description = '📝 Descripción'

    def periodo_licencia(self, obj):
        """Período de la licencia con formato"""
        if obj.fecha_inicio and obj.fecha_fin:
            return format_html(
                '<strong>{}</strong><br><small>al {}</small>',
                obj.fecha_inicio.strftime('%d/%m/%Y'),
                obj.fecha_fin.strftime('%d/%m/%Y')
            )
        return '-'
    periodo_licencia.short_description = '📅 Período'
    periodo_licencia.admin_order_field = 'fecha_inicio'

    def duracion_dias(self, obj):
        """Duración en días"""
        if obj.duracion:
            if obj.duracion == 1:
                return f'{obj.duracion} día'
            else:
                return f'{obj.duracion} días'
        return '-'
    duracion_dias.short_description = '⏱️ Duración'

    def estado_display(self, obj):
        """Estado con iconos y colores"""
        estados = {
            'pendiente': ('⏳', 'orange', 'Pendiente'),
            'aprobada': ('✅', 'green', 'Aprobada'), 
            'rechazada': ('❌', 'red', 'Rechazada')
        }
        
        icono, color, texto = estados.get(obj.estado, ('❓', 'gray', obj.estado))
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            color, icono, texto
        )
    estado_display.short_description = '📊 Estado'
    estado_display.admin_order_field = 'estado'

    def duracion_display(self, obj):
        """Duración calculada para readonly"""
        return self.duracion_dias(obj)
    duracion_display.short_description = 'Duración Calculada'

    def historia_cambios(self, obj):
        """Link al historial de cambios"""
        if obj.pk:
            try:
                url = reverse('admin:reloj_fichador_historicallicencia_changelist')
                return format_html(
                    '<a href="{}">Ver historial de cambios</a>',
                    url + f'?history_id={obj.pk}'
                )
            except:
                return 'Historial no disponible'
        return 'Guarde primero para ver el historial'
    historia_cambios.short_description = 'Historial'

    def acciones_licencia(self, obj):
        """Acciones rápidas"""
        acciones = []
        
        if obj.estado == 'pendiente':
            # Botones de aprobación/rechazo
            aprobar_url = reverse('admin:reloj_fichador_licencia_change', args=[obj.pk])
            acciones.append(f'<a class="button" href="{aprobar_url}" style="background: green; color: white; margin: 2px;">✅ Aprobar</a>')
            acciones.append(f'<a class="button" href="{aprobar_url}" style="background: red; color: white; margin: 2px;">❌ Rechazar</a>')
        
        if obj.archivo:
            # Link para descargar archivo
            acciones.append(f'<a class="button" href="{obj.archivo.url}" target="_blank">📄 Ver Archivo</a>')
        else:
            # Advertencia si no hay archivo
            acciones.append('<span style="color: orange; font-weight: bold;">⚠️ Sin archivo adjunto</span>')
        
        # Link a asistencia del operario
        asistencia_url = reverse('admin:reloj_fichador_registroasistencia_changelist')
        asistencia_url += f'?operario__id__exact={obj.operario.pk}'
        if obj.fecha_inicio and obj.fecha_fin:
            asistencia_url += f'&fecha__gte={obj.fecha_inicio}&fecha__lte={obj.fecha_fin}'
        
        acciones.append(f'<a class="button" href="{asistencia_url}">👥 Ver Asistencia</a>')
        
        return format_html('<br>'.join(acciones))
    acciones_licencia.short_description = '🔧 Acciones'

    def save_model(self, request, obj, form, change):
        """Personalizar guardado para auditoría"""
        if change and 'estado' in form.changed_data:
            # Si se está cambiando el estado y se está aprobando
            if obj.estado in ['aprobada', 'rechazada'] and not obj.aprobada_por:
                obj.aprobada_por = request.user
                obj.fecha_aprobacion = timezone.now()
                
                # Mostrar advertencia si no hay archivo adjunto
                if not obj.archivo:
                    if obj.estado == 'aprobada':
                        self.message_user(request, 
                            f"⚠️ ADVERTENCIA: Se aprobó la licencia de {obj.operario} sin archivo adjunto.", 
                            level='WARNING')
                    elif obj.estado == 'rechazada':
                        self.message_user(request, 
                            f"⚠️ ADVERTENCIA: Se rechazó la licencia de {obj.operario} sin archivo adjunto.", 
                            level='WARNING')
        
        super().save_model(request, obj, form, change)

    def aprobar_licencias_masivo(self, request, queryset):
        """Acción masiva para aprobar licencias"""
        count = 0
        sin_archivo = 0
        
        for licencia in queryset.filter(estado='pendiente'):
            licencia.estado = 'aprobada'
            licencia.aprobada_por = request.user
            licencia.fecha_aprobacion = timezone.now()
            licencia.save()
            count += 1
            
            if not licencia.archivo:
                sin_archivo += 1
        
        if count:
            mensaje = f'Se aprobaron {count} licencia(s) correctamente.'
            if sin_archivo > 0:
                mensaje += f' ⚠️ ADVERTENCIA: {sin_archivo} licencia(s) se aprobaron sin archivo adjunto.'
            self.message_user(request, mensaje, 
                            level='WARNING' if sin_archivo > 0 else 'SUCCESS')
        else:
            self.message_user(request, 'No hay licencias pendientes para aprobar.')
    aprobar_licencias_masivo.short_description = "✅ Aprobar licencias seleccionadas"

    def rechazar_licencias_masivo(self, request, queryset):
        """Acción masiva para rechazar licencias"""
        count = 0
        sin_archivo = 0
        
        for licencia in queryset.filter(estado='pendiente'):
            licencia.estado = 'rechazada'
            licencia.aprobada_por = request.user
            licencia.fecha_aprobacion = timezone.now()
            licencia.save()
            count += 1
            
            if not licencia.archivo:
                sin_archivo += 1
        
        if count:
            mensaje = f'Se rechazaron {count} licencia(s).'
            if sin_archivo > 0:
                mensaje += f' ⚠️ ADVERTENCIA: {sin_archivo} licencia(s) se rechazaron sin archivo adjunto.'
            self.message_user(request, mensaje, 
                            level='WARNING' if sin_archivo > 0 else 'SUCCESS')
        else:
            self.message_user(request, 'No hay licencias pendientes para rechazar.')
    rechazar_licencias_masivo.short_description = "❌ Rechazar licencias seleccionadas"

    def exportar_excel_licencias(self, request, queryset):
        """Exportar licencias a Excel"""
        # Implementación básica - se puede expandir
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = f'attachment; filename="licencias_{timezone.now().strftime("%Y%m%d")}.xlsx"'
        
        import openpyxl
        from openpyxl import Workbook
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Licencias"
        
        # Encabezados
        headers = ['DNI', 'Operario', 'Descripción', 'Fecha Inicio', 'Fecha Fin', 'Duración', 'Estado', 'Aprobada Por']
        for col, header in enumerate(headers, 1):
            ws.cell(row=1, column=col, value=header)
        
        # Datos
        for row, licencia in enumerate(queryset, 2):
            ws.cell(row=row, column=1, value=licencia.operario.dni)
            ws.cell(row=row, column=2, value=str(licencia.operario))
            ws.cell(row=row, column=3, value=licencia.descripcion or '-')
            ws.cell(row=row, column=4, value=licencia.fecha_inicio.strftime('%d/%m/%Y') if licencia.fecha_inicio else '-')
            ws.cell(row=row, column=5, value=licencia.fecha_fin.strftime('%d/%m/%Y') if licencia.fecha_fin else '-')
            ws.cell(row=row, column=6, value=f'{licencia.duracion} días' if licencia.duracion else '-')
            ws.cell(row=row, column=7, value=licencia.get_estado_display())
            ws.cell(row=row, column=8, value=str(licencia.aprobada_por) if licencia.aprobada_por else '-')
        
        wb.save(response)
        return response
    exportar_excel_licencias.short_description = "📊 Exportar a Excel"


# ------------------------------------------------------------------------------------
# ADMINS PARA CALENDARIO LABORAL Y GRUPOS DE SÁBADO
# ------------------------------------------------------------------------------------

@admin.register(CalendarioLaboral)
class CalendarioLaboralAdmin(UnfoldModelAdmin):
    """Admin customizado para definir días especiales (feriados, paros, etc.)"""

    list_display = ('fecha', 'tipo_dia_display', 'nombre', 'aplica_a_todas_areas', 'creado_el')
    list_filter = ('tipo_dia', 'fecha', 'aplica_a_todas_areas')
    search_fields = ('nombre', 'descripcion')
    date_hierarchy = 'fecha'

    fieldsets = (
        ('Información del Día', {
            'fields': ('fecha', 'tipo_dia', 'nombre'),
            'classes': ('wide',),
        }),
        ('Detalles', {
            'fields': ('descripcion', 'aplica_a_todas_areas', 'areas'),
            'classes': ('collapse',),
        }),
        ('Auditoría', {
            'fields': ('creado_el', 'actualizado_el'),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('creado_el', 'actualizado_el')

    filter_horizontal = ('areas',)

    def tipo_dia_display(self, obj):
        """Muestra el tipo de día con color según tipo"""
        color_map = {
            'laboral': '#10b981',      # Verde
            'feriado': '#f59e0b',      # Naranja
            'feriado_movible': '#3b82f6',  # Azul
            'paro': '#ef4444',         # Rojo
            'mantenimiento': '#8b5cf6',  # Púrpura
            'otro': '#6b7280',         # Gris
        }
        color = color_map.get(obj.tipo_dia, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_tipo_dia_display()
        )
    tipo_dia_display.short_description = 'Tipo de Día'

    actions = ['marcar_como_laboral', 'marcar_como_feriado', 'marcar_como_paro']

    def marcar_como_laboral(self, request, queryset):
        updated = queryset.update(tipo_dia='laboral')
        self.message_user(request, f"✅ {updated} día(s) marcado(s) como laborales")
    marcar_como_laboral.short_description = "✅ Marcar como Laborales"

    def marcar_como_feriado(self, request, queryset):
        updated = queryset.update(tipo_dia='feriado')
        self.message_user(request, f"🎉 {updated} día(s) marcado(s) como feriados")
    marcar_como_feriado.short_description = "🎉 Marcar como Feriados"

    def marcar_como_paro(self, request, queryset):
        updated = queryset.update(tipo_dia='paro')
        self.message_user(request, f"✊ {updated} día(s) marcado(s) como paros")
    marcar_como_paro.short_description = "✊ Marcar como Paros"


@admin.register(GrupoSabado)
class GrupoSabadoAdmin(UnfoldModelAdmin):
    """Admin para asignar operarios a grupos de sábado (A/B)"""

    list_display = ('operario', 'grupo_display', 'fecha_inicio', 'fecha_fin_display', 'es_activo')
    list_filter = ('grupo', 'fecha_inicio', 'operario')
    search_fields = ('operario__apellido', 'operario__nombre')

    fieldsets = (
        ('Asignación', {
            'fields': ('operario', 'grupo'),
            'classes': ('wide',),
        }),
        ('Vigencia', {
            'fields': ('fecha_inicio', 'fecha_fin'),
            'classes': ('wide',),
        }),
        ('Notas', {
            'fields': ('descripcion',),
            'classes': ('collapse',),
        }),
        ('Auditoría', {
            'fields': ('creado_el', 'actualizado_el'),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('creado_el', 'actualizado_el')

    def grupo_display(self, obj):
        """Muestra el grupo con color"""
        color = '#8b5cf6' if obj.grupo == 'A' else '#06b6d4'  # Púrpura para A, Cyan para B
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_grupo_display()
        )
    grupo_display.short_description = 'Grupo'

    def fecha_fin_display(self, obj):
        """Muestra la fecha fin o 'Indefinido'"""
        if obj.fecha_fin:
            return obj.fecha_fin.strftime('%d/%m/%Y')
        return format_html(
            '<span style="color: #10b981; font-weight: bold;">∞ Indefinido</span>'
        )
    fecha_fin_display.short_description = 'Fecha Fin'

    def es_activo(self, obj):
        """Muestra si la asignación está activa"""
        from django.utils import timezone
        activo = obj.is_active(timezone.now().date())
        icon = '✅' if activo else '❌'
        return format_html(
            '<span style="color: {};">{} {}</span>',
            '#10b981' if activo else '#ef4444',
            icon,
            'Activo' if activo else 'Inactivo'
        )
    es_activo.short_description = 'Estado'

    ordering = ('-fecha_inicio',)


@admin.register(SugerenciaFeriado)
class SugerenciaFeriadoAdmin(UnfoldModelAdmin):
    """Admin para revisar y procesar sugerencias de feriados."""

    list_display = (
        'fecha',
        'nombre',
        'mostrar_tipo',
        'mostrar_estado',
        'fuente',
        'ya_existe_en_calendario',
        'fecha_creada',
    )
    list_filter = (
        ('fecha', DateRangeFilter),
        'estado',
        'tipo_sugerencia',
        'fuente',
    )
    search_fields = ('nombre', 'fecha')
    ordering = ('estado', 'fecha')
    list_per_page = 30
    readonly_fields = (
        'fecha_creada',
        'fecha_procesada',
        'procesado_por',
        'fuente',
        'fuente_url',
        'mostrar_datos_fuente',
    )
    fieldsets = (
        ('Información del feriado', {
            'fields': ('fecha', 'nombre', 'tipo_sugerencia', 'estado', 'nota_admin'),
        }),
        ('Fuente', {
            'fields': ('fuente', 'fuente_url', 'mostrar_datos_fuente'),
        }),
        ('Auditoría', {
            'fields': ('fecha_creada', 'fecha_procesada', 'procesado_por'),
        }),
    )
    actions = ('accion_aceptar', 'accion_rechazar', 'accion_revisar_despues')

    def mostrar_tipo(self, obj):
        colores = {
            'feriado_nacional': '#1b5e20',
            'feriado_movible': '#1a237e',
            'otro': '#6d4c41',
        }
        color = colores.get(obj.tipo_sugerencia, '#424242')
        return format_html(
            '<span style="color:{}; font-weight:600;">{}</span>',
            color,
            obj.get_tipo_sugerencia_display()
        )

    mostrar_tipo.short_description = 'Tipo'

    def mostrar_estado(self, obj):
        colores = {
            'pendiente': '#ff6f00',
            'aceptado': '#2e7d32',
            'rechazado': '#c62828',
            'revisado_despues': '#0277bd',
        }
        color = colores.get(obj.estado, '#424242')
        return format_html(
            '<span style="color:{}; font-weight:600;">{}</span>',
            color,
            obj.get_estado_display()
        )

    mostrar_estado.short_description = 'Estado'

    def mostrar_datos_fuente(self, obj):
        if not obj.datos_fuente:
            return format_html('<span style="color:#757575;">Sin datos</span>')
        pretty = json.dumps(obj.datos_fuente, indent=2, ensure_ascii=False)
        return format_html('<pre style="white-space:pre-wrap;">{}</pre>', pretty)

    mostrar_datos_fuente.short_description = 'Datos originales'

    def ya_existe_en_calendario(self, obj):
        return obj.ya_existe_en_calendario

    ya_existe_en_calendario.boolean = True
    ya_existe_en_calendario.short_description = "En calendario"

    def accion_aceptar(self, request, queryset):
        aceptadas = 0
        for sugerencia in queryset:
            if sugerencia.estado == 'aceptado':
                continue
            sugerencia.aceptar(usuario=request.user)
            aceptadas += 1
        if aceptadas:
            messages.success(
                request,
                f"✅ {aceptadas} sugerencia(s) aceptadas y añadidas al calendario."
            )
        else:
            messages.info(request, "No había sugerencias pendientes para aceptar.")

    accion_aceptar.short_description = "✅ Aceptar sugerencias seleccionadas"

    def accion_rechazar(self, request, queryset):
        rechazadas = 0
        for sugerencia in queryset:
            if sugerencia.estado == 'rechazado':
                continue
            sugerencia.rechazar(usuario=request.user)
            rechazadas += 1
        if rechazadas:
            messages.success(
                request,
                f"❌ {rechazadas} sugerencia(s) marcadas como rechazadas."
            )
        else:
            messages.info(request, "No había sugerencias pendientes para rechazar.")

    accion_rechazar.short_description = "❌ Rechazar sugerencias seleccionadas"

    def accion_revisar_despues(self, request, queryset):
        actualizadas = queryset.exclude(estado='revisado_despues').update(estado='revisado_despues')
        if actualizadas:
            messages.success(
                request,
                f"🔄 {actualizadas} sugerencia(s) marcadas para revisar después."
            )
        else:
            messages.info(request, "No se actualizó ninguna sugerencia.")

    accion_revisar_despues.short_description = "🔄 Marcar para revisar después"
