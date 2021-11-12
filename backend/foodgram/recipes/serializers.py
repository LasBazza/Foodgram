from django.shortcuts import get_object_or_404
from rest_framework import serializers

from lists.models import FavoriteList, ShoppingList
from users.serializers import UserSerializer
from .models import Recipe, Ingredient, RecipeIngredient, Tag


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(
        source='recipeingredients',
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'author',
                  'tags', 'ingredients', 'image',
                  'text', 'cooking_time', 'is_favorited',
                  'is_in_shopping_cart')

    def to_representation(self, obj):
        self.fields['tags'] = TagSerializer(many=True)
        return super().to_representation(obj)

    def create(self, validated_data):
        ingredients = validated_data.pop('recipeingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient,
                id=ingredient['ingredient']['id']
            )
            RecipeIngredient.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=ingredient['amount']
            )
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('recipeingredients')
        tags = validated_data.pop('tags')
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.ingredients.clear()
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient,
                id=ingredient['ingredient']['id']
            )
            RecipeIngredient.objects.create(
                ingredient=current_ingredient,
                recipe=instance,
                amount=ingredient['amount']
            )
        instance.tags.set(tags)
        instance.save()
        return instance

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user is None or request.user.is_anonymous:
            return False
        return FavoriteList.objects.filter(
            user=request.user,
            recipes=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user is None or request.user.is_anonymous:
            return False
        return ShoppingList.objects.filter(
            user=request.user,
            recipes=obj
        ).exists()
