from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

users_router = DefaultRouter()
users_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(users_router.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]
