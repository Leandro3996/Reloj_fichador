from datetime import date

from django.core.management import call_command
from django.test import TestCase

from apps.reloj_fichador.models import CalendarioLaboral, SugerenciaFeriado


class SugerenciaFeriadoModelTest(TestCase):
    def setUp(self):
        self.sugerencia = SugerenciaFeriado.objects.create(
            fecha=date(2025, 1, 1),
            nombre="Año Nuevo",
            tipo_sugerencia="feriado_nacional",
            fuente="api_argentina",
        )

    def test_aceptar_crea_calendario(self):
        self.sugerencia.aceptar()
        self.sugerencia.refresh_from_db()

        self.assertEqual(self.sugerencia.estado, 'aceptado')
        self.assertTrue(
            CalendarioLaboral.objects.filter(fecha=date(2025, 1, 1)).exists()
        )

    def test_rechazar_actualiza_estado(self):
        self.sugerencia.rechazar(nota='No aplica')
        self.sugerencia.refresh_from_db()

        self.assertEqual(self.sugerencia.estado, 'rechazado')
        self.assertEqual(self.sugerencia.nota_admin, 'No aplica')


class SincronizarFeriadosCommandTest(TestCase):
    def test_crea_sugerencias_desde_api(self):
        sample_feriados = [
            {
                'fecha': date(2025, 3, 24),
                'nombre': 'Día Nacional de la Memoria',
                'tipo_sugerencia': 'feriado_nacional',
                'datos_originales': {'tipo': 'inamovible'},
                'fuente_url': 'https://argentinadatos.com/v1/feriados/2025',
            },
            {
                'fecha': date(2025, 4, 2),
                'nombre': 'Día del Veterano y de los Caídos en la Guerra de Malvinas',
                'tipo_sugerencia': 'feriado_nacional',
                'datos_originales': {'tipo': 'inamovible'},
                'fuente_url': 'https://argentinadatos.com/v1/feriados/2025',
            },
        ]

        with self.settings(DEBUG=True):
            with self._mock_api(sample_feriados):
                call_command('sincronizar_feriados', '--year', '2025')

        self.assertEqual(SugerenciaFeriado.objects.count(), 2)
        labels = list(SugerenciaFeriado.objects.values_list('nombre', flat=True))
        self.assertIn('Día Nacional de la Memoria', labels)

    def _mock_api(self, feriados):
        from unittest.mock import patch

        return patch(
            'apps.reloj_fichador.management.commands.sincronizar_feriados.obtener_feriados_api',
            return_value=feriados,
        )
