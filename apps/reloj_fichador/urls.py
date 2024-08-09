from django.urls import path
from . import views

app_name = 'reloj_fichador'

urlpatterns = [
    path('', views.home, name='home'),
    path('registrar_entrada/', views.registrar_entrada, name='registrar_entrada'),
    path('registrar_salida_transitoria/', views.registrar_salida_transitoria, name='registrar_salida_transitoria'),
    path('registrar_entrada_transitoria/', views.registrar_entrada_transitoria, name='registrar_entrada_transitoria'),
    path('registrar_salida/', views.registrar_salida, name='registrar_salida'),
    path('registros/', views.lista_registros, name='lista_registros'),
]

