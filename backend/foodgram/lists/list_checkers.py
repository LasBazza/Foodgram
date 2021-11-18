from .models import Follow, FavoriteList, ShoppingList


class ListChecker:

    def is_subcribed(self, instance, obj):
        request = instance.context.get('request')
        if request.user is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            follower=request.user,
            author=obj
        ).exists()

    def is_favorited(self, instance, obj):
        request = instance.context.get('request')
        if request.user is None or request.user.is_anonymous:
            return False
        return FavoriteList.objects.filter(
            user=request.user,
            recipes=obj
        ).exists()

    def is_in_shopping_cart(self, instance, obj):
        request = instance.context.get('request')
        if request.user is None or request.user.is_anonymous:
            return False
        return ShoppingList.objects.filter(
            user=request.user,
            recipes=obj
        ).exists()
