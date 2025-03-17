from django.test import TestCase
from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from ..models import Operario, Area, RegistroDiario

def safe_datetime(year, month, day, hour=0, minute=0, second=0):
    """Crea un datetime compatible con la configuración actual de USE_TZ"""
    dt = datetime(year, month, day, hour, minute, second)
    if getattr(settings, 'USE_TZ', False):
        return timezone.make_aware(dt)
    return dt

class RegistroDiarioModelTest(TestCase):
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
        
        # Hora de referencia para las pruebas (para evitar problemas con horarios nocturnos)
        cls.hora_base = safe_datetime(2023, 1, 1, 9, 0, 0)

    def test_registro_entrada_valido(self):
        """Prueba que se puede crear un registro de entrada válido"""
        registro = RegistroDiario(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=self.hora_base,
            origen_fichada='Auto'
        )
        registro.full_clean()  # No debería lanzar excepción
        registro.save()
        
        self.assertEqual(registro.tipo_movimiento, 'entrada')
        self.assertEqual(registro.operario.dni, 12345678)
        
    def test_secuencia_movimientos_valida(self):
        """Prueba que la secuencia entrada -> salida es válida"""
        # Creamos registro de entrada
        entrada = RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=self.hora_base,
            origen_fichada='Auto'
        )
        
        # Creamos registro de salida (2 horas después)
        salida = RegistroDiario(
            operario=self.operario,
            tipo_movimiento='salida',
            hora_fichada=self.hora_base + timedelta(hours=2),
            origen_fichada='Auto'
        )
        salida.full_clean()  # No debería lanzar excepción
        salida.save()
        
        self.assertEqual(RegistroDiario.objects.count(), 2)
        
    def test_secuencia_movimientos_invalida(self):
        """Prueba que una secuencia inválida (entrada -> entrada) lanza ValidationError"""
        # Creamos registro de entrada
        entrada1 = RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=self.hora_base,
            origen_fichada='Auto'
        )
        
        # Intentamos crear otro registro de entrada (debería fallar)
        entrada2 = RegistroDiario(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=self.hora_base + timedelta(hours=1),
            origen_fichada='Auto'
        )
        
        with self.assertRaises(ValidationError):
            entrada2.full_clean()
            
    def test_secuencia_movimientos_salida_transitoria(self):
        """Prueba la secuencia entrada -> salida_transitoria -> entrada_transitoria -> salida"""
        # Creamos registro de entrada
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=self.hora_base,
            origen_fichada='Auto'
        )
        
        # Creamos registro de salida transitoria (1 hora después)
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='salida_transitoria',
            hora_fichada=self.hora_base + timedelta(hours=1),
            origen_fichada='Auto'
        )
        
        # Creamos registro de entrada transitoria (2 horas después)
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada_transitoria',
            hora_fichada=self.hora_base + timedelta(hours=2),
            origen_fichada='Auto'
        )
        
        # Creamos registro de salida final (3 horas después)
        salida = RegistroDiario(
            operario=self.operario,
            tipo_movimiento='salida',
            hora_fichada=self.hora_base + timedelta(hours=3),
            origen_fichada='Auto'
        )
        salida.full_clean()
        salida.save()
        
        self.assertEqual(RegistroDiario.objects.count(), 4)
    
    def test_registro_fecha_logica(self):
        """Prueba el cálculo de fecha lógica, especialmente para turnos nocturnos"""
        # Hora nocturna (4 AM)
        hora_nocturna = safe_datetime(2023, 1, 2, 4, 0, 0)
        
        fecha_logica = RegistroDiario.calcular_fecha_logica(hora_nocturna)
        
        # Debería considerar que pertenece al día anterior (1 de enero)
        self.assertEqual(fecha_logica, datetime(2023, 1, 1).date())
        
        # Hora diurna (10 AM)
        hora_diurna = safe_datetime(2023, 1, 2, 10, 0, 0)
        
        fecha_logica = RegistroDiario.calcular_fecha_logica(hora_diurna)
        
        # Debería mantener la fecha actual (2 de enero)
        self.assertEqual(fecha_logica, datetime(2023, 1, 2).date())

    def test_forzar_registro_inconsistente(self):
        """Prueba que se puede forzar un registro inconsistente marcándolo como tal"""
        # Creamos registro de entrada
        entrada1 = RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=self.hora_base,
            origen_fichada='Auto'
        )
        
        # Intentamos crear otro registro de entrada
        # Normalmente fallaría, pero forzamos el registro
        entrada2 = RegistroDiario(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=self.hora_base + timedelta(hours=1),
            origen_fichada='Auto',
            inconsistencia=True,  # Marcamos como inconsistencia
            descripcion_inconsistencia="Entrada duplicada forzada para pruebas"
        )
        
        # No debería lanzar excepción porque estamos forzando la inconsistencia
        entrada2.full_clean()
        entrada2.save()
        
        self.assertEqual(RegistroDiario.objects.count(), 2)
        self.assertTrue(RegistroDiario.objects.filter(inconsistencia=True).exists()) 