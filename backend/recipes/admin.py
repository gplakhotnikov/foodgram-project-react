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
    search_fields = ('name', 'measurement_unit')
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
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name', 'author')
    empty_value_display = '-пусто-'

    def count_added(self, obj):
        return obj.favorite.count()


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ingredient',
        'recipe',
        'amount')
    empty_value_display = '-пусто-'


@admin.register(Favorite)
@admin.register(Cart)
class FavoriteShoppingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe')
    empty_value_display = '-пусто-'
