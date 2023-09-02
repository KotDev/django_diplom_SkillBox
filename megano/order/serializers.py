from rest_framework import serializers

from order.models import Order
from product.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    phone = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    fullName = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products",
        )

    def get_phone(self, obj):
        return obj.profile.phone

    def get_email(self, obj):
        return obj.profile.email

    def get_fullName(self, obj):
        return obj.profile.fullName
