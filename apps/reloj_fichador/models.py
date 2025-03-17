# models.py

from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta, datetime, time
from simple_history.models import HistoricalRecords
import os
import logging
import threading
from .utils import suppress_signal
from django.conf import settings

logger = logging.getLogger('reloj_fichador')

# ------------------------------------------------------------------------------------
# REGLAS DE HORAS (según tu descripción resumida)
# ------------------------------------------------------------------------------------
# Horas normales (condiciones generales, pero usaremos la nueva franja 06:00 a 20:00).
# Horas nocturnas 20:00 - 06:00 del día siguiente.
#
# Redondeo entrada: sube a la siguiente hora.
# Redondeo salida: baja a la hora anterior, SOLO si >= 8h desde la hora de entrada redondeada.
# ------------------------------------------------------------------------------------

def redondear_entrada(dt):
    """
    Redondea la hora de entrada hacia arriba a la próxima hora completa.
    """
    fecha_base = dt.replace(minute=0, second=0, microsecond=0)
    if dt.minute or dt.second or dt.microsecond:
        # Si hay minutos o segundos, subimos 1 hora
        fecha_base += timedelta(hours=1)
    return fecha_base

def redondear_salida(dt):
    """
    Redondea la hora de salida hacia abajo a la hora completa anterior,
    SOLO si se cumplieron >= 8h desde la hora de entrada redondeada.
    (NOTA: la comprobación real de las 8h la hacemos en el cálculo final).
    """
    # Tu función "pura" de redondeo a la baja es esta:
    return dt.replace(minute=0, second=0, microsecond=0)

def calcular_horas_por_franjas(inicio, fin, limites=None):
    """
    Calcula las horas normales y nocturnas entre dos momentos dados.
    
    Horas normales: Condiciones
    - Entrada válida: Ingreso posterior a las 4 am e inferior a las 21hs
    - Salida válida: Posterior a las 5 am e inferior a las 22hs (siempre posterior a la entrada)
    
    Horas nocturnas: Condiciones
    - Entrada válida: Ingreso posterior a las 20hs o inferior a las 5 am del día siguiente
    - Salida válida: Posterior a las 21hs o inferior a las 6 am del día siguiente (siempre posterior a la entrada)
    
    Args:
        inicio: Timestamp de inicio (datetime)
        fin: Timestamp de fin (datetime)
        limites: Diccionario opcional con los límites de franjas horarias
    
    Returns:
        Tupla (horas_normales, horas_nocturnas) como objetos timedelta
    """
    from django.utils import timezone
    from django.conf import settings
    
    # Solo normalizamos fechas si USE_TZ está habilitado
    if getattr(settings, 'USE_TZ', False):
        # Normalizar fechas de entrada solo si USE_TZ es True
        if hasattr(inicio, 'tzinfo') and inicio.tzinfo is None:
            inicio = timezone.make_aware(inicio)
        if hasattr(fin, 'tzinfo') and fin.tzinfo is None:
            fin = timezone.make_aware(fin)
        
    if limites is None:
        # Valores por defecto para los límites de las franjas
        fecha_base = inicio.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Límites para horas nocturnas (20:00 a 06:00)
        nocturnas_inicio = fecha_base.replace(hour=20)
        nocturnas_fin = (fecha_base + timedelta(days=1)).replace(hour=6)
        
        # Límites para horas normales (04:00 a 22:00)
        normales_inicio = fecha_base.replace(hour=4)
        normales_fin = fecha_base.replace(hour=22)
        
        limites = {
            'nocturnas_inicio': nocturnas_inicio,
            'nocturnas_fin': nocturnas_fin,
            'normales_inicio': normales_inicio,
            'normales_fin': normales_fin
        }
    
    # Inicialización de variables
    actual = inicio  # Punto de inicio actual
    total_normales = timedelta(0)  # Acumulador de horas normales
    total_nocturnas = timedelta(0)  # Acumulador de horas nocturnas
    
    # Mientras no hayamos llegado al final
    while actual < fin:
        # Primero, determinamos el siguiente punto de corte
        # El próximo límite dependerá de en qué franja nos encontramos actualmente
        
        # Inicializamos siguiente como el fin por defecto
        siguiente = fin
        
        # Determinamos los posibles puntos de corte basados en los límites
        posibles_cortes = [fin]
        
        # Añadimos los límites relevantes como posibles puntos de corte
        # Solo consideramos los límites futuros (superiores a actual)
        for key, value in limites.items():
            if value > actual:
                posibles_cortes.append(value)
        
        # El siguiente punto es el mínimo de todos los puntos de corte posibles
        siguiente = min(posibles_cortes)
        
        # Si el siguiente punto calculado es igual a actual, avanzamos 1 hora para evitar bucle infinito
        if siguiente <= actual:
            siguiente = actual + timedelta(hours=1)
            if siguiente > fin:
                siguiente = fin
        
        # Ahora clasificamos el segmento de tiempo según los criterios específicos
        
        # Verificar si cumple los requisitos de Horas Normales
        # Entrada válida: 4am a 21hs + Salida válida: 5am a 22hs
        if ((actual.time() >= time(4, 0) and actual.time() < time(21, 0)) and
            (siguiente.time() >= time(5, 0) and siguiente.time() < time(22, 0))):
            total_normales += siguiente - actual
            
        # Verificar si cumple los requisitos de Horas Nocturnas
        # Entrada válida: 20hs a 5am + Salida válida: 21hs a 6am
        elif ((actual.time() >= time(20, 0) or actual.time() < time(5, 0)) and
              (siguiente.time() >= time(21, 0) or siguiente.time() < time(6, 0))):
            total_nocturnas += siguiente - actual
            
        # Avanzar al siguiente punto de corte
        actual = siguiente
    
    return total_normales, total_nocturnas



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

    history = HistoricalRecords()

    class Meta:
        indexes = [
            models.Index(fields=['apellido']),
            models.Index(fields=['dni']),
        ]

    def __str__(self):
        full_name = f"{self.apellido}"
        if self.seg_apellido:
            full_name += f" {self.seg_apellido}"
        full_name += f", {self.nombre}"
        if self.seg_nombre:
            full_name += f" {self.seg_nombre}"
        return f"{full_name} - {self.dni}"


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # Obtener la extensión
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Solo se permiten archivos PDF, JPG, JPEG o PNG.')


class Licencia(models.Model):
    operario = models.ForeignKey(Operario, on_delete=models.CASCADE, related_name='licencias')
    archivo = models.FileField(upload_to='licencias/', validators=[validate_file_extension])
    descripcion = models.TextField(blank=True, null=True)
    fecha_subida = models.DateField(auto_now_add=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)

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
    operario = models.ForeignKey('Operario', on_delete=models.CASCADE)
    hora_fichada = models.DateTimeField(blank=True, null=True)
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO)
    origen_fichada = models.CharField(max_length=10, default='Auto')
    inconsistencia = models.BooleanField(choices=INCONSISTENCIAS_CHOICES, default=False)
    valido = models.BooleanField(default=True, help_text="Indica si el registro es válido.")
    descripcion_inconsistencia = models.TextField(blank=True, null=True, help_text="Descripción de la inconsistencia, si existe.")

    # Auxiliares para las diferencias
    dif_entrada_salida = models.DurationField(blank=True, null=True, help_text="Diferencia E->S (ciclo 1)")
    dif_entrada_salida2 = models.DurationField(blank=True, null=True, help_text="Diferencia E->S (ciclo 2)")
    dif_entrada_salida_total = models.DurationField(blank=True, null=True, help_text="Suma total de diferencias")

    history = HistoricalRecords()

    class Meta:
        indexes = [
            models.Index(fields=['operario']),
            models.Index(fields=['hora_fichada']),
        ]

    def __str__(self):
        fecha = self.hora_fichada.strftime('%Y/%m/%d %H:%M:%S') if self.hora_fichada else 'Hora no registrada'
        return f"{self.operario} - {self.tipo_movimiento} - {fecha}"

    def get_last_valid_record(self):
        """
        Obtiene el último registro válido para el operario (excluyendo el actual).
        """
        return RegistroDiario.objects.filter(
            operario=self.operario,
            valido=True
        ).exclude(pk=self.pk).order_by('-hora_fichada').first()

    @staticmethod
    def calcular_fecha_logica(hora_fichada):
        """
        Calcula la fecha lógica de un registro en función de si pertenece a un turno nocturno.
        Si la hora es < 06:00, se considera que pertenece al día anterior lógicamente,
        pero permite personalizar cómo manejar las horas tempranas.
        
        Compatible con configuraciones USE_TZ=True o False.
        """
        if not hora_fichada:
            return None

        # Normalizar la fecha si tiene zona horaria y estamos en USE_TZ=False
        from django.conf import settings
        if not getattr(settings, 'USE_TZ', False) and hasattr(hora_fichada, 'tzinfo') and hora_fichada.tzinfo is not None:
            # Quitar la zona horaria si estamos en modo USE_TZ=False
            hora_fichada = hora_fichada.replace(tzinfo=None)

        # Mantener la hora límite para turnos nocturnos
        hora_limite = datetime.strptime("06:00", "%H:%M").time()
        
        # Validar si el turno debe ajustarse al día anterior
        if hora_fichada.time() < hora_limite:
            # Añadir una condición específica si se necesita ajustar para horarios normales
            logger.debug(f"Ajustando fecha lógica para hora temprana: {hora_fichada}")
            return hora_fichada.date() - timedelta(days=1)

        # En caso contrario, mantener la fecha actual
        return hora_fichada.date()


    def calcular_diferencia_entrada_salida(self):
        """
        Calcula la diferencia (redondeada) entre la hora_entrada_redondeada y la hora_salida_real,
        y la almacena en dif_entrada_salida, dif_entrada_salida2, etc., según corresponda.
        """
        if not self.hora_fichada:
            return None

        if self.tipo_movimiento != 'salida':
            return None  # Solo calculamos la diferencia en la salida

        ultima_entrada = RegistroDiario.objects.filter(
            operario=self.operario,
            tipo_movimiento='entrada',
            valido=True,
            hora_fichada__lt=self.hora_fichada
        ).order_by('-hora_fichada').first()

        if not ultima_entrada:
            logger.warning(f"No se encontró una entrada previa válida para {self.operario}.")
            return None

        # Redondeamos la entrada previa
        entrada_redondeada = redondear_entrada(ultima_entrada.hora_fichada)
        diferencia = self.hora_fichada - entrada_redondeada

        # Guardamos en dif_entrada_salida (ciclo 1) o dif_entrada_salida2 (ciclo 2) si ya está ocupado
        if not self.dif_entrada_salida:
            self.dif_entrada_salida = diferencia
        else:
            self.dif_entrada_salida2 = diferencia

        # Sumamos a dif_entrada_salida_total
        acum = timedelta(0)
        if self.dif_entrada_salida:
            acum += self.dif_entrada_salida
        if self.dif_entrada_salida2:
            acum += self.dif_entrada_salida2

        self.dif_entrada_salida_total = acum

        # Establecer la bandera antes de guardar para prevenir recursión
        with suppress_signal():
            self.save(update_fields=['dif_entrada_salida', 'dif_entrada_salida2', 'dif_entrada_salida_total'])


        return diferencia

    def clean(self):
        super().clean()

        from django.conf import settings

        if not self.hora_fichada:
            self.hora_fichada = timezone.now()
            
        # Normalizar la fecha si tiene zona horaria y estamos en USE_TZ=False
        hora_fichada_normalizada = self.hora_fichada
        if not getattr(settings, 'USE_TZ', False) and hasattr(self.hora_fichada, 'tzinfo') and self.hora_fichada.tzinfo is not None:
            hora_fichada_normalizada = self.hora_fichada.replace(tzinfo=None)
            # Actualizar el campo para que sea compatible con SQLite
            self.hora_fichada = hora_fichada_normalizada

        movimiento_fecha = RegistroDiario.calcular_fecha_logica(hora_fichada_normalizada)

        # Mostrar mensaje informativo sobre registros desbalanceados
        print(f"Registros desbalancados para el operario {self.operario} en la fecha {movimiento_fecha}.")

        # Si el registro está marcado como inconsistencia, no validamos la secuencia
        # Esto permite que los operarios puedan registrar movimientos fuera de secuencia si es necesario
        # y que un administrador pueda revisar y decidir posteriormente si son válidos
        if self.inconsistencia:
            # El registro está marcado como inconsistente, omitimos validaciones adicionales
            # Este comportamiento es intencional para que la aplicación no bloquee al operario
            # en caso de que necesite registrar su asistencia a pesar de una inconsistencia
            return
        
        registros_del_dia = RegistroDiario.objects.filter(
            operario=self.operario,
            hora_fichada__date=movimiento_fecha,
            valido=True
        ).exclude(pk=self.pk).order_by('hora_fichada')

        movimientos_del_dia = list(registros_del_dia.values_list('tipo_movimiento', flat=True))
        ultimo_valido = self.get_last_valid_record()
        last_movement = ultimo_valido.tipo_movimiento if ultimo_valido else None
        day_changed = ultimo_valido and ultimo_valido.hora_fichada.date() != movimiento_fecha

        inconsistencias = []

        # Validación básica de secuencia de movimientos
        if not (day_changed or (last_movement == 'salida' and self.tipo_movimiento == 'entrada')):
            transiciones_validas = {
                'entrada': ['salida', 'salida_transitoria'],
                'salida_transitoria': ['entrada_transitoria'],
                'entrada_transitoria': ['salida'],
                'salida': ['entrada']
            }
            if movimientos_del_dia:
                last_today = movimientos_del_dia[-1]
                movimientos_permitidos = transiciones_validas.get(last_today, [])
                if self.tipo_movimiento not in movimientos_permitidos:
                    inconsistencias.append(
                        f"Después de {last_today} solo puede ir {', '.join(movimientos_permitidos)}."
                    )

        if inconsistencias:
            raise ValidationError({'tipo_movimiento': inconsistencias})

class Horas_trabajadas(models.Model):
    operario = models.ForeignKey('Operario', on_delete=models.CASCADE)
    fecha = models.DateField()
    horas_normales = models.DurationField(default=timedelta)
    horas_nocturnas = models.DurationField(default=timedelta)
    horas_extras = models.DurationField(default=timedelta)

    class Meta:
        app_label = 'reloj_fichador'
        verbose_name = "Horas trabajadas"
        verbose_name_plural = "Horas trabajadas"

    @classmethod
    def calcular_horas_trabajadas(cls, operario, fecha):
        """
        Calcula las horas normales, nocturnas y extras para un operario en una fecha lógica específica.
        """
        registros = RegistroDiario.objects.filter(
            operario=operario,
            valido=True
        ).order_by('hora_fichada')

        day_records = [
            r for r in registros 
            if RegistroDiario.calcular_fecha_logica(r.hora_fichada) == fecha
            or (r.hora_fichada.time() < time(6, 0) and r.hora_fichada.date() == fecha)
        ]

        total_horas_normales = timedelta()
        total_horas_nocturnas = timedelta()
        total_horas_extras = timedelta()

        if len(day_records) % 2 != 0:
            logger.warning(f"Registros desbalancados para el operario {operario} en la fecha {fecha}.")
            day_records = day_records[:-1]

        for entrada, salida in zip(day_records[::2], day_records[1::2]):
            if entrada.tipo_movimiento == 'entrada' and salida.tipo_movimiento == 'salida':
                entrada_redondeada = redondear_entrada(entrada.hora_fichada)
                salida_real = salida.hora_fichada

                # Calcular horas normales y nocturnas
                h_norm, h_noct = calcular_horas_por_franjas(entrada_redondeada, salida_real)
                total_horas_normales += h_norm
                total_horas_nocturnas += h_noct

                # Calcular horas extras (si aplica)
                diferencia_total = salida_real - entrada_redondeada
                if diferencia_total > timedelta(hours=8, minutes=30):  # Límite para calcular horas extras
                    exceso = diferencia_total - timedelta(hours=8, minutes=30)
                    # Añadir 30 minutos iniciales.
                    exceso += timedelta(minutes=30)
                    # Convertir el exceso a bloques de 15 minutos
                    bloques_15_min = (exceso.total_seconds() // 900)  # 900 segundos = 15 minutos
                    total_horas_extras += timedelta(minutes=15 * bloques_15_min)

        # Guardar en el modelo
        obj, _ = cls.objects.get_or_create(operario=operario, fecha=fecha)
        obj.horas_normales = total_horas_normales
        obj.horas_nocturnas = total_horas_nocturnas
        obj.horas_extras = total_horas_extras
        obj.save()


        return total_horas_normales, total_horas_nocturnas, total_horas_extras

    def __str__(self):
        return (f"{self.operario} - {self.fecha}: "
                f"Normales: {self.horas_normales}, "
                f"Nocturnas: {self.horas_nocturnas}, "
                f"Extras: {self.horas_extras}")


def calcular_diferencia_entrada_salida(entrada, salida):
    """
    Calcula la diferencia entre entrada y salida ya redondeadas.
    """
    if entrada and salida and salida > entrada:
        return salida - entrada
    return timedelta(0)


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
            horas_feriado = timedelta(hours=8)  # Ejemplo: 8h de feriado
            obj, _ = cls.objects.get_or_create(operario=operario, fecha=fecha)
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
        try:
            horas_trabajadas = Horas_trabajadas.objects.get(operario=operario, fecha=fecha)
            # En vez de recalcular, simplemente leer lo que ya está en horas_trabajadas:
            horas_extras = horas_trabajadas.horas_extras

            obj, _ = cls.objects.update_or_create(
                operario=operario, fecha=fecha,
                defaults={'horas_extras': horas_extras}
            )
            return obj.horas_extras
        except Horas_trabajadas.DoesNotExist:
            logger.warning(f"No se encontraron horas trabajadas para {operario} en {fecha}.")
            return timedelta(0)


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
        from .models import Horas_trabajadas, Horas_extras, Horas_feriado

        mes_inicio = datetime.strptime(mes, '%Y-%m').date().replace(day=1)

        horas_trabajadas = Horas_trabajadas.objects.filter(
            operario=operario,
            fecha__year=mes_inicio.year,
            fecha__month=mes_inicio.month
        ).aggregate(
            total_normales=Sum('horas_normales'),
            total_nocturnas=Sum('horas_nocturnas')
        )

        horas_extras = Horas_extras.objects.filter(
            operario=operario,
            fecha__year=mes_inicio.year,
            fecha__month=mes_inicio.month
        ).aggregate(total=Sum('horas_extras'))['total'] or timedelta()

        horas_feriado = Horas_feriado.objects.filter(
            operario=operario,
            fecha__year=mes_inicio.year,
            fecha__month=mes_inicio.month
        ).aggregate(total=Sum('horas_feriado'))['total'] or timedelta()

        obj, _ = cls.objects.get_or_create(operario=operario, mes_actual=mes)
        obj.horas_normales = horas_trabajadas['total_normales'] or timedelta()
        obj.horas_nocturnas = horas_trabajadas['total_nocturnas'] or timedelta()
        obj.horas_extras = horas_extras
        obj.horas_feriado = horas_feriado
        obj.save()
        return obj


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

    estado_justificacion = models.BooleanField(
        default=False,
        help_text="Marcar como justificado (1) o no justificado (0)"
    )
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.operario} - {self.fecha} - {self.get_estado_asistencia_display()}"

    def verificar_asistencia(self):
        from .models import RegistroDiario
        entradas = RegistroDiario.objects.filter(
            operario=self.operario,
            tipo_movimiento__in=['entrada', 'entrada_transitoria'],
            inconsistencia=False,
            hora_fichada__date=self.fecha,
            valido=True
        )
        if entradas.exists():
            self.estado_asistencia = self.presente
        else:
            self.estado_asistencia = self.ausente
        self.save()

    class Meta:
        unique_together = ('operario', 'fecha')
