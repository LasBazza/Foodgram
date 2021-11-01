from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer

User = get_user_model()


class UserRegistrationSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'password', 'id')
        read_only_fields = ('id', )


class UserSerializer(serializers.ModelSerializer):

    class Meta:             # добавить поле is_subscribed как read_only
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'id')
        read_only_fields = ('id',)


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    current_password = serializers.CharField()

