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
        """Prueba el redondeo de hora de entrada a la media hora más cercana"""
        # Caso 1: Sin minutos (no debe redondear)
        hora_exacta = timezone.make_aware(datetime(2023, 1, 1, 8, 0, 0))
        redondeada = redondear_entrada(hora_exacta)
        self.assertEqual(redondeada, hora_exacta)
        
        # Caso 2: Con minutos < 15 (debe redondear hacia abajo)
        hora_con_minutos = timezone.make_aware(datetime(2023, 1, 1, 8, 13, 0))
        redondeada = redondear_entrada(hora_con_minutos)
        expected = timezone.make_aware(datetime(2023, 1, 1, 8, 0, 0))
        self.assertEqual(redondeada, expected)
        
        # Caso 3: Con minutos entre 15 y 44 (debe redondear a media hora)
        hora_con_minutos = timezone.make_aware(datetime(2023, 1, 1, 8, 16, 0))
        redondeada = redondear_entrada(hora_con_minutos)
        expected = timezone.make_aware(datetime(2023, 1, 1, 8, 30, 0))
        self.assertEqual(redondeada, expected)
        
        # Caso 4: Con minutos >= 45 (debe redondear hacia arriba)
        hora_con_minutos = timezone.make_aware(datetime(2023, 1, 1, 8, 46, 0))
        redondeada = redondear_entrada(hora_con_minutos)
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


class CalculoHorasEnfermedadTest(TestCase):
    """Tests para la función calcular_horas_enfermedad_laborales()"""

    @classmethod
    def setUpTestData(cls):
        from ..models import CalendarioLaboral
        # Crear feriado para pruebas (31 de Octubre 2025 - Día de Difuntos)
        cls.feriado_octubre = CalendarioLaboral.objects.create(
            fecha=datetime(2025, 10, 31).date(),
            tipo_dia='feriado',
            nombre='Día de Difuntos'
        )

        # Crear feriado para pruebas (1 de Mayo 2025 - Día del Trabajo)
        cls.feriado_mayo = CalendarioLaboral.objects.create(
            fecha=datetime(2025, 5, 1).date(),
            tipo_dia='feriado',
            nombre='Día del Trabajo'
        )

    def test_horas_enfermedad_licencia_lunes_viernes(self):
        """
        Licencia de 5 días (Lun-Vie) sin domingos ni feriados.
        Debe contar 5 días × 8h = 40 horas.
        """
        from ..utils import calcular_horas_enfermedad_laborales

        # Licencia: Oct 27-31, 2025 (Lun-Vie)
        # Oct 31 está marcado como feriado en setUpTestData
        fecha_inicio = datetime(2025, 10, 27).date()  # Lunes
        fecha_fin = datetime(2025, 10, 31).date()      # Viernes (es feriado)

        dias_laborales, horas = calcular_horas_enfermedad_laborales(fecha_inicio, fecha_fin)

        # Oct 31 es feriado, así que solo contar Lun 27, Mar 28, Mié 29, Jue 30 = 4 días
        self.assertEqual(dias_laborales, 4)
        self.assertEqual(horas, timedelta(hours=32))

    def test_horas_enfermedad_excluye_domingos(self):
        """
        Licencia que incluye domingo.
        Debe excluir domingos (no contar como día laboral).

        Caso: Oct 25-31, 2025 (Sab-Vie)
        - Sábado 25: laboral (sin operario, se considera laboral)
        - Domingo 26: no laboral
        - Lun 27: laboral
        - Mar 28: laboral
        - Mié 29: laboral
        - Jue 30: laboral
        - Vie 31: feriado (no laboral)
        Resultado: 5 días laborales (Sab 25, Lun 27, Mar 28, Mié 29, Jue 30) = 40 horas
        """
        from ..utils import calcular_horas_enfermedad_laborales

        fecha_inicio = datetime(2025, 10, 25).date()  # Sábado
        fecha_fin = datetime(2025, 10, 31).date()     # Viernes (es feriado)

        dias_laborales, horas = calcular_horas_enfermedad_laborales(fecha_inicio, fecha_fin)

        # Contar: Sab 25, Lun 27, Mar 28, Mié 29, Jue 30 (5 días)
        # Excluir: Domingo 26, Feriado 31
        self.assertEqual(dias_laborales, 5)
        self.assertEqual(horas, timedelta(hours=40))

    def test_horas_enfermedad_excluye_feriados(self):
        """
        Licencia que incluye feriado nacional (Día del Trabajo).
        Debe excluir el feriado del cálculo.

        Caso: Apr 30 - May 5, 2025
        - Mié 30 Abr: laboral
        - Jue 1 May: FERIADO (Día del Trabajo)
        - Vie 2 May: laboral
        - Sáb 3 May: laboral (sin operario, se considera laboral)
        - Dom 4 May: no laboral
        - Lun 5 May: laboral
        Resultado: 4 días laborales (Mié 30, Vie 2, Sáb 3, Lun 5) = 32 horas
        """
        from ..utils import calcular_horas_enfermedad_laborales

        fecha_inicio = datetime(2025, 4, 30).date()
        fecha_fin = datetime(2025, 5, 5).date()

        dias_laborales, horas = calcular_horas_enfermedad_laborales(fecha_inicio, fecha_fin)

        # Contar: Mié 30, Vie 2, Sáb 3, Lun 5 (4 días)
        # Excluir: Feriado 1, Domingo 4
        self.assertEqual(dias_laborales, 4)
        self.assertEqual(horas, timedelta(hours=32))

    def test_horas_enfermedad_licencia_larga(self):
        """
        Licencia de 30 días que incluye múltiples domingos y feriados.
        Debe contar solo días laborales de lunes a viernes.

        Caso: Octubre 2025 completo (31 días)
        - Domingos: 5, 12, 19, 26 (4 domingos)
        - Feriado: 31 (Día de Difuntos)
        - Días laborales esperados: 31 - 4 domingos - 1 feriado = 26 días
        """
        from ..utils import calcular_horas_enfermedad_laborales

        fecha_inicio = datetime(2025, 10, 1).date()
        fecha_fin = datetime(2025, 10, 31).date()

        dias_laborales, horas = calcular_horas_enfermedad_laborales(fecha_inicio, fecha_fin)

        # Octubre 2025: 31 días totales
        # Domingos: 5, 12, 19, 26 (4 días)
        # Feriado (31): 1 día
        # Laborales: 31 - 4 - 1 = 26 días
        self.assertEqual(dias_laborales, 26)
        self.assertEqual(horas, timedelta(hours=208))

    def test_horas_enfermedad_un_solo_dia(self):
        """
        Licencia de un solo día (laboral).
        Debe contar 1 día = 8 horas.
        """
        from ..utils import calcular_horas_enfermedad_laborales

        # Lunes 27 de Octubre 2025
        fecha = datetime(2025, 10, 27).date()

        dias_laborales, horas = calcular_horas_enfermedad_laborales(fecha, fecha)

        self.assertEqual(dias_laborales, 1)
        self.assertEqual(horas, timedelta(hours=8))

    def test_horas_enfermedad_solo_domingos(self):
        """
        Licencia que abarca sábado y domingo.
        Debe contar 1 día laboral (sábado, sin operario asignado se considera laboral).
        """
        from ..utils import calcular_horas_enfermedad_laborales

        # Sábado 25 - Domingo 26 de Octubre 2025
        fecha_inicio = datetime(2025, 10, 25).date()
        fecha_fin = datetime(2025, 10, 26).date()

        dias_laborales, horas = calcular_horas_enfermedad_laborales(fecha_inicio, fecha_fin)

        # Sin operario asignado, sábado se considera laboral
        # Domingo 26 siempre es no laboral
        self.assertEqual(dias_laborales, 1)
        self.assertEqual(horas, timedelta(hours=8)) 