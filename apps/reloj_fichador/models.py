from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.timezone import is_naive, make_aware
from datetime import timedelta
import datetime

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
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_ingreso_empresa = models.DateField(null=True, blank=True)
    titulo_tecnico = models.BooleanField(default=False)

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
    hora_fichada = models.DateTimeField(blank=True, null=True)
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO)
    origen_fichada = models.CharField(max_length=10, default='Auto')  # Nueva columna para el origen

    def __str__(self):
        return f"{self.operario} - {self.tipo_movimiento} - {self.hora_fichada.strftime('%Y/%m/%d %H:%M:%S')}"

    def save(self, *args, **kwargs):
        if not self.hora_fichada:
            self.hora_fichada = timezone.now()
        if 'origen_fichada' not in kwargs:  # Si no se especifica, se establece como automático
            self.origen_fichada = self.origen_fichada or 'Auto'  # Esto asegura que se establezca correctamente
        super().save(*args, **kwargs)

        # Calcular horas trabajadas después de una salida
        if self.tipo_movimiento == 'salida':
            Horas_trabajadas.calcular_horas_trabajadas(self.operario, self.hora_fichada.date())
            Horas_extras.calcular_horas_extras(self.operario, self.hora_fichada.date())


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

        # Limitar las horas trabajadas a un máximo de 8 horas
        max_horas_trabajadas = timedelta(hours=8)
        if total_horas > max_horas_trabajadas:
            total_horas = max_horas_trabajadas

        # Redondeo de las horas trabajadas
        if total_horas >= timedelta(minutes=45):
            total_horas = timedelta(hours=round(total_horas.total_seconds() / 3600))
        else:
            total_horas = timedelta(minutes=(total_horas.total_seconds() // 60))

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

from django.utils.timezone import is_naive, make_aware

class Horas_extras(models.Model):
    operario = models.ForeignKey(Operario, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    horas_extras = models.DurationField(default=timedelta)

    class Meta:
        app_label = 'reloj_fichador'
        verbose_name = "Horas extras"
        verbose_name_plural = "Horas extras"

    @classmethod
    def calcular_horas_extras(cls, operario, fecha):
        # Obtener la primera área del operario
        area = operario.areas.first()
        if area:
            horario = area.horarios.first()
            if horario:
                hora_inicio_programada = horario.hora_inicio
                hora_salida_programada = horario.hora_fin
            else:
                return timedelta(0)
        else:
            return timedelta(0)

        # Convertir las horas programadas a datetime "aware"
        hora_inicio_programada = make_aware(
            datetime.datetime.combine(fecha, hora_inicio_programada)
        )
        hora_salida_programada = make_aware(
            datetime.datetime.combine(fecha, hora_salida_programada)
        )

        # Obtener la primera entrada y última salida
        entrada = RegistroDiario.objects.filter(
            operario=operario,
            tipo_movimiento='entrada',
            hora_fichada__date=fecha
        ).order_by('hora_fichada').first()

        salida = RegistroDiario.objects.filter(
            operario=operario,
            tipo_movimiento='salida',
            hora_fichada__date=fecha
        ).order_by('-hora_fichada').first()

        horas_extras_totales = timedelta()

        # Asegurarse de que entrada.hora_fichada sea "aware" si es necesario
        if entrada and is_naive(entrada.hora_fichada):
            entrada.hora_fichada = make_aware(entrada.hora_fichada)

        # Asegurarse de que salida.hora_fichada sea "aware" si es necesario
        if salida and is_naive(salida.hora_fichada):
            salida.hora_fichada = make_aware(salida.hora_fichada)

        # Calcular horas extras si el operario ingresa al menos una hora antes
        if entrada and entrada.hora_fichada < hora_inicio_programada - timedelta(hours=1):
            diferencia_entrada = hora_inicio_programada - entrada.hora_fichada

            # Aplicar reglas de redondeo para la entrada anticipada
            if diferencia_entrada >= timedelta(minutes=45):
                horas_extras_totales += timedelta(hours=round(diferencia_entrada.total_seconds() / 3600))
            elif diferencia_entrada >= timedelta(minutes=30):
                horas_extras_totales += timedelta(minutes=30)

        # Calcular horas extras si el operario se queda después de su horario de salida programado
        if salida and salida.hora_fichada > hora_salida_programada + timedelta(minutes=30):
            diferencia_salida = salida.hora_fichada - hora_salida_programada

            # Aplicar reglas de redondeo para la salida tardía
            if diferencia_salida >= timedelta(minutes=45):
                horas_extras_totales += timedelta(hours=round(diferencia_salida.total_seconds() / 3600))
            elif diferencia_salida >= timedelta(minutes=30):
                horas_extras_totales += timedelta(minutes=30)

        obj, created = cls.objects.get_or_create(operario=operario, fecha=fecha)
        obj.horas_extras = horas_extras_totales
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

