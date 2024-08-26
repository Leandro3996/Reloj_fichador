from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from .models import Operario, RegistroDiario, Horas_trabajadas, Horas_feriado, Horas_extras, Horas_totales
from django.http import HttpResponse


def home(request):
    # Optimizar consultas
    operarios = Operario.objects.prefetch_related('areas').all()  # Optimiza la relación ManyToMany con áreas
    horas_trabajadas = Horas_trabajadas.objects.select_related(
        'operario').all()  # Optimiza la relación ForeignKey con operario
    horas_extras = Horas_extras.objects.select_related('operario').all()
    horas_feriado = Horas_feriado.objects.select_related('operario').all()

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

        # Validar si la hora de salida es anterior a la de entrada (inconsistencia)
        if tipo == 'salida' and ultimo_movimiento == 'entrada':
            hora_actual = timezone.now()
            ultimo_registro = RegistroDiario.objects.filter(operario=operario).order_by('-hora_fichada').first()
            if hora_actual <= ultimo_registro.hora_fichada:
                mensaje_error = "Error: La hora de salida no puede ser anterior o igual a la hora de entrada.".upper()
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

def validar_secuencia_movimiento(operario, nuevo_movimiento, is_admin=False):
    ultimo_registro = RegistroDiario.objects.filter(operario=operario).order_by('-hora_fichada').first()

    if ultimo_registro:
        print(f"Último registro para el operario {operario.dni}: {ultimo_registro.tipo_movimiento} - {ultimo_registro.hora_fichada}")

        # Definir las transiciones válidas
        transiciones_validas = {
            'entrada': ['salida', 'salida_transitoria'],
            'salida_transitoria': ['entrada_transitoria'],
            'entrada_transitoria': ['salida'],
            'salida': ['entrada']
        }

        # Verificar si el nuevo movimiento es válido
        es_valido = nuevo_movimiento in transiciones_validas.get(ultimo_registro.tipo_movimiento, [])
        print(f"Nuevo movimiento: {nuevo_movimiento}, Es válido: {es_valido}")

        # Verificar si el nuevo movimiento es una salida antes de una entrada
        if es_valido and nuevo_movimiento == 'salida' and ultimo_registro.tipo_movimiento == 'entrada':
            hora_actual = timezone.now()
            if hora_actual <= ultimo_registro.hora_fichada:
                # Si la hora de salida es anterior o igual a la hora de entrada, es una inconsistencia
                print(f"Inconsistencia detectada: La hora de salida {hora_actual} es anterior o igual a la hora de entrada {ultimo_registro.hora_fichada}.")
                return False, "Error: La hora de salida no puede ser anterior o igual a la hora de entrada."

        # Permitir inconsistencia si es un admin
        if is_admin:
            return True, ultimo_registro.tipo_movimiento

        # Retornar si el movimiento es válido o no
        return es_valido, ultimo_registro.tipo_movimiento
    else:
        print(f"No se encontraron registros previos para el operario {operario.dni}.")
        # Si no hay un último registro, solo 'entrada' es válida
        return nuevo_movimiento == 'entrada', None
