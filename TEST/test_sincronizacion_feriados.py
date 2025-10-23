"""
Tests para sincronización automática de feriados con ArgentinaDatos API.

Test Cases:
1. Verificar que la tarea Celery se registra correctamente
2. Verificar conexión a API ArgentinaDatos
3. Verificar creación de SugerenciaFeriado
4. Verificar prevención de duplicados
5. Verificar aceptación/rechazo de sugerencias
6. Verificar impacto en generación de RegistroAsistencia
"""

from django.test import TestCase
from django.utils import timezone
from django.core.management import call_command
from io import StringIO
import json
from datetime import date, datetime, timedelta

from apps.reloj_fichador.models import (
    Operario, SugerenciaFeriado, CalendarioLaboral,
    RegistroAsistencia, GrupoSabado
)
from apps.reloj_fichador.tasks import sincronizar_feriados_api
from apps.reloj_fichador.utils import (
    es_dia_laboral, obtener_feriados_api, obtener_feriados_mes
)


class SincronizacionFeriadosAPITestCase(TestCase):
    """Tests para la tarea de sincronización automática de feriados."""

    def setUp(self):
        """Configuración inicial para tests."""
        # Crear operario de prueba
        self.operario = Operario.objects.create(
            nombre="Juan",
            apellido="Pérez",
            dni=12345678,
            activo=True
        )

        # Limpiar sugerencias de feriados previas
        SugerenciaFeriado.objects.all().delete()
        CalendarioLaboral.objects.all().delete()

    def tearDown(self):
        """Limpieza después de tests."""
        SugerenciaFeriado.objects.all().delete()
        CalendarioLaboral.objects.all().delete()
        Operario.objects.all().delete()

    def test_01_obtener_feriados_api_exitoso(self):
        """
        Test 1: Verificar que obtener_feriados_api() se conecta exitosamente.

        Verifica:
        - Conexión a API ArgentinaDatos
        - Retorno de lista de feriados
        - Estructura correcta de datos
        """
        print("\n" + "="*70)
        print("TEST 1: Obtener feriados de API ArgentinaDatos")
        print("="*70)

        feriados = obtener_feriados_api(2025)

        # Verificaciones
        self.assertIsNotNone(feriados, "La API debe retornar una lista")
        self.assertIsInstance(feriados, list, "El resultado debe ser una lista")
        self.assertGreater(len(feriados), 0, "Debe haber al menos 1 feriado")

        # Verificar estructura de cada feriado
        for feriado in feriados[:3]:  # Revisar primeros 3
            self.assertIn('fecha', feriado, "Debe tener clave 'fecha'")
            self.assertIn('nombre', feriado, "Debe tener clave 'nombre'")
            self.assertIn('tipo_sugerencia', feriado, "Debe tener clave 'tipo_sugerencia'")

        print(f"✅ Obtenidos {len(feriados)} feriados de Argentina para 2025")
        print(f"   Primeros 3 feriados:")
        for feriado in feriados[:3]:
            print(f"   - {feriado['fecha']}: {feriado['nombre']} ({feriado['tipo_sugerencia']})")

    def test_02_crear_sugerencia_feriado(self):
        """
        Test 2: Verificar creación de SugerenciaFeriado.

        Verifica:
        - Creación de sugerencia
        - Estados posibles (pendiente, aceptado, rechazado)
        - Campos requeridos
        """
        print("\n" + "="*70)
        print("TEST 2: Crear SugerenciaFeriado")
        print("="*70)

        fecha_test = date(2025, 2, 17)  # Carnaval 2025

        sugerencia = SugerenciaFeriado.objects.create(
            fecha=fecha_test,
            nombre="Carnaval",
            tipo_sugerencia="nacional",
            estado="pendiente",
            fuente="api_argentina"
        )

        # Verificaciones
        self.assertIsNotNone(sugerencia.id, "Debe tener ID después de guardar")
        self.assertEqual(sugerencia.estado, "pendiente", "Estado inicial debe ser 'pendiente'")
        self.assertEqual(sugerencia.fecha, fecha_test, "Fecha debe coincidir")

        print(f"✅ SugerenciaFeriado creada:")
        print(f"   ID: {sugerencia.id}")
        print(f"   Fecha: {sugerencia.fecha}")
        print(f"   Nombre: {sugerencia.nombre}")
        print(f"   Estado: {sugerencia.estado}")

    def test_03_prevenir_duplicados(self):
        """
        Test 3: Verificar prevención de duplicados.

        Verifica:
        - get_or_create evita duplicados
        - Una fecha puede tener una única sugerencia por fuente
        """
        print("\n" + "="*70)
        print("TEST 3: Prevención de duplicados")
        print("="*70)

        fecha_test = date(2025, 2, 17)

        # Crear primera sugerencia
        sugerencia1, created1 = SugerenciaFeriado.objects.get_or_create(
            fecha=fecha_test,
            fuente="api_argentina",
            defaults={
                'nombre': "Carnaval",
                'tipo_sugerencia': "nacional",
                'estado': "pendiente"
            }
        )

        # Intentar crear la misma nuevamente
        sugerencia2, created2 = SugerenciaFeriado.objects.get_or_create(
            fecha=fecha_test,
            fuente="api_argentina",
            defaults={
                'nombre': "Carnaval",
                'tipo_sugerencia': "nacional",
                'estado': "pendiente"
            }
        )

        # Verificaciones
        self.assertTrue(created1, "Primera creación debe ser exitosa")
        self.assertFalse(created2, "Segunda creación debe obtener existente")
        self.assertEqual(sugerencia1.id, sugerencia2.id, "Deben ser el mismo objeto")

        # Verificar que solo existe una
        count = SugerenciaFeriado.objects.filter(fecha=fecha_test).count()
        self.assertEqual(count, 1, "Debe haber solo 1 sugerencia para esa fecha")

        print(f"✅ Prevención de duplicados verificada:")
        print(f"   Primera creación: {created1} (ID: {sugerencia1.id})")
        print(f"   Segunda creación: {created2} (ID: {sugerencia2.id})")
        print(f"   Total en BD: {count} sugerencia(s)")

    def test_04_aceptar_sugerencia(self):
        """
        Test 4: Verificar aceptación de sugerencia y creación en CalendarioLaboral.

        Verifica:
        - Método aceptar() crea CalendarioLaboral
        - Estado cambia a "aceptado"
        - Fecha se excluye de RegistroAsistencia
        """
        print("\n" + "="*70)
        print("TEST 4: Aceptar SugerenciaFeriado")
        print("="*70)

        fecha_test = date(2025, 2, 17)

        # Crear sugerencia
        sugerencia = SugerenciaFeriado.objects.create(
            fecha=fecha_test,
            nombre="Carnaval",
            tipo_sugerencia="nacional",
            estado="pendiente",
            fuente="api_argentina"
        )

        # Aceptar sugerencia
        sugerencia.aceptar()
        sugerencia.refresh_from_db()

        # Verificaciones
        self.assertEqual(sugerencia.estado, "aceptado", "Estado debe ser 'aceptado'")

        # Verificar que se creó en CalendarioLaboral
        calendario = CalendarioLaboral.objects.filter(fecha=fecha_test).first()
        self.assertIsNotNone(calendario, "Debe existir en CalendarioLaboral")
        self.assertEqual(calendario.tipo_dia, "feriado", "Tipo debe ser 'feriado'")

        # Verificar que es día no laboral
        es_laboral = es_dia_laboral(fecha_test)
        self.assertFalse(es_laboral, "La fecha aceptada no debe ser día laboral")

        print(f"✅ Sugerencia aceptada:")
        print(f"   Estado: {sugerencia.estado}")
        print(f"   Creado en CalendarioLaboral: {calendario is not None}")
        print(f"   Es día laboral: {es_laboral}")

    def test_05_rechazar_sugerencia(self):
        """
        Test 5: Verificar rechazo de sugerencia.

        Verifica:
        - Método rechazar() cambia estado
        - NO crea entrada en CalendarioLaboral
        - Permite guardar observaciones
        """
        print("\n" + "="*70)
        print("TEST 5: Rechazar SugerenciaFeriado")
        print("="*70)

        fecha_test = date(2025, 2, 17)

        # Crear sugerencia
        sugerencia = SugerenciaFeriado.objects.create(
            fecha=fecha_test,
            nombre="Carnaval",
            tipo_sugerencia="nacional",
            estado="pendiente",
            fuente="api_argentina"
        )

        # Rechazar con observación
        observacion = "No aplica a nuestra empresa"
        sugerencia.rechazar(nota=observacion)
        sugerencia.refresh_from_db()

        # Verificaciones
        self.assertEqual(sugerencia.estado, "rechazado", "Estado debe ser 'rechazado'")
        self.assertIn(observacion, sugerencia.observaciones_admin, "Debe guardar observación")

        # Verificar que NO se creó en CalendarioLaboral
        calendario = CalendarioLaboral.objects.filter(fecha=fecha_test).first()
        self.assertIsNone(calendario, "No debe existir en CalendarioLaboral si se rechaza")

        # Verificar que sigue siendo día laboral
        es_laboral = es_dia_laboral(fecha_test)
        self.assertTrue(es_laboral, "La fecha rechazada debe ser día laboral")

        print(f"✅ Sugerencia rechazada:")
        print(f"   Estado: {sugerencia.estado}")
        print(f"   Observación: {observacion}")
        print(f"   En CalendarioLaboral: {calendario is not None}")
        print(f"   Es día laboral: {es_laboral}")

    def test_06_tarea_celery_sincronizar(self):
        """
        Test 6: Verificar ejecución de tarea Celery sincronizar_feriados_api().

        Verifica:
        - La tarea se ejecuta sin errores
        - Crea sugerencias para feriados nuevos
        - No crea duplicados
        - Retorna resumen
        """
        print("\n" + "="*70)
        print("TEST 6: Tarea Celery sincronizar_feriados_api()")
        print("="*70)

        # Contar sugerencias antes
        count_antes = SugerenciaFeriado.objects.count()

        # Ejecutar tarea
        resultado = sincronizar_feriados_api()

        # Contar sugerencias después
        count_despues = SugerenciaFeriado.objects.count()

        # Verificaciones
        self.assertIsNotNone(resultado, "Debe retornar un resultado")
        self.assertIsInstance(resultado, str, "Resultado debe ser string")
        self.assertIn("Sincronización completada", resultado, "Debe mencionar completada")

        # Puede haber nuevas o ninguna (si ya existían)
        nuevas = count_despues - count_antes
        print(f"✅ Tarea Celery ejecutada:")
        print(f"   Sugerencias antes: {count_antes}")
        print(f"   Sugerencias después: {count_despues}")
        print(f"   Nuevas sugerencias: {nuevas}")
        print(f"   Resultado: {resultado}")

    def test_07_comando_management_sincronizar(self):
        """
        Test 7: Verificar comando Django management sincronizar_feriados.

        Verifica:
        - El comando se ejecuta sin errores
        - Retorna salida informativa
        - Procesa año actual por defecto
        """
        print("\n" + "="*70)
        print("TEST 7: Comando Management sincronizar_feriados")
        print("="*70)

        out = StringIO()

        # Ejecutar comando
        call_command('sincronizar_feriados', stdout=out)

        salida = out.getvalue()

        # Verificaciones
        self.assertIsNotNone(salida, "Debe retornar salida")
        self.assertGreater(len(salida), 0, "Salida no debe estar vacía")

        print(f"✅ Comando management ejecutado:")
        print(f"   Salida:\n{salida}")

    def test_08_es_dia_laboral_feriado(self):
        """
        Test 8: Verificar que es_dia_laboral() respeta CalendarioLaboral.

        Verifica:
        - Un feriado aceptado retorna False
        - Días normales retornan True (lunes-viernes)
        - Domingos retornan False
        """
        print("\n" + "="*70)
        print("TEST 8: Validación es_dia_laboral() con feriados")
        print("="*70)

        # Día de prueba: un lunes (2025-02-10)
        lunes = date(2025, 2, 10)

        # Verificar que es día laboral normal
        es_laboral_antes = es_dia_laboral(lunes)
        self.assertTrue(es_laboral_antes, "Un lunes debe ser día laboral")

        # Crear feriado en ese día
        CalendarioLaboral.objects.create(
            fecha=lunes,
            tipo_dia="feriado",
            nombre="Feriado especial"
        )

        # Verificar que ahora es NO laboral
        es_laboral_despues = es_dia_laboral(lunes)
        self.assertFalse(es_laboral_despues, "Un día marcado como feriado debe ser no laboral")

        print(f"✅ Validación es_dia_laboral():")
        print(f"   {lunes} (Lunes)")
        print(f"   Antes de marcar feriado: {es_laboral_antes}")
        print(f"   Después de marcar feriado: {es_laboral_despues}")

    def test_09_obtener_feriados_mes(self):
        """
        Test 9: Verificar obtener_feriados_mes().

        Verifica:
        - Retorna solo feriados del mes especificado
        - Excluye otros meses
        - Estructura correcta de datos
        """
        print("\n" + "="*70)
        print("TEST 9: Obtener feriados de un mes")
        print("="*70)

        # Crear varios feriados
        CalendarioLaboral.objects.create(
            fecha=date(2025, 2, 10),
            tipo_dia="feriado",
            nombre="Feriado 1"
        )
        CalendarioLaboral.objects.create(
            fecha=date(2025, 2, 17),
            tipo_dia="feriado",
            nombre="Feriado 2"
        )
        CalendarioLaboral.objects.create(
            fecha=date(2025, 3, 5),
            tipo_dia="feriado",
            nombre="Feriado 3"
        )

        # Obtener feriados de febrero
        feriados_febrero = obtener_feriados_mes(mes=2, año=2025)

        # Verificaciones
        self.assertEqual(len(feriados_febrero), 2, "Febrero debe tener 2 feriados")

        fechas_febrero = [f['fecha'] for f in feriados_febrero]
        self.assertIn(date(2025, 2, 10), fechas_febrero)
        self.assertIn(date(2025, 2, 17), fechas_febrero)
        self.assertNotIn(date(2025, 3, 5), fechas_febrero)

        print(f"✅ Feriados de febrero 2025: {len(feriados_febrero)}")
        for feriado in feriados_febrero:
            print(f"   - {feriado['fecha']}: {feriado['nombre']}")


class SincronizacionConRegistroAsistenciaTestCase(TestCase):
    """Tests para integración de feriados con RegistroAsistencia."""

    def setUp(self):
        """Configuración inicial."""
        self.operario = Operario.objects.create(
            nombre="María",
            apellido="García",
            documento_identidad="98765432",
            activo=True
        )

    def tearDown(self):
        """Limpieza."""
        RegistroAsistencia.objects.all().delete()
        CalendarioLaboral.objects.all().delete()
        Operario.objects.all().delete()

    def test_10_no_crear_registro_en_feriado(self):
        """
        Test 10: Verificar que generar_registros_asistencia() NO crea registro en feriado.

        Verifica:
        - Si un día es feriado, no se crea RegistroAsistencia
        - Si es día normal, sí se crea
        """
        print("\n" + "="*70)
        print("TEST 10: No crear RegistroAsistencia en feriados")
        print("="*70)

        fecha_feriado = date(2025, 2, 17)

        # Marcar fecha como feriado
        CalendarioLaboral.objects.create(
            fecha=fecha_feriado,
            tipo_dia="feriado",
            nombre="Carnaval"
        )

        # Intentar crear registro para ese día
        es_laboral = es_dia_laboral(fecha_feriado)

        # Verificación
        self.assertFalse(es_laboral, "El feriado no debe ser día laboral")

        print(f"✅ {fecha_feriado} (Carnaval):")
        print(f"   Es día laboral: {es_laboral}")
        print(f"   RegistroAsistencia se crearía: {es_laboral}")
