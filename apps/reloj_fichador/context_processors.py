from django.conf import settings

def permissions(request):
    """
    Agrega funciones útiles para verificar permisos en las plantillas.
    """
    def has_permission(perm):
        """Comprueba si el usuario tiene un permiso específico"""
        return request.user.is_authenticated and request.user.has_perm(perm)
    
    def has_any_permission(perms):
        """Comprueba si el usuario tiene alguno de los permisos especificados"""
        if request.user.is_authenticated:
            for perm in perms:
                if request.user.has_perm(perm):
                    return True
        return False
        
    def has_all_permissions(perms):
        """Comprueba si el usuario tiene todos los permisos especificados"""
        if request.user.is_authenticated:
            for perm in perms:
                if not request.user.has_perm(perm):
                    return False
            return True
        return False
    
    return {
        'has_permission': has_permission,
        'has_any_permission': has_any_permission,
        'has_all_permissions': has_all_permissions,
        'is_debug': settings.DEBUG,
    } 