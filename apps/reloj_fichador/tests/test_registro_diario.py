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


class RegistroDiarioValidacionesExitosasTest(TestCase):
    """Tests para validar registros que DEBEN pasar todas las validaciones"""

    @classmethod
    def setUpTestData(cls):
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
        cls.hora_base = safe_datetime(2025, 11, 11, 9, 0, 0)

    def test_01_primera_entrada_del_dia(self):
        """Test: Primera entrada del día (sin registros previos)"""
        registro = RegistroDiario(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=self.hora_base,
            origen_fichada='Auto'
        )
        # No debe lanzar excepción
        registro.full_clean()
        registro.save()

        self.assertEqual(registro.tipo_movimiento, 'entrada')
        self.assertFalse(registro.inconsistencia)
        self.assertTrue(registro.valido)

    def test_02_secuencia_entrada_salida_simple(self):
        """Test: Secuencia básica entrada → salida"""
        # Entrada
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=self.hora_base,
            origen_fichada='Auto'
        )

        # Salida (8 horas después)
        salida = RegistroDiario(
            operario=self.operario,
            tipo_movimiento='salida',
            hora_fichada=self.hora_base + timedelta(hours=8),
            origen_fichada='Auto'
        )
        salida.full_clean()
        salida.save()

        self.assertEqual(RegistroDiario.objects.count(), 2)
        self.assertEqual(RegistroDiario.objects.filter(tipo_movimiento='entrada').count(), 1)
        self.assertEqual(RegistroDiario.objects.filter(tipo_movimiento='salida').count(), 1)

    def test_03_secuencia_con_descanso_completo(self):
        """Test: Secuencia entrada → salida_transitoria → entrada_transitoria → salida"""
        hora = self.hora_base

        # Entrada
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=hora,
            origen_fichada='Auto'
        )

        # Salida transitoria (para almuerzo)
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='salida_transitoria',
            hora_fichada=hora + timedelta(hours=4),
            origen_fichada='Auto'
        )

        # Entrada transitoria (regreso de almuerzo)
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada_transitoria',
            hora_fichada=hora + timedelta(hours=5),
            origen_fichada='Auto'
        )

        # Salida final
        salida = RegistroDiario(
            operario=self.operario,
            tipo_movimiento='salida',
            hora_fichada=hora + timedelta(hours=9),
            origen_fichada='Auto'
        )
        salida.full_clean()
        salida.save()

        self.assertEqual(RegistroDiario.objects.count(), 4)

    def test_04_multiples_ciclos_mismo_dia(self):
        """Test: Múltiples ciclos entrada-salida el mismo día"""
        hora = self.hora_base

        # Ciclo 1: mañana
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=hora,
        )
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='salida',
            hora_fichada=hora + timedelta(hours=4),
        )

        # Ciclo 2: tarde
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=hora + timedelta(hours=5),
        )
        salida = RegistroDiario(
            operario=self.operario,
            tipo_movimiento='salida',
            hora_fichada=hora + timedelta(hours=9),
        )
        salida.full_clean()
        salida.save()

        self.assertEqual(RegistroDiario.objects.count(), 4)

    def test_05_turno_nocturno_entrada_despues_20hs(self):
        """Test: Entrada en turno nocturno (después de las 20:00)"""
        hora_nocturna = safe_datetime(2025, 11, 11, 22, 0, 0)  # 22:00

        entrada = RegistroDiario(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=hora_nocturna,
        )
        entrada.full_clean()
        entrada.save()

        self.assertEqual(entrada.tipo_movimiento, 'entrada')
        self.assertFalse(entrada.inconsistencia)

    def test_06_turno_nocturno_salida_antes_06hs(self):
        """Test: Salida en turno nocturno (antes de las 06:00 del día siguiente)"""
        hora_entrada = safe_datetime(2025, 11, 11, 22, 0, 0)  # 22:00
        hora_salida = safe_datetime(2025, 11, 12, 5, 0, 0)    # 05:00 día siguiente

        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=hora_entrada,
        )

        salida = RegistroDiario(
            operario=self.operario,
            tipo_movimiento='salida',
            hora_fichada=hora_salida,
        )
        salida.full_clean()
        salida.save()

        # Verificar fecha lógica
        fecha_logica_salida = RegistroDiario.calcular_fecha_logica(hora_salida, 'salida')
        self.assertEqual(fecha_logica_salida, datetime(2025, 11, 11).date())

    def test_07_nueva_entrada_dia_siguiente(self):
        """Test: Nueva entrada el día siguiente después de salida del día anterior"""
        # Día 1
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=self.hora_base,
        )
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='salida',
            hora_fichada=self.hora_base + timedelta(hours=8),
        )

        # Día 2
        dia_siguiente = self.hora_base + timedelta(days=1)
        entrada = RegistroDiario(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=dia_siguiente,
        )
        entrada.full_clean()
        entrada.save()

        self.assertEqual(RegistroDiario.objects.count(), 3)


class RegistroDiarioInconsistenciasTest(TestCase):
    """Tests para validar que las INCONSISTENCIAS son detectadas correctamente"""

    @classmethod
    def setUpTestData(cls):
        cls.area = Area.objects.create(nombre="Producción")
        cls.operario = Operario.objects.create(
            dni=87654321,
            nombre="María",
            apellido="González",
            fecha_nacimiento="1990-03-20",
            fecha_ingreso_empresa="2015-06-15",
            activo=True
        )
        cls.operario.areas.add(cls.area)
        cls.hora_base = safe_datetime(2025, 11, 11, 9, 0, 0)

    def test_inc01_doble_entrada_sin_salida(self):
        """Test Inconsistencia: Dos entradas consecutivas sin salida intermedia"""
        # Primera entrada
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=self.hora_base,
        )

        # Segunda entrada (debe fallar)
        entrada2 = RegistroDiario(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=self.hora_base + timedelta(hours=1),
        )

        with self.assertRaises(ValidationError) as context:
            entrada2.full_clean()

        self.assertIn('tipo_movimiento', context.exception.message_dict)

    def test_inc02_doble_salida_sin_entrada(self):
        """Test Inconsistencia: Dos salidas consecutivas sin entrada intermedia"""
        # Entrada
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=self.hora_base,
        )

        # Primera salida
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='salida',
            hora_fichada=self.hora_base + timedelta(hours=8),
        )

        # Segunda salida (debe fallar)
        salida2 = RegistroDiario(
            operario=self.operario,
            tipo_movimiento='salida',
            hora_fichada=self.hora_base + timedelta(hours=9),
        )

        with self.assertRaises(ValidationError) as context:
            salida2.full_clean()

        self.assertIn('tipo_movimiento', context.exception.message_dict)

    def test_inc03_salida_sin_entrada_previa_en_el_dia(self):
        """Test Inconsistencia: Salida sin entrada previa en el mismo día"""
        # Intentar salida sin entrada
        salida = RegistroDiario(
            operario=self.operario,
            tipo_movimiento='salida',
            hora_fichada=self.hora_base + timedelta(hours=8),
        )

        with self.assertRaises(ValidationError) as context:
            salida.full_clean()

        self.assertIn('tipo_movimiento', context.exception.message_dict)

    def test_inc04_salida_transitoria_sin_entrada_previa(self):
        """Test Inconsistencia: Salida transitoria sin entrada previa"""
        salida_trans = RegistroDiario(
            operario=self.operario,
            tipo_movimiento='salida_transitoria',
            hora_fichada=self.hora_base + timedelta(hours=4),
        )

        with self.assertRaises(ValidationError) as context:
            salida_trans.full_clean()

        self.assertIn('tipo_movimiento', context.exception.message_dict)

    def test_inc05_entrada_transitoria_sin_salida_transitoria_previa(self):
        """Test Inconsistencia: Entrada transitoria sin salida transitoria previa"""
        # Entrada normal
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=self.hora_base,
        )

        # Entrada transitoria directa (debe fallar, debería ser salida_transitoria primero)
        entrada_trans = RegistroDiario(
            operario=self.operario,
            tipo_movimiento='entrada_transitoria',
            hora_fichada=self.hora_base + timedelta(hours=1),
        )

        with self.assertRaises(ValidationError) as context:
            entrada_trans.full_clean()

        self.assertIn('tipo_movimiento', context.exception.message_dict)

    def test_inc06_salida_despues_salida_transitoria(self):
        """Test Inconsistencia: Salida después de salida_transitoria (debe ser entrada_transitoria)"""
        # Entrada
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=self.hora_base,
        )

        # Salida transitoria
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='salida_transitoria',
            hora_fichada=self.hora_base + timedelta(hours=4),
        )

        # Salida directa (debe fallar)
        salida = RegistroDiario(
            operario=self.operario,
            tipo_movimiento='salida',
            hora_fichada=self.hora_base + timedelta(hours=5),
        )

        with self.assertRaises(ValidationError) as context:
            salida.full_clean()

        self.assertIn('tipo_movimiento', context.exception.message_dict)

    def test_inc07_salida_transitoria_despues_entrada_transitoria(self):
        """Test Inconsistencia: Salida_transitoria después de entrada_transitoria (debe ser salida)"""
        # Secuencia correcta hasta entrada_transitoria
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=self.hora_base,
        )
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='salida_transitoria',
            hora_fichada=self.hora_base + timedelta(hours=4),
        )
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada_transitoria',
            hora_fichada=self.hora_base + timedelta(hours=5),
        )

        # Salida transitoria de nuevo (debe fallar)
        salida_trans = RegistroDiario(
            operario=self.operario,
            tipo_movimiento='salida_transitoria',
            hora_fichada=self.hora_base + timedelta(hours=6),
        )

        with self.assertRaises(ValidationError) as context:
            salida_trans.full_clean()

        self.assertIn('tipo_movimiento', context.exception.message_dict)


class RegistroDiarioFuncionesAuxiliaresTest(TestCase):
    """Tests para funciones auxiliares del modelo RegistroDiario"""

    @classmethod
    def setUpTestData(cls):
        cls.area = Area.objects.create(nombre="Producción")
        cls.operario = Operario.objects.create(
            dni=11223344,
            nombre="Carlos",
            apellido="Rodríguez",
            activo=True
        )
        cls.operario.areas.add(cls.area)

    def test_calcular_fecha_logica_entrada_temprana(self):
        """Test: Entrada temprana (antes de las 06:00) mantiene fecha real"""
        hora_temprana = safe_datetime(2025, 11, 12, 5, 30, 0)  # 05:30 AM

        fecha_logica = RegistroDiario.calcular_fecha_logica(hora_temprana, 'entrada')

        # Debe mantener la fecha real (12 de noviembre)
        self.assertEqual(fecha_logica, datetime(2025, 11, 12).date())

    def test_calcular_fecha_logica_salida_temprana(self):
        """Test: Salida temprana (antes de las 06:00) ajusta a día anterior"""
        hora_temprana = safe_datetime(2025, 11, 12, 4, 0, 0)  # 04:00 AM

        fecha_logica = RegistroDiario.calcular_fecha_logica(hora_temprana, 'salida')

        # Debe ajustar al día anterior (11 de noviembre)
        self.assertEqual(fecha_logica, datetime(2025, 11, 11).date())

    def test_calcular_fecha_logica_hora_normal(self):
        """Test: Hora normal (después de las 06:00) mantiene fecha real"""
        hora_normal = safe_datetime(2025, 11, 12, 10, 0, 0)  # 10:00 AM

        fecha_logica = RegistroDiario.calcular_fecha_logica(hora_normal, 'entrada')

        self.assertEqual(fecha_logica, datetime(2025, 11, 12).date())

    def test_forzar_inconsistencia_marcada(self):
        """Test: Se puede forzar un registro inconsistente marcándolo explícitamente"""
        # Primera entrada
        RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=safe_datetime(2025, 11, 11, 9, 0, 0),
        )

        # Segunda entrada forzada (marcando inconsistencia)
        entrada_forzada = RegistroDiario(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=safe_datetime(2025, 11, 11, 10, 0, 0),
            inconsistencia=True,
            descripcion_inconsistencia="Registro forzado por corrección manual"
        )

        # No debe lanzar excepción porque está marcada como inconsistencia
        entrada_forzada.full_clean()
        entrada_forzada.save()

        self.assertTrue(entrada_forzada.inconsistencia)
        self.assertEqual(RegistroDiario.objects.count(), 2)

    def test_get_last_valid_record(self):
        """Test: Obtener el último registro válido del operario"""
        hora = safe_datetime(2025, 11, 11, 9, 0, 0)

        # Crear varios registros
        reg1 = RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=hora,
            valido=True
        )
        reg2 = RegistroDiario.objects.create(
            operario=self.operario,
            tipo_movimiento='salida',
            hora_fichada=hora + timedelta(hours=8),
            valido=True
        )

        # Crear un nuevo registro y verificar que obtiene el último válido
        nuevo_reg = RegistroDiario(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada=hora + timedelta(days=1),
        )

        ultimo = nuevo_reg.get_last_valid_record()

        self.assertEqual(ultimo.id_registro, reg2.id_registro)
        self.assertEqual(ultimo.tipo_movimiento, 'salida') 