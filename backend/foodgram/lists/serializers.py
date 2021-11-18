from rest_framework import serializers

from recipes.models import Recipe
from recipes.fileds import Base64ImageField


class RecipeForListsSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
