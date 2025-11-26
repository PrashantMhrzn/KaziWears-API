from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'size', 'color', 'stock_quantity', 'is_available', 'created_at', 'updated_at', 'unique_code']


class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.SlugRelatedField(slug_field='order_number', queryset=Order.objects.all())
    product = serializers.SlugRelatedField(slug_field='name', queryset=Product.objects.all())
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price_at_purchase']

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['customer', 'order_number', 'order_date', 'status', 'total_amount', 'shipping_address', 'payment_status', 'payment_method', 'items']