from django.conf import settings
from rest_framework.validators import ValidationError

from recipes.models import Ingredient, Tag


def validate_ingredients(data):
    unique = []
    if not data:
        raise ValidationError(
            {'ingredients': ['Заполните поле ингридиентов']})
    if len(data) < 1:
        raise ValidationError(
            {'ingredients': ['Необходимо выбрать ингридиенты']})
    for ingredient in data:
        if not ingredient.get('id'):
            raise ValidationError(
                {'ingredients': ['Отсутствует id ингредиента']})
        id = ingredient.get('id')
        if not Ingredient.objects.filter(id=id).exists():
            raise ValidationError(
                {'ingredients': ['Неизвестный ингридиент']})
        if id in unique:
            raise ValidationError(
                {'ingredients': ['Нельзя дублировать ингридиенты']})
        unique.append(id)
        amount = int(ingredient.get('amount'))
        if amount < settings.MIN_AMMOUNT:
            raise ValidationError(
                {'amount': ['Необходимо выбрать большее количество']})
    return data


def validate_cooking_time(data):
    if int(data) < settings.MIN_COOKING_TIME:
        raise ValidationError(
            {'cooking_time': ['Слишком маленькое время приготовления']})
    return data


def validate_tags(data):
    if not data:
        raise ValidationError(
            {'tags': ['Выберите тэги']})
    if len(data) < 1:
        raise ValidationError(
            {'tags': ['Необходимо выбрать минимум один тэг']})
    for tag in data:
        if not Tag.objects.filter(id=tag).exists():
            raise ValidationError(
                {'tags': ['Неизвестный тэг']})
    return data
