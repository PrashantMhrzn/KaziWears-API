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

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = Order
        fields = ['customer', 'order_number', 'order_date', 'status', 'total_amount', 'shipping_address', 'payment_status', 'payment_method']


