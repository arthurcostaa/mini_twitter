from django.urls import include, path
from rest_framework.routers import DefaultRouter

from mini_twitter import views

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
