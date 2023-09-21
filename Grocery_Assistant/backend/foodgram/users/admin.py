from django.contrib import admin

from .models import Subscriptions, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
    )
    search_fields = ('email', 'username',)
    list_filter = ('is_superuser', 'username', 'email')
    ordering = ['username']


@admin.register(Subscriptions)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'following',)
