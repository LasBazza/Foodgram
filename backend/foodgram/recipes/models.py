from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
        unique=True
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега',
        unique=True,
        db_index=True
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет',
        unique=True,
        validators=[RegexValidator(
            regex=r'^#[\da-fA-F]{6}$', message='Enter color HEX-code'
        )]
    )
    slug = models.SlugField(
        max_length=200,
        unique=True
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        'Recipe',
        related_name='recipeingredients',
        on_delete=models.CASCADE
    )
    amount = models.FloatField()

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['ingredient', 'recipe'],
            name='unique_ingredient_in_recipe'
        ), ]

        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'


class Recipe(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название рецепта')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes',
    )
    tags = models.ManyToManyField(Tag, related_name='tags')
    ingredients = models.ManyToManyField(
        Ingredient,
        through=RecipeIngredient,
        related_name='ingredients',
        verbose_name='Ингредиенты'
    )
    image = models.CharField(max_length=200, verbose_name='Изображение')
    text = models.TextField(verbose_name='Описание рецепта')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name} (by {self.author})'
