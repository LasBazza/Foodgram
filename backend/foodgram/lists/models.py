from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class ShoppingList(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь'
    )
    recipes = models.ManyToManyField(
        Recipe,
        related_name='in_shopping_list',
        verbose_name='Рецепты в списке покупок'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

        constraints = [models.UniqueConstraint(
            fields=['user', ],
            name='unique_shopping_list'
        ), ]


class FavoriteList(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_list',
        verbose_name='Пользователь'
    )
    recipes = models.ManyToManyField(
        Recipe,
        related_name='in_favorite_list',
        verbose_name='Избранное'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

        constraints = [models.UniqueConstraint(
            fields=['user', ],
            name='unique_favorite_list'
        ), ]


class Follow(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Автор'
    )
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Подписчик'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

        constraints = [models.UniqueConstraint(
            fields=['author', 'follower'],
            name='unique_follow'
        ), ]
