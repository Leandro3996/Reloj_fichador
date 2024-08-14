from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from .models import Operario, RegistroDiario
from django.http import HttpResponse

def home(request):
    return render(request, 'reloj_fichador/home.html')

def registrar_movimiento(request, tipo_movimiento):
    dni = request.POST.get('dni')
    try:
        operario = Operario.objects.get(dni=dni)
        es_valido, ultimo_movimiento = validar_secuencia_movimiento(operario, tipo_movimiento)
        if not es_valido:
            if ultimo_movimiento:
                mensaje_error = f"Inconsistencia: su última fichada fue '{ultimo_movimiento}'.".upper()
            else:
                mensaje_error = "Error: No se encontraron registros previos, y el primer movimiento debe ser 'Entrada'.".upper()
            messages.error(request, mensaje_error)
            return redirect('reloj_fichador:home')

        registro = RegistroDiario.objects.create(
            operario=operario,
            tipo_movimiento=tipo_movimiento,
            hora_fichada=timezone.now()
        )
        success_message = f"Registro exitoso: {operario} - {registro.tipo_movimiento} - {registro.hora_fichada.strftime('%d/%m/%Y %H:%M:%S')}".upper()
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

# Las siguientes vistas pueden ser simplificadas
def registrar_entrada(request):
    return render(request, 'reloj_fichador/base.html')

def registrar_salida_transitoria(request):
    return render(request, 'reloj_fichador/base.html')

def registrar_entrada_transitoria(request):
    return render(request, 'reloj_fichador/base.html')

def registrar_salida(request):
    return render(request, 'reloj_fichador/base.html')
