from django.contrib import admin
from .models import Order, CountProductinOrder


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Регистрация модели Заказа"""

    list_display = ['profile',
                    'totalCost',
                    'status',
                    'paymentType',
                    'deliveryType',
                    'city',
                    'createdAt']
    list_filter = ['profile', 'status', 'paymentType', 'deliveryType', 'city', 'createdAt']
    search_fields = ['profile']


@admin.register(CountProductinOrder)
class CountProductinOrderAdmin(admin.ModelAdmin):
    """Регистрация модели Продукт-Заказ"""

    list_display = ['order', 'product', 'count']
    list_filter = ['count', 'product']
    search_fields = ['order']
