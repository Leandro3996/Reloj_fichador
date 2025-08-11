from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.reloj_fichador.models import Licencia, RegistroAsistencia, Operario
from datetime import date, timedelta
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Prueba la funcionalidad de integración de licencias con asistencia'

    def add_arguments(self, parser):
        parser.add_argument(
            '--operario-dni',
            type=str,
            required=True,
            help='DNI del operario para la prueba'
        )

    def handle(self, *args, **options):
        dni_operario = options['operario_dni']
        
        try:
            operario = Operario.objects.get(dni=dni_operario)
        except Operario.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'No se encontró operario con DNI {dni_operario}'))
            return

        # Crear fechas para la prueba (desde ayer hasta mañana)
        hoy = timezone.now().date()
        fecha_inicio = hoy - timedelta(days=1)  # Ayer
        fecha_fin = hoy + timedelta(days=1)     # Mañana

        self.stdout.write(f'🧪 PRUEBA DE LICENCIA PARA: {operario}')
        self.stdout.write(f'📅 Período: {fecha_inicio} al {fecha_fin}')

        # Paso 1: Verificar estado inicial de asistencia
        self.stdout.write('\\n1️⃣ VERIFICANDO ESTADO INICIAL:')
        for fecha in [fecha_inicio, hoy, fecha_fin]:
            try:
                registro = RegistroAsistencia.objects.get(operario=operario, fecha=fecha)
                justif = "✅ Justificado" if registro.estado_justificacion else "❌ No justificado"
                licencia_info = f" (Licencia: {registro.licencia_relacionada.pk})" if registro.licencia_relacionada else ""
                self.stdout.write(f'  {fecha}: {registro.get_estado_asistencia_display()} - {justif}{licencia_info}')
            except RegistroAsistencia.DoesNotExist:
                self.stdout.write(f'  {fecha}: Sin registro de asistencia')

        # Paso 2: Crear licencia médica de prueba
        self.stdout.write('\\n2️⃣ CREANDO LICENCIA DE PRUEBA:')
        
        # Buscar un usuario admin para asignar como aprobador
        try:
            usuario_admin = User.objects.filter(is_superuser=True).first()
        except:
            usuario_admin = None
            
        licencia = Licencia.objects.create(
            operario=operario,
            descripcion='Licencia médica de prueba - comando probar_licencia',
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado='pendiente',
            aplicar_a_asistencia=True
        )
        
        self.stdout.write(f'  ✅ Licencia creada: ID {licencia.pk} - Estado: {licencia.estado}')

        # Paso 3: Aprobar la licencia (esto debería disparar Celery)
        self.stdout.write('\\n3️⃣ APROBANDO LICENCIA:')
        licencia.estado = 'aprobada'
        licencia.aprobada_por = usuario_admin
        licencia.save()  # Esto debería disparar procesar_licencia_aprobada.delay()
        
        self.stdout.write(f'  ✅ Licencia aprobada: ID {licencia.pk}')
        self.stdout.write(f'  📤 Tarea Celery enviada (verificar logs de Celery)')

        # Paso 4: Esperar un poco y verificar resultados
        self.stdout.write('\\n4️⃣ ESPERANDO PROCESAMIENTO (5 segundos)...')
        import time
        time.sleep(5)

        # Paso 5: Verificar estado final
        self.stdout.write('\\n5️⃣ VERIFICANDO RESULTADOS:')
        cambios_detectados = 0
        
        for fecha in [fecha_inicio, hoy, fecha_fin]:
            try:
                registro = RegistroAsistencia.objects.get(operario=operario, fecha=fecha)
                justif = "✅ Justificado" if registro.estado_justificacion else "❌ No justificado"
                licencia_info = f" (Licencia: {registro.licencia_relacionada.pk})" if registro.licencia_relacionada else ""
                
                if registro.estado_justificacion and registro.licencia_relacionada == licencia:
                    cambios_detectados += 1
                    self.stdout.write(self.style.SUCCESS(f'  ✅ {fecha}: {registro.get_estado_asistencia_display()} - {justif}{licencia_info}'))
                else:
                    self.stdout.write(f'  ⚠️  {fecha}: {registro.get_estado_asistencia_display()} - {justif}{licencia_info}')
                    
            except RegistroAsistencia.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'  ❌ {fecha}: Sin registro de asistencia creado'))

        # Resultado final
        self.stdout.write(f'\\n📊 RESUMEN:')
        if cambios_detectados == 3:
            self.stdout.write(self.style.SUCCESS('🎉 ¡ÉXITO! La integración funciona correctamente'))
        elif cambios_detectados > 0:
            self.stdout.write(self.style.WARNING(f'⚠️  PARCIAL: {cambios_detectados}/3 días procesados'))
        else:
            self.stdout.write(self.style.ERROR('❌ FALLO: No se procesó ningún día'))
            self.stdout.write('🔍 Verificar:')
            self.stdout.write('  - Logs de Celery: docker compose logs celery')
            self.stdout.write('  - Worker funcionando: docker compose ps')
            self.stdout.write('  - Redis conectado: docker compose logs redis')

        self.stdout.write(f'\\n🔧 LIMPIEZA:')
        self.stdout.write(f'Licencia de prueba ID {licencia.pk} creada (puedes eliminarla manualmente si quieres)')