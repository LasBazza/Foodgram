from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, IngredientViewSet, RecipeViewSet

router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet)
router_v1.register('ingredients', IngredientViewSet)
router_v1.register('recipes', RecipeViewSet)

api_patterns_v1 = [
    path('', include(router_v1.urls))
]
urlpatterns = [
    path('', include(api_patterns_v1))
]
