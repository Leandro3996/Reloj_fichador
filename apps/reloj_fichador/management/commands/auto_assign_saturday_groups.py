"""
Management command para asignar automáticamente grupos de sábado a operarios.

Algoritmo:
1. Para cada operario, analiza sus registros históricos de sábados (RegistroDiario)
2. Detecta el primer sábado que trabajó y su grupo correspondiente
3. Crea o actualiza el registro GrupoSabado con esta asignación
4. Los operarios sin registros de sábados quedan sin asignación (deben hacerlo manualmente)

Uso:
    # Asignar grupos a todos los operarios
    python manage.py auto_assign_saturday_groups

    # Asignar a un operario específico
    python manage.py auto_assign_saturday_groups --operario=123

    # Mostrar resultados sin guardar (dry-run)
    python manage.py auto_assign_saturday_groups --dry-run

    # Verboso
    python manage.py auto_assign_saturday_groups --verbosity=2
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
import logging

from apps.reloj_fichador.models import Operario, GrupoSabado
from apps.reloj_fichador.utils import detectar_grupo_sabado_operario

logger = logging.getLogger('reloj_fichador')


class Command(BaseCommand):
    help = 'Asigna automáticamente grupos de sábado a operarios basándose en su historial de registros'

    def add_arguments(self, parser):
        parser.add_argument(
            '--operario',
            type=int,
            help='ID del operario específico a asignar'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostrar cambios que se harían sin guardarlos'
        )

    def handle(self, *args, **options):
        verbosity = options.get('verbosity', 1)
        operario_id = options.get('operario')
        dry_run = options.get('dry_run', False)

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
        total_asignados = 0
        total_sin_registros = 0
        total_errores = 0

        self.stdout.write(
            self.style.SUCCESS('\n🔄 Asignando grupos de sábado...')
        )
        self.stdout.write(f'  Operarios: {operarios.count()}')
        if dry_run:
            self.stdout.write(self.style.WARNING('  Modo: DRY-RUN (no se guardarán cambios)'))
        self.stdout.write('')

        hoy = timezone.now().date()

        for operario in operarios:
            try:
                # Detectar grupo del operario
                grupo_auto, primer_sabado = detectar_grupo_sabado_operario(operario)

                if not grupo_auto:
                    # Operario sin registros de sábados
                    if verbosity >= 2:
                        self.stdout.write(
                            f'  ⊘ {operario.nombre:20} | Sin registros de sábados'
                        )
                    total_sin_registros += 1
                    logger.info(f'{operario} no tiene registros de sábados')
                    continue

                # Buscar asignación existente
                grupo_existente = GrupoSabado.objects.filter(
                    operario=operario,
                    fecha_inicio__lte=hoy
                ).exclude(
                    fecha_fin__isnull=False,
                    fecha_fin__lt=hoy
                ).first()

                if grupo_existente and grupo_existente.grupo == grupo_auto:
                    # Ya está correctamente asignado
                    if verbosity >= 2:
                        self.stdout.write(
                            f'  ✓ {operario.nombre:20} | Grupo {grupo_auto} (ya asignado desde {grupo_existente.fecha_inicio})'
                        )
                    continue

                # Crear o actualizar asignación
                if dry_run:
                    if verbosity >= 2:
                        if grupo_existente:
                            self.stdout.write(
                                self.style.WARNING(
                                    f'  ↻ {operario.nombre:20} | Grupo {grupo_existente.grupo} → {grupo_auto} '
                                    f'(primer sábado: {primer_sabado}) [DRY-RUN]'
                                )
                            )
                        else:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f'  + {operario.nombre:20} | Asignar Grupo {grupo_auto} '
                                    f'(primer sábado: {primer_sabado}) [DRY-RUN]'
                                )
                            )
                    total_asignados += 1
                else:
                    # Guardar la asignación
                    if grupo_existente:
                        # Actualizar: cerrar el anterior y crear uno nuevo
                        grupo_existente.fecha_fin = hoy - timedelta(days=1)
                        grupo_existente.save()

                    GrupoSabado.objects.create(
                        operario=operario,
                        grupo=grupo_auto,
                        fecha_inicio=hoy,
                        descripcion=f'Auto-detectado desde primer sábado trabajado ({primer_sabado})'
                    )

                    if verbosity >= 2:
                        if grupo_existente:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f'  ↻ {operario.nombre:20} | Grupo {grupo_existente.grupo} → {grupo_auto} '
                                    f'(primer sábado: {primer_sabado})'
                                )
                            )
                        else:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f'  + {operario.nombre:20} | Grupo {grupo_auto} '
                                    f'(primer sábado: {primer_sabado})'
                                )
                            )

                    logger.info(f'Asignado {operario} al grupo {grupo_auto} (primer sábado: {primer_sabado})')
                    total_asignados += 1

            except Exception as e:
                total_errores += 1
                self.stdout.write(
                    self.style.ERROR(f'  ✗ Error procesando {operario}: {str(e)}')
                )
                logger.error(f'Error asignando grupo para {operario}: {str(e)}')

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Procesados {operarios.count()} operarios:'
            )
        )
        self.stdout.write(f'   • {total_asignados} asignados/actualizados')
        self.stdout.write(f'   • {total_sin_registros} sin registros de sábados')
        if total_errores > 0:
            self.stdout.write(self.style.ERROR(f'   • {total_errores} errores'))

        if dry_run:
            self.stdout.write(
                self.style.WARNING('\n⚠️  Modo DRY-RUN: No se guardaron cambios')
            )
