from django.urls import path
from . import views_rrhh

app_name = 'rrhh'

urlpatterns = [
    # Dashboard
    path('', views_rrhh.DashboardView.as_view(), name='dashboard'),
    
    # Gestión de Operarios
    path('operarios/', views_rrhh.OperariosListView.as_view(), name='operarios_list'),
    path('operarios/<int:pk>/', views_rrhh.OperarioDetailView.as_view(), name='operario_detail'),
    path('operarios/<int:pk>/edit/', views_rrhh.OperarioUpdateView.as_view(), name='operario_edit'),
    path('operarios/create/', views_rrhh.OperarioCreateView.as_view(), name='operario_create'),
    
    # Áreas y Horarios
    path('areas/', views_rrhh.AreasListView.as_view(), name='areas_list'),
    path('horarios/', views_rrhh.HorariosListView.as_view(), name='horarios_list'),
    
    # Control de Asistencia
    path('asistencia/hoy/', views_rrhh.AsistenciaHoyView.as_view(), name='asistencia_hoy'),
    path('asistencia/calendario/', views_rrhh.AsistenciaCalendarioView.as_view(), name='asistencia_calendario'),
    path('registros/', views_rrhh.RegistrosListView.as_view(), name='registros_list'),
    path('inconsistencias/', views_rrhh.InconsistenciasView.as_view(), name='inconsistencias'),
    
    # Horas y Reportes
    path('horas/trabajadas/', views_rrhh.HorasTrabajadasView.as_view(), name='horas_trabajadas'),
    path('horas/extras/', views_rrhh.HorasExtrasView.as_view(), name='horas_extras'),
    path('reportes/', views_rrhh.ReportesView.as_view(), name='reportes'),
    
    # Licencias
    path('licencias/', views_rrhh.LicenciasListView.as_view(), name='licencias_list'),
    path('licencias/calendario/', views_rrhh.LicenciasCalendarioView.as_view(), name='licencias_calendario'),
    path('licencias/create/', views_rrhh.LicenciaCreateView.as_view(), name='licencia_create'),
    
    # Configuración
    path('configuracion/', views_rrhh.ConfiguracionView.as_view(), name='configuracion'),
    
    # APIs para AJAX
    path('api/dashboard-data/', views_rrhh.DashboardDataAPIView.as_view(), name='api_dashboard_data'),
    path('api/operarios-data/', views_rrhh.OperariosDataAPIView.as_view(), name='api_operarios_data'),
    path('api/asistencia-data/', views_rrhh.AsistenciaDataAPIView.as_view(), name='api_asistencia_data'),
    path('api/asistencia-detalle-dia/', views_rrhh.AsistenciaDetalleDiaAPIView.as_view(), name='api_asistencia_detalle_dia'),
    path('api/operario/<int:pk>/asistencia-chart/', views_rrhh.OperarioAsistenciaChartAPIView.as_view(), name='api_operario_asistencia_chart'),
    path('api/operario/<int:pk>/export/', views_rrhh.OperarioExportAPIView.as_view(), name='api_operario_export'),
    path('api/operario/<int:pk>/update/', views_rrhh.OperarioUpdateAPIView.as_view(), name='api_operario_update'),
]
