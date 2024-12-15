from django.urls import include, path
from rest_framework.routers import DefaultRouter

from mini_twitter import views

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
]
