from django.shortcuts import get_object_or_404
from rest_framework import serializers

from lists.list_checkers import ListChecker
from users.serializers import UserSerializer
from .models import Recipe, Ingredient, RecipeIngredient, Tag
from .fileds import Base64ImageField

checker = ListChecker()


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
        many=True,
    )
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'author',
                  'tags', 'ingredients', 'image',
                  'text', 'cooking_time', 'is_favorited',
                  'is_in_shopping_cart')

    def to_representation(self, obj):
        self.fields['tags'] = TagSerializer(many=True)
        return super().to_representation(obj)

    def set_ingredients(self, ingredients, instance):
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

    def create(self, validated_data):
        ingredients = validated_data.pop('recipeingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

        self.set_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('recipeingredients')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        self.set_ingredients(ingredients, instance)
        instance.tags.set(tags)
        return super().update(instance, validated_data)

    def get_is_favorited(self, obj):
        return checker.is_favorited(self, obj)

    def get_is_in_shopping_cart(self, obj):
        return checker.is_in_shopping_cart(self, obj)

    def validate_cooking_time(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Cooking time must be greater than zero.'
            )
        return value

    def validate_ingredients(self, value):
        ingredients = self.initial_data.get('ingredients')

        encountered_ingredients = []
        for ingredient in ingredients:
            if ingredient['id'] not in encountered_ingredients:
                encountered_ingredients.append(ingredient['id'])
            else:
                message = 'Ingredients should not be repeated'
                raise serializers.ValidationError(message)

        return value

    def validate_tags(self, value):
        tags = self.initial_data.get('tags')

        encountered_tags = []
        for tag in tags:
            if tag not in encountered_tags:
                encountered_tags.append(tag)
            else:
                message = 'Tags should not be repeated'
                raise serializers.ValidationError(message)
        return value
