# views_rrhh.py
"""
Vistas para la interfaz moderna de RRHH
Estas vistas proporcionan una interfaz amigable para el personal de recursos humanos
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, TemplateView
)
from django.db.models import Count, Sum, Q, Avg
from django.db.models import Value
from django.db.models.functions import Concat
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator
from datetime import datetime, timedelta, date, time
import json
from .models import (
    Operario, RegistroDiario, Horas_trabajadas, Horas_extras,
    Area, Horario, Licencia, RegistroAsistencia
)
from .forms import LicenciaForm
import pytz


class DashboardView(LoginRequiredMixin, TemplateView):
    """Vista principal del dashboard de RRHH"""
    template_name = 'rrhh/dashboard/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoy = timezone.now().date()
        
        # KPIs principales
        context['total_operarios'] = Operario.objects.count()
        context['operarios_activos'] = Operario.objects.filter(activo=True).count()
        
        # Asistencias de hoy
        presentes_hoy = RegistroAsistencia.objects.filter(
            fecha=hoy, 
            operario__activo=True
        ).count()
        context['presentes_hoy'] = presentes_hoy
        
        # Porcentaje de asistencia
        total_activos = context['operarios_activos']
        context['porcentaje_asistencia'] = round(
            (presentes_hoy / total_activos * 100) if total_activos > 0 else 0, 1
        )
        
        # Horas del mes
        inicio_mes = hoy.replace(day=1)
        
        # Sumar todas las horas del mes (normales + nocturnas + extras)
        horas_trabajadas_qs = Horas_trabajadas.objects.filter(
            fecha__gte=inicio_mes,
            fecha__lte=hoy
        )
        
        # Calcular total de horas (convertir durations a horas decimales)
        total_horas = 0
        for ht in horas_trabajadas_qs:
            horas_normales = ht.horas_normales.total_seconds() / 3600 if ht.horas_normales else 0
            horas_nocturnas = ht.horas_nocturnas.total_seconds() / 3600 if ht.horas_nocturnas else 0
            horas_extras_calc = ht.horas_extras.total_seconds() / 3600 if ht.horas_extras else 0
            total_horas += horas_normales + horas_nocturnas + horas_extras_calc
        
        context['horas_mes'] = round(total_horas, 1)
        
        # Horas extras del mes
        horas_extras_qs = Horas_extras.objects.filter(
            fecha__gte=inicio_mes,
            fecha__lte=hoy
        )
        
        # Convertir duraciones a horas decimales
        total_horas_extras = 0
        for he in horas_extras_qs:
            if he.horas_extras:
                total_horas_extras += he.horas_extras.total_seconds() / 3600
        
        context['horas_extras_mes'] = round(total_horas_extras, 1)
        
        # Inconsistencias pendientes
        context['inconsistencias_pendientes'] = RegistroDiario.objects.filter(
            inconsistencia=True,
            valido=True
        ).count()
        
        # Últimos registros
        context['ultimos_registros'] = RegistroDiario.objects.select_related(
            'operario'
        ).prefetch_related('operario__areas').order_by('-hora_fichada')[:10]
        
        # Estados de operarios hoy
        context['estados_operarios'] = self.get_estados_operarios_hoy()
        
        # Datos para gráficos
        context['datos_asistencias'] = self.get_datos_asistencias()
        context['datos_areas'] = self.get_datos_areas()
        
        # Áreas para filtros
        context['areas'] = Area.objects.all()
        
        # Alertas del sistema
        context['alertas'] = self.get_alertas_sistema()
        
        return context
    
    def get_estados_operarios_hoy(self):
        """Obtiene el estado de todos los operarios para hoy"""
        hoy = timezone.now().date()
        operarios_activos = Operario.objects.filter(activo=True).prefetch_related('areas')
        estados = []
        
        for operario in operarios_activos:
            # Filtrar registros del día usando hora_fichada
            inicio_dia = timezone.make_aware(datetime.combine(hoy, time.min))
            fin_dia = timezone.make_aware(datetime.combine(hoy, time.max))
            
            registros_hoy = RegistroDiario.objects.filter(
                operario=operario,
                hora_fichada__range=(inicio_dia, fin_dia)
            ).order_by('hora_fichada')
            
            entrada = None
            salida = None
            estado = "Ausente"
            color = "secondary"
            
            if registros_hoy.exists():
                for registro in registros_hoy:
                    if registro.tipo_movimiento == 'entrada' and not entrada:
                        entrada = registro.hora_fichada
                        estado = "Presente"
                        color = "success"
                    elif registro.tipo_movimiento == 'salida':
                        salida = registro.hora_fichada
                        estado = "Salió"
                        color = "warning"
            
            estados.append({
                'operario': operario,
                'estado': estado,
                'color': color,
                'entrada': entrada,
                'salida': salida
            })
        
        return estados[:10]  # Limitar a 10 para el dashboard
    
    def get_datos_asistencias(self):
        """Obtiene datos de asistencias para el gráfico"""
        hoy = timezone.now().date()
        fechas = []
        asistencias = []
        
        for i in range(7):
            fecha = hoy - timedelta(days=6-i)
            fechas.append(fecha.strftime('%d/%m'))
            
            # Contar asistencias únicas por día
            count = RegistroAsistencia.objects.filter(
                fecha=fecha,
                operario__activo=True
            ).count()
            asistencias.append(count)
        
        return json.dumps({
            'labels': fechas,
            'data': asistencias
        })
    
    def get_datos_areas(self):
        """Obtiene datos de distribución por áreas"""
        areas_data = Area.objects.annotate(
            total_operarios=Count('operario', filter=Q(operario__activo=True))
        ).filter(total_operarios__gt=0)
        
        labels = [area.nombre for area in areas_data]
        data = [area.total_operarios for area in areas_data]
        
        return json.dumps({
            'labels': labels,
            'data': data
        })
    
    def get_alertas_sistema(self):
        """Obtiene alertas importantes del sistema"""
        alertas = []
        
        # Operarios sin registro hoy
        hoy = timezone.now().date()
        inicio_dia = timezone.make_aware(datetime.combine(hoy, time.min))
        fin_dia = timezone.make_aware(datetime.combine(hoy, time.max))
        
        operarios_sin_registro = Operario.objects.filter(
            activo=True
        ).exclude(
            registrodiario__hora_fichada__range=(inicio_dia, fin_dia)
        ).count()
        
        if operarios_sin_registro > 0:
            alertas.append({
                'tipo': 'warning',
                'icono': 'person-x',
                'titulo': 'Operarios sin registro',
                'mensaje': f'{operarios_sin_registro} operarios no han registrado entrada hoy.',
                'fecha': timezone.now()
            })
        
        # Inconsistencias pendientes
        inconsistencias = RegistroDiario.objects.filter(
            inconsistencia=True,
            valido=True
        ).count()
        
        if inconsistencias > 5:
            alertas.append({
                'tipo': 'danger',
                'icono': 'exclamation-triangle',
                'titulo': 'Muchas inconsistencias',
                'mensaje': f'Hay {inconsistencias} inconsistencias que requieren revisión.',
                'fecha': timezone.now()
            })
        
        return alertas


class OperariosListView(LoginRequiredMixin, TemplateView):
    """Vista de lista de operarios con funcionalidad tipo Excel"""
    template_name = 'rrhh/operarios/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Query base con datos relacionados y agregaciones
        operarios = Operario.objects.prefetch_related('areas').annotate(
            total_registros_mes=Count(
                'registrodiario',
                filter=Q(registrodiario__hora_fichada__month=timezone.now().month),
                distinct=True
            )
        ).order_by('apellido', 'nombre')
        
        # Aplicar filtros si existen
        area_filter = self.request.GET.get('area')
        estado_filter = self.request.GET.get('estado')
        search = self.request.GET.get('search')
        
        if area_filter and area_filter != '':
            operarios = operarios.filter(areas__id=area_filter)
        
        if estado_filter and estado_filter != '':
            if estado_filter == 'activo':
                operarios = operarios.filter(activo=True)
            elif estado_filter == 'inactivo':
                operarios = operarios.filter(activo=False)
        
        if search and search.strip():
            operarios = operarios.filter(
                Q(nombre__icontains=search) |
                Q(apellido__icontains=search) |
                Q(seg_nombre__icontains=search) |
                Q(seg_apellido__icontains=search) |
                Q(dni__icontains=search)
            ).distinct()
        
        # Datos para el contexto
        context['operarios'] = operarios
        context['areas'] = Area.objects.all().order_by('nombre')
        context['total_operarios'] = operarios.count()
        context['operarios_activos'] = operarios.filter(activo=True).count()
        context['operarios_inactivos'] = operarios.filter(activo=False).count()
        
        # Filtros aplicados para mantener estado en el template
        context['current_filters'] = {
            'area': area_filter,
            'estado': estado_filter,
            'search': search
        }
        
        return context


class AsistenciaHoyView(LoginRequiredMixin, TemplateView):
    """Vista de asistencia del día actual con filtros avanzados"""
    template_name = 'rrhh/asistencia/hoy.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoy = timezone.now().date()
        
        # Obtener filtros de la URL
        area_filter = self.request.GET.get('area')
        estado_filter = self.request.GET.get('estado')
        horario_filter = self.request.GET.get('horario')
        search = self.request.GET.get('search')
        
        # Query base de operarios activos
        operarios_query = Operario.objects.filter(activo=True).prefetch_related('areas')
        
        # Aplicar filtros
        if area_filter:
            operarios_query = operarios_query.filter(areas__id=area_filter)
        
        if horario_filter:
            # Como no hay campo horario directo en Operario, filtramos por horarios de las áreas
            operarios_query = operarios_query.filter(areas__horarios__id=horario_filter)
        
        if search and search.strip():
            operarios_query = operarios_query.filter(
                Q(nombre__icontains=search) |
                Q(apellido__icontains=search) |
                Q(seg_nombre__icontains=search) |
                Q(seg_apellido__icontains=search) |
                Q(dni__icontains=search)
            )
        
        operarios_activos = operarios_query.distinct()
        asistencia_data = []
        
        # Generar datos de asistencia
        for operario in operarios_activos:
            # Filtrar registros del día usando hora_fichada
            inicio_dia = timezone.make_aware(datetime.combine(hoy, time.min))
            fin_dia = timezone.make_aware(datetime.combine(hoy, time.max))
            
            registros_hoy = RegistroDiario.objects.filter(
                operario=operario,
                hora_fichada__range=(inicio_dia, fin_dia)
            ).order_by('hora_fichada')
            
            entrada = None
            salida = None
            estado = "Ausente"
            
            for registro in registros_hoy:
                if registro.tipo_movimiento == 'entrada' and not entrada:
                    entrada = registro
                elif registro.tipo_movimiento == 'salida':
                    salida = registro
            
            if entrada:
                estado = "Presente" if not salida else "Salió"
            
            data_operario = {
                'operario': operario,
                'entrada': entrada,
                'salida': salida,
                'estado': estado,
                'registros': list(registros_hoy)
            }
            
            # Aplicar filtro de estado si está presente
            if estado_filter:
                if estado_filter == 'presente' and estado != 'Presente':
                    continue
                elif estado_filter == 'ausente' and estado != 'Ausente':
                    continue
                elif estado_filter == 'salio' and estado != 'Salió':
                    continue
            
            asistencia_data.append(data_operario)
        
        # Calcular estadísticas
        total_presentes = sum(1 for data in asistencia_data if data['entrada'])
        total_operarios = len(asistencia_data)
        
        # Datos para el contexto
        context.update({
            'asistencia_data': asistencia_data,
            'fecha': hoy,
            'total_presentes': total_presentes,
            'total_operarios': total_operarios,
            'areas': Area.objects.all().order_by('nombre'),
            'horarios': Horario.objects.all().order_by('nombre'),
            'current_filters': {
                'area': area_filter,
                'estado': estado_filter,
                'horario': horario_filter,
                'search': search
            }
        })
        
        return context


# Vista detalle completa del operario
class OperarioDetailView(LoginRequiredMixin, DetailView):
    model = Operario
    template_name = 'rrhh/operarios/detail.html'
    context_object_name = 'operario'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        operario = self.get_object()
        hoy = timezone.now().date()
        inicio_mes = hoy.replace(day=1)
        
        # Calcular estadísticas del mes actual
        registros_mes = RegistroDiario.objects.filter(
            operario=operario,
            hora_fichada__range=(
                timezone.make_aware(datetime.combine(inicio_mes, time.min)),
                timezone.make_aware(datetime.combine(hoy, time.max))
            )
        )
        
        # Días trabajados (días únicos con registros)
        dias_trabajados = registros_mes.values('hora_fichada__date').distinct().count()
        
        # Calcular puntualidad (entradas a tiempo vs total de entradas)
        # Como Operario no tiene campo horario directo, buscaremos en las áreas asociadas
        entradas_mes = registros_mes.filter(tipo_movimiento='entrada')
        entradas_puntuales = 0
        puntualidad = 0
        
        if entradas_mes.count() > 0:
            # Obtener horarios de las áreas del operario
            horarios_operario = []
            for area in operario.areas.all():
                horarios_operario.extend(area.horarios.all())
            
            # Si tiene al menos un horario, usar el primero para calcular puntualidad
            if horarios_operario:
                horario_referencia = horarios_operario[0]
                
                for entrada in entradas_mes:
                    hora_entrada_real = entrada.hora_fichada.time()
                    hora_entrada_esperada = horario_referencia.hora_inicio
                    
                    # Tolerancia de 10 minutos
                    tolerancia = timedelta(minutes=10)
                    entrada_datetime = datetime.combine(date.today(), hora_entrada_real)
                    esperada_datetime = datetime.combine(date.today(), hora_entrada_esperada)
                    
                    if entrada_datetime <= esperada_datetime + tolerancia:
                        entradas_puntuales += 1
                
                puntualidad = round((entradas_puntuales / entradas_mes.count() * 100), 1)
        
        # Horas trabajadas del mes
        horas_trabajadas_mes = Horas_trabajadas.objects.filter(
            operario=operario,
            fecha__gte=inicio_mes,
            fecha__lte=hoy
        )
        
        total_horas = 0
        for ht in horas_trabajadas_mes:
            if ht.horas_normales:
                total_horas += ht.horas_normales.total_seconds() / 3600
            if ht.horas_nocturnas:
                total_horas += ht.horas_nocturnas.total_seconds() / 3600
            if ht.horas_extras:
                total_horas += ht.horas_extras.total_seconds() / 3600
        
        # Horas extras del mes
        horas_extras_mes = Horas_extras.objects.filter(
            operario=operario,
            fecha__gte=inicio_mes,
            fecha__lte=hoy
        )
        
        total_horas_extras = 0
        for he in horas_extras_mes:
            if he.horas_extras:
                total_horas_extras += he.horas_extras.total_seconds() / 3600
        
        # Últimos 10 registros
        ultimos_registros = RegistroDiario.objects.filter(
            operario=operario
        ).order_by('-hora_fichada')[:10]
        
        context['stats'] = {
            'dias_trabajados': dias_trabajados,
            'puntualidad': puntualidad,
            'horas_trabajadas': round(total_horas, 1),
            'horas_extras': round(total_horas_extras, 1)
        }
        context['ultimos_registros'] = ultimos_registros
        
        return context


class OperarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Operario
    template_name = 'rrhh/operarios/form.html'
    fields = ['nombre', 'apellido', 'dni', 'areas', 'activo']


class OperarioCreateView(LoginRequiredMixin, CreateView):
    model = Operario
    template_name = 'rrhh/operarios/form.html'
    fields = ['nombre', 'apellido', 'dni', 'areas', 'activo']


class AreasListView(LoginRequiredMixin, ListView):
    model = Area
    template_name = 'rrhh/areas/list.html'
    context_object_name = 'areas'


class HorariosListView(LoginRequiredMixin, ListView):
    model = Horario
    template_name = 'rrhh/horarios/list.html'
    context_object_name = 'horarios'


class RegistrosListView(LoginRequiredMixin, TemplateView):
    template_name = 'rrhh/asistencia/registros.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        registros = RegistroDiario.objects.select_related(
            'operario'
        ).prefetch_related('operario__areas').order_by('-hora_fichada')
        
        # Aplicar filtros
        fecha_desde = self.request.GET.get('fecha_desde')
        fecha_hasta = self.request.GET.get('fecha_hasta')
        operario_id = self.request.GET.get('operario')
        
        if fecha_desde:
            try:
                fecha_desde_dt = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
                inicio_desde = timezone.make_aware(datetime.combine(fecha_desde_dt, time.min))
                registros = registros.filter(hora_fichada__gte=inicio_desde)
            except ValueError:
                pass
                
        if fecha_hasta:
            try:
                fecha_hasta_dt = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
                fin_hasta = timezone.make_aware(datetime.combine(fecha_hasta_dt, time.max))
                registros = registros.filter(hora_fichada__lte=fin_hasta)
            except ValueError:
                pass
                
        if operario_id:
            registros = registros.filter(operario_id=operario_id)
        
        # Paginación
        paginator = Paginator(registros, 50)
        page = self.request.GET.get('page')
        context['registros'] = paginator.get_page(page)
        context['operarios'] = Operario.objects.filter(activo=True)
        
        return context


class InconsistenciasView(LoginRequiredMixin, TemplateView):
    template_name = 'rrhh/asistencia/inconsistencias.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        inconsistencias = RegistroDiario.objects.filter(
            inconsistencia=True,
            valido=True
        ).select_related('operario').prefetch_related('operario__areas').order_by('-hora_fichada')
        
        context['inconsistencias'] = inconsistencias
        context['total_inconsistencias'] = inconsistencias.count()
        
        return context


class HorasTrabajadasView(LoginRequiredMixin, TemplateView):
    template_name = 'rrhh/horas/trabajadas.html'


class HorasExtrasView(LoginRequiredMixin, TemplateView):
    template_name = 'rrhh/horas/extras.html'


class ReportesView(LoginRequiredMixin, TemplateView):
    template_name = 'rrhh/reportes/index.html'


class LicenciasListView(LoginRequiredMixin, ListView):
    model = Licencia
    template_name = 'rrhh/licencias/list.html'
    context_object_name = 'licencias'


class LicenciasCalendarioView(LoginRequiredMixin, TemplateView):
    template_name = 'rrhh/licencias/calendario.html'


class LicenciaCreateView(LoginRequiredMixin, CreateView):
    model = Licencia
    form_class = LicenciaForm
    template_name = 'rrhh/licencias/form.html'


class ConfiguracionView(LoginRequiredMixin, TemplateView):
    template_name = 'rrhh/configuracion/index.html'


# APIs para AJAX
class DashboardDataAPIView(LoginRequiredMixin, TemplateView):
    """API para obtener datos del dashboard vía AJAX"""
    
    def get(self, request, *args, **kwargs):
        # Aquí retornaremos datos JSON para actualizar el dashboard
        return JsonResponse({
            'status': 'success',
            'data': 'Dashboard data here'
        })


class OperariosDataAPIView(LoginRequiredMixin, TemplateView):
    """API para obtener datos de operarios para DataTables"""
    
    def get(self, request, *args, **kwargs):
        # Aquí retornaremos datos JSON para DataTables
        return JsonResponse({
            'draw': 1,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': []
        })


class AsistenciaDataAPIView(LoginRequiredMixin, TemplateView):
    """API para obtener datos de asistencia"""
    
    def get(self, request, *args, **kwargs):
        return JsonResponse({
            'status': 'success',
            'data': 'Asistencia data here'
        })


class OperarioAsistenciaChartAPIView(LoginRequiredMixin, TemplateView):
    """API para obtener datos del gráfico de asistencia del operario"""
    
    def get(self, request, pk, *args, **kwargs):
        try:
            operario = get_object_or_404(Operario, pk=pk)
            hoy = timezone.now().date()
            fecha_inicio = hoy - timedelta(days=30)
            
            # Generar datos para los últimos 30 días
            labels = []
            values = []
            
            current_date = fecha_inicio
            while current_date <= hoy:
                labels.append(current_date.strftime('%d/%m'))
                
                # Verificar si hay registros para esta fecha
                inicio_dia = timezone.make_aware(datetime.combine(current_date, time.min))
                fin_dia = timezone.make_aware(datetime.combine(current_date, time.max))
                
                registros = RegistroDiario.objects.filter(
                    operario=operario,
                    hora_fichada__range=(inicio_dia, fin_dia)
                ).exists()
                
                values.append(1 if registros else 0)
                current_date += timedelta(days=1)
            
            return JsonResponse({
                'labels': labels,
                'values': values
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class OperarioExportAPIView(LoginRequiredMixin, TemplateView):
    """API para exportar datos del operario"""
    
    def get(self, request, pk, *args, **kwargs):
        try:
            operario = get_object_or_404(Operario, pk=pk)
            
            # Por ahora retornar JSON, más adelante implementar Excel
            data = {
                'operario': {
                    'nombre': operario.nombre_completo(),
                    'dni': operario.dni,
                    'area': operario.area.nombre if operario.area else None,
                    'activo': operario.activo,
                    'email': operario.email,
                    'telefono': operario.telefono
                }
            }
            
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class OperarioUpdateAPIView(LoginRequiredMixin, TemplateView):
    """API para actualizar datos básicos del operario vía AJAX"""
    
    def post(self, request, pk, *args, **kwargs):
        try:
            operario = get_object_or_404(Operario, pk=pk)
            
            # Actualizar campos permitidos
            if 'activo' in request.POST:
                operario.activo = request.POST.get('activo') == 'true'
            
            if 'email' in request.POST:
                operario.email = request.POST.get('email', '')
            
            if 'telefono' in request.POST:
                operario.telefono = request.POST.get('telefono', '')
            
            operario.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class AsistenciaCalendarioView(LoginRequiredMixin, TemplateView):
    """Vista de calendario mensual de asistencia"""
    template_name = 'rrhh/asistencia/calendario.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener mes del parámetro o usar mes actual
        mes_param = self.request.GET.get('mes')
        if mes_param:
            try:
                fecha_mes = datetime.strptime(mes_param + '-01', '%Y-%m-%d').date()
            except ValueError:
                fecha_mes = timezone.now().date().replace(day=1)
        else:
            fecha_mes = timezone.now().date().replace(day=1)
        
        # Calcular primer y último día del mes
        primer_dia = fecha_mes
        if fecha_mes.month == 12:
            ultimo_dia = fecha_mes.replace(year=fecha_mes.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            ultimo_dia = fecha_mes.replace(month=fecha_mes.month + 1, day=1) - timedelta(days=1)
        
        # Obtener filtros
        area_filter = self.request.GET.get('area')
        estado_filter = self.request.GET.get('estado')
        
        # Query base de operarios
        operarios_query = Operario.objects.all()
        if area_filter:
            operarios_query = operarios_query.filter(areas__id=area_filter)
        if estado_filter == 'activo':
            operarios_query = operarios_query.filter(activo=True)
        elif estado_filter == 'inactivo':
            operarios_query = operarios_query.filter(activo=False)
        
        operarios = operarios_query.distinct()
        
        # Generar datos de asistencia por día
        datos_asistencia = {}
        fecha_actual = primer_dia
        
        while fecha_actual <= ultimo_dia:
            inicio_dia = timezone.make_aware(datetime.combine(fecha_actual, time.min))
            fin_dia = timezone.make_aware(datetime.combine(fecha_actual, time.max))
            
            # Contar presentes (operarios con registros del día)
            operarios_con_registro = RegistroDiario.objects.filter(
                operario__in=operarios,
                hora_fichada__range=(inicio_dia, fin_dia)
            ).values('operario').distinct().count()
            
            # Contar tardanzas (entradas después de la hora programada)
            tardanzas = 0
            for operario in operarios:
                # Obtener horarios de las áreas del operario
                horarios_operario = []
                for area in operario.areas.all():
                    horarios_operario.extend(area.horarios.all())
                
                if horarios_operario:
                    horario_referencia = horarios_operario[0]  # Usar el primer horario encontrado
                    
                    entradas = RegistroDiario.objects.filter(
                        operario=operario,
                        tipo_movimiento='entrada',
                        hora_fichada__range=(inicio_dia, fin_dia)
                    )
                    
                    for entrada in entradas:
                        hora_entrada_real = entrada.hora_fichada.time()
                        hora_entrada_esperada = horario_referencia.hora_inicio
                        
                        # Tolerancia de 10 minutos
                        tolerancia = timedelta(minutes=10)
                        entrada_datetime = datetime.combine(date.today(), hora_entrada_real)
                        esperada_datetime = datetime.combine(date.today(), hora_entrada_esperada)
                        
                        if entrada_datetime > esperada_datetime + tolerancia:
                            tardanzas += 1
            
            total_operarios = operarios.count()
            ausentes = total_operarios - operarios_con_registro
            
            datos_asistencia[fecha_actual.strftime('%Y-%m-%d')] = {
                'presentes': operarios_con_registro,
                'ausentes': ausentes,
                'tardanzas': tardanzas,
                'total': total_operarios
            }
            
            fecha_actual += timedelta(days=1)
        
        # Calcular estadísticas del mes
        total_dias_laborables = sum(1 for fecha, datos in datos_asistencia.items() 
                                  if datetime.strptime(fecha, '%Y-%m-%d').weekday() < 5)  # Lunes a Viernes
        
        if total_dias_laborables > 0:
            total_presencias = sum(datos['presentes'] for datos in datos_asistencia.values())
            total_posibles = total_dias_laborables * operarios.count()
            promedio_asistencia = round((total_presencias / total_posibles * 100) if total_posibles > 0 else 0, 1)
        else:
            promedio_asistencia = 0
        
        total_tardanzas = sum(datos['tardanzas'] for datos in datos_asistencia.values())
        total_ausencias = sum(datos['ausentes'] for datos in datos_asistencia.values())
        
        context.update({
            'mes_actual': fecha_mes,
            'areas': Area.objects.all().order_by('nombre'),
            'datos_asistencia': json.dumps(datos_asistencia),
            'stats': {
                'dias_laborables': total_dias_laborables,
                'promedio_asistencia': promedio_asistencia,
                'tardanzas': total_tardanzas,
                'ausencias': total_ausencias
            }
        })
        
        return context


class AsistenciaDetalleDiaAPIView(LoginRequiredMixin, TemplateView):
    """API para obtener el detalle de asistencia de un día específico"""
    
    def get(self, request, *args, **kwargs):
        try:
            fecha_param = request.GET.get('fecha')
            if not fecha_param:
                return JsonResponse({'error': 'Fecha requerida'}, status=400)
            
            fecha = datetime.strptime(fecha_param, '%Y-%m-%d').date()
            inicio_dia = timezone.make_aware(datetime.combine(fecha, time.min))
            fin_dia = timezone.make_aware(datetime.combine(fecha, time.max))
            
            # Obtener todos los operarios activos
            operarios = Operario.objects.filter(activo=True).prefetch_related('areas').order_by('apellido', 'nombre')
            registros_data = []
            
            for operario in operarios:
                # Buscar registros del día
                registros_dia = RegistroDiario.objects.filter(
                    operario=operario,
                    hora_fichada__range=(inicio_dia, fin_dia)
                ).order_by('hora_fichada')
                
                entrada = None
                salida = None
                estado = "Ausente"
                estado_class = "danger"
                
                for registro in registros_dia:
                    if registro.tipo_movimiento == 'entrada' and not entrada:
                        entrada = registro.hora_fichada.strftime('%H:%M')
                    elif registro.tipo_movimiento == 'salida':
                        salida = registro.hora_fichada.strftime('%H:%M')
                
                if entrada:
                    estado = "Presente"
                    estado_class = "success"
                    
                    # Verificar tardanza usando los horarios de las áreas
                    primer_horario = operario.get_primer_horario()
                    if primer_horario and primer_horario.hora_inicio:
                        hora_entrada_real = datetime.strptime(entrada, '%H:%M').time()
                        hora_entrada_esperada = primer_horario.hora_inicio
                        
                        tolerancia = timedelta(minutes=10)
                        entrada_datetime = datetime.combine(date.today(), hora_entrada_real)
                        esperada_datetime = datetime.combine(date.today(), hora_entrada_esperada)
                        
                        if entrada_datetime > esperada_datetime + tolerancia:
                            estado = "Tardanza"
                            estado_class = "warning"
                    
                    if salida:
                        estado = "Completo"
                        estado_class = "success"
                
                registros_data.append({
                    'operario': operario.nombre_completo(),
                    'area': operario.area.nombre if operario.area else '',
                    'entrada': entrada,
                    'salida': salida,
                    'estado': estado,
                    'estado_class': estado_class
                })
            
            return JsonResponse({
                'registros': registros_data,
                'fecha': fecha.strftime('%Y-%m-%d'),
                'total': len(registros_data)
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
