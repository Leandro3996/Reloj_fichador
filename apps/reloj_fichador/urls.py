from django.urls import path
from . import views
from .views import registrar_movimiento_tipo

app_name = 'reloj_fichador'

urlpatterns = [
    path('', views.home, name='home'),
    path('registrar/<str:tipo>/', registrar_movimiento_tipo, name='registrar_movimiento_tipo'),
]
