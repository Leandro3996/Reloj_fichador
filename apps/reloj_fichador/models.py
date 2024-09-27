from django.db import models
from django.db.models import Sum, F, ExpressionWrapper, fields
from django.utils import timezone
from django.utils.timezone import is_naive, make_aware
from django.core.exceptions import ValidationError
from datetime import timedelta, datetime
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
    foto = models.ImageField(upload_to='operarios_fotos/', null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)


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
    descripcion = models.TextField(blank=True, null=True)
    fecha_subida = models.DateField(auto_now_add=True)
    fecha_inicio = models.DateField(null=True, blank=True)  # Fecha de inicio de la licencia
    fecha_fin = models.DateField(null=True, blank=True)  # Fecha de fin de la licencia

    @property
    def duracion(self):
        if self.fecha_inicio and self.fecha_fin:
            return (self.fecha_fin - self.fecha_inicio).days
        return None

    def __str__(self):
        return f"Licencia {self.archivo.name} para {self.operario.nombre} ({self.duracion} días)"

class RegistroDiario(models.Model):
    TIPO_MOVIMIENTO = [
        ('entrada', 'Entrada'),
        ('salida_transitoria', 'Salida Transitoria'),
        ('entrada_transitoria', 'Entrada Transitoria'),
        ('salida', 'Salida'),
    ]
    INCONSISTENCIAS_CHOICES = [
        (True, 'Inconsistencia'),
        (False, ''),
    ]

    id_registro = models.AutoField(primary_key=True)
    operario = models.ForeignKey(Operario, on_delete=models.CASCADE)
    hora_fichada = models.DateTimeField(blank=True, null=True)
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO)
    origen_fichada = models.CharField(max_length=10, default='Auto')
    inconsistencia = models.BooleanField(choices=INCONSISTENCIAS_CHOICES, default=False)

    def __str__(self):
        return f"{self.operario} - {self.tipo_movimiento} - {self.hora_fichada.strftime('%Y/%m/%d %H:%M:%S')}"

    def clean(self):
        # Validar que la hora de salida no sea anterior a la hora de entrada
        if self.tipo_movimiento == 'salida':
            ultimo_registro = RegistroDiario.objects.filter(operario=self.operario).order_by('-hora_fichada').first()
            if ultimo_registro and ultimo_registro.tipo_movimiento == 'entrada':
                if self.hora_fichada <= ultimo_registro.hora_fichada:
                    self.inconsistencia = "Inconsistencia: La hora de salida no puede ser anterior o igual a la hora de entrada."
                    raise ValidationError(self.inconsistencia)
                else:
                    self.inconsistencia = None  # No hay inconsistencia

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
            hora_fichada__date=fecha + timedelta(days=1)  # Considerar salida después de medianoche
        ).order_by('hora_fichada')

        total_horas_normales = timedelta()
        total_horas_nocturnas = timedelta()

        for i in range(len(entradas)):
            if i < len(salidas):
                entrada = entradas[i].hora_fichada
                salida = salidas[i].hora_fichada

                # Redondeo de la entrada si es necesario
                if entrada.hour >= 20:
                    entrada_redondeada = entrada.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
                elif entrada.hour >= 4 and entrada.hour < 5:
                    entrada_redondeada = entrada.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
                else:
                    entrada_redondeada = entrada

                # Redondeo de la salida si es necesario
                if salida.hour == 5 and salida.minute >= 30:
                    salida_redondeada = salida.replace(minute=0, second=0, microsecond=0)
                else:
                    salida_redondeada = salida

                # Calcular las horas trabajadas desde la entrada redondeada hasta la salida redondeada
                horas_normales, horas_nocturnas = cls.dividir_horas_normales_y_nocturnas(entrada_redondeada, salida_redondeada)

                # Si el operario fichó entrada entre las 20:00 y las 05:00, no puede haber horas normales
                if entrada_redondeada.hour >= 20 or entrada_redondeada.hour < 4:
                    total_horas_nocturnas += horas_nocturnas
                else:
                    total_horas_normales += horas_normales

                # Solo excluir si existe una salida correspondiente
                primera_salida = salidas.first()
                if primera_salida:
                    salidas = salidas.exclude(id_registro=primera_salida.id_registro)
            else:
                # Considerar que el turno sigue hasta el final del día o una hora específica si no hay salida
                salida = datetime.combine(fecha + timedelta(days=1), datetime.max.time())
                horas_normales, horas_nocturnas = cls.dividir_horas_normales_y_nocturnas(entradas[i].hora_fichada, salida)

                if entradas[i].hora_fichada.hour >= 20 or entradas[i].hora_fichada.hour < 4:
                    total_horas_nocturnas += horas_nocturnas
                else:
                    total_horas_normales += horas_normales

        # Aplicar redondeos

        # No redondear horas normales si no se cumplen las 8 horas mínimas
        max_horas_trabajadas = timedelta(hours=8)
        if total_horas_normales > max_horas_trabajadas:
            total_horas_normales = max_horas_trabajadas

        # Redondeo de las horas nocturnas si exceden las 8 horas
        max_horas_nocturnas = timedelta(hours=8)
        if total_horas_nocturnas > max_horas_nocturnas:
            total_horas_nocturnas = max_horas_nocturnas

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
        fin_noche = (entrada + timedelta(days=1)).replace(hour=5, minute=0, second=0)

        horas_normales = timedelta()
        horas_nocturnas = timedelta()

        # Caso 1: Entrada y salida ambas antes de las 21:00 (horario normal)
        if salida <= inicio_noche:
            horas_normales += salida - entrada

        # Caso 2: Entrada antes de las 21:00 y salida después de las 21:00
        elif entrada < inicio_noche and salida > inicio_noche:
            horas_normales += inicio_noche - entrada
            if salida <= fin_noche:
                horas_nocturnas += salida - inicio_noche
            else:
                horas_nocturnas += fin_noche - inicio_noche
                horas_normales += salida - fin_noche

        # Caso 3: Entrada en el rango nocturno y salida en el rango nocturno
        elif entrada >= inicio_noche or entrada < fin_noche:
            if salida <= fin_noche:
                horas_nocturnas += salida - entrada
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
        # Obtener todas las entradas y salidas del día
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

        total_horas_trabajadas = timedelta()
        horas_extras_totales = timedelta()

        for i in range(len(entradas)):
            if i < len(salidas):
                entrada = entradas[i].hora_fichada
                salida = salidas[i].hora_fichada

                # Redondeo de la hora de entrada y salida según la lógica
                entrada_redondeada = entrada.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
                salida_redondeada = salida.replace(minute=0, second=0, microsecond=0) if salida.minute < 30 else salida.replace(minute=30, second=0, microsecond=0)

                total_horas_trabajadas += salida_redondeada - entrada_redondeada

        # Solo considerar horas extras si se supera las 8 horas de trabajo normales
        if total_horas_trabajadas > timedelta(hours=8):
            horas_extras_totales = total_horas_trabajadas - timedelta(hours=8)

            # Aplicar redondeo según las condiciones
            if horas_extras_totales >= timedelta(hours=2, minutes=45):
                horas_extras_totales = timedelta(hours=3)
            if horas_extras_totales >= timedelta(hours=2, minutes=30):
                horas_extras_totales = timedelta(hours=2, minutes=30)
            if horas_extras_totales >= timedelta(hours=1, minutes=45):
                horas_extras_totales = timedelta(hours=2)
            elif horas_extras_totales >= timedelta(hours=1, minutes=30):
                horas_extras_totales = timedelta(hours=1, minutes=30)
            elif horas_extras_totales >= timedelta(hours=1):
                horas_extras_totales = timedelta(hours=1)
            elif horas_extras_totales >= timedelta(minutes=45):
                horas_extras_totales = timedelta(hours=1)
            elif horas_extras_totales >= timedelta(minutes=30):
                horas_extras_totales = timedelta(minutes=30)
            else:
                horas_extras_totales = timedelta(0)

        # Guardar las horas extras calculadas
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
        mes_inicio = datetime.strptime(mes, '%Y-%m').date().replace(day=1)

        # Sumar las horas normales y nocturnas por separado
        horas_trabajadas = Horas_trabajadas.objects.filter(
            operario=operario, fecha__month=mes_inicio.month, fecha__year=mes_inicio.year
        ).aggregate(
            total_normales=Sum('horas_trabajadas'),
            total_nocturnas=Sum('horas_nocturnas')
        )

        horas_extras = Horas_extras.objects.filter(
            operario=operario, fecha__month=mes_inicio.month, fecha__year=mes_inicio.year
        ).aggregate(total=Sum('horas_extras'))['total'] or timedelta()

        obj, created = cls.objects.get_or_create(operario=operario, mes_actual=mes)
        obj.horas_normales = horas_trabajadas['total_normales'] or timedelta()
        obj.horas_nocturnas = horas_trabajadas['total_nocturnas'] or timedelta()
        obj.horas_extras = horas_extras
        obj.save()
        return obj

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


