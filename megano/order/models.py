from django.db import models

from accounts.models import Profile
from product.models import Product


class Order(models.Model):
    """Модель заказов"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Профиль', related_name='profile')
    createdAt = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    deliveryType = models.CharField(max_length=30,verbose_name="Способ доставки")
    paymentType = models.CharField(max_length=30, verbose_name='Способ оплаты')
    totalCost = models.DecimalField(default=0, max_digits=10, db_index=True, decimal_places=2, verbose_name='Сумма')
    status = models.CharField(max_length=50, verbose_name="Статус оплаты")
    city = models.CharField(max_length=200, verbose_name="Город")
    address = models.CharField(max_length=200, verbose_name="Адрес")
    products = models.ManyToManyField(Product, verbose_name='Продукты', related_name='orders')

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"{self.profile} - {self.city}"


class CountProductinOrder(models.Model):
    """Промежуточная модель заказов"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    count = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Продукт-заказ"
        verbose_name_plural = "Продукты-заказы"