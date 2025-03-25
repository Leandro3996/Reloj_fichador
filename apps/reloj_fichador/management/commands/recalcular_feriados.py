from django.core.management.base import BaseCommand
from apps.reloj_fichador.models import Operario, DiaFeriado, Horas_trabajadas
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Recalcula las horas feriado para todos los días feriados registrados'

    def handle(self, *args, **options):
        # Obtener todos los operarios activos
        operarios = Operario.objects.filter(activo=True)
        self.stdout.write(f"Procesando {operarios.count()} operarios activos...")

        # Obtener todos los días feriados
        feriados = DiaFeriado.objects.all().order_by('fecha')
        self.stdout.write(f"Encontrados {feriados.count()} días feriados...")

        total_actualizaciones = 0

        for feriado in feriados:
            self.stdout.write(f"Procesando feriado: {feriado.fecha} - {feriado.descripcion}")
            
            for operario in operarios:
                try:
                    # Recalcular horas trabajadas para este día (actualizará también horas feriado)
                    Horas_trabajadas.calcular_horas_trabajadas(operario, feriado.fecha)
                    total_actualizaciones += 1
                    
                    if total_actualizaciones % 10 == 0:
                        self.stdout.write(f"Procesadas {total_actualizaciones} actualizaciones...")
                except Exception as e:
                    logger.error(f"Error al procesar feriado {feriado.fecha} para operario {operario}: {str(e)}")
                    self.stdout.write(self.style.ERROR(f"Error al procesar operario {operario}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS(f"Proceso completado. Se actualizaron {total_actualizaciones} registros.")) 