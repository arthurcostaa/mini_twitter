from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.validators import ValidationError

from mini_twitter.models import Comment, Post
from mini_twitter.permissions import IsOwnerOrReadOnly
from mini_twitter.serializers import (
    CommentCreateSerializer,
    CommentRetrieveUpdateSerializer,
    PostSerializer,
    PostLikesSerializer,
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
            permission_classes = [AllowAny]
        else:
            permission_classes = [
                IsAuthenticated,
                IsOwnerOrReadOnly,
            ]
        return [permission() for permission in permission_classes]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post'],
        url_path='like',
        url_name='like',
        permission_classes=[IsAuthenticated]
    )
    def like_post(self, request, pk=None):
        """Adiciona um like em um post."""
        post = self.get_object()
        user = request.user
        liked = post.likes.filter(id=user.id).exists()

        if not liked:
            post.likes.add(user)

        serializer = PostLikesSerializer(post)
        return Response(serializer.data)

    @like_post.mapping.delete
    def unlike_post(self, request, pk=None):
        """Remove like de um post."""
        post = self.get_object()
        user = request.user
        liked = post.likes.filter(id=user.id).exists()

        if liked:
            post.likes.remove(user)

        serializer = PostLikesSerializer(post)
        return Response(serializer.data)

    @like_post.mapping.get
    def user_liked_post(self, request, pk=None):
        """Verifica se o usuário de like em um post."""
        post = self.get_object()
        user = request.user
        liked = post.likes.filter(id=user.id).exists()
        return Response({'liked': liked})


class PostLikedList(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.post_likes.all()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

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
