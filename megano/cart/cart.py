from decimal import Decimal
from django.conf import settings
from django.http import HttpRequest

from product.models import Product


class Cart(object):
    """Корзина для продуктов"""

    def __init__(self, request: HttpRequest):
        """Инициализация корзины при помощи django-session"""

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)  # Достаём существующую сессию
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}  # Создаём новую сессию
        self.cart = cart  # Оставляем текущую сессию

    def add(self, product, count: int) -> None:
        """Метод для добавленя продукта в корзину"""

        product_id = str(product.id)  # Получаем id продукта
        try:
            price = product.sale_products.salePrice  # Проверяем есть ли скидка на товар
        except Exception:
            price = product.price  # Если скидки нет возвращаем обычную цену товара
        if product_id not in self.cart:  # Проверяем есть ли этот продукт в корзине
            self.cart[product_id] = {
                "count": count,
                "price": str(price),
            }  # Добавляем новый продукт
        else:
            self.cart[product_id][
                "count"
            ] += count  # Прибавляем кол-во продукта к существующему продукту
        self.save()  # Сохраняем сессию

    def save(self) -> None:
        """Метод сохранения сессии"""

        self.session.save()

    def remove_all(self, product) -> None:
        """Метод для полного удаления продукта из корзины"""

        product_id = str(product.id)
        if product_id in self.cart:  # Проверяем есть продукт в корзине
            del self.cart[product_id]  # Удаляем продукт из сессии
            self.save()

    def remove(self, product, count: int) -> None:
        product_id = str(product.id)
        if product_id in self.cart:  # Проверяем есть продукт в корзине
            self.cart[product_id][
                "count"
            ] -= count  # Удаляем указанное кол-во продуктов из сессии
            self.save()

    def __iter__(self):
        """Метод для получения всех продуктов из корзины"""

        prodict_ids = self.cart.keys()  # Получаем id продуктов
        products = Product.objects.filter(
            id__in=prodict_ids
        )  # Получаем все объекты продуктов из корзины
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["count"]
            yield item

    def total_price(self) -> float:
        """Метод для получения полной суммы всех товаров в корзине"""

        return sum(
            Decimal(item["price"]) * item["count"] for item in self.cart.values()
        )

    def count_product(self, product_id: int) -> int:
        """Метод для получения кол-во продукта в корзине"""

        try:
            return self.cart[str(product_id)]["count"]
        except KeyError:
            return 0

    def clear(self) -> None:
        """Метод для очищения корзины"""

        del self.session[settings.CART_SESSION_ID]  # Удаляем текущую сессию
        self.save()


def create_product_list(cart: Cart) -> tuple:
    """Функция для получения списка продуктов и их кол-во"""

    product_list = [
        product["product"] for product in cart
    ]  # Получаем продукты из корзины
    count = {
        product["product"].id: cart.count_product(
            product_id=product["product"].id
        )  # Получаем кол-во продукта
        for product in cart
    }
    return product_list, count
