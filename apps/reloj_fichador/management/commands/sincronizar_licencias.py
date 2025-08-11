from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.reloj_fichador.models import Licencia, RegistroAsistencia
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Sincroniza licencias aprobadas existentes con el sistema de asistencia'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fecha-desde',
            type=str,
            help='Fecha desde la cual sincronizar (formato: YYYY-MM-DD). Por defecto: hace 30 días'
        )
        parser.add_argument(
            '--solo-reporte',
            action='store_true',
            help='Solo mostrar qué se haría, sin hacer cambios'
        )
        parser.add_argument(
            '--usar-celery',
            action='store_true',
            help='Usar Celery para procesamiento asíncrono (recomendado para muchas licencias)'
        )

    def handle(self, *args, **options):
        fecha_desde = options.get('fecha_desde')
        solo_reporte = options.get('solo_reporte', False)
        usar_celery = options.get('usar_celery', False)

        if fecha_desde:
            try:
                fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
            except ValueError:
                self.stdout.write(
                    self.style.ERROR('Formato de fecha inválido. Use YYYY-MM-DD')
                )
                return
        else:
            fecha_desde = (timezone.now().date() - timedelta(days=30))

        self.stdout.write(f'Sincronizando licencias desde: {fecha_desde}')
        if solo_reporte:
            self.stdout.write(self.style.WARNING('MODO REPORTE: No se harán cambios'))
        if usar_celery:
            self.stdout.write(self.style.SUCCESS('MODO CELERY: Procesamiento asíncrono activado'))

        # Buscar licencias aprobadas con fechas válidas
        licencias = Licencia.objects.filter(
            estado='aprobada',
            aplicar_a_asistencia=True,
            fecha_inicio__isnull=False,
            fecha_fin__isnull=False,
            fecha_fin__gte=fecha_desde
        ).select_related('operario')

        total_licencias = licencias.count()
        total_dias_procesados = 0
        total_ausencias_justificadas = 0

        self.stdout.write(f'Encontradas {total_licencias} licencias aprobadas para procesar')

        if usar_celery and not solo_reporte:
            # Modo Celery: Enviar tareas asíncronas
            from apps.reloj_fichador.tasks import sincronizar_licencia_historica
            
            for licencia in licencias:
                self.stdout.write(f'📤 Enviando licencia {licencia.pk} - {licencia.operario} a Celery')
                task = sincronizar_licencia_historica.delay(
                    licencia.pk, 
                    fecha_desde if fecha_desde >= licencia.fecha_inicio else licencia.fecha_inicio,
                    licencia.fecha_fin
                )
                self.stdout.write(f'  ✅ Task enviada: {task.task_id}')
                total_dias_procesados += licencia.duracion or 0
            
            self.stdout.write(self.style.SUCCESS(f'\\n📋 RESUMEN (Modo Celery):'))
            self.stdout.write(f'  • Licencias enviadas a Celery: {total_licencias}')
            self.stdout.write(f'  • Días estimados a procesar: {total_dias_procesados}')
            self.stdout.write(f'  • Verifique los logs de Celery para el progreso detallado')
            return

        # Modo síncrono tradicional
        for licencia in licencias:
            self.stdout.write(f'\\nProcesando licencia {licencia.pk} - {licencia.operario}')
            self.stdout.write(f'  Período: {licencia.fecha_inicio} al {licencia.fecha_fin}')
            
            fecha_actual = max(licencia.fecha_inicio, fecha_desde)
            dias_licencia = 0
            dias_justificados = 0

            while fecha_actual <= licencia.fecha_fin:
                dias_licencia += 1
                
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
                        if not solo_reporte:
                            self.stdout.write(f'    ✅ Creado registro de ausencia justificada para {fecha_actual}')
                        else:
                            self.stdout.write(f'    📝 Se crearía registro de ausencia justificada para {fecha_actual}')
                        dias_justificados += 1
                    else:
                        # Verificar si necesita actualización
                        necesita_actualizacion = False
                        if not registro_asistencia.estado_justificacion:
                            if not solo_reporte:
                                registro_asistencia.estado_justificacion = True
                                necesita_actualizacion = True
                            else:
                                self.stdout.write(f'    📝 Se marcaría como justificado: {fecha_actual}')
                                
                        if not registro_asistencia.licencia_relacionada:
                            if not solo_reporte:
                                registro_asistencia.licencia_relacionada = licencia
                                necesita_actualizacion = True
                                
                        if registro_asistencia.estado_asistencia != RegistroAsistencia.ausente:
                            # Si está presente, no debería estar justificado por licencia
                            if not solo_reporte:
                                registro_asistencia.licencia_relacionada = None
                                registro_asistencia.estado_justificacion = False
                                necesita_actualizacion = True
                            
                        if necesita_actualizacion and not solo_reporte:
                            registro_asistencia.save()
                            self.stdout.write(f'    🔄 Actualizado registro existente para {fecha_actual}')
                            dias_justificados += 1
                        elif not necesita_actualizacion:
                            self.stdout.write(f'    ℹ️  Ya procesado: {fecha_actual}')

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'    ❌ Error procesando {fecha_actual}: {e}')
                    )

                fecha_actual += timedelta(days=1)

            self.stdout.write(f'  📊 Licencia procesada: {dias_justificados}/{dias_licencia} días')
            total_dias_procesados += dias_licencia
            total_ausencias_justificadas += dias_justificados

        # Resumen final
        self.stdout.write(self.style.SUCCESS(f'\\n📋 RESUMEN:'))
        self.stdout.write(f'  • Licencias procesadas: {total_licencias}')
        self.stdout.write(f'  • Días totales procesados: {total_dias_procesados}')
        self.stdout.write(f'  • Ausencias justificadas: {total_ausencias_justificadas}')
        
        if solo_reporte:
            self.stdout.write(self.style.WARNING('\\n⚠️  Ejecute sin --solo-reporte para aplicar los cambios'))
        else:
            self.stdout.write(self.style.SUCCESS('\\n✅ Sincronización completada'))