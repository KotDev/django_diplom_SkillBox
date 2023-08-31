from django.http import HttpRequest
from rest_framework import status, pagination
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product, Sale
from shop.models import Category, Tag
from shop.serializers import CategorySerializer, CatalogSerializer, TagSerializer, SaleSerializer
from .pagination import CustomPagination
from .filter_catalog import filter_product, filter_sorted, filter_popular_product


class CategoryView(APIView):
    """View Категории"""

    def get(self, request: HttpRequest) -> Response:
        category = Category.objects.filter(parent__isnull=True)
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)


class CatalogView(ListAPIView):
    """View для каталога"""

    serializer_class = CatalogSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        data_request = self.request.GET
        data = filter_product(data_request)  # Преобразуем данные из request к словарю для фильтра
        products = Product.objects.filter(**data)  # Получаем продукты по фильтру
        products = filter_sorted(data_request, query=products)  # Сортируем продукты по сортировке
        return products


class ProductLimitedView(APIView):
    """View для продуктов с лимитом"""

    def get(self, request: HttpRequest) -> Response:
        products = Product.objects.filter(limited_edition=True)[:16]
        serializer = CatalogSerializer(products, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class BannersView(APIView):
    """View для 5 случайных продуктов"""

    def get(self, request: HttpRequest) -> Response:
        products = Product.objects.order_by('?')[:5]  # Получаем 5 случайных продуктов
        serializer = CatalogSerializer(products, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class TagsView(APIView):
    """View для тэгов"""

    def get(self, request: HttpRequest) -> Response:
        category_id = request.GET.get('category')  # Получаем id категории если оно есть
        if category_id is None:
            serializer = TagSerializer(Tag.objects.all(), many=True)  # Если нет id категории то возвращаем все тэги
            return Response(serializer.data, status=status.HTTP_200_OK)
        products = Product.objects.filter(category_id=category_id)  # Фильтруем продукты по категории
        tag_set = set()
        for product in products:
            for tag in product.tags.all():
                tag_set.add(tag)  # Получаем уникальные тэги
        serializer = TagSerializer(tag_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PopularView(APIView):
    """View для популярных продуктов"""

    def get(self, request: HttpRequest) -> Response:
        products = filter_popular_product(query=Product.objects.order_by('sorted_index')[:8])
        serializer = CatalogSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SaleView(ListAPIView):
    """View для продуктов со скидкой"""

    serializer_class = SaleSerializer
    model = Sale
    pagination_class = CustomPagination
    queryset = Sale.objects.all()





