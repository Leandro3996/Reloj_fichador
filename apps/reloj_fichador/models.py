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
import pytz

logger = logging.getLogger('reloj_fichador')

# ------------------------------------------------------------------------------------
# REGLAS DE HORAS (según tu descripción resumida)
# ------------------------------------------------------------------------------------
# Horas normales (condiciones generales, pero usaremos la nueva franja 06:00 a 20:00).
# Horas nocturnas 20:00 - 06:00 del día siguiente.
#
# Redondeo entrada: a la media hora más cercana:
#   - Si minutos < 15: redondea hacia abajo a la hora en punto
#   - Si minutos entre 15 y 44: redondea a la media hora
#   - Si minutos >= 45: redondea hacia arriba a la siguiente hora
# Redondeo salida: baja a la hora anterior, SOLO si >= 8h desde la hora de entrada redondeada.
# ------------------------------------------------------------------------------------

class ConfiguracionRedondeo(models.Model):
    minutos_redondeo_baja = models.PositiveSmallIntegerField(
        default=15,
        help_text="Minutos máximos para redondear hacia la hora en punto. Ejemplo: con 15, 09:14 se redondea a 09:00."
    )
    minutos_redondeo_media = models.PositiveSmallIntegerField(
        default=45,
        help_text="Minutos máximos para redondear a la media hora. Ejemplo: con 45, 09:30 a 09:44 se redondea a 09:30."
    )

    class Meta:
        verbose_name = "Configuración de Redondeo"
        verbose_name_plural = "Configuración de Redondeo"

    def __str__(self):
        return "Configuración de Redondeo de Entrada"
    
class ConfiguracionRedondeoSalida(models.Model):
    minutos_redondeo_salida = models.PositiveSmallIntegerField(
        default=0,
        help_text="Minutos a los que se redondea la salida hacia abajo. Ejemplo: con 0, 17:23 se redondea a 17:00."
    )

    class Meta:
        verbose_name = "Configuración de Redondeo de Salida"
        verbose_name_plural = "Configuración de Redondeo de Salida"

    def __str__(self):
        return "Configuración de Redondeo de Salida"

def redondear_entrada(dt):
    """
    Redondea la hora de entrada según los límites configurados en ConfiguracionRedondeo.
    """
    import pytz
    argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
    if dt.tzinfo is not None:
        dt_local = dt.astimezone(argentina_tz)
    else:
        dt_local = argentina_tz.localize(dt)

    minutos = dt_local.minute

    # Obtener configuración (toma la primera, o usa valores por defecto)
    config = ConfiguracionRedondeo.objects.first()
    min_baja = config.minutos_redondeo_baja if config else 15
    min_media = config.minutos_redondeo_media if config else 45

    if minutos < min_baja:
        fecha_base = dt_local.replace(minute=0, second=0, microsecond=0)
    elif minutos < min_media:
        fecha_base = dt_local.replace(minute=30, second=0, microsecond=0)
    else:
        fecha_base = dt_local.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

    return fecha_base

def redondear_salida(dt):
    """
    Redondea la hora de salida hacia abajo según la configuración.
    """
    import pytz
    argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
    if dt.tzinfo is not None:
        dt_local = dt.astimezone(argentina_tz)
    else:
        dt_local = argentina_tz.localize(dt)

    config = ConfiguracionRedondeoSalida.objects.first()
    min_salida = config.minutos_redondeo_salida if config else 0

    # Redondear hacia abajo a la hora anterior más los minutos configurados
    fecha_base = dt_local.replace(minute=min_salida, second=0, microsecond=0)
    if dt_local.minute < min_salida:
        fecha_base -= timedelta(hours=1)
    return fecha_base

def calcular_horas_por_franjas(inicio, fin, limites=None):
    """
    Lógica simplificada:
    - Si entrada y salida son el mismo día: todo normal.
    - Si entrada y salida son días distintos y la entrada es >= 20:00: todo nocturno.
    - Si entrada y salida son el mismo día y la entrada es >= 20:00: todo nocturno.
    """
    argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
    if inicio.tzinfo is not None:
        inicio = inicio.astimezone(argentina_tz)
    else:
        inicio = argentina_tz.localize(inicio)
    if fin.tzinfo is not None:
        fin = fin.astimezone(argentina_tz)
    else:
        fin = argentina_tz.localize(fin)

    # Si entrada y salida son el mismo día
    if inicio.date() == fin.date():
        if inicio.time() >= time(20, 0):
            # Todo nocturno
            return timedelta(0), fin - inicio
        else:
            # Todo normal
            return fin - inicio, timedelta(0)
    else:
        # Días distintos: si la entrada es >= 20:00, todo nocturno
        if inicio.time() >= time(20, 0):
            return timedelta(0), fin - inicio
        else:
            # Todo normal (caso poco frecuente)
            return fin - inicio, timedelta(0)


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
    ESTADO_CHOICES = [
        ('pendiente', '⏳ Pendiente'),
        ('aprobada', '✅ Aprobada'),
        ('rechazada', '❌ Rechazada'),
    ]
    
    operario = models.ForeignKey(Operario, on_delete=models.CASCADE, related_name='licencias')
    archivo = models.FileField(upload_to='licencias/', validators=[validate_file_extension], 
                                blank=True, null=True, help_text="Archivo adjunto (opcional)")
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción o motivo de la licencia")
    fecha_subida = models.DateField(auto_now_add=True)
    fecha_inicio = models.DateField(null=True, blank=True, help_text="Fecha de inicio de la licencia")
    fecha_fin = models.DateField(null=True, blank=True, help_text="Fecha de fin de la licencia")
    
    # Nuevos campos para integración con asistencia
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente', 
                             help_text="Estado de aprobación de la licencia")
    aplicar_a_asistencia = models.BooleanField(default=True, 
                                             help_text="Si está marcado, justificará automáticamente las ausencias en el período")
    
    # Campos de auditoría
    aprobada_por = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True,
                                   help_text="Usuario que aprobó/rechazó la licencia")
    fecha_aprobacion = models.DateTimeField(null=True, blank=True,
                                          help_text="Fecha y hora de aprobación/rechazo")
    observaciones = models.TextField(blank=True, null=True,
                                   help_text="Observaciones del aprobador")

    history = HistoricalRecords()

    class Meta:
        indexes = [
            models.Index(fields=['operario', 'fecha_inicio']),
            models.Index(fields=['estado']),
        ]

    @property
    def duracion(self):
        if self.fecha_inicio and self.fecha_fin:
            return (self.fecha_fin - self.fecha_inicio).days + 1  # +1 para incluir ambos días
        return None

    def clean(self):
        super().clean()
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_inicio > self.fecha_fin:
                raise ValidationError({'fecha_fin': 'La fecha de fin debe ser posterior a la fecha de inicio.'})
            
            # Validar que no se solapen con otras licencias aprobadas del mismo operario
            if self.estado == 'aprobada':
                licencias_existentes = Licencia.objects.filter(
                    operario=self.operario,
                    estado='aprobada',
                    fecha_inicio__lte=self.fecha_fin,
                    fecha_fin__gte=self.fecha_inicio
                ).exclude(pk=self.pk)
                
                if licencias_existentes.exists():
                    raise ValidationError('Ya existe una licencia aprobada que se solapa con este período.')

    def save(self, *args, **kwargs):
        # Si se está aprobando la licencia, registrar fecha y procesar con Celery
        es_aprobacion_nueva = False
        if self.pk:
            try:
                original = Licencia.objects.get(pk=self.pk)
                if original.estado != 'aprobada' and self.estado == 'aprobada':
                    self.fecha_aprobacion = timezone.now()
                    es_aprobacion_nueva = True
            except Licencia.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        # Procesar asistencia de forma asíncrona después de guardar
        # (Celery ejecutará después, pero también procesa de forma síncrona para visibilidad)
        if es_aprobacion_nueva:
            from .tasks import procesar_licencia_aprobada
            # Ejecutar de forma síncrona para que el usuario vea los cambios inmediatamente
            procesar_licencia_aprobada(self.pk)
            # Alternativamente, descomentar para ejecutar de forma asíncrona (más performante):
            # procesar_licencia_aprobada.delay(self.pk)

    def actualizar_asistencia(self):
        """
        Método legacy para compatibilidad. El procesamiento real
        se hace de forma asíncrona en tasks.procesar_licencia_aprobada
        """
        if self.estado == 'aprobada':
            from .tasks import procesar_licencia_aprobada
            # Ejecutar inmediatamente si es necesario (para comandos de management)
            return procesar_licencia_aprobada.delay(self.pk)
        return None

    def __str__(self):
        duracion_str = f" ({self.duracion} días)" if self.duracion else ""
        estado_str = f" - {self.get_estado_display()}"
        return f"Licencia para {self.operario.apellido}, {self.operario.nombre}{duracion_str}{estado_str}"


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
        Ordena por ID para obtener el registro creado más recientemente.
        """
        return RegistroDiario.objects.filter(
            operario=self.operario,            
            valido=True
        ).exclude(pk=self.pk).order_by('-id_registro').first()

    @staticmethod
    def calcular_fecha_logica(hora_fichada, tipo_movimiento=None):
        """
        Calcula la fecha lógica de un registro en función de si pertenece a un turno nocturno.
        Si la hora es < 06:00 y es un registro de salida, se considera que pertenece al día anterior lógicamente.
        Para las entradas tempranas (antes de las 6am), se mantiene la fecha real.
        
        Args:
            hora_fichada: La hora del registro
            tipo_movimiento: El tipo de movimiento ('entrada', 'salida', etc). Si no se proporciona,
                             se aplica la regla general (entradas < 6am pertenecen al día actual)
        
        Siempre opera en horario de Argentina.
        """
        if not hora_fichada:
            return None

        import pytz
        argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')

        # Si el datetime tiene tzinfo, convertir a horario local
        if hora_fichada.tzinfo is not None:
            hora_local = hora_fichada.astimezone(argentina_tz)
        else:
            hora_local = argentina_tz.localize(hora_fichada)

        hora_limite = datetime.strptime("06:00", "%H:%M").time()
        
        # Si es una entrada temprana, no ajustamos la fecha lógica
        if tipo_movimiento == 'entrada' and hora_local.time() < hora_limite:
            logger.debug(f"Entrada temprana: Manteniendo fecha real para {hora_local}")
            return hora_local.date()
            
        # Para salidas y otros casos, aplicamos la regla estándar
        if hora_local.time() < hora_limite:
            logger.debug(f"Ajustando fecha lógica para hora temprana: {hora_local}")
            return hora_local.date() - timedelta(days=1)
            
        return hora_local.date()


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
        import pytz
        import inspect

        if not self.hora_fichada:
            self.hora_fichada = timezone.now()
            
        # Normalizar la fecha según la configuración de USE_TZ
        hora_fichada_normalizada = self.hora_fichada
        if getattr(settings, 'USE_TZ', False):
            # Si USE_TZ=True, asegurarse de que la fecha esté en la zona horaria de Argentina
            argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
            if hora_fichada_normalizada.tzinfo is None:
                hora_fichada_normalizada = pytz.utc.localize(hora_fichada_normalizada)
            hora_fichada_normalizada = hora_fichada_normalizada.astimezone(argentina_tz)
        elif hasattr(hora_fichada_normalizada, 'tzinfo') and hora_fichada_normalizada.tzinfo is not None:
            # Si USE_TZ=False pero tiene zona horaria, quitarla
            hora_fichada_normalizada = hora_fichada_normalizada.replace(tzinfo=None)
            # Actualizar el campo para que sea compatible con la base de datos
            self.hora_fichada = hora_fichada_normalizada

        movimiento_fecha = RegistroDiario.calcular_fecha_logica(hora_fichada_normalizada, self.tipo_movimiento)

        # Si el registro está marcado como inconsistencia, no validamos la secuencia
        if self.inconsistencia:
            return
        
        # Detectar si la llamada viene del admin de Django
        es_desde_admin = False
        for frame_info in inspect.stack():
            if 'django/contrib/admin' in frame_info.filename or 'admin.py' in frame_info.filename:
                es_desde_admin = True
                break
        
        # Si viene desde admin, permitir cualquier secuencia para correcciones manuales
        if es_desde_admin:
            return
        
        inconsistencias = []
        
        # Obtener el último registro válido
        ultimo_valido = self.get_last_valid_record()
        
        if self.tipo_movimiento == 'entrada':
            if ultimo_valido:
                # Validación desde template: solo permitir entrada después de salida
                if ultimo_valido.tipo_movimiento != 'salida':
                    argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
                    hora_local = ultimo_valido.hora_fichada.astimezone(argentina_tz)
                    fecha_ultimo = hora_local.strftime('%d/%m/%Y %H:%M:%S')
                    inconsistencias.append(
                        f"Inconsistencia: Su último movimiento fue <strong>{ultimo_valido.get_tipo_movimiento_display()}</strong> <strong>{fecha_ultimo}</strong>"
                    )
                
                # Validación 2: Convertida a advertencia
                if self.hora_fichada <= ultimo_valido.hora_fichada:
                    logger.warning(f"Advertencia: Entrada ({self.hora_fichada}) menor o igual a última salida ({ultimo_valido.hora_fichada})")
                    # No agregamos a inconsistencias para permitir el registro
        
        elif self.tipo_movimiento == 'salida':
            # Validación 3: No puede haber una salida sin una entrada previa en el mismo día
            entrada_del_dia = RegistroDiario.objects.filter(
                operario=self.operario,
                tipo_movimiento='entrada',
                hora_fichada__date=movimiento_fecha,
                valido=True
            ).exists()
            
            if not entrada_del_dia:
                inconsistencias.append(
                    "<span style='color: orange; font-weight: bold;'>Atención: Usted no ha registrado una ENTRADA el día de hoy.</span>"
                )

        elif self.tipo_movimiento in ['salida_transitoria', 'entrada_transitoria']:
            # Validación para movimientos transitorios: permitir si hay una ENTRADA válida previa (aunque sea de la jornada lógica anterior)
            ultima_entrada = RegistroDiario.objects.filter(
                operario=self.operario,
                tipo_movimiento='entrada',
                valido=True,
                hora_fichada__lt=self.hora_fichada
            ).order_by('-id_registro').first()

            if not ultima_entrada:
                inconsistencias.append(
                    "<span style='color: orange; font-weight: bold;'>Atención: Los movimientos transitorios solo son válidos después de una ENTRADA.</span>"
                )


        # Validación de secuencia de movimientos desde la última ENTRADA (jornada lógica)
        # 1. Buscar la última ENTRADA antes de la hora fichada actual
        ultima_entrada = RegistroDiario.objects.filter(
            operario=self.operario,
            tipo_movimiento='entrada',
            hora_fichada__lt=self.hora_fichada,
            valido=True
        ).order_by('-id_registro').first()

        if ultima_entrada:
            # 2. Tomar todos los movimientos válidos desde esa ENTRADA hasta el actual (excluyendo el actual)
            registros_jornada = RegistroDiario.objects.filter(
                operario=self.operario,
                id_registro__gt=ultima_entrada.id_registro,
                valido=True
            ).exclude(pk=self.pk).order_by('id_registro')
            movimientos_jornada = ['entrada'] + list(registros_jornada.values_list('tipo_movimiento', flat=True))
        else:
            # Si no hay ENTRADA previa, usar los movimientos del día como fallback
            registros_jornada = RegistroDiario.objects.filter(
                operario=self.operario,
                hora_fichada__date=movimiento_fecha,
                valido=True
            ).exclude(pk=self.pk).order_by('id_registro')
            movimientos_jornada = list(registros_jornada.values_list('tipo_movimiento', flat=True))

        last_movement = movimientos_jornada[-1] if movimientos_jornada else None
        day_changed = ultimo_valido and ultimo_valido.hora_fichada.date() != movimiento_fecha

        # Validación básica de secuencia de movimientos
        if not (day_changed or (last_movement == 'salida' and self.tipo_movimiento == 'entrada')):
            transiciones_validas = {
                'entrada': ['salida', 'salida_transitoria'],
                'salida_transitoria': ['entrada_transitoria'],
                'entrada_transitoria': ['salida'],
                'salida': ['entrada']
            }
            if movimientos_jornada:
                last_today = movimientos_jornada[-1]
                movimientos_permitidos = transiciones_validas.get(last_today, [])
                if self.tipo_movimiento not in movimientos_permitidos:
                    # Obtener el objeto RegistroDiario correspondiente al último movimiento para usar get_tipo_movimiento_display()
                    ultimo_registro = registros_jornada.last() if registros_jornada else None
                    if ultimo_registro:
                        argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
                        hora_local = ultimo_registro.hora_fichada.astimezone(argentina_tz)
                        fecha_ultimo = hora_local.strftime('%d/%m/%Y %H:%M:%S')
                        tipo_movimiento_display = ultimo_registro.get_tipo_movimiento_display()
                    else:
                        fecha_ultimo = ''
                        tipo_movimiento_display = last_today
                    inconsistencias.append(
                        f"Inconsistencia: Su último movimiento fue <strong>{tipo_movimiento_display}</strong> <strong>{fecha_ultimo}</strong>"
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
        registros = RegistroDiario.objects.filter(
            operario=operario,
            valido=True
        ).order_by('hora_fichada')

        day_records = [
            r for r in registros
            if (
                r.tipo_movimiento in ('entrada', 'salida') and
                RegistroDiario.calcular_fecha_logica(r.hora_fichada, r.tipo_movimiento) == fecha
            )
        ]

        if len(day_records) % 2 != 0:
            logger.warning(f"Registros desbalancados para el operario {operario} en la fecha {fecha}.")
            day_records = day_records[:-1]

        total_normales = timedelta()
        total_nocturnas = timedelta()
        for entrada, salida in zip(day_records[::2], day_records[1::2]):
            entrada_redondeada = redondear_entrada(entrada.hora_fichada)
            salida_real = salida.hora_fichada
            # Usar la lógica simplificada para clasificar el bloque
            normales, nocturnas = calcular_horas_por_franjas(entrada_redondeada, salida_real)
            total_normales += normales
            total_nocturnas += nocturnas

        # Determinar el tipo de jornada principal
        if total_nocturnas >= total_normales:
            horas_jornada = min(total_nocturnas + total_normales, timedelta(hours=8))
            horas_normales = timedelta()
            horas_nocturnas = horas_jornada
        else:
            horas_jornada = min(total_nocturnas + total_normales, timedelta(hours=8))
            horas_normales = horas_jornada
            horas_nocturnas = timedelta()

        total_trabajado = total_nocturnas + total_normales
        excedente = total_trabajado - timedelta(hours=8)

        horas_extras = timedelta()
        if excedente >= timedelta(minutes=30):
            # Convertir excedente a minutos totales
            minutos_excedente = int(excedente.total_seconds() / 60)
            
            # Redondear a bloques de 30 minutos hacia abajo
            bloques_30_min = minutos_excedente // 30
            horas_extras = timedelta(minutes=30 * bloques_30_min)
        else:
            horas_extras = timedelta()

        obj, _ = cls.objects.get_or_create(operario=operario, fecha=fecha)
        obj.horas_normales = horas_normales
        obj.horas_nocturnas = horas_nocturnas
        obj.horas_extras = horas_extras
        obj.save()

        return horas_normales, horas_nocturnas, horas_extras

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


class HorasEnfermedad(models.Model):
    """
    Modelo para registrar horas de enfermedad acumuladas por licencias médicas.
    Cada vez que se aprueba una licencia médica, se crea un registro aquí
    para auditoría y tracking.
    """
    operario = models.ForeignKey(Operario, on_delete=models.CASCADE)
    licencia = models.ForeignKey('Licencia', on_delete=models.SET_NULL, null=True, blank=True)
    horas_enfermedad = models.DurationField(default=timedelta,
                                           help_text="Horas de enfermedad de esta licencia (duracion × 8h)")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    mes_periodo = models.CharField(max_length=20,
                                   help_text="Mes al que corresponden estas horas (YYYY-MM)")

    class Meta:
        app_label = 'reloj_fichador'
        verbose_name = "Horas enfermedad"
        verbose_name_plural = "Horas enfermedad"
        indexes = [
            models.Index(fields=['operario', 'mes_periodo']),
            models.Index(fields=['licencia']),
        ]

    def __str__(self):
        horas = int(self.horas_enfermedad.total_seconds() / 3600)
        return f"{self.operario} - {horas}h enfermedad - {self.mes_periodo}"


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
    horas_enfermedad = models.DurationField(default=timedelta,
                                           help_text="Horas acumuladas por licencias médicas aprobadas")

    class Meta:
        app_label = 'reloj_fichador'
        verbose_name = "Horas totales"
        verbose_name_plural = "Horas totales"

    @classmethod
    def calcular_horas_totales(cls, operario, mes):
        from .models import Horas_trabajadas, Horas_extras, Horas_feriado, HorasEnfermedad

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

        # Sumar horas de enfermedad acumuladas por licencias médicas
        horas_enfermedad = HorasEnfermedad.objects.filter(
            operario=operario,
            mes_periodo=mes
        ).aggregate(total=Sum('horas_enfermedad'))['total'] or timedelta()

        obj, _ = cls.objects.get_or_create(operario=operario, mes_actual=mes)
        obj.horas_normales = horas_trabajadas['total_normales'] or timedelta()
        obj.horas_nocturnas = horas_trabajadas['total_nocturnas'] or timedelta()
        obj.horas_extras = horas_extras
        obj.horas_feriado = horas_feriado
        obj.horas_enfermedad = horas_enfermedad
        obj.save()
        return obj


# Modelo proxy para los reportes
class Reporte(RegistroDiario):
    """Modelo proxy para la sección de reportes"""
    class Meta:
        proxy = True
        verbose_name = "Reporte"
        verbose_name_plural = "📊 Reportes"


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
    
    # Campo para vincular con licencias
    licencia_relacionada = models.ForeignKey('Licencia', on_delete=models.SET_NULL, null=True, blank=True,
                                           help_text="Licencia que justifica esta ausencia")

    def __str__(self):
        justificacion = " (Justificado)" if self.estado_justificacion else ""
        return f"{self.operario} - {self.fecha} - {self.get_estado_asistencia_display()}{justificacion}"

    def verificar_asistencia(self):
        """
        Verifica la asistencia basándose en registros de entrada y licencias aprobadas
        """
        from .models import RegistroDiario
        
        # Primero verificar si hay registros de entrada
        entradas = RegistroDiario.objects.filter(
            operario=self.operario,
            tipo_movimiento__in=['entrada', 'entrada_transitoria'],
            inconsistencia=False,
            hora_fichada__date=self.fecha,
            valido=True
        )
        
        if entradas.exists():
            self.estado_asistencia = self.presente
            # Si está presente, no necesita justificación por licencia
            if self.licencia_relacionada:
                self.licencia_relacionada = None
                self.estado_justificacion = False
                self.descripcion = None
        else:
            self.estado_asistencia = self.ausente
            # Verificar si hay una licencia aprobada que cubra esta fecha
            self.verificar_licencia()
        
        self.save()

    def verificar_licencia(self):
        """
        Verifica si existe una licencia aprobada que justifique la ausencia en esta fecha
        """
        licencia = Licencia.objects.filter(
            operario=self.operario,
            estado='aprobada',
            aplicar_a_asistencia=True,
            fecha_inicio__lte=self.fecha,
            fecha_fin__gte=self.fecha
        ).first()
        
        if licencia:
            self.estado_justificacion = True
            self.licencia_relacionada = licencia
            if not self.descripcion or 'licencia' not in self.descripcion.lower():
                self.descripcion = f'Ausencia justificada por licencia (ID: {licencia.pk})'
            logger.info(f'Ausencia justificada automáticamente para {self.operario} el {self.fecha} por licencia {licencia.pk}')
        else:
            # Si no hay licencia y no hay justificación manual, marcar como no justificado
            if self.licencia_relacionada:
                self.licencia_relacionada = None
                self.estado_justificacion = False
                # Solo limpiar descripción si era automática
                if self.descripcion and 'licencia' in self.descripcion.lower():
                    self.descripcion = None

    @property
    def es_ausencia_justificada_por_licencia(self):
        """
        Retorna True si la ausencia está justificada por una licencia
        """
        return self.estado_justificacion and self.licencia_relacionada is not None

    class Meta:
        unique_together = ('operario', 'fecha')
        indexes = [
            models.Index(fields=['operario', 'fecha']),
            models.Index(fields=['estado_asistencia', 'estado_justificacion']),
        ]


# ------------------------------------------------------------------------------------
# MODELOS PARA CALENDARIO LABORAL Y GRUPOS DE SÁBADO
# ------------------------------------------------------------------------------------

class CalendarioLaboral(models.Model):
    """
    Modelo para definir días especiales (feriados, paros, mantenimiento, etc.)
    Por defecto, cualquier fecha no registrada es día laboral normal.
    """
    TIPO_DIA_CHOICES = [
        ('laboral', '✅ Día Laboral Normal'),
        ('feriado', '🎉 Feriado Nacional'),
        ('feriado_movible', '📅 Feriado Movible'),
        ('paro', '✊ Paro/Conflicto Laboral'),
        ('mantenimiento', '🔧 Mantenimiento/Clausura'),
        ('otro', '❓ Otro'),
    ]

    fecha = models.DateField(unique=True, help_text="Fecha del día especial")
    tipo_dia = models.CharField(
        max_length=20,
        choices=TIPO_DIA_CHOICES,
        default='laboral',
        help_text="Tipo de día especial"
    )
    nombre = models.CharField(
        max_length=100,
        help_text="Nombre del evento (ej: Día de la Independencia, Paro General)"
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        help_text="Descripción detallada del evento"
    )
    aplica_a_todas_areas = models.BooleanField(
        default=True,
        help_text="Si está desmarcado, solo aplica a las áreas seleccionadas"
    )
    areas = models.ManyToManyField(
        Area,
        blank=True,
        help_text="Áreas afectadas (si no aplica a todas)"
    )
    creado_el = models.DateTimeField(auto_now_add=True)
    actualizado_el = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Calendario Laboral"
        verbose_name_plural = "Calendarios Laborales"
        ordering = ['fecha']
        indexes = [
            models.Index(fields=['fecha']),
            models.Index(fields=['tipo_dia']),
        ]

    def __str__(self):
        return f"{self.fecha} - {self.get_tipo_dia_display()} - {self.nombre}"

    def es_no_laboral(self):
        """Retorna True si el día NO es laboral (es feriado, paro, etc.)"""
        return self.tipo_dia != 'laboral'


class GrupoSabado(models.Model):
    """
    Modelo para asignar operarios a grupos de sábado (A/B).
    Grupo A: trabaja semanas pares de sábado
    Grupo B: trabaja semanas impares de sábado
    """
    GRUPO_CHOICES = [
        ('A', 'Grupo A - Semanas Pares'),
        ('B', 'Grupo B - Semanas Impares'),
    ]

    operario = models.ForeignKey(
        Operario,
        on_delete=models.CASCADE,
        related_name='grupos_sabado',
        help_text="Operario asignado"
    )
    grupo = models.CharField(
        max_length=1,
        choices=GRUPO_CHOICES,
        help_text="Grupo de sábado del operario"
    )
    fecha_inicio = models.DateField(
        help_text="Fecha desde la que tiene efecto esta asignación"
    )
    fecha_fin = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha hasta la que tiene efecto (NULL = indefinido)"
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        help_text="Motivo del cambio de grupo (opcional)"
    )
    creado_el = models.DateTimeField(auto_now_add=True)
    actualizado_el = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Grupo de Sábado"
        verbose_name_plural = "Grupos de Sábado"
        ordering = ['operario', '-fecha_inicio']
        indexes = [
            models.Index(fields=['operario', 'fecha_inicio']),
            models.Index(fields=['grupo']),
        ]

    def __str__(self):
        fecha_fin_str = self.fecha_fin.strftime('%Y-%m-%d') if self.fecha_fin else "Indefinido"
        return f"{self.operario} - {self.get_grupo_display()} ({self.fecha_inicio} a {fecha_fin_str})"

    def is_active(self, fecha=None):
        """Verifica si esta asignación está activa en una fecha determinada"""
        if fecha is None:
            fecha = timezone.now().date()

        if self.fecha_fin:
            return self.fecha_inicio <= fecha <= self.fecha_fin
        else:
            return fecha >= self.fecha_inicio

    def clean(self):
        """Validación: no puede haber dos grupos activos simultáneamente para el mismo operario"""
        from django.core.exceptions import ValidationError

        if self.fecha_fin and self.fecha_inicio > self.fecha_fin:
            raise ValidationError("La fecha de inicio no puede ser posterior a la de fin.")

        # Verificar solapamientos con otros grupos
        overlapping = GrupoSabado.objects.filter(
            operario=self.operario
        ).exclude(pk=self.pk)

        for otro in overlapping:
            # Caso 1: Este grupo es indefinido
            if not self.fecha_fin:
                if not otro.fecha_fin and otro.fecha_inicio <= self.fecha_inicio:
                    raise ValidationError(
                        f"Ya existe un grupo asignado indefinidamente desde {otro.fecha_inicio}. "
                        f"Finaliza primero ese grupo."
                    )
                elif otro.fecha_fin and otro.fecha_fin >= self.fecha_inicio:
                    raise ValidationError(
                        f"Hay solapamiento con grupo existente ({otro.fecha_inicio} a {otro.fecha_fin})"
                    )
            # Caso 2: Ambos tienen fecha fin
            elif otro.fecha_fin:
                if not (self.fecha_fin < otro.fecha_inicio or self.fecha_inicio > otro.fecha_fin):
                    raise ValidationError(
                        f"Hay solapamiento con grupo existente ({otro.fecha_inicio} a {otro.fecha_fin})"
                    )
            # Caso 3: El otro es indefinido
            else:
                if otro.fecha_inicio <= self.fecha_fin:
                    raise ValidationError(
                        f"Hay solapamiento con grupo indefinido desde {otro.fecha_inicio}"
                    )


# ------------------------------------------------------------------------------------
# MODELO PARA SUGERENCIAS DE FERIADOS DESDE API
# ------------------------------------------------------------------------------------

class SugerenciaFeriado(models.Model):
    """
    Modelo para almacenar sugerencias de feriados obtenidas de la API ArgentinaDatos.
    El administrador puede aceptar o rechazar cada sugerencia.
    """
    TIPO_SUGERENCIA_CHOICES = [
        ('feriado_nacional', '🎉 Feriado Nacional'),
        ('feriado_movible', '📅 Feriado Movible'),
        ('otro', '❓ Otro'),
    ]

    FUENTE_CHOICES = [
        ('api_argentina', 'API ArgentinaDatos'),
        ('manual', 'Ingresado Manualmente'),
        ('sistema', 'Sistema Automático'),
    ]

    ESTADO_CHOICES = [
        ('pendiente', '⏳ Pendiente'),
        ('aceptado', '✅ Aceptado'),
        ('rechazado', '❌ Rechazado'),
        ('revisado_despues', '🔄 Revisar Después'),
    ]

    fecha = models.DateField(help_text="Fecha sugerida del feriado")
    nombre = models.CharField(
        max_length=200,
        help_text="Nombre del feriado (ej: Año Nuevo, Carnaval)"
    )
    tipo_sugerencia = models.CharField(
        max_length=20,
        choices=TIPO_SUGERENCIA_CHOICES,
        default='otro',
        help_text="Tipo de feriado"
    )
    fuente = models.CharField(
        max_length=20,
        choices=FUENTE_CHOICES,
        default='api_argentina',
        help_text="De dónde proviene la sugerencia"
    )
    fuente_url = models.URLField(
        null=True,
        blank=True,
        help_text="URL desde donde se obtuvo la sugerencia"
    )
    datos_fuente = models.JSONField(
        null=True,
        blank=True,
        help_text="Datos originales provistos por la fuente (JSON completo)"
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        help_text="Estado actual de la sugerencia"
    )
    nota_admin = models.TextField(
        blank=True,
        null=True,
        help_text="Notas del administrador (ej: por qué se rechazó)"
    )

    # Auditoría
    fecha_creada = models.DateTimeField(auto_now_add=True)
    fecha_procesada = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Fecha en que se procesó la sugerencia"
    )
    procesado_por = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Usuario que procesó la sugerencia"
    )

    class Meta:
        verbose_name = "Sugerencia de Feriado"
        verbose_name_plural = "Sugerencias de Feriados"
        ordering = ['estado', '-fecha_creada']
        indexes = [
            models.Index(fields=['fecha']),
            models.Index(fields=['estado']),
            models.Index(fields=['fuente']),
        ]
        unique_together = ('fecha', 'fuente')  # No duplicados de la misma fuente

    def __str__(self):
        return f"{self.fecha} - {self.nombre} ({self.get_estado_display()})"

    def aceptar(self, usuario=None):
        """Acepta la sugerencia y crea CalendarioLaboral"""
        from django.utils import timezone

        self.estado = 'aceptado'
        self.fecha_procesada = timezone.now()
        self.procesado_por = usuario
        self.save()

        # Crear entrada en CalendarioLaboral si no existe
        tipo_dia_map = {
            'feriado_nacional': 'feriado',
            'feriado_movible': 'feriado_movible',
            'otro': 'otro',
        }

        CalendarioLaboral.objects.get_or_create(
            fecha=self.fecha,
            defaults={
                'tipo_dia': tipo_dia_map.get(self.tipo_sugerencia, 'otro'),
                'nombre': self.nombre,
                'descripcion': f'Importado de {self.get_fuente_display()}',
            }
        )

        logger.info(f'Sugerencia de feriado aceptada: {self.fecha} - {self.nombre}')

    def rechazar(self, usuario=None, nota=''):
        """Rechaza la sugerencia"""
        from django.utils import timezone

        self.estado = 'rechazado'
        self.fecha_procesada = timezone.now()
        self.procesado_por = usuario
        if nota:
            self.nota_admin = nota
        self.save()

        logger.info(f'Sugerencia de feriado rechazada: {self.fecha} - {self.nombre}')

    @property
    def ya_existe_en_calendario(self):
        """Verifica si ya existe en CalendarioLaboral"""
        return CalendarioLaboral.objects.filter(fecha=self.fecha).exists()

    @property
    def es_proximo(self):
        """Verifica si el feriado es próximo (próximos 30 días)"""
        from datetime import timedelta
        from django.utils import timezone

        hoy = timezone.now().date()
        fecha_limite = hoy + timedelta(days=30)
        return hoy <= self.fecha <= fecha_limite
