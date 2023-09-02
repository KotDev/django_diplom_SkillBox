from django.contrib import admin
from .models import Avatar, Profile


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    """Регистрация модели аватара"""

    list_display = ["alt", "src"]
    search_fields = ["alt"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Регистрация модели профиля"""

    list_display = ["user", "fullName", "phone", "email"]
    search_fields = ["user", "fullName", "email"]
