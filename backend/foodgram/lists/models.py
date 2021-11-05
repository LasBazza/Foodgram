from django.db import models
from django.contrib.auth import get_user_model

from recipes.models import Recipe

User = get_user_model()


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list'
    )
    recipes = models.ManyToManyField(Recipe)


class FavoriteList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='FavoriteList'
    )
    recipes = models.ManyToManyField(Recipe)


class Follow(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers')
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions')
