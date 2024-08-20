from django.db import models
from django.db.models import Sum
from datetime import timedelta

class Horario(models.Model):
    nombre = models.CharField(max_length=50, help_text="Nombre del horario (por ejemplo, Turno Mañana)")
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.nombre}: {self.hora_inicio.strftime('%H:%M')} - {self.hora_fin.strftime('%H:%M')}"


class Area(models.Model):
    nombre = models.CharField(max_length=50)
    horarios = models.ManyToManyField(Horario)

    def __str__(self):
        return self.nombre

class Operario(models.Model):
    dni = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=20)
    seg_nombre = models.CharField(max_length=20, null=True, blank=True)
    apellido = models.CharField(max_length=20)
    seg_apellido = models.CharField(max_length=20, null=True, blank=True)
    areas = models.ManyToManyField(Area)

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
        ('salida_transitoria', 'Salida Transitoria'),
        ('entrada_transitoria', 'Entrada Transitoria'),
        ('salida', 'Salida'),
    ]

    id_registro = models.AutoField(primary_key=True)
    operario = models.ForeignKey(Operario, on_delete=models.CASCADE)
    hora_fichada = models.DateTimeField(auto_now_add=True)
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO)

    def __str__(self):
        return f"{self.operario} - {self.tipo_movimiento} - {self.hora_fichada.strftime('%Y/%m/%d %H:%M:%S')}"

class Licencias(models.Model):
    dni = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=250)
    certificado = models.ImageField()

class Horas_trabajadas(models.Model):
    operario = models.ForeignKey(Operario, on_delete=models.CASCADE)
    fecha = models.DateField()
    horas_trabajadas = models.DurationField(default=timedelta)
    class Meta:
        app_label = 'reloj_fichador'
        verbose_name = "Horas normales"
        verbose_name_plural = "Horas normales"


    @classmethod
    def calcular_horas_trabajadas(cls, operario, fecha):
        entradas = RegistroDiario.objects.filter(operario=operario, tipo_movimiento='entrada', hora_fichada__date=fecha)
        salidas = RegistroDiario.objects.filter(operario=operario, tipo_movimiento='salida', hora_fichada__date=fecha)

        total_horas = timedelta()

        for entrada in entradas:
            salida = salidas.filter(hora_fichada__gte=entrada.hora_fichada).first()
            if salida:
                total_horas += (salida.hora_fichada - entrada.hora_fichada)

        obj, created = cls.objects.get_or_create(operario=operario, fecha=fecha)
        obj.horas_trabajadas = total_horas
        obj.save()
        return obj.horas_trabajadas

class Horas_feriado(models.Model):
    operario = models.ForeignKey(Operario, on_delete=models.CASCADE)
    fecha = models.DateField()
    horas_feriado = models.DurationField(default=timedelta)
    class Meta:
        app_label = 'reloj_fichador'
        verbose_name = "Horas feriado"
        verbose_name_plural = "Horas feriado"

    @classmethod
    def sumar_horas_feriado(cls, operario, fecha, es_feriado=False):
        if es_feriado:
            horas_feriado = timedelta(hours=8)  # Suponiendo 8 horas de feriado
            obj, created = cls.objects.get_or_create(operario=operario, fecha=fecha)
            obj.horas_feriado = horas_feriado
            obj.save()
            return obj.horas_feriado
        return timedelta()

class Horas_extras(models.Model):
    operario = models.ForeignKey(Operario, on_delete=models.CASCADE)
    mes = models.CharField(max_length=20)
    horas_extras = models.DurationField(default=timedelta)
    class Meta:
        app_label = 'reloj_fichador'
        verbose_name = "Horas extras"
        verbose_name_plural = "Horas extras"

    @classmethod
    def calcular_horas_extras(cls, operario, mes, horas_laborales_mes=192):
        horas_trabajadas_mes = \
        Horas_trabajadas.objects.filter(operario=operario, fecha__month=mes).aggregate(total=Sum('horas_trabajadas'))[
            'total'] or timedelta()
        horas_extras = max(horas_trabajadas_mes - timedelta(hours=horas_laborales_mes), timedelta())

        obj, created = cls.objects.get_or_create(operario=operario, mes=mes)
        obj.horas_extras = horas_extras
        obj.save()
        return obj.horas_extras

class Horas_totales(models.Model):
    operario = models.ForeignKey(Operario, on_delete=models.CASCADE)
    mes_actual = models.CharField(max_length=20)
    horas_totales = models.DurationField(default=timedelta)
    class Meta:
        app_label = 'reloj_fichador'
        verbose_name = "Horas totales"
        verbose_name_plural = "Horas totales"

    @classmethod
    def calcular_horas_totales(cls, operario, mes):
        horas_trabajadas = \
        Horas_trabajadas.objects.filter(operario=operario, fecha__month=mes).aggregate(total=Sum('horas_trabajadas'))[
            'total'] or timedelta()
        horas_feriado = \
        Horas_feriado.objects.filter(operario=operario, fecha__month=mes).aggregate(total=Sum('horas_feriado'))[
            'total'] or timedelta()
        horas_extras = Horas_extras.objects.filter(operario=operario, mes=mes).aggregate(total=Sum('horas_extras'))[
                           'total'] or timedelta()

        total_horas = horas_trabajadas + horas_feriado + horas_extras

        obj, created = cls.objects.get_or_create(operario=operario, mes_actual=mes)
        obj.horas_totales = total_horas
        obj.save()
        return obj.horas_totales

