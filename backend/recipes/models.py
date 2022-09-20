from django.db import models
from django.core import validators
from django.conf import settings

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название тэга',
        help_text='Укажите необходимый тэг')
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цвет',
        help_text='Укажите цвет (должен быть уникальным)')
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Адрес',
        help_text='Укажите адрес (должен быть уникальным)')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингридиента',
        help_text='Укажите название ингридиента')
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
        help_text='Выберите единицу измерения')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique ingredient'),)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор публикации',
        help_text='Укажите автора публикации')
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэг',
        help_text='Укажите необходимый тэг')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации',
        help_text='Введите дату публикации')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        verbose_name='Ингридиент',
        help_text='Укажите ингридиент')
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта')
    image = models.ImageField(
        blank=True,
        upload_to='recipes/',
        verbose_name='Изображение для рецепта',
        help_text='Выберите изображение для рецепта')
    text = models.TextField(
        verbose_name='Текст рецепта',
        help_text='Укажите инструкции для приготовления')
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(
                settings.MIN_COOKING_TIME,
                message='Время приготовления должно быть больше'),),
        verbose_name='Время приготовления',
        help_text='Укажите время приготовления')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        verbose_name='Ингридиент',
        help_text='Укажите необходимый ингридиент')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Укажите необходимый рецепт')
    amount = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(
                settings.MIN_AMMOUNT,
                message='Необходимо выбрать больше ингридиентов'),),
        verbose_name='Количество',
        help_text='Укажите количество ингридиентов')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество ингридиентов'
        constraints = (
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'),)

    def __str__(self):
        return self.amount


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь',
        help_text='Укажите пользователя')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт',
        help_text='Укажите рецепт')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = (
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite_recipe'),)

    def __str__(self):
        return self.recipe


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
        help_text='Выберите пользователя')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт',
        help_text='Выберите рецепт')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'
        constraints = (
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_cart_recipe'),)

    def __str__(self):
        return self.recipe
