from django.contrib import admin
from .models import Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Регистрация модели Категории товара"""

    list_display = ['title',
                    'src',
                    'alt',
                    'parent']
    list_filter = ['title', 'parent']
    search_fields = ['title']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Регистрация модели тэга товара"""

    list_display = ["name"]
    search_fields = ['name']