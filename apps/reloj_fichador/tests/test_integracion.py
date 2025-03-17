from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta, date
from ..models import (
    Operario, Area, RegistroDiario, Horas_trabajadas, 
    Horas_extras, Horas_feriado, Horas_totales, RegistroAsistencia
)

class IntegracionTest(TestCase):
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
        
        # Crear segundo operario para comparación
        cls.operario2 = Operario.objects.create(
            dni=87654321,
            nombre="María",
            apellido="Gómez",
            fecha_nacimiento="1990-03-20",
            fecha_ingreso_empresa="2015-05-10",
            activo=True
        )
        cls.operario2.areas.add(cls.area)
        
        # Definir fecha base para pruebas
        cls.hoy = timezone.now().date()
        cls.inicio_mes = date(cls.hoy.year, cls.hoy.month, 1)
    
    def crear_registros_mes_completo(self, operario, dias_trabajados=20, horas_por_dia=8, 
                             hora_entrada=9, minutos_entrada=0, hora_salida=17, minutos_salida=0,
                             incluir_nocturno=False, incluir_horas_extras=False):
        """Crea registros de entrada y salida para un mes completo"""
        for dia in range(1, dias_trabajados + 1):
            fecha_trabajo = self.inicio_mes + timedelta(days=dia-1)
            
            # Si es fin de semana, saltar
            if fecha_trabajo.weekday() >= 5:  # 5=sábado, 6=domingo
                continue
                
            # Determinar horas según parámetros
            if incluir_nocturno and dia % 5 == 0:  # Cada 5 días, turno nocturno
                dt_entrada = datetime.combine(fecha_trabajo, time(22, 0))
                dt_salida = datetime.combine(fecha_trabajo + timedelta(days=1), time(6, 0))
            else:
                # Turno normal
                dt_entrada = datetime.combine(fecha_trabajo, time(hora_entrada, minutos_entrada))
                # Añadir horas extras algunos días
                if incluir_horas_extras and dia % 3 == 0:  # Cada 3 días
                    dt_salida = datetime.combine(fecha_trabajo, time(hora_salida + 2, minutos_salida))
                else:
                    dt_salida = datetime.combine(fecha_trabajo, time(hora_salida, minutos_salida))
            
            # Crear registros
            RegistroDiario.objects.create(
                operario=operario,
                tipo_movimiento='entrada',
                hora_fichada=timezone.make_aware(dt_entrada),
                origen_fichada='Auto'
            )
            
            RegistroDiario.objects.create(
                operario=operario,
                tipo_movimiento='salida',
                hora_fichada=timezone.make_aware(dt_salida),
                origen_fichada='Auto'
            )
    
    def test_calculo_horas_totales_mes(self):
        """Prueba el cálculo de horas totales para un mes completo"""
        # Crear registros para un mes
        self.crear_registros_mes_completo(
            self.operario, 
            dias_trabajados=20,  # 20 días laborables
            incluir_nocturno=True,  # Algunos turnos nocturnos
            incluir_horas_extras=True  # Algunas horas extras
        )
        
        # Calcular horas trabajadas para cada día
        fechas_trabajadas = set()
        for registro in RegistroDiario.objects.filter(operario=self.operario):
            fecha_logica = RegistroDiario.calcular_fecha_logica(registro.hora_fichada)
            fechas_trabajadas.add(fecha_logica)
        
        for fecha in fechas_trabajadas:
            Horas_trabajadas.calcular_horas_trabajadas(self.operario, fecha)
            Horas_extras.calcular_horas_extras(self.operario, fecha)
        
        # Calcular horas totales del mes
        mes_str = self.inicio_mes.strftime('%Y-%m')
        horas_totales = Horas_totales.calcular_horas_totales(self.operario, mes_str)
        
        # Verificar que se calcularon las horas correctamente
        self.assertIsNotNone(horas_totales)
        self.assertGreater(horas_totales.horas_normales, timedelta(0))
        
        # Verificar que hay horas nocturnas (creamos algunos turnos nocturnos)
        self.assertGreater(horas_totales.horas_nocturnas, timedelta(0))
        
        # Verificar que hay horas extras (creamos algunos días con horas extras)
        self.assertGreater(horas_totales.horas_extras, timedelta(0))
    
    def test_verificacion_asistencia(self):
        """Prueba el sistema de verificación de asistencia"""
        # Crear un registro de asistencia sin fichadas
        registro_asistencia = RegistroAsistencia.objects.create(
            operario=self.operario,
            fecha=self.hoy
        )
        
        # Por defecto, debería estar marcado como ausente
        self.assertEqual(registro_asistencia.estado_asistencia, 'ausente')
        
        # Crear una fichada de entrada para hoy
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=timezone.make_aware(datetime.combine(self.hoy, time(8, 0))),
            origen_fichada='Auto'
        )
        
        # Verificar asistencia
        registro_asistencia.verificar_asistencia()
        
        # Ahora debería estar marcado como presente
        self.assertEqual(registro_asistencia.estado_asistencia, 'presente')
    
    def test_horas_feriado(self):
        """Prueba el registro y cálculo de horas en día feriado"""
        # Marcar un día como feriado y crear registros
        dia_feriado = self.inicio_mes + timedelta(days=5)  # El día 6 del mes
        
        # Crear fichadas para ese día
        dt_entrada = datetime.combine(dia_feriado, time(9, 0))
        dt_salida = datetime.combine(dia_feriado, time(17, 0))
        
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=timezone.make_aware(dt_entrada),
            origen_fichada='Auto'
        )
        
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='salida',
            hora_fichada=timezone.make_aware(dt_salida),
            origen_fichada='Auto'
        )
        
        # Calcular horas trabajadas
        Horas_trabajadas.calcular_horas_trabajadas(self.operario, dia_feriado)
        
        # Registrar horas de feriado (simulando que la aplicación lo marcó como feriado)
        horas_feriado = Horas_feriado.sumar_horas_feriado(self.operario, dia_feriado, es_feriado=True)
        
        # Verificar que se registraron 8 horas de feriado
        self.assertEqual(horas_feriado, timedelta(hours=8))
        
        # Calcular horas totales del mes
        mes_str = self.inicio_mes.strftime('%Y-%m')
        horas_totales = Horas_totales.calcular_horas_totales(self.operario, mes_str)
        
        # Verificar que las horas de feriado se sumaron correctamente
        self.assertEqual(horas_totales.horas_feriado, timedelta(hours=8))
    
    def test_comparacion_horas_operarios(self):
        """Prueba que el cálculo de horas es correcto comparando dos operarios con patrones diferentes"""
        # Operario 1: Trabajo normal de 9 a 17 horas
        self.crear_registros_mes_completo(
            self.operario, 
            dias_trabajados=20,
            hora_entrada=9, 
            hora_salida=17,
            incluir_horas_extras=False
        )
        
        # Operario 2: Trabajo con horas extras 
        self.crear_registros_mes_completo(
            self.operario2, 
            dias_trabajados=20,
            hora_entrada=9, 
            hora_salida=19,  # 2 horas extra diarias
            incluir_horas_extras=True
        )
        
        # Calcular horas para ambos operarios
        fechas_trabajadas = set()
        for registro in RegistroDiario.objects.all():
            fecha_logica = RegistroDiario.calcular_fecha_logica(registro.hora_fichada)
            fechas_trabajadas.add((registro.operario, fecha_logica))
        
        for operario, fecha in fechas_trabajadas:
            Horas_trabajadas.calcular_horas_trabajadas(operario, fecha)
            Horas_extras.calcular_horas_extras(operario, fecha)
        
        # Calcular horas totales del mes
        mes_str = self.inicio_mes.strftime('%Y-%m')
        horas_totales1 = Horas_totales.calcular_horas_totales(self.operario, mes_str)
        horas_totales2 = Horas_totales.calcular_horas_totales(self.operario2, mes_str)
        
        # El operario 2 debe tener más horas totales (normales + extras)
        total_op1 = horas_totales1.horas_normales + horas_totales1.horas_extras
        total_op2 = horas_totales2.horas_normales + horas_totales2.horas_extras
        
        self.assertGreater(total_op2, total_op1)
        self.assertGreater(horas_totales2.horas_extras, horas_totales1.horas_extras) 