from django.db import models
from django.core import validators

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Тэг',
        help_text='Укажите необходимый тэг')
    color = models.CharField(
        max_length=20,
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

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэг',
        help_text='Укажите необходимый тэг')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор публикации',
        help_text='Укажите автора публикации')
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
    cooking_time = models.IntegerField(
        validators=(
            validators.MinValueValidator(
                1, message='Минимальное время приготовления 1 минута'),),
        verbose_name='Время приготовления',
        help_text='Укажите время приготовления (более 1 минуты)')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент',
        help_text='Укажите необходимый ингридиент')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Укажите необходимый рецепт')
    amount = models.PositiveIntegerField(
        validators=(
            validators.MinValueValidator(
                1, message='Необходим хотя бы один ингридиент'),),
        verbose_name='Количество',
        help_text='Укажите количество')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество ингридиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient')]


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
        ordering = ['-id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite_recipe')]


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
        ordering = ['-id']
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_cart_recipe')]
