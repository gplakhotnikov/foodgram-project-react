from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта',
        help_text='Введите адрес электронной почты')
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя',
        help_text='Введите имя пользователя')
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        help_text='Введите имя')
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        help_text='Введите фамилию')
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
        help_text='Придумайте пароль')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Тот, кто подписывается')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор (подписка)',
        help_text='Тот, на кого подписываются')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'user'),
                name='unique_follow'),)

    def __str__(self):
        return f"{self.user} подписан на {self.author}"
