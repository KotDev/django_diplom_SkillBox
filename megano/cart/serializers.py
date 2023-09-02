from product.serializers import ProductSerializer
from rest_framework import serializers


class BasketSerializer(ProductSerializer):
    count = serializers.SerializerMethodField()

    def get_count(self, obj):
        return self.context["count"][obj.id]
