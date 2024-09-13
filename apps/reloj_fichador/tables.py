import django_tables2 as tables
from .models import Operario, RegistroDiario

class OperarioTable(tables.Table):
    class Meta:
        model = Operario
        template_name = "django_tables2/bootstrap.html"
        fields = ("dni", "nombre", "apellido", "fecha_ingreso", "activo")

class RegistroDiarioTable(tables.Table):
    class Meta:
        model = RegistroDiario
        template_name = "django_tables2/bootstrap.html"
        fields = ("operario", "hora_fichada", "tipo_movimiento", "origen_fichada")

class LicenciaTable(tables.Table):
    class Meta:
        model = RegistroDiario
        template_name = "django_tables2/bootstrap.html"
        fields = ("operario", "descripcion", "fecha_subida", "fecha_inicio","fecha_fin","archivo",)

