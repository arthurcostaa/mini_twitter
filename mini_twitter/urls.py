from django.urls import include, path
from rest_framework.routers import DefaultRouter

from mini_twitter import views

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='user')
router.register('comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/', views.PostCreate.as_view(), name='post-create'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
    path('feed/', views.PostList.as_view(), name='post-list'),
]
