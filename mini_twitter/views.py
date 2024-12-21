from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets

from mini_twitter.models import Comment, Post
from mini_twitter.permissions import IsOwnerOrReadOnly
from mini_twitter.serializers import (
    CommentSerializer,
    CommentUpdateSerializer,
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


class PostCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class PostList(generics.ListAPIView):
    queryset = Post.objects.prefetch_related('comments')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentCreate(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        print(serializer.validated_data)
        return serializer.save(author=self.request.user)
