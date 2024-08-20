from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from .models import Operario, RegistroDiario, Horas_trabajadas, Horas_feriado, Horas_extras
from django.http import HttpResponse

def home(request):
    operarios = Operario.objects.all()  # O filtra por algún criterio si es necesario
    horas_trabajadas = Horas_trabajadas.objects.all()
    horas_extras = Horas_extras.objects.all()
    horas_feriado = Horas_feriado.objects.all()
    return render(request, 'reloj_fichador/home.html', {
        'operarios': operarios,
        'horas_trabajadas': horas_trabajadas,
        'horas_extras': horas_extras,
        'horas_feriado': horas_feriado,
    })

def registrar_movimiento_tipo(request, tipo):
    dni = request.POST.get('dni')
    try:
        operario = Operario.objects.get(dni=dni)
        es_valido, ultimo_movimiento = validar_secuencia_movimiento(operario, tipo)
        if not es_valido:
            if ultimo_movimiento:
                mensaje_error = f"Inconsistencia: su última fichada fue '{ultimo_movimiento}'.".upper()
            else:
                mensaje_error = "Error: No se encontraron registros previos, y el primer movimiento debe ser 'Entrada'.".upper()
            messages.error(request, mensaje_error)
            return redirect('reloj_fichador:home')

        registro = RegistroDiario.objects.create(
            operario=operario,
            tipo_movimiento=tipo,
            hora_fichada=timezone.now()
        )

        # Utiliza el método get_tipo_movimiento_display() para obtener el valor legible del tipo de movimiento
        tipo_movimiento_legible = registro.get_tipo_movimiento_display()

        success_message = f"Registro exitoso: {operario.nombre} {operario.apellido} - {tipo_movimiento_legible} - {registro.hora_fichada.strftime('%d/%m/%Y %H:%M:%S')}".upper()
        messages.success(request, success_message)
        return redirect('reloj_fichador:home')
    except Operario.DoesNotExist:
        return render(request, 'reloj_fichador/base.html', {'error': 'Operario no encontrado'.upper()})


def validar_secuencia_movimiento(operario, nuevo_movimiento):
    ultimo_registro = RegistroDiario.objects.filter(operario=operario).order_by('-hora_fichada').first()
    if ultimo_registro:
        transiciones_validas = {
            'entrada': ['salida', 'salida_transitoria'],
            'salida_transitoria': ['entrada_transitoria'],
            'entrada_transitoria': ['salida'],
            'salida': ['entrada']
        }
        es_valido = nuevo_movimiento in transiciones_validas.get(ultimo_registro.tipo_movimiento, [])
        return es_valido, ultimo_registro.tipo_movimiento
    return nuevo_movimiento == 'entrada', None  # Asumir que 'entrada' es válida si no hay registros previos
