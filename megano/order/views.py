from django.http import HttpRequest
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.cart import Cart
from order.models import Order, CountProductinOrder
from product.models import Product
from .serializers import OrderSerializer


class OrderView(APIView):
    """View для заказа"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: HttpRequest) -> Response:
        data = Order.objects.filter(profile_id=request.user.profile.pk)  # Получаем заказы пользователя
        serialize = OrderSerializer(data, many=True)  # Сериализуем данные
        return Response(serialize.data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest) -> Response:
        cart = Cart(request)  # Инициализируем корзину
        # Получаем данные из request
        request_data = [(data['id'], data['price'], data['count']) for data in request.data]
        products = Product.objects.filter(id__in=[data[0] for data in request_data])  # Получаем объекты продуктов
        order = Order.objects.create(profile=request.user.profile,
                                     totalCost=cart.total_price())  # Создаём заказ на основе полученых данных
        response_data = {"orderId": order.pk}
        order.products.set(products)  # Добавляем продукты к заказу
        order.save()  # Сохраняем данные в db
        return Response(response_data, status=status.HTTP_200_OK)


class OrderDetailView(APIView):
    """View для деталей продукта"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: HttpRequest, id: int) -> Response:
        data = Order.objects.get(pk=id)  # Получаем объект заказа по id
        serialized = OrderSerializer(data)
        cart = Cart(request).cart  # Получаем сессию корзины
        data = serialized.data
        try:
            products_in_order = data['products']  # Достаём продукт из сериализованных данных
            query = CountProductinOrder.objects.filter(order_id=id)  # Получаем объект заказа
            prods = {obj.product.pk: obj.count for obj in query}  # Получаем уникальные продукты
            for prod in products_in_order:
                prod['count'] = prods[prod['id']]
        except Exception:
            products_in_order = data['products']  # Достаём продукт из сериализованных данных
            for prod in products_in_order:
                prod['count'] = cart[str(prod['id'])]['count']

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest, id: int) -> Response:
        cart = Cart(request)  # Инициализируем корзину
        order = Order.objects.get(id=id)  # Получаем добъект заказа
        data = request.data
        order.fullName = data['fullName']  # Записываем имя пользователя
        order.phone = data['phone']  # Записываем телефон пользователя
        order.email = data['email']  # Записываем email пользователя
        order.deliveryType = data['deliveryType']  # Записываем тип доставки
        order.city = data['city']  # Записываем город
        order.address = data['address']  # Записываем адрес
        order.paymentType = data['paymentType']  # Записываем тип оплаты
        order.status = 'Ожидает оплаты'  # Записываем статус оплаты
        if data['deliveryType'] == 'express':  # Проверяем тип доставки
            order.totalCost += 50
        else:
            if order.totalCost < 200:
                order.totalCost += 20

        for product in data['products']:
            obj = Product.objects.get(id=product['id'])
            obj.count = obj.count - product['count']
            print(obj.count)
            if obj.count == 0:
                obj.available = False
            obj.save()
            CountProductinOrder.objects.get_or_create(
                order_id=order.pk,
                product_id=product['id'],
                count=product['count']
            )  # Создаём заказ в промежуточной таблице заказов

        order.save()  # Сохраняем данные в модели
        cart.clear()  # Очищаем корзину
        return Response(request.data, status=status.HTTP_201_CREATED)


class PaymentView(APIView):
    """View для оплаты заказа"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: HttpRequest, id: int) -> Response:
        order = Order.objects.get(id=id)  # Получаем объект заказа
        order.status = 'Оплачен'  # Изменяем статус заказа
        order.save()  # Сохраняем данные в db
        return Response(request.data, status=status.HTTP_200_OK)