from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Ingredient, Tag, Recipe, RecipeIngredient

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff'
    )
    list_filter = ('username', 'email', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')


class TagInline(admin.TabularInline):
    model = Recipe.tags.through


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug', 'id')
    search_fields = ('name', 'color', 'slug')
    list_filter = ('name', )

    inlines = [
        TagInline,
    ]


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', 'id')
    list_filter = ('name', )

    inlines = (RecipeIngredientInline,)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'id', 'count_in_favorite')
    list_filter = ('name', 'author', 'tags')

    readonly_fields = ('count_in_favorite', )

    fields = (
        'name',
        'author',
        'image',
        'text',
        'cooking_time',
        'count_in_favorite'
    )

    inlines = (
        TagInline,
        RecipeIngredientInline
    )
    exclude = ('tags', )


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount')
    list_filter = ('ingredient', 'recipe', 'amount')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
