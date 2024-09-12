import django_tables2 as tables
from .models import Operario

class OperarioTable(tables.Table):
    class Meta:
        model = Operario
        template_name = "django_tables2/bootstrap.html"  # Usa una plantilla de tabla de Bootstrap
        fields = ("dni", "nombre", "apellido", "fecha_ingreso", "activo")  # Personaliza las columnas
