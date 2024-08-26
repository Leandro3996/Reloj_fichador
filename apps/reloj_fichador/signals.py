from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import RegistroDiario, RegistroAsistencia

@receiver(post_save, sender=RegistroDiario)
def actualizar_asistencia(sender, instance, created, **kwargs):
    if created:  # Solo actuar cuando se crea un nuevo registro
        fecha_actual = instance.hora_fichada.date()
        operario = instance.operario

        # Verifica si ya existe un registro de asistencia para la fecha actual
        registro_asistencia, created = RegistroAsistencia.objects.get_or_create(
            operario=operario,
            fecha=fecha_actual
        )

        # Actualiza la asistencia del operario
        registro_asistencia.verificar_asistencia()

@receiver(post_delete, sender=RegistroDiario)
def actualizar_asistencia_despues_de_borrar(sender, instance, **kwargs):
    # Obtener la fecha y el operario relacionado con el registro eliminado
    fecha_actual = instance.hora_fichada.date()
    operario = instance.operario

    # Verificar si ya existe un registro de asistencia para la fecha actual
    try:
        registro_asistencia = RegistroAsistencia.objects.get(operario=operario, fecha=fecha_actual)
        registro_asistencia.verificar_asistencia()  # Actualizar el estado de asistencia
    except RegistroAsistencia.DoesNotExist:
        # Si no existe el registro de asistencia, no es necesario hacer nada
        pass
