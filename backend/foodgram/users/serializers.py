from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from lists.list_checkers import ListChecker
from lists.serializers import RecipeForListsSerializer
from recipes.models import Recipe

User = get_user_model()

checker = ListChecker()


class UserRegistrationSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'password', 'id')
        read_only_fields = ('id', )


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'id', 'is_subscribed')
        read_only_fields = ('id',)

    def get_is_subscribed(self, obj):
        return checker.is_subcribed(self, obj)


class UserSubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email', 'is_subscribed',
                  'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return checker.is_subcribed(self, obj)

    def get_recipes(self, obj):
        recipes_limit = self.context.get('request').query_params.get(
            'recipes_limit')
        queryset = Recipe.objects.filter(author=obj)
        if recipes_limit:
            recipes_limit = int(recipes_limit)
            queryset = queryset[:recipes_limit]
        serializer = RecipeForListsSerializer(queryset, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    current_password = serializers.CharField()
