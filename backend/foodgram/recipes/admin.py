from django.contrib import admin

from .models import Ingredient, Tag, Recipe, RecipeIngredient


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug', 'id')
    search_fields = ('name', 'color', 'slug')
    list_filter = ('name', )


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', 'id')
    list_filter = ('name', )


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'id')
    list_filter = ('name', 'author', 'tags')


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount')
    list_filter = ('ingredient', 'recipe', 'amount')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
