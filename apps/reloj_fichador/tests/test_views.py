from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from ..models import Operario, Area, RegistroDiario
from datetime import datetime, timedelta
import json

class RegistroMovimientoViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Configuración inicial para todas las pruebas
        cls.area = Area.objects.create(nombre="Producción")
        cls.operario = Operario.objects.create(
            dni=12345678,
            nombre="Juan",
            apellido="Pérez",
            fecha_nacimiento="1985-05-15",
            fecha_ingreso_empresa="2010-08-01",
            activo=True
        )
        cls.operario.areas.add(cls.area)
        
        # Crear usuario para las pruebas de admin
        cls.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )

    def setUp(self):
        self.client = Client()
        # Limpiar registros diarios entre pruebas
        RegistroDiario.objects.all().delete()
    
    def test_registro_entrada_exitoso(self):
        """Prueba el registro exitoso de una entrada"""
        # Configurar datos para la solicitud
        data = {
            'dni': self.operario.dni,
            'tipo_movimiento': 'entrada'
        }
        
        # Simular solicitud AJAX
        response = self.client.post(
            reverse('reloj_fichador:registrar_movimiento_tipo', args=['entrada']),
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        # Verificar respuesta
        self.assertEqual(response.status_code, 200)
        
        # Parsear el JSON de respuesta
        content = json.loads(response.content.decode('utf-8'))
        self.assertTrue(content['success'])
        
        # Verificar que se creó el registro
        self.assertEqual(RegistroDiario.objects.count(), 1)
        registro = RegistroDiario.objects.first()
        self.assertEqual(registro.tipo_movimiento, 'entrada')
        self.assertEqual(registro.operario, self.operario)
    
    def test_registro_salida_despues_entrada(self):
        """Prueba el registro de salida después de una entrada"""
        # Crear primero un registro de entrada
        entrada = RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=timezone.now() - timedelta(hours=8),
            origen_fichada='Auto'
        )
        
        # Configurar datos para la solicitud
        data = {
            'dni': self.operario.dni,
            'tipo_movimiento': 'salida'
        }
        
        # Simular solicitud AJAX
        response = self.client.post(
            reverse('reloj_fichador:registrar_movimiento_tipo', args=['salida']),
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        # Verificar respuesta
        self.assertEqual(response.status_code, 200)
        
        # Parsear el JSON de respuesta
        content = json.loads(response.content.decode('utf-8'))
        self.assertTrue(content['success'])
        
        # Verificar que se creó el registro
        self.assertEqual(RegistroDiario.objects.count(), 2)
        salida = RegistroDiario.objects.last()
        self.assertEqual(salida.tipo_movimiento, 'salida')
    
    def test_registro_entrada_duplicada(self):
        """Prueba que detecta una inconsistencia al hacer doble entrada"""
        # Crear primero un registro de entrada
        entrada = RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=timezone.now() - timedelta(hours=1),
            origen_fichada='Auto'
        )
        
        # Configurar datos para la solicitud
        data = {
            'dni': self.operario.dni,
            'tipo_movimiento': 'entrada'
        }
        
        # Simular solicitud AJAX
        response = self.client.post(
            reverse('reloj_fichador:registrar_movimiento_tipo', args=['entrada']),
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        # Verificar respuesta (debería indicar inconsistencia)
        self.assertEqual(response.status_code, 400)
        
        # Parsear el JSON de respuesta
        content = json.loads(response.content.decode('utf-8'))
        self.assertFalse(content['success'])
        self.assertTrue(content['inconsistencia'])
    
    def test_registro_forzar_inconsistencia(self):
        """Prueba que se puede forzar un registro a pesar de inconsistencias"""
        # Crear primero un registro de entrada
        entrada = RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=timezone.now() - timedelta(hours=1),
            origen_fichada='Auto'
        )
        
        # Configurar datos para la solicitud (con override)
        data = {
            'dni': self.operario.dni,
            'tipo_movimiento': 'entrada',
            'inconsistency_override': 'True'
        }
        
        # Simular solicitud AJAX
        response = self.client.post(
            reverse('reloj_fichador:registrar_movimiento_tipo', args=['entrada']),
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        # Verificar respuesta (debería ser exitosa a pesar de inconsistencia)
        self.assertEqual(response.status_code, 200)
        
        # Parsear el JSON de respuesta
        content = json.loads(response.content.decode('utf-8'))
        self.assertTrue(content['success'])
        
        # Verificar que se creó el registro con inconsistencia
        self.assertEqual(RegistroDiario.objects.count(), 2)
        entrada2 = RegistroDiario.objects.last()
        self.assertEqual(entrada2.tipo_movimiento, 'entrada')
        self.assertTrue(entrada2.inconsistencia)
        self.assertTrue(entrada2.valido)  # Válido a pesar de inconsistencia
    
    def test_operario_no_encontrado(self):
        """Prueba que se maneja correctamente un DNI que no existe"""
        # Configurar datos para la solicitud con DNI inexistente
        data = {
            'dni': 99999999,  # DNI que no existe
            'tipo_movimiento': 'entrada'
        }
        
        # Simular solicitud AJAX
        response = self.client.post(
            reverse('reloj_fichador:registrar_movimiento_tipo', args=['entrada']),
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        # Verificar respuesta (debería indicar error)
        self.assertEqual(response.status_code, 404)
        
        # Parsear el JSON de respuesta
        content = json.loads(response.content.decode('utf-8'))
        self.assertFalse(content['success'])
        self.assertIn('OPERARIO NO ENCONTRADO', content['message'])
    
    def test_solicitud_no_ajax(self):
        """Prueba que rechaza solicitudes que no son AJAX"""
        # Configurar datos para la solicitud
        data = {
            'dni': self.operario.dni,
            'tipo_movimiento': 'entrada'
        }
        
        # Solicitud normal (no AJAX)
        response = self.client.post(
            reverse('reloj_fichador:registrar_movimiento_tipo', args=['entrada']),
            data
        )
        
        # Debería redirigir a la página principal
        self.assertEqual(response.status_code, 302)
        
        # Verificar que no se creó ningún registro
        self.assertEqual(RegistroDiario.objects.count(), 0)


class ReporteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Configuración inicial para todas las pruebas
        cls.area = Area.objects.create(nombre="Producción")
        cls.operario = Operario.objects.create(
            dni=12345678,
            nombre="Juan",
            apellido="Pérez",
            fecha_nacimiento="1985-05-15",
            fecha_ingreso_empresa="2010-08-01",
            activo=True
        )
        cls.operario.areas.add(cls.area)
        
        # Crear registros para pruebas
        for i in range(5):
            fecha = timezone.now() - timedelta(days=i)
            # Entrada del día
            RegistroDiario.objects.create(
                operario=cls.operario,
                tipo_movimiento='entrada',
                hora_fichada=fecha.replace(hour=8, minute=0),
                origen_fichada='Auto'
            )
            # Salida del día
            RegistroDiario.objects.create(
                operario=cls.operario,
                tipo_movimiento='salida',
                hora_fichada=fecha.replace(hour=17, minute=0),
                origen_fichada='Auto'
            )
        
        # Crear usuario para las pruebas de admin
        cls.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )

    def setUp(self):
        self.client = Client()
    
    def test_generar_reporte_view(self):
        """Prueba la generación de reportes desde la vista pública"""
        response = self.client.get(reverse('reloj_fichador:generar_reporte'))
        
        # Verificar que la respuesta es correcta
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reloj_fichador/reporte.html')
        
        # Verificar que se pasaron los registros al contexto
        self.assertIn('registros', response.context)
        
        # Verificar que solo se incluyen registros no inconsistentes
        registros_inconsistentes = RegistroDiario.objects.filter(inconsistencia=True)
        for registro in registros_inconsistentes:
            self.assertNotIn(registro, response.context['registros'])
    
    def test_admin_generar_reporte(self):
        """Prueba la generación de reportes desde el admin"""
        # Iniciar sesión como administrador
        self.client.login(username='admin', password='admin123')
        
        # Obtener IDs de los registros para pasarlos como parámetro
        ids = list(RegistroDiario.objects.values_list('id_registro', flat=True))
        
        # Construir URL para la acción de admin
        url = f"{reverse('admin:reloj_fichador_registrodiario_changelist')}?_selected_action={','.join(map(str, ids))}"
        
        # Enviar solicitud para generar reporte
        response = self.client.post(
            url,
            {'action': 'generar_reporte', 'post': 'yes'}
        )
        
        # Verificar que la respuesta es correcta
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reloj_fichador/reporte.html') 