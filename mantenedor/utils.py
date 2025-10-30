"""
Utilidades para la configuración del admin de Django
"""

import os


def environment_callback(request):
    """
    Callback para mostrar el entorno actual en el admin.
    Retorna una tupla (nombre, color_css)
    """
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'

    if debug:
        return ("Desarrollo", "warning")  # Badge amarillo
    else:
        return ("Producción", "success")  # Badge verde


def dashboard_callback(request, context):
    """
    Callback para añadir datos personalizados al dashboard.
    Permite inyectar información adicional en el contexto del admin.
    """
    from apps.reloj_fichador.models import (
        Operario,
        RegistroDiario,
        Horas_trabajadas,
        RegistroAsistencia,
        CalendarioLaboral,
        SugerenciaFeriado,
    )
    from django.utils import timezone
    from datetime import timedelta

    hoy = timezone.now().date()
    rango_alerta = hoy + timedelta(days=30)

    sugerencias_pendientes = SugerenciaFeriado.objects.filter(estado='pendiente').order_by('fecha')
    feriados_proximos = CalendarioLaboral.objects.filter(
        fecha__gte=hoy,
        fecha__lte=rango_alerta
    ).order_by('fecha')[:5]

    # Estadísticas básicas
    context.update({
        'total_operarios': Operario.objects.filter(activo=True).count(),
        'registros_hoy': RegistroDiario.objects.filter(hora_fichada__date=hoy).count(),
        'operarios_presentes_hoy': RegistroDiario.objects.filter(
            hora_fichada__date=hoy,
            tipo_movimiento='entrada'
        ).values('operario').distinct().count(),
        'sugerencias_feriados_pendientes': sugerencias_pendientes,
        'feriados_proximos': feriados_proximos,
    })

    return context
