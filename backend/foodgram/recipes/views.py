from django.shortcuts import get_object_or_404
from django.db.models import Sum
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from lists.serializers import RecipeForListsSerializer
from lists.models import FavoriteList, ShoppingList
from users.permissions import IsAuthorOrReadOnlyPermission
from .to_pdf_maker.to_pdf_maker import shopping_cart_to_pdf
from .models import Tag, Recipe, Ingredient, RecipeIngredient
from .pagination import CustomPagination
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeSerializer)
from .filters import RecipeFilter, IngredientFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    permission_classes = [IsAuthorOrReadOnlyPermission, ]

    def get_serializer_class(self):
        if self.action in ['favorite', 'shopping_cart']:
            return RecipeForListsSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['get', 'delete'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def favorite(self, request, pk):
        return self.list_method(request, pk, 'favorite list')

    @action(
        detail=True,
        methods=['get', 'delete'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        return self.list_method(request, pk, 'shopping list')

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients_in_recipes = RecipeIngredient.objects.filter(
            recipe__in_shopping_list__user=request.user
        ).select_related('ingredient')
        result_list = ingredients_in_recipes.values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        return shopping_cart_to_pdf(result_list)

    def list_method(self, request, pk, list_type):
        model = {
            'favorite list': FavoriteList,
            'shopping list': ShoppingList
        }
        related_name = {
            'favorite list': 'favorite_list',
            'shopping list': 'shopping_list'
        }
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'GET':

            list_object, _ = (
                model.get(list_type).objects.get_or_create(user=user)
            )
            if getattr(list_object, 'recipes').filter(id=recipe.id).exists():
                return Response(
                    data=[f'This recipe is already in your {list_type}'],
                    status=status.HTTP_400_BAD_REQUEST
                )
            getattr(list_object, 'recipes').add(recipe)
            serializer = self.get_serializer(recipe)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        if model.get(list_type).objects.filter(
                user=user,
                recipes=recipe
        ).exists():
            getattr(
                getattr(user, related_name[list_type]), 'recipes'
            ).remove(recipe)
            return Response(
                data=['Recipe is successfully removed from '
                      f'your {list_type}'],
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            data=[f'This recipe is not in your {list_type}'],
            status=status.HTTP_400_BAD_REQUEST
        )
