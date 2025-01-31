# views.py

from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from .models import Operario, RegistroDiario, Horas_trabajadas, Horas_extras, Horas_feriado, Licencia
from django import forms
from .forms import LicenciaForm
from django_tables2 import SingleTableView
from .tables import OperarioTable
from datetime import datetime
import logging
from django.core.exceptions import ValidationError

# Configura el logger
logger = logging.getLogger(__name__)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@require_POST
def registrar_movimiento_tipo(request, tipo_movimiento):
    if not is_ajax(request):
        messages.error(request, "MÉTODO NO PERMITIDO ⚠️")
        logger.warning(f"Solicitud no AJAX recibida para registrar_movimiento_tipo con tipo_movimiento={tipo_movimiento}")
        return redirect('reloj_fichador:home')

    dni = request.POST.get('dni')
    inconsistency_override = request.POST.get('inconsistency_override') == 'True'

    if not tipo_movimiento:
        logger.error("No se proporcionó tipo_movimiento en la solicitud.")
        return JsonResponse({'success': False, 'message': "DEBE SELECCIONAR UN TIPO DE MOVIMIENTO ⚠️"}, status=400)

    try:
        operario = Operario.objects.get(dni=dni)
        logger.info(f"Operario encontrado: {operario.nombre} {operario.apellido}")
    except Operario.DoesNotExist:
        error_message = "OPERARIO NO ENCONTRADO ⚠️"
        logger.error(f"Operario con DNI={dni} no encontrado.")
        return JsonResponse({'success': False, 'message': error_message}, status=404)

    if not inconsistency_override:
        # Intentar crear y validar el registro
        registro = RegistroDiario(
            operario=operario,
            tipo_movimiento=tipo_movimiento,
            hora_fichada=timezone.now(),
        )
        try:
            registro.full_clean()  # Ejecuta la validación personalizada
            registro.save()  # Guarda normalmente
            tipo_movimiento_legible = registro.get_tipo_movimiento_display()
            success_message = f"REGISTRO EXITOSO: {operario.nombre} {operario.apellido} - {tipo_movimiento_legible} - {registro.hora_fichada.strftime('%d/%m/%Y %H:%M:%S')}"
            logger.info(f"Registro creado exitosamente: {success_message}")
            return JsonResponse({'success': True, 'message': success_message})
        except ValidationError as ve:
            # Inconsistencia detectada
            descripcion_inconsistencia = "; ".join(ve.message_dict.get('tipo_movimiento', []))
            logger.warning(f"Inconsistencia detectada en registro: {descripcion_inconsistencia}")
            return JsonResponse({
                'success': False,
                'inconsistencia': True,
                'descripcion_inconsistencia': descripcion_inconsistencia,
                'tipo_movimiento': tipo_movimiento
            }, status=400)
        except Exception as e:
            logger.exception(f"Excepción inesperada al registrar_movimiento_tipo: {e}")
            return JsonResponse({'success': False, 'message': 'ERROR INTERNO DEL SERVIDOR ⚠️'}, status=500)
    else:
        # Override: crear el registro como inconsistente
        registro = RegistroDiario(
            operario=operario,
            tipo_movimiento=tipo_movimiento,
            hora_fichada=timezone.now(),
            inconsistencia=True,
            valido=True,
            descripcion_inconsistencia="Fichada con inconsistencia por decisión del operario."
        )
        try:
            registro.save()
            tipo_movimiento_legible = registro.get_tipo_movimiento_display()
            success_message = f"REGISTRO CON INCONSISTENCIA: {operario.nombre} {operario.apellido} - {tipo_movimiento_legible} - {registro.hora_fichada.strftime('%d/%m/%Y %H:%M:%S')}"
            logger.info(f"Registro creado con inconsistencia: {success_message}")
            return JsonResponse({'success': True, 'message': success_message})
        except Exception as e:
            logger.exception(f"Excepción inesperada al registrar_movimiento_tipo con override: {e}")
            return JsonResponse({'success': False, 'message': 'ERROR INTERNO DEL SERVIDOR ⚠️'}, status=500)
        

def home(request):
    # Optimizar consultas
    operarios = Operario.objects.prefetch_related('areas').all()  # Optimiza la relación ManyToMany con áreas
    horas_trabajadas = Horas_trabajadas.objects.select_related('operario').all()  # Optimiza la relación ForeignKey con operario
    horas_extras = Horas_extras.objects.select_related('operario').all()
    horas_feriado = Horas_feriado.objects.select_related('operario').all()

    return render(request, 'reloj_fichador/home.html', {
        'operarios': operarios,
        'horas_trabajadas': horas_trabajadas,
        'horas_extras': horas_extras,
        'horas_feriado': horas_feriado,
    })

class LicenciaForm(forms.ModelForm):
    class Meta:
        model = Licencia
        fields = ['archivo', 'descripcion']

class OperarioListView(SingleTableView):
    model = Operario
    table_class = OperarioTable
    template_name = "operarios_list.html"

def generar_reporte_view(request):
    # Obtener los datos de tu modelo, excluyendo fichadas inconsistentes
    registros = RegistroDiario.objects.filter(inconsistencia=False)

    # Definir el contexto a pasar a la plantilla
    context = {
        'registros': registros,
        'current_time': datetime.now(),
        'current_page': 1,
        'total_pages': 1  # Puedes cambiar esta lógica si tienes paginación
    }

    # Renderizar la plantilla
    return render(request, 'reloj_fichador/reporte.html', context)