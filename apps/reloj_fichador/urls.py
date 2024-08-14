from django.urls import path
from . import views

app_name = 'reloj_fichador'

urlpatterns = [
    path('', views.home, name='home'),
    path('registros/', views.registrar_movimiento, name='registrar_movimiento'),
    path('registros/<str:tipo_movimiento>/', views.registrar_movimiento, name='registrar_movimiento'),
    path('entrada/', views.registrar_entrada, name='registrar_entrada'),
    path('salida_transitoria/', views.registrar_salida_transitoria, name='registrar_salida_transitoria'),
    path('entrada_transitoria/', views.registrar_entrada_transitoria, name='registrar_entrada_transitoria'),
    path('salida/', views.registrar_salida, name='registrar_salida'),
]

