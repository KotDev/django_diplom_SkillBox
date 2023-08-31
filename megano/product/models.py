from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg

from shop.models import Tag, Category


class Product(models.Model):
    """Модель для хранения товара"""
    title = models.CharField(max_length=200, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name='Категория')
    price = models.DecimalField(default=0, max_digits=10, db_index=True, decimal_places=2, verbose_name='Цена')
    count = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='Кол-во')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    description = models.TextField(verbose_name='Короткое описание')
    fullDescription = models.TextField(verbose_name='Полное описания')
    freeDelivery = models.BooleanField(default=False, verbose_name='Бесплатная доставка')
    tags = models.ManyToManyField(Tag, related_name='tags_product', verbose_name="Тэг")
    available = models.BooleanField(default=True, verbose_name='В наличии')
    limited_edition = models.BooleanField(default=False, verbose_name='Ограниченый тираж')
    sorted_index = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
                                       verbose_name='Индекс сортировки')

    @property
    def rating(self):
        """Подсчёт рейтинга продукта"""
        avg_rating = self.reviews.filter(product=self).aggregate(Avg('rate'))['rate__avg']
        return avg_rating if avg_rating else 0.0

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.title} - {self.price}$"


class Specifications(models.Model):
    """Модель для хранения спецификации о товаре"""
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    value = models.CharField(max_length=200, db_index=True, verbose_name='Значение')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='specifications',
                                verbose_name='Продукты')

    class Meta:
        verbose_name = "Спецификация"
        verbose_name_plural = "Спецификации"

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель для хранения отзывов о товаре"""
    author = models.CharField(max_length=200, verbose_name='Автор')
    email = models.EmailField(verbose_name='Почта автора')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Товар')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    rate = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Оценка')

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"{self.author} - {self.rate}"


def product_image_directori_path(instance: "ProductImage", filename: str) -> str:
    """Путь для хранения картинок товара"""
    return f"app_shop/product_image/product_{instance.pk}/images/{filename}"


class ProductImage(models.Model):
    """Модель для хранения изображения о товаре"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Продукты')
    src = models.ImageField(upload_to=product_image_directori_path, null=True, blank=True, verbose_name='Ссылка')
    alt = models.CharField(max_length=128, verbose_name='Описание')

    class Meta:
        verbose_name = "Картинка товара"
        verbose_name_plural = "Картинки товаров"

    def __str__(self):
        return f"{self.alt} - {self.src}"


class Sale(models.Model):
    """Модель скидок товара"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='sale_products', verbose_name='Продукт')
    sale = models.IntegerField(blank=True, default=0, db_index=True,
                               validators=[MinValueValidator(0), MaxValueValidator(99)],
                               verbose_name='Скидка в %')
    dateTo = models.DateTimeField(blank=True, null=True, verbose_name='Дата начала скидки')
    dateFrom = models.DateTimeField(default="", verbose_name='Дата окончания скидки')

    @property
    def salePrice(self) -> float:
        """Подсчёт скидки на продукт"""
        return float(self.product.price) * (self.sale / 100)

    class Meta:
        verbose_name = "Скидка товара"
        verbose_name_plural = "Скидки товаров"

    def __str__(self):
        return f"{self.sale}%"