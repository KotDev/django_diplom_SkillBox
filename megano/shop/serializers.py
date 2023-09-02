from django.db.models import Count
from rest_framework import serializers

from shop.models import Category, Tag
from product.models import Product, ProductImage, Sale


class CategorySerializer(serializers.ModelSerializer):

    subcategories = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "title", "image", "subcategories")

    def get_subcategories(self, obj):
        subcategories = obj.children.all()
        subcategories_data = [
            {
                "id": subcat.id,
                "title": subcat.title,
                "image": {
                    "src": subcat.src.url,
                    "alt": subcat.alt,
                },
            }
            for subcat in subcategories
        ]
        return subcategories_data

    def get_image(self, obj):
        image_data = {
            "src": obj.src.url,
            "alt": obj.alt,
        }
        return image_data


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("src", "alt")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class CatalogSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()
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
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        )

    def get_reviews(self, obj):
        reviews = obj.reviews.aggregate(count_text=Count("text"))["count_text"]
        return reviews

    def get_price(self, obj) -> float:
        try:
            return obj.sale_products.salePrice
        except Exception:
            return float(obj.price)


class SaleSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    salePrice = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ("id", "price", "salePrice", "dateFrom", "dateTo", "title", "images")

    def get_price(self, obj):
        return obj.product.price

    def get_salePrice(self, obj):
        return obj.salePrice

    def get_title(self, obj):
        return obj.product.title

    def get_images(self, obj):
        images = []
        images_tmp = obj.product.images.all()
        for image in images_tmp:
            images.append({"src": f"/media/{image.src}", "alt": image.alt})
        return images

    def get_id(self, obj):
        return obj.product_id
