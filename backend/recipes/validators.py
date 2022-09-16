from rest_framework.validators import ValidationError

from recipes.models import Ingredient, Tag


def validate_ingredients(data):
    if not data:
        raise ValidationError({'ingredients': ['Заполните поле ингридиентов']})
    if len(data) < 1:
        raise ValidationError({'ingredients': ['Выберите ингридиенты']})
    unique_ingredient = []
    for ingredient in data:
        if not ingredient.get('id'):
            raise ValidationError({'ingredients': ['Укажите id ингредиента']})
        id = ingredient.get('id')
        if not Ingredient.objects.filter(id=id).exists():
            raise ValidationError({'ingredients': ['Неизвестный ингридиент']})
        if id in unique_ingredient:
            raise ValidationError(
                {'ingredients': ['Нельзя дублировать ингридиенты']})
        unique_ingredient.append(id)
        amount = int(ingredient.get('amount'))
        if amount < 1:
            raise ValidationError({'amount': ['Количество не может быть менее 1']})
    return data


def validate_tags(data):
    if not data:
        raise ValidationError({'tags': ['Выберите тэги']})
    if len(data) < 1:
        raise ValidationError({'tags': ['Необходимо указать тэги']})
    for tag in data:
        if not Tag.objects.filter(id=tag).exists():
            raise ValidationError({'tags': ['Неизвестный тэг']})
    return data
