from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab  # Importar crontab para la programación de tareas

# Configura el entorno predeterminado de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mantenedor.settings')

app = Celery('mantenedor')
app.conf.update(
    broker_connection_retry_on_startup=True
)

# Lee la configuración de Django y la aplica a Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubre automáticamente las tareas en todos los archivos tasks.py
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# Configura el horario de ejecución de Celery Beat
app.conf.beat_schedule = {
    'generar-registros-asistencia-5am': {
        'task': 'apps.reloj_fichador.tasks.generar_registros_asistencia',  # Ruta a la tarea
        'schedule': crontab(hour=1, minute=0),  # Se ejecuta todos los días a las 1:00 AM
    },
}



