from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from lists.models import Follow
from lists.serializers import RecipeForListsSerializer

User = get_user_model()


class IsSubscribeChecker:

    def is_subcribed(self, instance, obj):
        request = instance.context.get('request')
        if request.user is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            follower=request.user,
            author=obj
        ).exists()


is_subscribe_checker = IsSubscribeChecker()


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
        return is_subscribe_checker.is_subcribed(self, obj)


class UserSubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = RecipeForListsSerializer(read_only=True, many=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email', 'is_subscribed',
                  'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return is_subscribe_checker.is_subcribed(self, obj)

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    current_password = serializers.CharField()

