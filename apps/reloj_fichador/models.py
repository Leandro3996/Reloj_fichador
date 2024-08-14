from django.db import models


class Operario(models.Model):
    dni = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=20)
    seg_nombre = models.CharField(max_length=20, null=True, blank=True)
    apellido = models.CharField(max_length=20)
    seg_apellido = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        # Construyendo el nombre completo considerando nombres y apellidos secundarios
        full_name = f"{self.nombre}"
        if self.seg_nombre:
            full_name += f" {self.seg_nombre}"
        full_name += f" {self.apellido}"
        if self.seg_apellido:
            full_name += f" {self.seg_apellido}"

        return f"{self.dni} - {full_name}"

class RegistroDiario(models.Model):
    TIPO_MOVIMIENTO = [
        ('entrada', 'Entrada'),
        ('sal_transitoria', 'Salida Transitoria'),
        ('ent_transitoria', 'Entrada Transitoria'),
        ('salida', 'Salida'),
    ]

    id_registro = models.AutoField(primary_key=True)
    operario = models.ForeignKey(Operario, on_delete=models.CASCADE)
    hora_fichada = models.DateTimeField(auto_now_add=True)
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO)

    def __str__(self):
        return f"{self.operario} - {self.tipo_movimiento} - {self.hora_fichada.strftime('%Y/%m/%d %H:%M:%S')}"


