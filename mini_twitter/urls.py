from django.urls import include, path
from rest_framework.routers import DefaultRouter

from mini_twitter import views

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='user')
router.register('posts', views.PostViewSet, basename='posts')
router.register('comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('posts/liked/', views.PostLikedList.as_view(), name='post-liked'),
    path('', include(router.urls)),
]
