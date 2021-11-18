from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class ShoppingList(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list'
    )
    recipes = models.ManyToManyField(
        Recipe,
        related_name='in_shopping_list'
    )


class FavoriteList(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_list'
    )
    recipes = models.ManyToManyField(
        Recipe,
        related_name='in_favorite_list'
    )


class Follow(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers')
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions')
