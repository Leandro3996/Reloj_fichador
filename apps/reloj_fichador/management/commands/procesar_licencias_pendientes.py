"""
Management command para procesar todas las licencias aprobadas que aún no han sido procesadas.

Uso:
    python manage.py procesar_licencias_pendientes
    python manage.py procesar_licencias_pendientes --operario 146
    python manage.py procesar_licencias_pendientes --verbose
"""

from django.core.management.base import BaseCommand
from apps.reloj_fichador.models import Licencia, HorasEnfermedad
from apps.reloj_fichador.tasks import procesar_licencia_aprobada


class Command(BaseCommand):
    help = 'Procesa todas las licencias aprobadas que aún no han sido procesadas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--operario',
            type=int,
            help='ID del operario para procesar solo sus licencias',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Mostrar información detallada del procesamiento',
        )

    def handle(self, *args, **options):
        operario_id = options.get('operario')
        verbose = options.get('verbose', False)

        # Buscar licencias aprobadas que NO tengan HorasEnfermedad
        licencias = Licencia.objects.filter(estado='aprobada')

        if operario_id:
            licencias = licencias.filter(operario_id=operario_id)

        # Filtrar solo las que no han sido procesadas
        licencias_sin_procesar = []
        for licencia in licencias:
            horas_enf_count = HorasEnfermedad.objects.filter(
                operario=licencia.operario,
                licencia=licencia
            ).count()
            if horas_enf_count == 0:
                licencias_sin_procesar.append(licencia)

        if not licencias_sin_procesar:
            self.stdout.write(self.style.SUCCESS('✓ Todas las licencias aprobadas ya han sido procesadas'))
            return

        self.stdout.write(
            self.style.WARNING(f'⏳ Encontradas {len(licencias_sin_procesar)} licencias sin procesar')
        )

        processed = 0
        for licencia in licencias_sin_procesar:
            try:
                if verbose:
                    self.stdout.write(
                        f"\n📋 Procesando licencia {licencia.pk}:"
                        f"\n  - Operario: {licencia.operario}"
                        f"\n  - Período: {licencia.fecha_inicio} a {licencia.fecha_fin}"
                        f"\n  - Duración: {(licencia.fecha_fin - licencia.fecha_inicio).days + 1} días"
                    )

                # Procesar
                resultado = procesar_licencia_aprobada(licencia.pk)

                if verbose:
                    self.stdout.write(f"  - Resultado: {resultado}")

                processed += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ {licencia.pk}: {licencia.operario.apellido}, {licencia.operario.nombre}')
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error procesando licencia {licencia.pk}: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Procesadas {processed}/{len(licencias_sin_procesar)} licencias')
        )
