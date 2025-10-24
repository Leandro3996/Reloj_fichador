"""
Management command para recalcular Horas_totales de todos los operarios.

Útil cuando hay cambios en la lógica de cálculo que requieren actualizar
registros existentes (ej: cambio en cálculo de horas de enfermedad).

Uso:
    # Recalcular todas las horas de todos los operarios
    python manage.py recalcular_horas_totales

    # Recalcular solo para un operario específico
    python manage.py recalcular_horas_totales --operario=123

    # Recalcular para un mes específico
    python manage.py recalcular_horas_totales --mes=2025-10

    # Recalcular para un operario y mes específicos
    python manage.py recalcular_horas_totales --operario=123 --mes=2025-10

    # Verboso
    python manage.py recalcular_horas_totales --verbosity=2
"""

from django.core.management.base import BaseCommand
from django.db.models import Q
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import logging

from apps.reloj_fichador.models import Operario, Horas_totales

logger = logging.getLogger('reloj_fichador')


class Command(BaseCommand):
    help = 'Recalcula Horas_totales para todos los operarios o un rango específico'

    def add_arguments(self, parser):
        parser.add_argument(
            '--operario',
            type=int,
            help='ID del operario específico a recalcular'
        )
        parser.add_argument(
            '--mes',
            type=str,
            help='Mes específico en formato YYYY-MM (ej: 2025-10)'
        )
        parser.add_argument(
            '--rango',
            type=str,
            help='Rango de meses: YYYY-MM:YYYY-MM (ej: 2025-01:2025-12)'
        )
        parser.add_argument(
            '--todos-operarios',
            action='store_true',
            help='Recalcular para todos los operarios (default)'
        )

    def handle(self, *args, **options):
        verbosity = options.get('verbosity', 1)
        operario_id = options.get('operario')
        mes = options.get('mes')
        rango = options.get('rango')

        # Validar formato de mes
        if mes:
            try:
                datetime.strptime(mes, '%Y-%m')
            except ValueError:
                self.stdout.write(
                    self.style.ERROR(f'Formato de mes inválido: {mes}. Use YYYY-MM')
                )
                return

        # Validar formato de rango
        meses_a_procesar = []
        if rango:
            try:
                fecha_inicio_str, fecha_fin_str = rango.split(':')
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m')
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m')

                fecha_actual = fecha_inicio
                while fecha_actual <= fecha_fin:
                    meses_a_procesar.append(fecha_actual.strftime('%Y-%m'))
                    fecha_actual += relativedelta(months=1)
            except (ValueError, AttributeError):
                self.stdout.write(
                    self.style.ERROR(f'Formato de rango inválido: {rango}. Use YYYY-MM:YYYY-MM')
                )
                return
        elif mes:
            meses_a_procesar = [mes]
        else:
            # Si no se especifica mes, usar últimos 24 meses
            fecha_actual = datetime.now()
            for i in range(24):
                meses_a_procesar.append(fecha_actual.strftime('%Y-%m'))
                fecha_actual -= relativedelta(months=1)
            meses_a_procesar.reverse()

        # Obtener operarios
        if operario_id:
            try:
                operarios = [Operario.objects.get(id=operario_id)]
            except Operario.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Operario con ID {operario_id} no existe')
                )
                return
        else:
            operarios = Operario.objects.all().order_by('id')

        # Procesar
        total_registros = 0
        total_operarios = operarios.count()

        self.stdout.write(
            self.style.SUCCESS(
                f'\n🔄 Recalculando Horas_totales...'
            )
        )
        self.stdout.write(
            f'  Operarios: {total_operarios}'
        )
        self.stdout.write(
            f'  Meses: {len(meses_a_procesar)} ({meses_a_procesar[0]} a {meses_a_procesar[-1]})'
        )
        self.stdout.write('')

        for operario in operarios:
            for mes_str in meses_a_procesar:
                try:
                    obj = Horas_totales.calcular_horas_totales(operario, mes_str)
                    total_registros += 1

                    if verbosity >= 2:
                        horas_normales_int = int(obj.horas_normales.total_seconds() / 3600)
                        horas_nocturnas_int = int(obj.horas_nocturnas.total_seconds() / 3600)
                        horas_extras_int = int(obj.horas_extras.total_seconds() / 3600)
                        horas_feriado_int = int(obj.horas_feriado.total_seconds() / 3600)
                        horas_enfermedad_int = int(obj.horas_enfermedad.total_seconds() / 3600)

                        self.stdout.write(
                            f'  ✓ {operario.nombre:20} {mes_str} | '
                            f'Normal: {horas_normales_int:3}h | '
                            f'Nocturna: {horas_nocturnas_int:3}h | '
                            f'Extras: {horas_extras_int:3}h | '
                            f'Feriado: {horas_feriado_int:3}h | '
                            f'Enfermedad: {horas_enfermedad_int:3}h'
                        )

                    logger.info(f'Recalculadas horas totales para {operario} en {mes_str}')

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'  ✗ Error recalculando {operario} {mes_str}: {str(e)}'
                        )
                    )
                    logger.error(f'Error recalculando horas para {operario} {mes_str}: {str(e)}')

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Recalculados {total_registros} registros de Horas_totales'
            )
        )
