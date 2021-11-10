from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from users.permissions import IsAuthorPermission
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer
from .models import Tag, Recipe, Ingredient
from .pagination import CustomPagination
from lists.models import FavoriteList, ShoppingList
from lists.serializers import RecipeForListsSerializer





class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = permissions.AllowAny


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = permissions.AllowAny


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsAuthorPermission]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['favorite', 'shopping_cart']:
            return RecipeForListsSerializer
        return RecipeSerializer

    def partial_update(self, request, *args, **kwargs):
        return Response(
            data=['Method PATCH is not allowed'],
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

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

    def list_method(self, request, pk, type_of_list):
        instance = {
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
            serializer = self.get_serializer(recipe)
            list_object, created = (
                instance.get(type_of_list).objects.get_or_create(user=user)
            )
            if getattr(list_object, 'recipes').filter(id=recipe.id).exists():
                return Response(
                    data=[f'This recipe is already in your {type_of_list}'],
                    status=status.HTTP_400_BAD_REQUEST
                )
            getattr(list_object, 'recipes').add(recipe)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        if instance.get(type_of_list).objects.filter(
                user=user,
                recipes=recipe
        ).exists():
            getattr(
                getattr(user, related_name[type_of_list]), 'recipes'
            ).remove(recipe)
            return Response(
                data=['Recipe is successfully removed from '
                      f'your {type_of_list}'],
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            data=[f'This recipe is not in your {type_of_list}'],
            status=status.HTTP_400_BAD_REQUEST
        )
