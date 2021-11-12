from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.pagination import CustomPagination
from lists.models import Follow
from .serializers import (UserRegistrationSerializer, UserSerializer,
                          PasswordSerializer, UserSubscriptionSerializer)

User = get_user_model()


class CreateListRetrieveViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    pass


class UserViewSet(CreateListRetrieveViewSet):
    queryset = User.objects.all()
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        elif self.action == 'set_password':
            return PasswordSerializer
        elif self.action in ['subscribe', 'subscriptions']:
            return UserSubscriptionSerializer
        else:
            return UserSerializer

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def set_password(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['get', 'delete'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, pk):
        user = request.user
        if request.method == 'GET':
            if pk == user.id:
                return Response(
                    data=['You can`t subscribe to yourself'],
                    status=status.HTTP_400_BAD_REQUEST
                )
            author = get_object_or_404(User, id=pk)
            follow, created = Follow.objects.get_or_create(
                author=author,
                follower=user
            )
            if created is False:
                return Response(
                    data=['You are already subscribed to this user'],
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = self.get_serializer(author)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        author = get_object_or_404(User, id=pk)
        if (pk == user.id or not Follow.objects.filter(
                author=author, follower=user).exists()):
            return Response(
                data='You are not subscribed to this user',
                status=status.HTTP_400_BAD_REQUEST
            )
        Follow.objects.filter(author=author, follower=user).delete()
        return Response(
            data=['You sucsessfully unsubscribed from this user'],
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        authors = User.objects.filter(followers__follower=request.user)
        serializer = self.get_serializer(authors, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
