from django.db import models

class Operario(models.Model):
    dni = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=20)
    seg_nombre = models.CharField(max_length=20, null=True, blank=True)
    apellido = models.CharField(max_length=20)
    seg_apellido = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Entrada(models.Model):
    operario = models.ForeignKey(Operario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"Entrada de {self.operario} en {self.fecha}"

class SalidaTra(models.Model):
    operario = models.ForeignKey(Operario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"Salida transitoria de {self.operario} en {self.fecha}"

class EntradaTra(models.Model):
    operario = models.ForeignKey(Operario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"Entrada transitoria de {self.operario} en {self.fecha}"

class Salida(models.Model):
    operario = models.ForeignKey(Operario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"Salida de {self.operario} en {self.fecha}"

class HorasMensual(models.Model):
    dni = models.IntegerField()
    operario = models.CharField(max_length=40)
    horas_del_mes = models.IntegerField()
    horas_trabajadas = models.IntegerField()
    horas_extras = models.IntegerField()

    def __str__(self):
        return f"Horas mensuales de {self.operario} (DNI: {self.dni})"

