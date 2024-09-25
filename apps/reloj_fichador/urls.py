from django.urls import path
from . import views
from .views import registrar_movimiento_tipo, OperarioListView, generar_reporte_view

app_name = 'reloj_fichador'

urlpatterns = [
    path('', views.home, name='home'),
    path('registrar/<str:tipo>/', registrar_movimiento_tipo, name='registrar_movimiento_tipo'),
    path('operarios/', OperarioListView.as_view(), name='operarios-list'),
    path('reporte/', generar_reporte_view, name='generar_reporte'),
]
