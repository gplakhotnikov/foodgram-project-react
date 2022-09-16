from django.contrib import admin

from recipes.models import Favorite, IngredientAmount, Recipe, Cart
from recipes.models import Ingredient, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug',)
    list_editable = ('name', 'color', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',)
    list_editable = ('name', 'measurement_unit')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'author',
        'image',
        'count_added')
    exclude = ('ingredients',)
    #inlines = (IngredientAmountInline,)
    list_filter = ('author', 'name', 'tags')
    search_fields = ('author__username', 'name', 'tags__name')
    empty_value_display = '-пусто-'

    def count_added(self, obj):
        return obj.favorite.count()


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'recipe',
        'ingredient',
        'amount')
    search_fields = ('recipe__name', 'ingredient__name')
    empty_value_display = '-пусто-'


@admin.register(Favorite)
@admin.register(Cart)
class FavoriteShoppingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe')
    search_fields = ('user__username', 'recipe__name')
    empty_value_display = '-пусто-'
