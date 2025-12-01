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
        fields = ['id', 'order', 'product', 'quantity', 'price_at_purchase', 'color', 'size']

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_number', 'order_date', 'status', 'total_amount', 'shipping_address', 'payment_status', 'payment_method', 'items']

class CartItemSeializer(serializers.ModelSerializer):
    cart = serializers.SlugRelatedField(slug_field='cart_number', queryset=Cart.objects.all())
    product = serializers.SlugRelatedField(slug_field='name', queryset=Product.objects.all())
    class Meta:
        model = CartItems
        fields = ['id', 'cart', 'product', 'quantity', 'size', 'color']


class CartSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    cart_items = CartItemSeializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at', 'cart_number', 'cart_items']
        
class CheckoutSerializer(serializers.Serializer):
    shipping_address = serializers.CharField(required=True)
    payment_method = serializers.ChoiceField(
        choices=[
            ('esewa', 'E-sewa'),
            ('connectips', 'ConnectIPS'),
            ('cod', 'Cash on Delivery'),
            ('visa', 'Visa'),
            ('mastercard', 'Mastercard')
        ],
        required=True
    )

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'stripe_payment_intent_id', 'amount', 'status', 'created_at']