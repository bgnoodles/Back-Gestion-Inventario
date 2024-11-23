from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Permiso personalizado que verifica si el usuario tiene el rol de 'admin'.
    """
    def has_permission(self, request, view):
        # Solo permitirá el acceso a usuarios cuyo rol sea 'admin'
        return request.user.usuario.rol == 'admin'
