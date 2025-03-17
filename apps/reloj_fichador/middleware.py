import sys
import traceback
import logging
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('reloj_fichador')

class ErrorHandlerMiddleware(MiddlewareMixin):
    """
    Middleware para capturar y manejar errores de forma personalizada.
    """
    
    def process_exception(self, request, exception):
        """
        Maneja las excepciones no capturadas y renderiza una página de error personalizada.
        """
        # Solo procesar errores si DEBUG es False (producción)
        if settings.DEBUG:
            return None
            
        error_details = None
        if request.user.is_superuser:
            # Solo mostrar detalles técnicos a superusuarios
            error_details = "".join(traceback.format_exception(*sys.exc_info()))
            
        # Registrar el error en los logs
        logger.error(
            f"Error no capturado: {exception}",
            exc_info=True,
            extra={
                'request': request,
                'user_id': getattr(request.user, 'id', None),
                'user_username': getattr(request.user, 'username', None),
            }
        )
        
        # Generar respuesta de error según el tipo de excepción
        context = {
            'error_details': error_details,
            'exception': str(exception),
            'user': request.user,
        }
        
        # Manejar distintos tipos de error
        from django.core.exceptions import PermissionDenied
        from django.http import Http404
        
        if isinstance(exception, PermissionDenied):
            html = render_to_string('errors/403.html', context, request=request)
            return HttpResponseForbidden(html)
            
        elif isinstance(exception, Http404):
            html = render_to_string('errors/404.html', context, request=request)
            return HttpResponseNotFound(html)
            
        else:
            # Error 500 para cualquier otra excepción
            html = render_to_string('errors/500.html', context, request=request)
            return HttpResponseServerError(html)
            
    def process_response(self, request, response):
        """
        Maneja las respuestas HTTP con códigos de error y renderiza una página personalizada.
        """
        if not settings.DEBUG:
            if response.status_code == 403:
                if not hasattr(response, 'content') or not response.content:
                    html = render_to_string('errors/403.html', {
                        'user': request.user,
                        'show_permissions_info': True
                    }, request=request)
                    response = HttpResponseForbidden(html)
                    
            elif response.status_code == 404:
                if not hasattr(response, 'content') or not response.content:
                    html = render_to_string('errors/404.html', {
                        'user': request.user
                    }, request=request)
                    response = HttpResponseNotFound(html)
                    
            elif response.status_code == 400:
                if not hasattr(response, 'content') or not response.content:
                    html = render_to_string('errors/400.html', {
                        'user': request.user
                    }, request=request)
                    response = HttpResponseBadRequest(html)
                    
            elif response.status_code >= 500:
                if not hasattr(response, 'content') or not response.content:
                    html = render_to_string('errors/500.html', {
                        'user': request.user
                    }, request=request)
                    response = HttpResponseServerError(html)
                    
        return response

class PermissionMiddleware(MiddlewareMixin):
    """
    Middleware para añadir mensajes claros sobre permisos faltantes.
    """
    def process_exception(self, request, exception):
        """
        Detecta excepciones de permisos y añade información útil.
        """
        if settings.DEBUG:
            return None
            
        from django.core.exceptions import PermissionDenied
        
        if isinstance(exception, PermissionDenied):
            # Intentar extraer el permiso requerido del mensaje de error
            permission = None
            if hasattr(exception, 'args') and len(exception.args) > 0:
                error_msg = str(exception.args[0])
                if 'permission' in error_msg.lower():
                    permission = error_msg
            
            html = render_to_string('errors/permissions.html', {
                'user': request.user,
                'permission_required': permission,
                'show_permissions_info': True
            }, request=request)
            
            return HttpResponseForbidden(html)
        
        return None 