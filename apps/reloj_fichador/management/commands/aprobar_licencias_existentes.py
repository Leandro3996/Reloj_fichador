"""
Management command para aprobar todas las licencias existentes que están en estado 'pendiente'
y procesar sus horas de enfermedad.

Este comando es útil después de cambiar el default de licencias a 'aprobada',
para actualizar las licencias históricas.

Uso:
    python manage.py aprobar_licencias_existentes
    python manage.py aprobar_licencias_existentes --dry-run
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.reloj_fichador.models import Licencia
from apps.reloj_fichador.tasks import procesar_licencia_aprobada


class Command(BaseCommand):
    help = 'Aprueba todas las licencias pendientes y procesa sus horas de enfermedad'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostrar qué se haría sin ejecutar cambios',
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)

        # Buscar licencias pendientes
        licencias_pendientes = Licencia.objects.filter(estado='pendiente')

        if not licencias_pendientes.exists():
            self.stdout.write(self.style.SUCCESS('✓ No hay licencias pendientes para aprobar'))
            return

        self.stdout.write(
            self.style.WARNING(f'⏳ Encontradas {licencias_pendientes.count()} licencias pendientes')
        )

        if dry_run:
            self.stdout.write(self.style.WARNING('\n[DRY-RUN] No se realizarán cambios\n'))

        aprobadas = 0
        procesadas = 0

        for licencia in licencias_pendientes:
            self.stdout.write(
                f"\n📋 Licencia {licencia.pk}:"
                f"\n  - Operario: {licencia.operario}"
                f"\n  - Período: {licencia.fecha_inicio} a {licencia.fecha_fin}"
            )

            if dry_run:
                self.stdout.write(self.style.WARNING('  [DRY-RUN] Se aprobaría esta licencia'))
                aprobadas += 1
                continue

            try:
                # Aprobar la licencia
                licencia.estado = 'aprobada'
                licencia.fecha_aprobacion = timezone.now()
                licencia.save(update_fields=['estado', 'fecha_aprobacion'])
                aprobadas += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Aprobada'))

                # Procesar horas de enfermedad si tiene fechas
                if licencia.fecha_inicio and licencia.fecha_fin:
                    try:
                        resultado = procesar_licencia_aprobada(licencia.pk)
                        procesadas += 1
                        self.stdout.write(self.style.SUCCESS(f'  ✓ Procesada: {resultado}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'  ✗ Error procesando: {str(e)}'))
                else:
                    self.stdout.write(self.style.WARNING(f'  ⚠ Sin fechas, no se procesaron horas'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Error: {str(e)}'))

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Resumen: {aprobadas} aprobadas, {procesadas} procesadas')
        )
