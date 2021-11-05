from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

users_router_v1 = DefaultRouter()
users_router_v1.register('users', UserViewSet)

api_patterns_v1 = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(users_router_v1.urls)),
]

urlpatterns = [
    path('', include(api_patterns_v1))
]
