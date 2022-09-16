from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User, Subscription


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    search_fields = ('email', 'username')
    list_filter = ('email', 'username')
    ordering = ('pk',)
    empty_value_display = '-пусто-'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'author')
    search_fields = ('user__username', 'author__username')
    empty_value_display = '-пусто-'
