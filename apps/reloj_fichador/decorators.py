from functools import wraps
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.template.loader import render_to_string

def permission_required(perm, raise_exception=True):
    """
    Verificar que el usuario tiene el permiso especificado.
    Similar a django.contrib.auth.decorators.permission_required pero
    con mensajes de error personalizados.
    
    Si raise_exception=True, PermissionDenied es lanzado cuando el usuario
    no tiene el permiso requerido, permitiendo que el middleware personalizado
    capture la excepción.
    
    Si raise_exception=False, se renderiza el template de error personalizado
    y se retorna directamente.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.has_perm(perm):
                return view_func(request, *args, **kwargs)
            
            # Determinar nombre legible del permiso
            app_label, codename = perm.split('.', 1)
            permission_name = perm
            
            if raise_exception:
                # Dejar que el middleware maneje la excepción
                raise PermissionDenied(f"Se requiere el permiso: {permission_name}")
            
            # Renderizar la plantilla de error y retornar directamente
            html = render_to_string('errors/permissions.html', {
                'user': request.user,
                'permission_required': permission_name,
                'show_permissions_info': True
            }, request=request)
            
            return HttpResponseForbidden(html)
        return _wrapped_view
    return decorator

def staff_required(view_func):
    """
    Verificar que el usuario tiene status de staff.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        
        html = render_to_string('errors/permissions.html', {
            'user': request.user,
            'permission_required': 'Estatus de Staff',
            'show_permissions_info': True
        }, request=request)
        
        return HttpResponseForbidden(html)
    return _wrapped_view

def superuser_required(view_func):
    """
    Verificar que el usuario es superusuario.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        html = render_to_string('errors/permissions.html', {
            'user': request.user,
            'permission_required': 'Estatus de Superusuario',
            'show_permissions_info': True
        }, request=request)
        
        return HttpResponseForbidden(html)
    return _wrapped_view 