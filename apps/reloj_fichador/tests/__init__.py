from .test_models import OperarioModelTest
from .test_registro_diario import RegistroDiarioModelTest
from .test_calculo_horas import CalculoHorasTest
from .test_views import RegistroMovimientoViewTest, ReporteViewTest
from .test_integracion import IntegracionTest

# Este archivo facilita la ejecución de todos los tests
# Para ejecutar todos los tests: python manage.py test apps.reloj_fichador
# Para ejecutar un módulo específico: python manage.py test apps.reloj_fichador.tests.test_views
# Para ejecutar una clase específica: python manage.py test apps.reloj_fichador.tests.test_views.RegistroMovimientoViewTest
