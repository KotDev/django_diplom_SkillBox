from django.http import HttpRequest
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductSerializer, ReviewsSerializer


class ProductsDetailView(APIView):
    """View для деталей продуктов"""

    def get(self, request: HttpRequest, id: int) -> Response:
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewProductView(APIView):
    """View для написания отзыва к продукту"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: HttpRequest, id: int) -> Response:
        serializer = ReviewsSerializer(data=request.data, context={'id': id})  # Сериализуем данные
        if serializer.is_valid():
            serializer.save()  # Сохраняем данные в db
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

