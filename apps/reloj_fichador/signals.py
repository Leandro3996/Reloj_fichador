# signals.py

from django.db.models.signals import post_save, post_delete, pre_delete, pre_save
from django.dispatch import receiver
from .models import (
    RegistroDiario, RegistroAsistencia,
    Horas_trabajadas, Horas_extras, Horas_totales, Licencia, HorasEnfermedad
)
from .utils import suppress_signal, _thread_locals
from datetime import timedelta
import logging

logger = logging.getLogger('reloj_fichador')


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
    if getattr(_thread_locals, 'in_save', False):
        return  # Prevenir recursión si la lógica vuelve a disparar la señal

    operario = instance.operario
    fecha_logica = RegistroDiario.calcular_fecha_logica(instance.hora_fichada, instance.tipo_movimiento)
    mes_logico = fecha_logica.strftime('%Y-%m')

    with suppress_signal():  # Prevenimos cascadas infinitas de señales
        # 1) Calculamos y guardamos horas trabajadas (sin recorte previo)
        Horas_trabajadas.calcular_horas_trabajadas(operario, fecha_logica)
        
        # 2) Calculamos horas extras (usa las horas normales+nocturnas reales)
        Horas_extras.calcular_horas_extras(operario, fecha_logica)
        
        # 3) **Primero recortamos en Horas_trabajadas a un máximo de 8h**
        try:
            ht = Horas_trabajadas.objects.get(operario=operario, fecha=fecha_logica)
            total_reales = ht.horas_normales + ht.horas_nocturnas
            limite_jornada = timedelta(hours=8)  # O 8h30, según tus reglas

            if total_reales > limite_jornada:
                ratio_n = ht.horas_normales / total_reales if total_reales else 0
                ratio_noct = ht.horas_nocturnas / total_reales if total_reales else 0

                ht.horas_normales = limite_jornada * ratio_n
                ht.horas_nocturnas = limite_jornada * ratio_noct

            ht.save()
        except Horas_trabajadas.DoesNotExist:
            pass

        # 4) Ahora que Horas_trabajadas tiene los valores recortados, recalculamos Horas_totales
        Horas_totales.calcular_horas_totales(operario, mes_logico)



@receiver(post_delete, sender=RegistroDiario)
def actualizar_horas_despues_de_eliminar(sender, instance, **kwargs):
    """
    Cuando se elimina un RegistroDiario, recalculamos todo también.
    """
    operario = instance.operario
    fecha_logica = RegistroDiario.calcular_fecha_logica(instance.hora_fichada, instance.tipo_movimiento)
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


@receiver(post_save, sender=Licencia)
def recalcular_horas_al_aprobar_licencia(sender, instance, created, **kwargs):
    """
    Cuando se aprueba una licencia, recalcula automáticamente Horas_totales
    para todos los meses afectados por la licencia (fecha_inicio a fecha_fin).

    Esto es especialmente importante cuando hay cambios en la lógica de cálculo
    de horas de enfermedad, como excluir domingos o feriados.
    """
    # Solo procesar si la licencia fue aprobada
    if not (instance.estado == 'aprobada' and instance.aplicar_a_asistencia):
        return

    if not (instance.fecha_inicio and instance.fecha_fin):
        return

    try:
        from datetime import date
        from dateutil.relativedelta import relativedelta

        operario = instance.operario
        fecha_actual = instance.fecha_inicio

        # Iterar sobre todos los meses que abarca la licencia
        meses_procesados = set()
        while fecha_actual <= instance.fecha_fin:
            mes_str = fecha_actual.strftime('%Y-%m')

            # Evitar procesar el mismo mes múltiples veces
            if mes_str not in meses_procesados:
                try:
                    Horas_totales.calcular_horas_totales(operario, mes_str)
                    meses_procesados.add(mes_str)
                    logger.info(
                        f'Recalculadas Horas_totales para {operario} en {mes_str} '
                        f'(licencia {instance.id} aprobada)'
                    )
                except Exception as e:
                    logger.error(
                        f'Error recalculando Horas_totales para {operario} {mes_str}: {str(e)}'
                    )

            fecha_actual += timedelta(days=1)

    except Exception as e:
        logger.error(f'Error en signal de recalcular licencia {instance.id}: {str(e)}')


@receiver(pre_delete, sender=Licencia)
def limpiar_datos_al_eliminar_licencia(sender, instance, **kwargs):
    """
    Cuando se elimina una licencia:
    1. Elimina los registros de HorasEnfermedad asociados
    2. Des-justifica los RegistroAsistencia que estaban vinculados a esta licencia
    3. Recalcula Horas_totales de los meses afectados
    """
    try:
        operario = instance.operario
        meses_afectados = set()

        # 1. Recopilar meses afectados antes de eliminar
        if instance.fecha_inicio and instance.fecha_fin:
            fecha_actual = instance.fecha_inicio
            while fecha_actual <= instance.fecha_fin:
                meses_afectados.add(fecha_actual.strftime('%Y-%m'))
                fecha_actual += timedelta(days=1)

        # 2. Eliminar HorasEnfermedad asociadas
        horas_eliminadas = HorasEnfermedad.objects.filter(licencia=instance).delete()
        logger.info(f'Eliminados {horas_eliminadas[0]} registros de HorasEnfermedad para licencia {instance.id}')

        # 3. Des-justificar RegistroAsistencia vinculados a esta licencia
        registros_actualizados = RegistroAsistencia.objects.filter(
            licencia_relacionada=instance
        ).update(
            estado_justificacion=False,
            licencia_relacionada=None,
            descripcion=None
        )
        logger.info(f'Des-justificados {registros_actualizados} registros de asistencia para licencia {instance.id}')

        # 4. Recalcular Horas_totales de los meses afectados
        for mes_str in meses_afectados:
            try:
                Horas_totales.calcular_horas_totales(operario, mes_str)
                logger.info(f'Recalculadas Horas_totales para {operario} en {mes_str} (licencia {instance.id} eliminada)')
            except Exception as e:
                logger.error(f'Error recalculando Horas_totales para {operario} {mes_str}: {str(e)}')

    except Exception as e:
        logger.error(f'Error en signal pre_delete de licencia {instance.id}: {str(e)}')


# Variable para almacenar fechas originales antes del save
_licencia_fechas_originales = {}


@receiver(pre_save, sender=Licencia)
def guardar_fechas_originales_licencia(sender, instance, **kwargs):
    """
    Antes de guardar una licencia, guarda las fechas originales
    para detectar si cambiaron después del save.
    """
    if instance.pk:
        try:
            original = Licencia.objects.get(pk=instance.pk)
            _licencia_fechas_originales[instance.pk] = {
                'fecha_inicio': original.fecha_inicio,
                'fecha_fin': original.fecha_fin,
                'estado': original.estado,
            }
        except Licencia.DoesNotExist:
            pass


@receiver(post_save, sender=Licencia)
def reprocesar_si_cambiaron_fechas(sender, instance, created, **kwargs):
    """
    Después de guardar una licencia, si las fechas cambiaron:
    1. Limpia los datos del período anterior
    2. Re-procesa el nuevo período
    """
    if created:
        # Las licencias nuevas ya se procesan en el método save() del modelo
        return

    original = _licencia_fechas_originales.pop(instance.pk, None)
    if not original:
        return

    fechas_cambiaron = (
        original['fecha_inicio'] != instance.fecha_inicio or
        original['fecha_fin'] != instance.fecha_fin
    )

    if not fechas_cambiaron:
        return

    if instance.estado != 'aprobada':
        return

    try:
        operario = instance.operario
        logger.info(f'Detectado cambio de fechas en licencia {instance.id}: '
                   f'{original["fecha_inicio"]}-{original["fecha_fin"]} → '
                   f'{instance.fecha_inicio}-{instance.fecha_fin}')

        # 1. Eliminar HorasEnfermedad anteriores de esta licencia
        HorasEnfermedad.objects.filter(licencia=instance).delete()

        # 2. Des-justificar registros del período ANTERIOR
        if original['fecha_inicio'] and original['fecha_fin']:
            RegistroAsistencia.objects.filter(
                operario=operario,
                fecha__gte=original['fecha_inicio'],
                fecha__lte=original['fecha_fin'],
                licencia_relacionada=instance
            ).update(
                estado_justificacion=False,
                licencia_relacionada=None,
                descripcion=None
            )

            # Recalcular Horas_totales del período anterior
            meses_anteriores = set()
            fecha_actual = original['fecha_inicio']
            while fecha_actual <= original['fecha_fin']:
                meses_anteriores.add(fecha_actual.strftime('%Y-%m'))
                fecha_actual += timedelta(days=1)

            for mes_str in meses_anteriores:
                Horas_totales.calcular_horas_totales(operario, mes_str)

        # 3. Re-procesar el nuevo período
        if instance.fecha_inicio and instance.fecha_fin and instance.aplicar_a_asistencia:
            from .tasks import procesar_licencia_aprobada
            procesar_licencia_aprobada(instance.pk)
            logger.info(f'Re-procesada licencia {instance.id} con nuevas fechas')

    except Exception as e:
        logger.error(f'Error re-procesando licencia {instance.id} por cambio de fechas: {str(e)}')
