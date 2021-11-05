from django.contrib import admin

from .models import FavoriteList, ShoppingList


class FavoriteListAdmin(admin.ModelAdmin):
    list_display = ('user', )
    list_filter = ('user', )


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user', )
    list_filter = ('user',)


admin.site.register(FavoriteList, FavoriteListAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
