from rest_framework import serializers

from product.models import Product, Review, Specifications
from shop.serializers import ProductImageSerializer, TagSerializer


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("author", "email", "text", "rate", "date")

    def create(self, validated_data):
        validated_data["product"] = Product.objects.get(**self.context)
        return Review.objects.create(**validated_data)


class SpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specifications
        fields = ("name", "value")


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    tags = TagSerializer(many=True)
    reviews = ReviewsSerializer(many=True)
    specifications = SpecificationsSerializer(many=True)
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
        )

    def get_price(self, obj) -> float:
        try:
            return obj.sale_products.salePrice
        except Exception:
            return float(obj.price)
