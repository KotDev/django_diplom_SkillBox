from django.http import HttpRequest
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product
from .cart import Cart, create_product_list
from .serializers import BasketSerializer


class BasketView(APIView):
    """View для корзины"""

    def get(self, request: HttpRequest) -> Response:
        """Функция отрисовывает продукты из корзины на странице корзины"""

        cart = Cart(request)  # Инициализируем корзину
        product_list, count = create_product_list(cart)  # Достаём продукты из корзины и их кол-во
        serializer = BasketSerializer(product_list, many=True, context={'count': count})
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: HttpRequest) -> Response:
        """Функция добавляет продукт в корзину или добавляет продукт
        к существующему продукту в корзине"""

        cart = Cart(request)  # Инициализируем корзину
        product_id = request.data['id']  # Достаём id продукта из request
        count_product = request.data['count']  # Достаём кол-во продукта из request
        product = Product.objects.get(id=product_id)  # Получаем нужный продукт по id
        if product.count <= count_product:  # Сверяем кол-во продукта в db и в request
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif product.count <= cart.count_product(product_id):  # Сверяем кол-во продукта в db и в корзине
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            cart.add(product=product,
                     count=count_product)  # Добавляем продукт в корзину
        product_list, count = create_product_list(cart) # Достаём продукты из корзины и их кол-во
        serializer = BasketSerializer(product_list, many=True, context={'count': count})
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: HttpRequest) -> Response:
        """Функция для удаления продукта из корзины"""

        cart = Cart(request)  # Инициализируем корзину
        product_id = request.data['id']
        count_product = request.data['count']
        product = Product.objects.get(id=product_id)
        # Сверяем кол-во продуктов в корзине и кол-во продуктов из request
        if cart.count_product(product_id) == count_product:
            cart.remove_all(product)  # Удаляем сессию тем самым очищая корзину
        else:
            cart.remove(product, count_product)  # Удаляем нужное ко-во продукта из корзины
        product_list, count = create_product_list(cart)
        serializer = BasketSerializer(product_list, many=True, context={'count': count})
        return Response(serializer.data, status=status.HTTP_200_OK)