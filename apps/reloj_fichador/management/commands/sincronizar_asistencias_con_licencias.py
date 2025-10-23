"""
Comando de management para sincronizar todos los registros de asistencia
basándose en licencias médicas aprobadas.

Uso:
    python manage.py sincronizar_asistencias_con_licencias
    python manage.py sincronizar_asistencias_con_licencias --operario=146
    python manage.py sincronizar_asistencias_con_licencias --mes=2025-06
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from apps.reloj_fichador.models import Operario, Licencia, RegistroAsistencia
import logging

logger = logging.getLogger('reloj_fichador')


class Command(BaseCommand):
    help = 'Sincroniza registros de asistencia con licencias médicas aprobadas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--operario',
            type=int,
            help='ID del operario a sincronizar (opcional)',
        )
        parser.add_argument(
            '--mes',
            type=str,
            help='Mes a sincronizar en formato YYYY-MM (opcional)',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Mostrar detalles del proceso',
        )

    def handle(self, *args, **options):
        verbose = options.get('verbose', False)
        operario_id = options.get('operario')
        mes = options.get('mes')

        self.stdout.write(
            self.style.SUCCESS('🔄 Iniciando sincronización de asistencias con licencias...\n')
        )

        # Obtener todas las licencias aprobadas
        licencias_query = Licencia.objects.filter(
            estado='aprobada',
            aplicar_a_asistencia=True,
            fecha_inicio__isnull=False,
            fecha_fin__isnull=False
        )

        if operario_id:
            licencias_query = licencias_query.filter(operario_id=operario_id)
            self.stdout.write(f"📌 Filtrando por operario ID: {operario_id}\n")

        if mes:
            try:
                mes_date = datetime.strptime(mes, '%Y-%m').date()
                licencias_query = licencias_query.filter(
                    fecha_inicio__year=mes_date.year,
                    fecha_inicio__month=mes_date.month
                )
                self.stdout.write(f"📌 Filtrando por mes: {mes}\n")
            except ValueError:
                self.stdout.write(
                    self.style.ERROR(f'❌ Formato de mes inválido: {mes}. Usar YYYY-MM\n')
                )
                return

        licencias = licencias_query.select_related('operario')

        total_licencias = licencias.count()
        self.stdout.write(f"📋 Licencias a procesar: {total_licencias}\n")

        if total_licencias == 0:
            self.stdout.write(self.style.WARNING('⚠️  No hay licencias que procesar\n'))
            return

        registros_creados = 0
        registros_actualizados = 0
        registros_con_error = 0

        for licencia in licencias:
            if verbose:
                self.stdout.write(
                    f"\n📄 Procesando licencia #{licencia.pk} "
                    f"({licencia.operario.nombre} {licencia.operario.apellido})"
                )
                self.stdout.write(
                    f"   Rango: {licencia.fecha_inicio} → {licencia.fecha_fin} "
                    f"({(licencia.fecha_fin - licencia.fecha_inicio).days + 1} días)"
                )

            fecha_actual = licencia.fecha_inicio
            dias_procesados_licencia = 0

            while fecha_actual <= licencia.fecha_fin:
                try:
                    registro_asistencia, created = RegistroAsistencia.objects.get_or_create(
                        operario=licencia.operario,
                        fecha=fecha_actual,
                        defaults={
                            'estado_asistencia': RegistroAsistencia.ausente,
                            'estado_justificacion': True,
                            'descripcion': f'Ausencia justificada por licencia (ID: {licencia.pk})',
                            'licencia_relacionada': licencia
                        }
                    )

                    if created:
                        registros_creados += 1
                        if verbose:
                            self.stdout.write(f"   ✓ CREADO: {fecha_actual}")
                    else:
                        # Si el registro existe pero no está justificado, actualizar
                        if not registro_asistencia.estado_justificacion:
                            registro_asistencia.estado_justificacion = True
                            registro_asistencia.licencia_relacionada = licencia
                            if not registro_asistencia.descripcion or 'licencia' not in registro_asistencia.descripcion.lower():
                                registro_asistencia.descripcion = f'Ausencia justificada por licencia (ID: {licencia.pk})'
                            registro_asistencia.save()
                            registros_actualizados += 1
                            if verbose:
                                self.stdout.write(f"   ✓ ACTUALIZADO: {fecha_actual}")
                        else:
                            if verbose:
                                self.stdout.write(f"   - YA JUSTIFICADO: {fecha_actual}")

                    dias_procesados_licencia += 1

                except Exception as e:
                    registros_con_error += 1
                    self.stdout.write(
                        self.style.ERROR(
                            f"   ❌ ERROR en {fecha_actual}: {str(e)}"
                        )
                    )
                    logger.error(f"Error procesando fecha {fecha_actual} para licencia {licencia.pk}: {e}")

                fecha_actual += timedelta(days=1)

            if verbose:
                self.stdout.write(
                    f"   Total de días procesados: {dias_procesados_licencia}"
                )

        # Resumen final
        self.stdout.write(self.style.SUCCESS('\n' + '='*70))
        self.stdout.write(self.style.SUCCESS('📊 RESUMEN DE SINCRONIZACIÓN:'))
        self.stdout.write(self.style.SUCCESS('='*70))
        self.stdout.write(f'  ✅ Registros creados: {registros_creados}')
        self.stdout.write(f'  ✅ Registros actualizados: {registros_actualizados}')
        self.stdout.write(f'  ❌ Registros con error: {registros_con_error}')
        self.stdout.write(f'  📋 Total procesado: {registros_creados + registros_actualizados}')
        self.stdout.write(self.style.SUCCESS('='*70 + '\n'))

        if registros_creados + registros_actualizados > 0:
            self.stdout.write(
                self.style.SUCCESS('✨ Sincronización completada exitosamente!\n')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️  No hubo cambios que realizar\n')
            )

        logger.info(
            f"Sincronización completada: {registros_creados} creados, "
            f"{registros_actualizados} actualizados, {registros_con_error} errores"
        )
