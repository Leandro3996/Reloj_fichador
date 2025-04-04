"""
URL configuration for reloj_fichador project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Definir handlers para errores HTTP
handler400 = 'apps.reloj_fichador.views.error_400'
handler403 = 'apps.reloj_fichador.views.error_403'
handler404 = 'apps.reloj_fichador.views.error_404'
handler500 = 'apps.reloj_fichador.views.error_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.reloj_fichador.urls', namespace='reloj_fichador')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
