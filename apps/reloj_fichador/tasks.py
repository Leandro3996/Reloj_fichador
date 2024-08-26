from celery import shared_task
from django.utils import timezone
from .models import Operario, RegistroAsistencia

@shared_task
def generar_registros_asistencia():
    """
    Esta tarea genera registros de asistencia para todos los operarios activos en la fecha actual.
    Si el registro ya existe, verifica la asistencia.
    """
    hoy = timezone.now().date()
    operarios_activos = Operario.objects.filter(activo=True)

    for operario in operarios_activos:
        # Utiliza get_or_create para evitar duplicados y manejar la lógica de verificación de asistencia
        registro, created = RegistroAsistencia.objects.get_or_create(
            operario=operario,
            fecha=hoy
        )
        if created:
            print(f"Registro de asistencia creado para {operario} en {hoy}.")
        else:
            print(f"Registro de asistencia ya existente para {operario} en {hoy}.")

        # Verifica la asistencia del operario
        registro.verificar_asistencia()

@shared_task
def crear_asistencia_prueba(operario_id):
    try:
        print(f"Iniciando tarea para operario con ID {operario_id}")
        operario = Operario.objects.get(id=operario_id)
        print(f"Operario encontrado: {operario}")
        RegistroAsistencia.objects.create(
            operario=operario,
            fecha=timezone.now().date(),
            estado_asistencia='presente',
            descripcion="Asistencia de prueba"
        )
        print(f"Asistencia creada para operario con ID {operario_id}")
    except Operario.DoesNotExist:
        print(f"Operario con ID {operario_id} no existe")
    except Exception as e:
        print(f"Error al crear asistencia: {e}")
    return "Proceso completado"

@shared_task
def prueba_tarea():
    """
    Esta es una tarea de prueba simple para asegurarse de que Celery esté funcionando correctamente.
    """
    print("¡La tarea de Celery se ejecutó correctamente!")
    return "Tarea completada"
