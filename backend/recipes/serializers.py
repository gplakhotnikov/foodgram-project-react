from django.shortcuts import get_object_or_404
from django.db import transaction
from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Favorite, IngredientAmount, Recipe, Cart
from recipes.models import Ingredient, Tag
from recipes.validators import validate_ingredients, validate_tags
from recipes.validators import validate_cooking_time
from users.serializers import CustomUserSerializer


def required(value):
    if value is None:
        raise serializers.ValidationError('Это обязательное поле')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientAmountSerializer(
        read_only=True, many=True, source='ingredientamount_set')
    image = Base64ImageField(validators=[required])
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')
        extra_kwargs = {'image': {'required': True}}

    def get_is_favorited(self, obj):
        user_id = self.context.get('request').user.id
        return Favorite.objects.filter(
            user=user_id, recipe=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user_id = self.context.get('request').user.id
        return Cart.objects.filter(
            user=user_id, recipe=obj.id).exists()

    def create_ingredient_amount(self, valid_ingredients, recipe):
        for ingredient_data in valid_ingredients:
            ingredient = get_object_or_404(
                Ingredient, id=ingredient_data.get('id'))
            IngredientAmount.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=ingredient_data.get('amount'))

    def create_tags(self, data, recipe):
        valid_tags = validate_tags(data.get('tags'))
        tags = Tag.objects.filter(id__in=valid_tags)
        recipe.tags.set(tags)

    @transaction.atomic
    def create(self, validated_data):
        valid_ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.create_tags(self.initial_data, recipe)
        self.create_ingredient_amount(valid_ingredients, recipe)
        return recipe

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        validate_cooking_time(self.initial_data.get('cooking_time'))
        valid_ingredients = validate_ingredients(ingredients)
        data['ingredients'] = valid_ingredients
        return data

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.save()
        instance.tags.remove()
        self.create_tags(self.initial_data, instance)
        instance.ingredientamount_set.filter(recipe__in=[instance.id]).delete()
        valid_ingredients = validated_data.get(
            'ingredients', instance.ingredients)
        self.create_ingredient_amount(valid_ingredients, instance)
        return instance


class ShortRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(validators=[required])

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')
        extra_kwargs = {'image': {'required': True}}
