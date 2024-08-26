from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.timezone import is_naive, make_aware
from django.core.exceptions import ValidationError
from datetime import timedelta
import datetime
import os

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


from django.db import models


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
    activo = models.BooleanField(default=True)

    def __str__(self):
        full_name = f"{self.apellido}"
        if self.seg_apellido:
            full_name += f" {self.seg_apellido}"
        full_name += f", {self.nombre}"
        if self.seg_nombre:
            full_name += f" {self.seg_nombre}"
        return f"{full_name} - {self.dni}"

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # Obtener la extensión del archivo
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Solo se permiten archivos PDF, JPG, JPEG o PNG.')

class Licencia(models.Model):
    operario = models.ForeignKey(Operario, on_delete=models.CASCADE, related_name='licencias')
    archivo = models.FileField(upload_to='licencias/', validators=[validate_file_extension])
    fecha_subida = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Licencia {self.archivo.name} para {self.operario.nombre}"

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
    origen_fichada = models.CharField(max_length=10, default='Auto')

    def __str__(self):
        return f"{self.operario} - {self.tipo_movimiento} - {self.hora_fichada.strftime('%Y/%m/%d %H:%M:%S')}"

    def clean(self):
        # Validar que la hora de salida no sea anterior a la hora de entrada
        if self.tipo_movimiento == 'salida':
            ultimo_registro = RegistroDiario.objects.filter(operario=self.operario).order_by('-hora_fichada').first()
            if ultimo_registro and ultimo_registro.tipo_movimiento == 'entrada':
                if self.hora_fichada <= ultimo_registro.hora_fichada:
                    raise ValidationError("Inconsistencia: La hora de salida no puede ser anterior o igual a la hora de entrada.")

    def save(self, *args, **kwargs):
        if not self.hora_fichada:
            self.hora_fichada = timezone.now()
        if 'origen_fichada' not in kwargs:
            self.origen_fichada = self.origen_fichada or 'Auto'

        try:
            # Llamar a clean() antes de guardar para ejecutar las validaciones
            self.clean()

            # Guardar primero para asegurar que el id_registro se haya asignado
            super().save(*args, **kwargs)

            # Realizar cálculos de horas trabajadas y extras después de guardar
            if self.tipo_movimiento == 'salida':
                Horas_trabajadas.calcular_horas_trabajadas(self.operario, self.hora_fichada.date())
                Horas_extras.calcular_horas_extras(self.operario, self.hora_fichada.date())

                # Actualizar las horas totales para el mes actual
                mes_actual = self.hora_fichada.strftime('%Y-%m')  # Formato Año-Mes
                Horas_totales.calcular_horas_totales(self.operario, mes_actual)
        except AttributeError as e:
            # Manejar específicamente el caso de un error en las horas trabajadas
            raise ValidationError(f"Error al calcular horas: {str(e)}. Verifique la secuencia de fichadas.")

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
    horas_nocturnas = models.DurationField(default=timedelta)  # Campo para horas nocturnas

    class Meta:
        app_label = 'reloj_fichador'
        verbose_name = "Horas normales"
        verbose_name_plural = "Horas normales"

    @classmethod
    def calcular_horas_trabajadas(cls, operario, fecha):
        entradas = RegistroDiario.objects.filter(
            operario=operario,
            tipo_movimiento='entrada',
            hora_fichada__date=fecha
        ).order_by('hora_fichada')

        salidas = RegistroDiario.objects.filter(
            operario=operario,
            tipo_movimiento='salida',
            hora_fichada__date=fecha
        ).order_by('hora_fichada')

        total_horas_normales = timedelta()
        total_horas_nocturnas = timedelta()

        for i in range(len(entradas)):
            if i < len(salidas):
                entrada = entradas[i].hora_fichada
                salida = salidas.filter(hora_fichada__gte=entrada).first().hora_fichada

                # Calcular horas normales y nocturnas
                horas_normales, horas_nocturnas = cls.dividir_horas_normales_y_nocturnas(entrada, salida)
                total_horas_normales += horas_normales
                total_horas_nocturnas += horas_nocturnas

                # Excluir la salida utilizada para evitar duplicados
                salidas = salidas.exclude(id_registro=salidas.first().id_registro)

        # Limitar las horas trabajadas a un máximo de 8 horas
        max_horas_trabajadas = timedelta(hours=8)
        if total_horas_normales > max_horas_trabajadas:
            total_horas_normales = max_horas_trabajadas

        # Redondeo de las horas trabajadas
        if total_horas_normales >= timedelta(minutes=45):
            total_horas_normales = timedelta(hours=round(total_horas_normales.total_seconds() / 3600))
        else:
            total_horas_normales = timedelta(minutes=(total_horas_normales.total_seconds() // 60))

        # Limitar las horas nocturnas a un máximo de 8 horas
        max_horas_nocturnas = timedelta(hours=8)
        if total_horas_nocturnas > max_horas_nocturnas:
            total_horas_nocturnas = max_horas_nocturnas

        # Redondeo de las horas nocturnas
        if total_horas_nocturnas >= timedelta(minutes=45):
            total_horas_nocturnas = timedelta(hours=round(total_horas_nocturnas.total_seconds() / 3600))
        else:
            total_horas_nocturnas = timedelta(minutes=(total_horas_nocturnas.total_seconds() // 60))

        # Guardar los resultados en la base de datos
        obj, created = cls.objects.get_or_create(operario=operario, fecha=fecha)
        obj.horas_trabajadas = total_horas_normales
        obj.horas_nocturnas = total_horas_nocturnas
        obj.save()

        return obj.horas_trabajadas, obj.horas_nocturnas

    @staticmethod
    def dividir_horas_normales_y_nocturnas(entrada, salida):
        # Definir el rango nocturno desde las 21:00 hasta las 05:00 del día siguiente
        inicio_noche = entrada.replace(hour=21, minute=0, second=0)
        fin_noche = entrada.replace(hour=5, minute=0, second=0) + timedelta(days=1)

        horas_normales = timedelta()
        horas_nocturnas = timedelta()

        # Caso 1: Entrada y salida ambas antes de las 21:00 (horario normal)
        if salida <= inicio_noche:
            horas_normales += salida - entrada

        # Caso 2: Entrada antes de las 21:00 y salida después de las 21:00
        elif entrada < inicio_noche and salida > inicio_noche:
            horas_normales += inicio_noche - entrada
            # Verificar si la salida está en el rango nocturno o fuera de él
            if salida <= fin_noche:
                horas_nocturnas += salida - inicio_noche
            else:
                horas_nocturnas += fin_noche - inicio_noche
                horas_normales += salida - fin_noche

        # Caso 3: Entrada y salida ambas en el rango nocturno (21:00 - 05:00)
        elif entrada >= inicio_noche or entrada < fin_noche:
            # Si la salida también está en el rango nocturno
            if salida <= fin_noche:
                horas_nocturnas += salida - entrada
            # Si la salida es después de las 05:00 (final del rango nocturno)
            else:
                horas_nocturnas += fin_noche - entrada
                horas_normales += salida - fin_noche

        # Caso 4: Entrada después de las 05:00 y salida antes de las 21:00 (horario normal)
        else:
            horas_normales += salida - entrada

        return horas_normales, horas_nocturnas

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

        # Asegúrate de que entrada.hora_fichada sea "aware" si es necesario
        if entrada and is_naive(entrada.hora_fichada):
            entrada.hora_fichada = make_aware(entrada.hora_fichada)

        # Asegúrate de que salida.hora_fichada sea "aware" si es necesario
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
    horas_normales = models.DurationField(default=timedelta)
    horas_nocturnas = models.DurationField(default=timedelta)
    horas_extras = models.DurationField(default=timedelta)
    horas_feriado = models.DurationField(default=timedelta)

    class Meta:
        app_label = 'reloj_fichador'
        verbose_name = "Horas totales"
        verbose_name_plural = "Horas totales"

    @classmethod
    def calcular_horas_totales(cls, operario, mes):
        # Obtener el mes en formato correcto (e.g., '2024-08')
        mes_inicio = datetime.datetime.strptime(mes, '%Y-%m').date().replace(day=1)

        horas_trabajadas = Horas_trabajadas.objects.filter(
            operario=operario, fecha__month=mes_inicio.month, fecha__year=mes_inicio.year
        ).aggregate(total=Sum('horas_trabajadas'))['total'] or timedelta()

        horas_extras = Horas_extras.objects.filter(
            operario=operario, fecha__month=mes_inicio.month, fecha__year=mes_inicio.year
        ).aggregate(total=Sum('horas_extras'))['total'] or timedelta()

        horas_nocturnas = cls.calcular_horas_nocturnas(operario, mes_inicio.month)  # Calculamos las horas nocturnas

        obj, created = cls.objects.get_or_create(operario=operario, mes_actual=mes)
        obj.horas_normales = horas_trabajadas
        obj.horas_extras = horas_extras
        obj.horas_nocturnas = horas_nocturnas
        obj.save()
        return obj

    @classmethod
    def calcular_horas_nocturnas(cls, operario, mes):
        registros = RegistroDiario.objects.filter(
            operario=operario,
            hora_fichada__month=mes,
            tipo_movimiento__in=['entrada', 'salida']
        ).order_by('hora_fichada')

        total_nocturnas = timedelta()
        for i in range(0, len(registros), 2):
            if i + 1 < len(registros):
                entrada = registros[i].hora_fichada
                salida = registros[i + 1].hora_fichada

                # Calcular horas nocturnas dentro del intervalo
                nocturnas = cls.calcular_intervalo_nocturno(entrada, salida)
                total_nocturnas += nocturnas  # Sumar solo las horas nocturnas

        return total_nocturnas

    @staticmethod
    def calcular_intervalo_nocturno(entrada, salida):
        inicio_noche = entrada.replace(hour=21, minute=0, second=0)
        fin_noche = entrada.replace(hour=5, minute=0, second=0) + timedelta(days=1)

        total_nocturno = timedelta()

        # Calcular las horas nocturnas dentro del intervalo definido
        if entrada < inicio_noche and salida > inicio_noche:
            entrada = inicio_noche

        if entrada <= fin_noche and salida > fin_noche:
            total_nocturno += fin_noche - entrada
        elif entrada <= fin_noche:
            total_nocturno += salida - entrada

        # Limitar las horas nocturnas a un máximo de 8 horas
        max_horas_nocturnas = timedelta(hours=8)
        if total_nocturno > max_horas_nocturnas:
            total_nocturno = max_horas_nocturnas

        # Redondeo de las horas nocturnas
        if total_nocturno >= timedelta(minutes=45):
            total_nocturno = timedelta(hours=round(total_nocturno.total_seconds() / 3600))
        else:
            total_nocturno = timedelta(minutes=(total_nocturno.total_seconds() // 60))

        return total_nocturno


class RegistroAsistencia(models.Model):
    presente = 'presente'
    ausente = 'ausente'

    estado_asistencia_choices = [
        (presente, '✅ Presente'),
        (ausente, '❌ Ausente'),
    ]

    operario = models.ForeignKey(Operario, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    estado_asistencia = models.CharField(max_length=10, choices=estado_asistencia_choices, default=ausente)

    estado_justificacion = models.BooleanField(default=False,
                                               help_text="Marcar como justificado (1) o no justificado (0)")
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.operario} - {self.fecha} - {self.get_estado_asistencia_display()}"

    def verificar_asistencia(self):
        entradas = RegistroDiario.objects.filter(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada__date=self.fecha
        )
        if entradas.exists():
            self.estado_asistencia = self.presente
        else:
            self.estado_asistencia = self.ausente
        self.save()

    class Meta:
        unique_together = ('operario', 'fecha')


