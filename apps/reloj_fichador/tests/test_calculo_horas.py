from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta, time
from ..models import (
    Operario, Area, RegistroDiario, Horas_trabajadas, GrupoSabado,
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


class SaturdayGroupDetectionTest(TestCase):
    """Tests para la detección automática de grupos de sábado desde RegistroDiario"""

    @classmethod
    def setUpTestData(cls):
        from datetime import datetime, timedelta
        import pytz

        argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')

        # Crear área de prueba
        area = Area.objects.create(nombre='Test Area')

        # Crear operarios de prueba
        cls.operario1 = Operario.objects.create(
            nombre='Juan',
            apellido='Pérez',
            dni=10000001
        )
        cls.operario1.areas.add(area)

        cls.operario2 = Operario.objects.create(
            nombre='María',
            apellido='García',
            dni=10000002
        )
        cls.operario2.areas.add(area)

        # Operario sin registros de sábados
        cls.operario3 = Operario.objects.create(
            nombre='Carlos',
            apellido='López',
            dni=10000003
        )
        cls.operario3.areas.add(area)

        # Crear registros de sábados para operario1
        # Primer sábado del sistema (2025-04-05, índice 0, Grupo A)
        from apps.reloj_fichador.utils import suppress_signal

        cls.primer_sabado = datetime(2025, 4, 5, 8, 0, tzinfo=argentina_tz)
        with suppress_signal():
            RegistroDiario.objects.create(
                operario=cls.operario1,
                hora_fichada=cls.primer_sabado,
                tipo_movimiento='entrada',
                valido=True
            )
            RegistroDiario.objects.create(
                operario=cls.operario1,
                hora_fichada=cls.primer_sabado.replace(hour=17),
                tipo_movimiento='salida',
                valido=True
            )

            # Segundo sábado del sistema (2025-04-12, índice 1, Grupo B)
            cls.segundo_sabado = datetime(2025, 4, 12, 8, 0, tzinfo=argentina_tz)
            RegistroDiario.objects.create(
                operario=cls.operario2,
                hora_fichada=cls.segundo_sabado,
                tipo_movimiento='entrada',
                valido=True
            )
            RegistroDiario.objects.create(
                operario=cls.operario2,
                hora_fichada=cls.segundo_sabado.replace(hour=17),
                tipo_movimiento='salida',
                valido=True
            )

    def test_detectar_grupo_sabado_operario_grupo_a(self):
        """Verifica que operario1 sea detectado como Grupo A"""
        from apps.reloj_fichador.utils import detectar_grupo_sabado_operario

        grupo, primer_sabado = detectar_grupo_sabado_operario(self.operario1)

        self.assertEqual(grupo, 'A')
        self.assertEqual(primer_sabado, self.primer_sabado.date())

    def test_detectar_grupo_sabado_operario_grupo_b(self):
        """Verifica que operario2 sea detectado como Grupo B"""
        from apps.reloj_fichador.utils import detectar_grupo_sabado_operario

        grupo, primer_sabado = detectar_grupo_sabado_operario(self.operario2)

        self.assertEqual(grupo, 'B')
        self.assertEqual(primer_sabado, self.segundo_sabado.date())

    def test_detectar_grupo_sin_registros(self):
        """Verifica que operario3 (sin registros de sábados) retorne None"""
        from apps.reloj_fichador.utils import detectar_grupo_sabado_operario

        grupo, primer_sabado = detectar_grupo_sabado_operario(self.operario3)

        self.assertIsNone(grupo)
        self.assertIsNone(primer_sabado)

    def test_obtener_grupo_sabado_esperado_grupo_a(self):
        """Verifica que el primer sábado sea Grupo A"""
        from apps.reloj_fichador.utils import obtener_grupo_sabado_esperado

        grupo = obtener_grupo_sabado_esperado(self.primer_sabado.date())
        self.assertEqual(grupo, 'A')

    def test_obtener_grupo_sabado_esperado_grupo_b(self):
        """Verifica que el segundo sábado sea Grupo B"""
        from apps.reloj_fichador.utils import obtener_grupo_sabado_esperado

        grupo = obtener_grupo_sabado_esperado(self.segundo_sabado.date())
        self.assertEqual(grupo, 'B')

    def test_obtener_grupo_sabado_esperado_alternancia(self):
        """Verifica la alternancia correcta de grupos en sábados consecutivos"""
        from apps.reloj_fichador.utils import obtener_grupo_sabado_esperado
        from datetime import timedelta

        # Testear 8 sábados consecutivos
        sabado_actual = self.primer_sabado.date()
        grupos_esperados = ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B']

        for i, grupo_esperado in enumerate(grupos_esperados):
            grupo = obtener_grupo_sabado_esperado(sabado_actual)
            self.assertEqual(
                grupo, grupo_esperado,
                f'Sábado {i+1} ({sabado_actual}) debería ser Grupo {grupo_esperado}, pero se detectó Grupo {grupo}'
            )
            sabado_actual = sabado_actual + timedelta(weeks=1)

    def test_obtener_grupo_sabado_operario_con_asignacion_manual(self):
        """Verifica que se prioriza la asignación manual sobre auto-detección"""
        from apps.reloj_fichador.utils import obtener_grupo_sabado_operario

        # Crear asignación manual como Grupo B para operario1 (aunque auto-detecte A)
        grupo_sabado = GrupoSabado.objects.create(
            operario=self.operario1,
            grupo='B',
            fecha_inicio=datetime.now().date(),
            descripcion='Asignación manual de prueba'
        )

        # Debe retornar el grupo manual (B) en lugar del auto-detectado (A)
        grupo = obtener_grupo_sabado_operario(self.operario1)
        self.assertEqual(grupo, 'B')

    def test_hay_intercambio_sabado(self):
        """Verifica detección de intercambios de sábado"""
        from apps.reloj_fichador.utils import hay_intercambio_sabado

        # operario1 tiene registro el primer sábado
        tiene_intercambio = hay_intercambio_sabado(self.operario1, self.primer_sabado.date())
        self.assertTrue(tiene_intercambio)

        # operario1 no tiene registro el segundo sábado
        tiene_intercambio = hay_intercambio_sabado(self.operario1, self.segundo_sabado.date())
        self.assertFalse(tiene_intercambio)


class CorreccionHorasNegativasTest(TestCase):
    """
    Tests para verificar la corrección del bug de horas negativas.

    Bug original: Registros duplicados o entrada redondeada >= salida
    causaban horas negativas en Horas_trabajadas.

    Corrección: Validación de pares entrada-salida y entrada < salida.
    """

    @classmethod
    def setUpTestData(cls):
        """Configuración inicial para todas las pruebas"""
        cls.area = Area.objects.create(nombre="Producción")
        cls.operario = Operario.objects.create(
            dni=41697878,
            nombre="Maico",
            apellido="Tisera",
            fecha_nacimiento="1990-05-15",
            fecha_ingreso_empresa="2015-08-01",
            activo=True
        )
        cls.operario.areas.add(cls.area)

    def test_registros_duplicados_entrada_entrada_no_causan_horas_negativas(self):
        """
        Test Caso 1: Registros duplicados (entrada-entrada).

        Escenario: Un operario ficha entrada dos veces seguidas.
        Comportamiento esperado: El sistema debe saltar el par inválido
        y no generar horas negativas.
        """
        from apps.reloj_fichador.utils import suppress_signal

        fecha = datetime(2025, 11, 5).date()

        # Crear dos entradas seguidas (como en el bug original)
        with suppress_signal():
            RegistroDiario.objects.create(
                operario=self.operario,
                tipo_movimiento='entrada',
                hora_fichada=timezone.make_aware(datetime(2025, 11, 5, 15, 52, 56)),
                valido=True,
                inconsistencia=True  # Marcado como inconsistencia
            )
            RegistroDiario.objects.create(
                operario=self.operario,
                tipo_movimiento='entrada',
                hora_fichada=timezone.make_aware(datetime(2025, 11, 5, 15, 53, 5)),
                valido=True,
                inconsistencia=True  # Marcado como inconsistencia
            )

        # Calcular horas trabajadas
        horas_normales, horas_nocturnas, horas_extras = Horas_trabajadas.calcular_horas_trabajadas(
            self.operario, fecha
        )

        # Verificar que NO hay horas negativas
        self.assertGreaterEqual(horas_normales, timedelta(0),
            "Las horas normales no deben ser negativas")
        self.assertGreaterEqual(horas_nocturnas, timedelta(0),
            "Las horas nocturnas no deben ser negativas")
        self.assertGreaterEqual(horas_extras, timedelta(0),
            "Las horas extras no deben ser negativas")

        # Verificar que el resultado es 0 (porque no hay par válido)
        self.assertEqual(horas_normales, timedelta(0))
        self.assertEqual(horas_nocturnas, timedelta(0))
        self.assertEqual(horas_extras, timedelta(0))

    def test_entrada_redondeada_mayor_que_salida_no_causa_horas_negativas(self):
        """
        Test Caso 2: Entrada redondeada >= Salida.

        Escenario: Entrada a las 15:52:56 (redondea a 16:00), Salida a las 15:53:05.
        Comportamiento esperado: El sistema debe detectar entrada >= salida y saltar el par.
        """
        from apps.reloj_fichador.utils import suppress_signal

        fecha = datetime(2025, 11, 5).date()

        # Crear entrada y salida muy cercanas (salida antes de entrada redondeada)
        with suppress_signal():
            RegistroDiario.objects.create(
                operario=self.operario,
                tipo_movimiento='entrada',
                hora_fichada=timezone.make_aware(datetime(2025, 11, 5, 15, 52, 56)),
                valido=True
            )
            RegistroDiario.objects.create(
                operario=self.operario,
                tipo_movimiento='salida',
                hora_fichada=timezone.make_aware(datetime(2025, 11, 5, 15, 53, 5)),
                valido=True
            )

        # Calcular horas trabajadas
        horas_normales, horas_nocturnas, horas_extras = Horas_trabajadas.calcular_horas_trabajadas(
            self.operario, fecha
        )

        # Verificar que NO hay horas negativas
        self.assertGreaterEqual(horas_normales, timedelta(0))
        self.assertGreaterEqual(horas_nocturnas, timedelta(0))
        self.assertGreaterEqual(horas_extras, timedelta(0))

    def test_caso_martin_registros_con_inconsistencia_procesados_correctamente(self):
        """
        Test Caso 3: Flujo real de corrección manual (Caso Martín).

        Escenario:
        - Día 1: Entrada sin salida (olvida fichar)
        - Día 2: Entrada con inconsistencia (porque falta salida del día anterior)
        - Responsable añade manualmente la salida del Día 1

        Comportamiento esperado: El Día 2 debe procesarse correctamente aunque
        tenga inconsistencia=True, porque después de la corrección manual forma
        un par válido.
        """
        from apps.reloj_fichador.utils import suppress_signal

        fecha_dia1 = datetime(2025, 11, 11).date()
        fecha_dia2 = datetime(2025, 11, 12).date()

        with suppress_signal():
            # Día 1: Entrada a las 6:59 AM
            RegistroDiario.objects.create(
                operario=self.operario,
                tipo_movimiento='entrada',
                hora_fichada=timezone.make_aware(datetime(2025, 11, 11, 6, 59, 0)),
                valido=True
            )

            # Día 2: Entrada con inconsistencia a las 6:57 AM
            RegistroDiario.objects.create(
                operario=self.operario,
                tipo_movimiento='entrada',
                hora_fichada=timezone.make_aware(datetime(2025, 11, 12, 6, 57, 0)),
                valido=True,
                inconsistencia=True  # Marcado porque falta salida del día anterior
            )

            # Día 2: Salida normal a las 5:00 PM
            RegistroDiario.objects.create(
                operario=self.operario,
                tipo_movimiento='salida',
                hora_fichada=timezone.make_aware(datetime(2025, 11, 12, 17, 0, 0)),
                valido=True
            )

            # Responsable añade manualmente la salida del Día 1 a las 5:00 PM
            RegistroDiario.objects.create(
                operario=self.operario,
                tipo_movimiento='salida',
                hora_fichada=timezone.make_aware(datetime(2025, 11, 11, 17, 0, 0)),
                valido=True
            )

        # Calcular horas del Día 1
        horas_normales_dia1, horas_nocturnas_dia1, horas_extras_dia1 = \
            Horas_trabajadas.calcular_horas_trabajadas(self.operario, fecha_dia1)

        # Calcular horas del Día 2
        horas_normales_dia2, horas_nocturnas_dia2, horas_extras_dia2 = \
            Horas_trabajadas.calcular_horas_trabajadas(self.operario, fecha_dia2)

        # Verificar Día 1: Debe calcular correctamente (6:59 AM -> 5:00 PM)
        # Entrada redondea a 7:00 AM, salida 5:00 PM = 10 horas
        # 8 horas normales + 2 horas extras
        self.assertGreater(horas_normales_dia1, timedelta(0),
            "El Día 1 debe tener horas normales después de la corrección manual")
        self.assertGreaterEqual(horas_normales_dia1, timedelta(0))
        self.assertGreaterEqual(horas_nocturnas_dia1, timedelta(0))

        # Verificar Día 2: Debe calcular correctamente aunque tenga inconsistencia
        # Entrada redondea a 7:00 AM, salida 5:00 PM = 10 horas
        self.assertGreater(horas_normales_dia2, timedelta(0),
            "El Día 2 debe procesarse aunque tenga inconsistencia porque forma par válido")
        self.assertGreaterEqual(horas_normales_dia2, timedelta(0))
        self.assertGreaterEqual(horas_nocturnas_dia2, timedelta(0))

    def test_casos_normales_siguen_funcionando(self):
        """
        Test Caso 4: Casos normales.

        Escenario: Registros normales de entrada-salida válidos.
        Comportamiento esperado: Deben seguir funcionando correctamente.
        """
        from apps.reloj_fichador.utils import suppress_signal

        fecha = datetime(2025, 11, 13).date()

        with suppress_signal():
            # Entrada normal a las 8:00 AM
            RegistroDiario.objects.create(
                operario=self.operario,
                tipo_movimiento='entrada',
                hora_fichada=timezone.make_aware(datetime(2025, 11, 13, 8, 0, 0)),
                valido=True
            )

            # Salida normal a las 5:00 PM
            RegistroDiario.objects.create(
                operario=self.operario,
                tipo_movimiento='salida',
                hora_fichada=timezone.make_aware(datetime(2025, 11, 13, 17, 0, 0)),
                valido=True
            )

        # Calcular horas trabajadas
        horas_normales, horas_nocturnas, horas_extras = Horas_trabajadas.calcular_horas_trabajadas(
            self.operario, fecha
        )

        # Verificar cálculo correcto: 8:00 AM a 5:00 PM = 9 horas
        # 8 horas normales + 1 hora extra
        self.assertEqual(horas_normales, timedelta(hours=8))
        self.assertEqual(horas_nocturnas, timedelta(hours=0))
        self.assertEqual(horas_extras, timedelta(hours=1))

        # Verificar NO hay horas negativas
        self.assertGreaterEqual(horas_normales, timedelta(0))
        self.assertGreaterEqual(horas_nocturnas, timedelta(0))
        self.assertGreaterEqual(horas_extras, timedelta(0))

    def test_multiples_pares_entrada_salida_uno_invalido(self):
        """
        Test Caso 5: Múltiples pares entrada-salida, uno inválido.

        Escenario: Dos pares de entrada-salida en el mismo día, uno válido y uno inválido.
        Comportamiento esperado: Debe procesar el par válido e ignorar el inválido,
        sin generar horas negativas.
        """
        from apps.reloj_fichador.utils import suppress_signal

        fecha = datetime(2025, 11, 14).date()

        with suppress_signal():
            # PAR 1: VÁLIDO - Entrada 8:00 AM, Salida 12:00 PM
            RegistroDiario.objects.create(
                operario=self.operario,
                tipo_movimiento='entrada',
                hora_fichada=timezone.make_aware(datetime(2025, 11, 14, 8, 0, 0)),
                valido=True
            )
            RegistroDiario.objects.create(
                operario=self.operario,
                tipo_movimiento='salida',
                hora_fichada=timezone.make_aware(datetime(2025, 11, 14, 12, 0, 0)),
                valido=True
            )

            # PAR 2: INVÁLIDO - Entrada 15:52:56, Salida 15:53:05 (salida antes de entrada redondeada)
            RegistroDiario.objects.create(
                operario=self.operario,
                tipo_movimiento='entrada',
                hora_fichada=timezone.make_aware(datetime(2025, 11, 14, 15, 52, 56)),
                valido=True,
                inconsistencia=True
            )
            RegistroDiario.objects.create(
                operario=self.operario,
                tipo_movimiento='salida',
                hora_fichada=timezone.make_aware(datetime(2025, 11, 14, 15, 53, 5)),
                valido=True,
                inconsistencia=True
            )

        # Calcular horas trabajadas
        horas_normales, horas_nocturnas, horas_extras = Horas_trabajadas.calcular_horas_trabajadas(
            self.operario, fecha
        )

        # Verificar que solo se contó el primer par (4 horas)
        self.assertEqual(horas_normales, timedelta(hours=4))
        self.assertEqual(horas_nocturnas, timedelta(hours=0))
        self.assertEqual(horas_extras, timedelta(hours=0))

        # Verificar que NO hay horas negativas
        self.assertGreaterEqual(horas_normales, timedelta(0))
        self.assertGreaterEqual(horas_nocturnas, timedelta(0))
        self.assertGreaterEqual(horas_extras, timedelta(0))

    def test_turno_nocturno_no_genera_horas_negativas(self):
        """
        Test Caso 6: Turno nocturno dentro del mismo día.

        Escenario: Entrada a las 10:00 PM, salida a las 11:59 PM del mismo día.
        Comportamiento esperado: Debe calcular horas nocturnas sin problemas.
        """
        from apps.reloj_fichador.utils import suppress_signal

        fecha = datetime(2025, 11, 15).date()

        with suppress_signal():
            # Entrada a las 10:00 PM
            RegistroDiario.objects.create(
                operario=self.operario,
                tipo_movimiento='entrada',
                hora_fichada=timezone.make_aware(datetime(2025, 11, 15, 22, 0, 0)),
                valido=True
            )

            # Salida a las 11:59 PM del mismo día
            RegistroDiario.objects.create(
                operario=self.operario,
                tipo_movimiento='salida',
                hora_fichada=timezone.make_aware(datetime(2025, 11, 15, 23, 59, 0)),
                valido=True
            )

        # Calcular horas trabajadas
        horas_normales, horas_nocturnas, horas_extras = Horas_trabajadas.calcular_horas_trabajadas(
            self.operario, fecha
        )

        # Verificar que se calcularon horas nocturnas (aproximadamente 2 horas)
        self.assertEqual(horas_normales, timedelta(hours=0))
        self.assertGreater(horas_nocturnas, timedelta(hours=0),
            "Debe haber horas nocturnas para turno que inicia después de las 20:00")
        self.assertEqual(horas_extras, timedelta(hours=0))

        # Verificar que NO hay horas negativas
        self.assertGreaterEqual(horas_normales, timedelta(0))
        self.assertGreaterEqual(horas_nocturnas, timedelta(0))
        self.assertGreaterEqual(horas_extras, timedelta(0)) 