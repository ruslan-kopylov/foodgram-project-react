from django.contrib import admin

from .models import CustomUser, Subscribe


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name')
    search_fields = ('email', 'username',)
    list_filter = ('email', 'username')


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'subscriber')
    search_fields = ('author', 'subscriber',)
    list_filter = ('author', 'subscriber',)
