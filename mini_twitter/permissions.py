from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissão customizada para permitir que o usuário consiga editar apenas
    os seus dados e objetos que ele é dono.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            hasattr(obj, 'author') and obj.author == request.user or
            hasattr(obj, 'username') and obj.username == request.user.username
        )
