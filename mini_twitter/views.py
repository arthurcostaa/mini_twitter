from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.validators import ValidationError

from mini_twitter.models import Comment, Post
from mini_twitter.permissions import IsOwnerOrReadOnly
from mini_twitter.serializers import (
    CommentCreateSerializer,
    CommentRetrieveUpdateSerializer,
    PostSerializer,
    UserSerializer,
)


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


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentRetrieveUpdateSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        if timezone.now() <= comment.created_at + timedelta(hours=1):
            return serializer.save()
        raise ValidationError('Não é mais possível atualizar o comentário.')
