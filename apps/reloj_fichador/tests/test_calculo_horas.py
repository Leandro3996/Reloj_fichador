from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta, time
from ..models import (
    Operario, Area, RegistroDiario, Horas_trabajadas, 
    redondear_entrada, redondear_salida, calcular_horas_por_franjas
)

class CalculoHorasTest(TestCase):
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
        
        # Fecha base para las pruebas
        cls.fecha_base = timezone.make_aware(datetime(2023, 1, 1))

    def test_redondeo_entrada(self):
        """Prueba el redondeo de hora de entrada hacia arriba"""
        # Caso 1: Sin minutos (no debe redondear)
        hora_exacta = timezone.make_aware(datetime(2023, 1, 1, 8, 0, 0))
        redondeada = redondear_entrada(hora_exacta)
        self.assertEqual(redondeada, hora_exacta)
        
        # Caso 2: Con minutos (debe redondear hacia la próxima hora)
        hora_con_minutos = timezone.make_aware(datetime(2023, 1, 1, 8, 15, 0))
        redondeada = redondear_entrada(hora_con_minutos)
        expected = timezone.make_aware(datetime(2023, 1, 1, 9, 0, 0))
        self.assertEqual(redondeada, expected)
        
        # Caso 3: Con segundos (debe redondear hacia la próxima hora)
        hora_con_segundos = timezone.make_aware(datetime(2023, 1, 1, 8, 0, 30))
        redondeada = redondear_entrada(hora_con_segundos)
        expected = timezone.make_aware(datetime(2023, 1, 1, 9, 0, 0))
        self.assertEqual(redondeada, expected)
    
    def test_redondeo_salida(self):
        """Prueba el redondeo de hora de salida hacia abajo"""
        # Caso 1: Sin minutos (no debe redondear)
        hora_exacta = timezone.make_aware(datetime(2023, 1, 1, 17, 0, 0))
        redondeada = redondear_salida(hora_exacta)
        self.assertEqual(redondeada, hora_exacta)
        
        # Caso 2: Con minutos (debe redondear hacia la hora anterior)
        hora_con_minutos = timezone.make_aware(datetime(2023, 1, 1, 17, 45, 0))
        redondeada = redondear_salida(hora_con_minutos)
        expected = timezone.make_aware(datetime(2023, 1, 1, 17, 0, 0))
        self.assertEqual(redondeada, expected)
    
    def test_calculo_horas_normales_diurnas(self):
        """Prueba el cálculo de horas en un turno diurno normal"""
        # Horario normal de 9 AM a 5 PM
        inicio = timezone.make_aware(datetime(2023, 1, 1, 9, 0, 0))
        fin = timezone.make_aware(datetime(2023, 1, 1, 17, 0, 0))
        
        horas_normales, horas_nocturnas = calcular_horas_por_franjas(inicio, fin)
        
        # Debería ser 8 horas normales y 0 nocturnas
        self.assertEqual(horas_normales, timedelta(hours=8))
        self.assertEqual(horas_nocturnas, timedelta(hours=0))
    
    def test_calculo_horas_nocturnas(self):
        """Prueba el cálculo de horas en un turno nocturno"""
        # Horario nocturno de 10 PM a 6 AM del día siguiente
        inicio = timezone.make_aware(datetime(2023, 1, 1, 22, 0, 0))
        fin = timezone.make_aware(datetime(2023, 1, 2, 6, 0, 0))
        
        horas_normales, horas_nocturnas = calcular_horas_por_franjas(inicio, fin)
        
        # Debería ser 0 horas normales y 8 nocturnas
        self.assertEqual(horas_normales, timedelta(hours=0))
        self.assertEqual(horas_nocturnas, timedelta(hours=8))
    
    def test_calculo_horas_mixtas(self):
        """Prueba el cálculo de horas en un turno mixto (diurno y nocturno)"""
        # Horario mixto de 6 PM a 12 AM
        inicio = timezone.make_aware(datetime(2023, 1, 1, 18, 0, 0))
        fin = timezone.make_aware(datetime(2023, 1, 2, 0, 0, 0))
        
        horas_normales, horas_nocturnas = calcular_horas_por_franjas(inicio, fin)
        
        # Debería tener horas normales (18:00-20:00) y nocturnas (20:00-00:00)
        self.assertEqual(horas_normales, timedelta(hours=2))
        self.assertEqual(horas_nocturnas, timedelta(hours=4))
    
    def test_integracion_registro_calculo_horas(self):
        """Prueba la integración entre registros y cálculo de horas"""
        # Crear registros de entrada y salida para un día
        fecha = datetime(2023, 1, 1).date()
        
        # Entrada a las 8:15 AM (se redondea a 9:00 AM)
        entrada = RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=timezone.make_aware(datetime(2023, 1, 1, 8, 15, 0)),
            origen_fichada='Auto'
        )
        
        # Salida a las 5:45 PM 
        salida = RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='salida',
            hora_fichada=timezone.make_aware(datetime(2023, 1, 1, 17, 45, 0)),
            origen_fichada='Auto'
        )
        
        # Calcular horas trabajadas
        horas_normales, horas_nocturnas, horas_extras = Horas_trabajadas.calcular_horas_trabajadas(
            self.operario, fecha
        )
        
        # Verificar resultados:
        # Entrada redondeada: 9:00 AM
        # Salida: 5:45 PM
        # Total: 8 horas 45 minutos 
        # Como > 8.5h, se considera que hay horas extras (15 min)
        self.assertEqual(horas_normales, timedelta(hours=8))  # 8 horas normales
        self.assertEqual(horas_nocturnas, timedelta(hours=0))  # 0 horas nocturnas
        self.assertEqual(horas_extras, timedelta(minutes=15))  # 15 minutos extras
        
    def test_calculo_horas_sin_registros(self):
        """Prueba el cálculo de horas cuando no hay registros"""
        fecha = datetime(2023, 1, 1).date()
        
        # Calcular horas trabajadas sin registros
        horas_normales, horas_nocturnas, horas_extras = Horas_trabajadas.calcular_horas_trabajadas(
            self.operario, fecha
        )
        
        # No debería haber horas registradas
        self.assertEqual(horas_normales, timedelta(hours=0))
        self.assertEqual(horas_nocturnas, timedelta(hours=0))
        self.assertEqual(horas_extras, timedelta(hours=0))
    
    def test_calculo_horas_registros_desequilibrados(self):
        """Prueba el cálculo con registros desequilibrados (ej. solo entrada sin salida)"""
        fecha = datetime(2023, 1, 1).date()
        
        # Solo crear registro de entrada
        entrada = RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=timezone.make_aware(datetime(2023, 1, 1, 8, 0, 0)),
            origen_fichada='Auto'
        )
        
        # Calcular horas trabajadas 
        horas_normales, horas_nocturnas, horas_extras = Horas_trabajadas.calcular_horas_trabajadas(
            self.operario, fecha
        )
        
        # No debería haber horas registradas ya que no hay par entrada-salida
        self.assertEqual(horas_normales, timedelta(hours=0))
        self.assertEqual(horas_nocturnas, timedelta(hours=0))
        self.assertEqual(horas_extras, timedelta(hours=0)) 