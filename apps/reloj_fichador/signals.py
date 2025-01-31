# signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import (
    RegistroDiario, RegistroAsistencia,
    Horas_trabajadas, Horas_extras, Horas_totales
)
from .utils import suppress_signal, _thread_locals
from datetime import timedelta


@receiver(post_save, sender=RegistroDiario)
def actualizar_asistencia(sender, instance, created, **kwargs):
    if created:  # Solo actuar cuando se crea un nuevo registro
        fecha_actual = instance.hora_fichada.date()
        operario = instance.operario

        # Verifica si ya existe un registro de asistencia para la fecha actual
        registro_asistencia, _ = RegistroAsistencia.objects.get_or_create(
            operario=operario,
            fecha=fecha_actual
        )
        # Actualiza la asistencia del operario
        registro_asistencia.verificar_asistencia()


@receiver(post_delete, sender=RegistroDiario)
def actualizar_asistencia_despues_de_borrar(sender, instance, **kwargs):
    fecha_actual = instance.hora_fichada.date()
    operario = instance.operario

    try:
        registro_asistencia = RegistroAsistencia.objects.get(operario=operario, fecha=fecha_actual)
        registro_asistencia.verificar_asistencia()
    except RegistroAsistencia.DoesNotExist:
        pass


@receiver(post_save, sender=RegistroDiario)
def actualizar_horas_despues_de_guardar(sender, instance, **kwargs):
    """
    Cada vez que se guarda un RegistroDiario nuevo o se actualiza uno existente,
    recalculamos horas trabajadas, extras y totales.
    
    Además, haremos el 'recorte' de horas normales/nocturnas a 8h
    solo después de que Horas_extras ya haya visto la cifra real.
    """
    if getattr(_thread_locals, 'in_save', False):
        return  # Prevenir recursión si la lógica vuelve a disparar la señal

    operario = instance.operario
    fecha_logica = RegistroDiario.calcular_fecha_logica(instance.hora_fichada)
    mes_logico = fecha_logica.strftime('%Y-%m')

    with suppress_signal():  # Prevenimos cascadas infinitas de señales
        # 1) Calculamos y guardamos horas trabajadas (sin recorte previo)
        Horas_trabajadas.calcular_horas_trabajadas(operario, fecha_logica)
        
        # 2) Calculamos horas extras (usa las horas normales+nocturnas reales)
        Horas_extras.calcular_horas_extras(operario, fecha_logica)
        
        # 3) Calculamos horas totales del mes
        Horas_totales.calcular_horas_totales(operario, mes_logico)

        # 4) Ahora SÍ recortamos en Horas_trabajadas a un máximo de 8h (u 8h30, según reglas).
        try:
            ht = Horas_trabajadas.objects.get(operario=operario, fecha=fecha_logica)
            # Suma real (guardada en horas_trabajadas)
            total_reales = ht.horas_normales + ht.horas_nocturnas
            limite_jornada = timedelta(hours=8)  # Cambia aquí si quieres 8h30, etc.

            if total_reales > limite_jornada:
                # Repartimos las 8 horas entre normales y nocturnas de forma proporcional
                ratio_n = ht.horas_normales / total_reales if total_reales else 0
                ratio_noct = ht.horas_nocturnas / total_reales if total_reales else 0

                ht.horas_normales = limite_jornada * ratio_n
                ht.horas_nocturnas = limite_jornada * ratio_noct

            # Guardamos el recorte
            ht.save()

        except Horas_trabajadas.DoesNotExist:
            # Si no existe, simplemente no hacemos nada
            pass


@receiver(post_delete, sender=RegistroDiario)
def actualizar_horas_despues_de_eliminar(sender, instance, **kwargs):
    """
    Cuando se elimina un RegistroDiario, recalculamos todo también.
    """
    operario = instance.operario
    fecha_logica = RegistroDiario.calcular_fecha_logica(instance.hora_fichada)
    mes_logico = fecha_logica.strftime('%Y-%m')

    with suppress_signal():
        Horas_trabajadas.calcular_horas_trabajadas(operario, fecha_logica)
        Horas_extras.calcular_horas_extras(operario, fecha_logica)
        Horas_totales.calcular_horas_totales(operario, mes_logico)


@receiver(post_save, sender=Horas_trabajadas)
def actualizar_horas_extras(sender, instance, **kwargs):
    """
    Cada vez que se guardan Horas_trabajadas, se recalculan las extras
    (aunque ojo: ya las recalcamos en post_save de RegistroDiario).
    """
    operario = instance.operario
    fecha = instance.fecha

    with suppress_signal():
        Horas_extras.calcular_horas_extras(operario, fecha)
