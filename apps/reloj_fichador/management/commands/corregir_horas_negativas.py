"""
Management command para identificar y corregir registros con horas negativas.

Este comando encuentra registros en Horas_trabajadas y Horas_totales con valores
negativos y los recalcula usando la lógica corregida.

Uso:
    # Ver registros afectados sin corregir (dry-run)
    python manage.py corregir_horas_negativas --dry-run

    # Corregir todos los registros con horas negativas
    python manage.py corregir_horas_negativas

    # Corregir solo un operario específico
    python manage.py corregir_horas_negativas --operario=304

    # Verboso (muestra detalles de cada corrección)
    python manage.py corregir_horas_negativas --verbosity=2
"""

from django.core.management.base import BaseCommand
from django.db.models import Q
from datetime import timedelta
import logging

from apps.reloj_fichador.models import (
    Operario,
    Horas_trabajadas,
    Horas_totales,
    RegistroDiario
)

logger = logging.getLogger('reloj_fichador')


class Command(BaseCommand):
    help = 'Identifica y corrige registros con horas negativas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostrar registros afectados sin aplicar correcciones'
        )
        parser.add_argument(
            '--operario',
            type=int,
            help='ID del operario específico a corregir'
        )

    def handle(self, *args, **options):
        verbosity = options.get('verbosity', 1)
        dry_run = options.get('dry_run', False)
        operario_id = options.get('operario')

        self.stdout.write(
            self.style.WARNING(
                '\n🔍 Buscando registros con horas negativas...\n'
            )
        )

        # 1. Buscar registros en Horas_trabajadas con valores negativos
        query_trabajadas = Q(horas_normales__lt=timedelta()) | \
                          Q(horas_nocturnas__lt=timedelta()) | \
                          Q(horas_extras__lt=timedelta())

        if operario_id:
            query_trabajadas &= Q(operario_id=operario_id)

        registros_trabajadas = Horas_trabajadas.objects.filter(
            query_trabajadas
        ).select_related('operario').order_by('fecha')

        # 2. Buscar registros en Horas_totales con valores negativos
        query_totales = Q(horas_normales__lt=timedelta()) | \
                       Q(horas_nocturnas__lt=timedelta()) | \
                       Q(horas_extras__lt=timedelta()) | \
                       Q(horas_feriado__lt=timedelta()) | \
                       Q(horas_enfermedad__lt=timedelta())

        if operario_id:
            query_totales &= Q(operario_id=operario_id)

        registros_totales = Horas_totales.objects.filter(
            query_totales
        ).select_related('operario').order_by('mes_actual')

        total_trabajadas = registros_trabajadas.count()
        total_totales = registros_totales.count()

        self.stdout.write(
            f'  📊 Horas_trabajadas con valores negativos: {total_trabajadas}'
        )
        self.stdout.write(
            f'  📊 Horas_totales con valores negativos: {total_totales}\n'
        )

        if total_trabajadas == 0 and total_totales == 0:
            self.stdout.write(
                self.style.SUCCESS('✅ No se encontraron registros con horas negativas\n')
            )
            return

        # Mostrar detalles de registros afectados
        if verbosity >= 1:
            self.stdout.write(self.style.WARNING('📋 Registros afectados en Horas_trabajadas:\n'))
            for reg in registros_trabajadas:
                self.stdout.write(
                    f'  ID: {reg.id:5} | {reg.operario.apellido:15} | '
                    f'Fecha: {reg.fecha} | '
                    f'N: {self._format_duration(reg.horas_normales):8} | '
                    f'NC: {self._format_duration(reg.horas_nocturnas):8} | '
                    f'EX: {self._format_duration(reg.horas_extras):8}'
                )

            if total_totales > 0:
                self.stdout.write(self.style.WARNING('\n📋 Registros afectados en Horas_totales:\n'))
                for reg in registros_totales:
                    self.stdout.write(
                        f'  ID: {reg.id:5} | {reg.operario.apellido:15} | '
                        f'Mes: {reg.mes_actual} | '
                        f'N: {self._format_duration(reg.horas_normales):8} | '
                        f'NC: {self._format_duration(reg.horas_nocturnas):8} | '
                        f'EX: {self._format_duration(reg.horas_extras):8}'
                    )

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'\n⚠️  Modo DRY-RUN: No se aplicaron cambios.'
                )
            )
            self.stdout.write(
                f'   Ejecute sin --dry-run para corregir estos {total_trabajadas + total_totales} registros.\n'
            )
            return

        # Aplicar correcciones
        self.stdout.write(
            self.style.SUCCESS('\n🔧 Aplicando correcciones...\n')
        )

        corregidos_trabajadas = 0
        errores = 0

        # Corregir Horas_trabajadas
        for reg in registros_trabajadas:
            try:
                antes = {
                    'normales': reg.horas_normales,
                    'nocturnas': reg.horas_nocturnas,
                    'extras': reg.horas_extras
                }

                # Recalcular usando la lógica corregida
                Horas_trabajadas.calcular_horas_trabajadas(reg.operario, reg.fecha)

                # Recargar el registro para ver los nuevos valores
                reg.refresh_from_db()

                despues = {
                    'normales': reg.horas_normales,
                    'nocturnas': reg.horas_nocturnas,
                    'extras': reg.horas_extras
                }

                corregidos_trabajadas += 1

                if verbosity >= 2:
                    self.stdout.write(
                        f'  ✓ ID {reg.id}: {reg.operario.apellido} - {reg.fecha}'
                    )
                    self.stdout.write(
                        f'    Antes:   N={self._format_duration(antes["normales"]):8} | '
                        f'NC={self._format_duration(antes["nocturnas"]):8} | '
                        f'EX={self._format_duration(antes["extras"]):8}'
                    )
                    self.stdout.write(
                        f'    Después: N={self._format_duration(despues["normales"]):8} | '
                        f'NC={self._format_duration(despues["nocturnas"]):8} | '
                        f'EX={self._format_duration(despues["extras"]):8}\n'
                    )

                logger.info(f'Corregidas horas negativas para {reg.operario} en {reg.fecha}')

            except Exception as e:
                errores += 1
                self.stdout.write(
                    self.style.ERROR(
                        f'  ✗ Error corrigiendo ID {reg.id} ({reg.operario} - {reg.fecha}): {str(e)}'
                    )
                )
                logger.error(f'Error corrigiendo horas: {str(e)}')

        # Corregir Horas_totales (recalculando el mes completo)
        corregidos_totales = 0
        meses_procesados = set()

        for reg in registros_totales:
            try:
                # Evitar procesar el mismo mes varias veces
                clave = (reg.operario.id, reg.mes_actual)
                if clave in meses_procesados:
                    continue
                meses_procesados.add(clave)

                antes = {
                    'normales': reg.horas_normales,
                    'nocturnas': reg.horas_nocturnas,
                    'extras': reg.horas_extras,
                    'feriado': reg.horas_feriado,
                    'enfermedad': reg.horas_enfermedad
                }

                # Recalcular horas totales del mes
                Horas_totales.calcular_horas_totales(reg.operario, reg.mes_actual)

                # Recargar
                reg.refresh_from_db()

                despues = {
                    'normales': reg.horas_normales,
                    'nocturnas': reg.horas_nocturnas,
                    'extras': reg.horas_extras,
                    'feriado': reg.horas_feriado,
                    'enfermedad': reg.horas_enfermedad
                }

                corregidos_totales += 1

                if verbosity >= 2:
                    self.stdout.write(
                        f'  ✓ ID {reg.id}: {reg.operario.apellido} - {reg.mes_actual}'
                    )
                    self.stdout.write(
                        f'    Antes:   N={self._format_duration(antes["normales"]):8} | '
                        f'NC={self._format_duration(antes["nocturnas"]):8}'
                    )
                    self.stdout.write(
                        f'    Después: N={self._format_duration(despues["normales"]):8} | '
                        f'NC={self._format_duration(despues["nocturnas"]):8}\n'
                    )

                logger.info(f'Corregidas horas totales para {reg.operario} en {reg.mes_actual}')

            except Exception as e:
                errores += 1
                self.stdout.write(
                    self.style.ERROR(
                        f'  ✗ Error corrigiendo ID {reg.id} ({reg.operario} - {reg.mes_actual}): {str(e)}'
                    )
                )
                logger.error(f'Error corrigiendo horas totales: {str(e)}')

        # Resumen final
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Correcciones completadas:'
            )
        )
        self.stdout.write(f'   Horas_trabajadas corregidas: {corregidos_trabajadas}')
        self.stdout.write(f'   Horas_totales corregidas: {corregidos_totales}')
        if errores > 0:
            self.stdout.write(
                self.style.ERROR(f'   Errores encontrados: {errores}')
            )
        self.stdout.write('')

    def _format_duration(self, td):
        """Formatea un timedelta para mostrar horas:minutos"""
        if td is None:
            return "None"
        total_seconds = td.total_seconds()
        is_negative = total_seconds < 0
        total_seconds = abs(total_seconds)
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        sign = "-" if is_negative else ""
        return f"{sign}{hours:02d}:{minutes:02d}"
