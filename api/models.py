from django.db import models
from django.contrib.auth import get_user_model
from .utils import generate_random_code
# Create your models here.
User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    SIZE_CHOICES = (
        ('small', 'S'),
        ('medium', 'M'),
        ('large', 'L'),
        ('extra-large', 'XL'),
    )
    name = models.CharField(null=False, blank=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    size = models.CharField(choices=SIZE_CHOICES)
    color = models.CharField(null=True, blank=False)
    stock_quantity = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # if you use generate_random_code(), it would call the function once when the model is loaded and use the same value for every new instance
    unique_code = models.CharField(default=generate_random_code, unique=True, max_length=6)

    def __str__(self):
        return f'{self.category}: {self.name}'

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    PAYMENT_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    )
    PAYMENT_METHOD = (
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('cod', 'Cash on delivery'),
        ('esewa', 'E-sewa'),
        ('connectips', 'ConnectIPS'),
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(default=generate_random_code, unique=True, max_length=6)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_address = models.TextField()
    payment_status = models.CharField(choices=PAYMENT_CHOICES)
    payment_method = models.CharField(choices=PAYMENT_METHOD)

    def __str__(self):
        return f"Order #{self.order_number} by {self.customer.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.order_number}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cart_number = models.CharField(default=generate_random_code, unique=True, max_length=6)

    def __str__(self):
        return f'Cart number: {self.cart_number} of User: {self.user}'

class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=50)

    def __str__(self):
        return f'Cart Item: {self.product} of Cart: {self.cart}'
    
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    stripe_payment_intent_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment of Order:{self.order} Amount:{self.amount} and ID:{self.stripe_payment_intent_id}'