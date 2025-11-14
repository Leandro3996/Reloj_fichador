from celery import shared_task
from django.utils import timezone
from .models import Operario, RegistroAsistencia, Licencia
from .utils import es_dia_laboral, calcular_horas_enfermedad_laborales
from datetime import timedelta
import logging

logger = logging.getLogger('reloj_fichador')

@shared_task
def generar_registros_asistencia():
    """
    Esta tarea genera registros de asistencia para todos los operarios activos en la fecha actual.
    SOLO genera registros para días laborales (lunes-viernes, sábados programados, excluye domingos y feriados).
    Si el registro ya existe, verifica la asistencia.
    """
    hoy = timezone.now().date()
    operarios_activos = Operario.objects.filter(activo=True)

    # Validar si hoy es día laboral
    if not es_dia_laboral(hoy):
        logger.info(f"Hoy ({hoy}) no es día laboral. No se generan registros de asistencia.")
        return f"Hoy no es día laboral. Registros no generados."

    registros_creados = 0
    registros_verificados = 0

    for operario in operarios_activos:
        # Validar si para este operario hoy es día laboral
        # (importante para sábados donde no todos trabajan)
        if not es_dia_laboral(hoy, operario):
            logger.debug(f"{operario} no trabaja hoy ({hoy}, {hoy.strftime('%A')}). Registro no creado.")
            continue

        # Utiliza get_or_create para evitar duplicados y manejar la lógica de verificación de asistencia
        registro, created = RegistroAsistencia.objects.get_or_create(
            operario=operario,
            fecha=hoy
        )
        if created:
            registros_creados += 1
            logger.info(f"Registro de asistencia creado para {operario} en {hoy}.")
        else:
            registros_verificados += 1
            logger.debug(f"Registro de asistencia ya existente para {operario} en {hoy}.")

        # Verifica la asistencia del operario
        registro.verificar_asistencia()

    return f"Procesamiento completado. Creados: {registros_creados}, Verificados: {registros_verificados}"

@shared_task
def crear_asistencia_prueba(operario_id):
    try:
        print(f"Iniciando tarea para operario con ID {operario_id}")
        operario = Operario.objects.get(id=operario_id)
        print(f"Operario encontrado: {operario}")
        RegistroAsistencia.objects.create(
            operario=operario,
            fecha=timezone.now().date(),
            estado_asistencia='presente',
            descripcion="Asistencia de prueba"
        )
        print(f"Asistencia creada para operario con ID {operario_id}")
    except Operario.DoesNotExist:
        print(f"Operario con ID {operario_id} no existe")
    except Exception as e:
        print(f"Error al crear asistencia: {e}")
    return "Proceso completado"

@shared_task
def procesar_licencia_aprobada(licencia_id):
    """
    Procesa una licencia aprobada, creando/actualizando registros de asistencia
    de forma asíncrona para evitar bloqueos en el admin.

    También acumula las horas de enfermedad en el modelo HorasEnfermedad
    para que se sumen a Horas_totales.

    CASO DE USO REAL:
    - Persona falta el día X (se crea RegistroAsistencia sin justificación)
    - Persona presenta certificado médico el día Y (se carga y aprueba licencia)
    - Sistema retroactivamente justifica todos los días de la ausencia
    """
    try:
        from .models import HorasEnfermedad, Horas_totales

        licencia = Licencia.objects.get(pk=licencia_id)
        logger.info(f'Iniciando procesamiento asíncrono de licencia {licencia_id} para {licencia.operario}')

        if not (licencia.estado == 'aprobada' and licencia.aplicar_a_asistencia and
                licencia.fecha_inicio and licencia.fecha_fin):
            logger.warning(f'Licencia {licencia_id} no cumple criterios para procesamiento automático')
            return f'Licencia {licencia_id} no procesada - no cumple criterios'

        # ✅ CALCULAR HORAS ENFERMEDAD SOLO EN DÍAS LABORALES
        # Excluye domingos y feriados del CalendarioLaboral
        dias_laborales, horas_enfermedad_total = calcular_horas_enfermedad_laborales(
            licencia.fecha_inicio,
            licencia.fecha_fin
        )
        logger.info(f'Cálculo de horas enfermedad: {dias_laborales} días laborales = {int(horas_enfermedad_total.total_seconds() / 3600)}h para {licencia.operario}')

        # ✅ PASO CRÍTICO: Buscar registros SIN justificación ANTERIORES a la licencia
        # (Caso real: persona falta, luego presenta certificado)
        registros_sin_justificacion_previos = RegistroAsistencia.objects.filter(
            operario=licencia.operario,
            fecha__lt=licencia.fecha_inicio,  # Fechas ANTES de la licencia
            estado_asistencia=RegistroAsistencia.ausente,
            estado_justificacion=False,
            licencia_relacionada__isnull=True
        ).order_by('-fecha')[:30]  # Últimos 30 días sin justificación

        registros_justificados_previos = 0
        for registro_previo in registros_sin_justificacion_previos:
            # Solo justificar si está "cerca" de la fecha de inicio (máximo 30 días antes)
            dias_diferencia = (licencia.fecha_inicio - registro_previo.fecha).days
            if 0 < dias_diferencia <= 30:  # Solo si está entre 1 y 30 días antes
                registro_previo.estado_justificacion = True
                registro_previo.licencia_relacionada = licencia
                registro_previo.descripcion = f'Ausencia justificada retroactivamente por licencia (ID: {licencia.pk})'
                registro_previo.save()
                registros_justificados_previos += 1
                logger.info(f'Justificado retroactivamente registro anterior: {licencia.operario} en {registro_previo.fecha}')

        # Procesar día por día
        fecha_actual = licencia.fecha_inicio
        dias_procesados = 0
        dias_justificados = 0

        while fecha_actual <= licencia.fecha_fin:
            try:
                registro_asistencia, created = RegistroAsistencia.objects.get_or_create(
                    operario=licencia.operario,
                    fecha=fecha_actual,
                    defaults={
                        'estado_asistencia': RegistroAsistencia.ausente,
                        'estado_justificacion': True,
                        'descripcion': f'Ausencia justificada por licencia (ID: {licencia.pk})',
                        'licencia_relacionada': licencia
                    }
                )

                if created:
                    dias_justificados += 1
                    logger.debug(f'Creado registro de ausencia justificada para {licencia.operario} en {fecha_actual}')
                else:
                    # Actualizar si no está justificado o no tiene licencia relacionada
                    actualizado = False
                    if not registro_asistencia.estado_justificacion:
                        registro_asistencia.estado_justificacion = True
                        actualizado = True
                    if not registro_asistencia.licencia_relacionada:
                        registro_asistencia.licencia_relacionada = licencia
                        actualizado = True
                    if 'licencia' not in (registro_asistencia.descripcion or '').lower():
                        registro_asistencia.descripcion = f'Ausencia justificada por licencia (ID: {licencia.pk})'
                        actualizado = True

                    if actualizado:
                        registro_asistencia.save()
                        dias_justificados += 1
                        logger.debug(f'Actualizado registro existente para {licencia.operario} en {fecha_actual}')

                dias_procesados += 1

            except Exception as e:
                logger.error(f'Error procesando fecha {fecha_actual} para licencia {licencia_id}: {e}')

            fecha_actual += timedelta(days=1)

        # ✅ CREAR REGISTRO DE HORAS DE ENFERMEDAD
        try:
            mes_periodo = licencia.fecha_inicio.strftime('%Y-%m')
            horas_enfermedad_obj, created = HorasEnfermedad.objects.get_or_create(
                operario=licencia.operario,
                licencia=licencia,
                mes_periodo=mes_periodo,
                defaults={
                    'horas_enfermedad': horas_enfermedad_total
                }
            )

            if not created:
                # Si ya existe, actualizar las horas
                horas_enfermedad_obj.horas_enfermedad = horas_enfermedad_total
                horas_enfermedad_obj.save()

            logger.info(f'Horas de enfermedad registradas: {int(horas_enfermedad_total.total_seconds() / 3600)}h para {licencia.operario}')

            # ✅ RECALCULAR HORAS_TOTALES DEL MES
            Horas_totales.calcular_horas_totales(licencia.operario, mes_periodo)
            logger.info(f'Horas_totales recalculadas para {licencia.operario} en {mes_periodo}')

        except Exception as e:
            logger.error(f'Error registrando horas de enfermedad para licencia {licencia_id}: {e}')

        resultado = f'Licencia {licencia_id} procesada: {dias_justificados}/{dias_procesados} días justificados, {registros_justificados_previos} días retroactivos justificados, {int(horas_enfermedad_total.total_seconds() / 3600)}h enfermedad'
        logger.info(resultado)
        return resultado

    except Licencia.DoesNotExist:
        error_msg = f'Licencia {licencia_id} no existe'
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f'Error procesando licencia {licencia_id}: {e}'
        logger.error(error_msg)
        return error_msg

@shared_task
def verificar_licencias_activas():
    """
    Tarea programada que verifica licencias activas y actualiza
    automáticamente los registros de asistencia si es necesario.
    Se puede ejecutar diariamente con celery-beat.
    """
    hoy = timezone.now().date()
    
    # Buscar licencias aprobadas que incluyan la fecha de hoy
    licencias_activas = Licencia.objects.filter(
        estado='aprobada',
        aplicar_a_asistencia=True,
        fecha_inicio__lte=hoy,
        fecha_fin__gte=hoy
    ).select_related('operario')
    
    registros_actualizados = 0
    
    for licencia in licencias_activas:
        try:
            registro_asistencia, created = RegistroAsistencia.objects.get_or_create(
                operario=licencia.operario,
                fecha=hoy,
                defaults={
                    'estado_asistencia': RegistroAsistencia.ausente,
                    'estado_justificacion': True,
                    'descripcion': f'Ausencia justificada por licencia (ID: {licencia.pk})',
                    'licencia_relacionada': licencia
                }
            )
            
            if created or not registro_asistencia.estado_justificacion:
                if not created:
                    registro_asistencia.estado_justificacion = True
                    registro_asistencia.licencia_relacionada = licencia
                    registro_asistencia.descripcion = f'Ausencia justificada por licencia (ID: {licencia.pk})'
                    registro_asistencia.save()
                
                registros_actualizados += 1
                logger.debug(f'Justificada ausencia automática para {licencia.operario} por licencia {licencia.pk}')
                
        except Exception as e:
            logger.error(f'Error verificando licencia activa {licencia.pk}: {e}')
    
    resultado = f'Verificación completada: {registros_actualizados} registros actualizados para {licencias_activas.count()} licencias activas'
    logger.info(resultado)
    return resultado

@shared_task
def sincronizar_licencia_historica(licencia_id, fecha_desde=None, fecha_hasta=None):
    """
    Sincroniza una licencia específica con el sistema de asistencia
    en un rango de fechas determinado. Útil para correcciones manuales.
    """
    try:
        licencia = Licencia.objects.get(pk=licencia_id)
        
        if not fecha_desde:
            fecha_desde = licencia.fecha_inicio
        if not fecha_hasta:
            fecha_hasta = licencia.fecha_fin
            
        if not (fecha_desde and fecha_hasta):
            return f'Licencia {licencia_id} no tiene fechas válidas'
        
        logger.info(f'Sincronizando licencia {licencia_id} desde {fecha_desde} hasta {fecha_hasta}')
        
        fecha_actual = fecha_desde
        dias_sincronizados = 0
        
        while fecha_actual <= fecha_hasta:
            if licencia.estado == 'aprobada' and licencia.aplicar_a_asistencia:
                # Justificar ausencia
                registro, created = RegistroAsistencia.objects.get_or_create(
                    operario=licencia.operario,
                    fecha=fecha_actual,
                    defaults={
                        'estado_asistencia': RegistroAsistencia.ausente,
                        'estado_justificacion': True,
                        'descripcion': f'Ausencia justificada por licencia (ID: {licencia.pk})',
                        'licencia_relacionada': licencia
                    }
                )
                
                if not created and not registro.estado_justificacion:
                    registro.estado_justificacion = True
                    registro.licencia_relacionada = licencia
                    registro.save()
                    
            else:
                # Remover justificación si la licencia ya no está aprobada
                try:
                    registro = RegistroAsistencia.objects.get(
                        operario=licencia.operario,
                        fecha=fecha_actual,
                        licencia_relacionada=licencia
                    )
                    registro.licencia_relacionada = None
                    registro.estado_justificacion = False
                    if 'licencia' in (registro.descripcion or '').lower():
                        registro.descripcion = None
                    registro.save()
                except RegistroAsistencia.DoesNotExist:
                    pass
            
            dias_sincronizados += 1
            fecha_actual += timedelta(days=1)
        
        resultado = f'Licencia {licencia_id} sincronizada: {dias_sincronizados} días procesados'
        logger.info(resultado)
        return resultado
        
    except Exception as e:
        error_msg = f'Error sincronizando licencia {licencia_id}: {e}'
        logger.error(error_msg)
        return error_msg

@shared_task
def sincronizar_feriados_api():
    """
    Tarea programada que sincroniza los feriados desde la API ArgentinaDatos.
    Se ejecuta automáticamente (por defecto, cada 1º de enero para el año actual y próximo).
    Esta tarea no elimina sugerencias existentes, solo añade nuevas.
    """
    from .utils import obtener_feriados_api
    from .models import SugerenciaFeriado, CalendarioLaboral

    año_actual = timezone.now().year

    try:
        logger.info(f"Iniciando sincronización automática de feriados para {año_actual}")

        # Obtener feriados de la API
        feriados_api = obtener_feriados_api(año_actual)

        if not feriados_api:
            logger.warning(f"No se pudieron obtener feriados de la API para {año_actual}")
            return f"Error: No se obtuvieron feriados para {año_actual}"

        nuevas_sugerencias = 0
        ya_existentes = 0
        ya_aceptadas = 0

        for feriado_dict in feriados_api:
            try:
                fecha = feriado_dict['fecha']
                nombre = feriado_dict['nombre']
                tipo = feriado_dict['tipo_sugerencia']

                # Verificar si ya existe en CalendarioLaboral
                if CalendarioLaboral.objects.filter(
                    fecha=fecha,
                    tipo_dia__in=['feriado', 'feriado_movible']
                ).exists():
                    ya_aceptadas += 1
                    continue

                # Crear o actualizar sugerencia
                sugerencia, creada = SugerenciaFeriado.objects.get_or_create(
                    fecha=fecha,
                    fuente='api_argentina',
                    defaults={
                        'nombre': nombre,
                        'tipo_sugerencia': tipo,
                        'estado': 'pendiente',
                    }
                )

                if creada:
                    nuevas_sugerencias += 1
                    logger.info(f"Nueva sugerencia de feriado creada: {fecha} - {nombre}")
                else:
                    ya_existentes += 1

            except Exception as e:
                logger.error(f"Error procesando feriado en sincronización automática: {str(e)}")

        resultado = (
            f"Sincronización completada: "
            f"{nuevas_sugerencias} nuevas sugerencias, "
            f"{ya_existentes} ya existentes, "
            f"{ya_aceptadas} ya aceptadas en calendario"
        )
        logger.info(resultado)
        return resultado

    except Exception as e:
        error_msg = f"Error en sincronización automática de feriados: {str(e)}"
        logger.error(error_msg)
        return error_msg

@shared_task
def prueba_tarea():
    """
    Esta es una tarea de prueba simple para asegurarse de que Celery esté funcionando correctamente.
    """
    print("¡La tarea de Celery se ejecutó correctamente!")
    return "Tarea completada"

@shared_task(name='corregir_horas_negativas_automatico')
def corregir_horas_negativas_automatico():
    """
    Tarea periódica para detectar y corregir registros con horas negativas.

    Esta tarea ejecuta el management command 'corregir_horas_negativas' de forma
    automática según el schedule configurado en Celery Beat.

    El comando busca y corrige:
    - Registros en Horas_trabajadas con valores negativos
    - Registros en Horas_totales con valores negativos

    Retorna:
        str: Mensaje con el resultado de la corrección

    Raises:
        Exception: Si ocurre algún error durante la ejecución
    """
    from django.core.management import call_command
    from django.core.mail import mail_admins
    from io import StringIO

    try:
        logger.info("Iniciando corrección automática de horas negativas...")

        # Capturar output del comando
        out = StringIO()
        call_command('corregir_horas_negativas', verbosity=2, stdout=out)
        output = out.getvalue()

        # Analizar si hubo correcciones
        correcciones_realizadas = False
        if "Horas_trabajadas corregidas:" in output:
            # Extraer número de correcciones
            try:
                horas_trabajadas_line = [line for line in output.split('\n') if 'Horas_trabajadas corregidas:' in line][0]
                num_horas_trabajadas = int(horas_trabajadas_line.split(':')[1].strip())

                horas_totales_line = [line for line in output.split('\n') if 'Horas_totales corregidas:' in line][0]
                num_horas_totales = int(horas_totales_line.split(':')[1].strip())

                if num_horas_trabajadas > 0 or num_horas_totales > 0:
                    correcciones_realizadas = True
            except (IndexError, ValueError):
                pass

        # Si hubo correcciones, enviar email a admins
        if correcciones_realizadas:
            mail_admins(
                subject='[Reloj Fichador] Horas negativas corregidas automáticamente',
                message=f"Se ejecutó la corrección automática de horas negativas.\n\n{output}",
                fail_silently=True
            )
            logger.warning(f"Horas negativas detectadas y corregidas:\n{output}")
        else:
            logger.info("Corrección automática completada: No se encontraron registros negativos")

        return output

    except Exception as e:
        error_msg = f"Error en corrección automática de horas negativas: {str(e)}"
        logger.error(error_msg)

        # Notificar a admins sobre el error
        mail_admins(
            subject='[ERROR] Corrección automática de horas negativas falló',
            message=error_msg,
            fail_silently=True
        )
        raise
