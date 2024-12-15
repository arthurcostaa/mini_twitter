from django.contrib.auth.models import User
from rest_framework import permissions, viewsets

from mini_twitter.permissions import IsOwnerOrReadOnly
from mini_twitter.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Define as permissões de acordo com o tipo de ação que está sendo
        realizada. É possível criar um usuário sem estar autenticado, porém
        as outras ações exigem que o usário esteja autenticado.
        """
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [
                permissions.IsAuthenticated,
                IsOwnerOrReadOnly,
            ]
        return [permission() for permission in permission_classes]
