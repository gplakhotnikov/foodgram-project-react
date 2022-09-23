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
    list_filter = ('measurement_unit',)
    search_fields = ('name', 'measurement_unit')
    empty_value_display = '-пусто-'


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ingredient',
        'recipe',
        'amount')
    list_filter = ('recipe__tags',)
    search_fields = ('recipe__name',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteShoppingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',)
    list_filter = ('recipe__tags',)
    search_fields = ('recipe__name', 'user__username', 'user__email')
    empty_value_display = '-пусто-'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe')
    list_filter = ('recipe__tags',)
    search_fields = ('recipe__name', 'user__username', 'user__email')
    empty_value_display = '-пусто-'


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'author',
        'image',
        'count_added')
    inlines = (IngredientAmountInline,)
    list_filter = ('tags',)
    search_fields = ('name', 'author__username', 'author__email')
    empty_value_display = '-пусто-'

    def get_form(self, request, obj=None, **kwargs):
        form = super(RecipeAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['image'].required = True
        return form

    def count_added(self, obj):
        return obj.favorite.count()
