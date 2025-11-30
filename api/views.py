from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Category, Product, Order, OrderItem, User, Cart, Payment
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, CheckoutSerializer, CartSerializer, PaymentSerializer
from django.db import transaction
import stripe
import os
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Create your views here.
@api_view(['GET'])
def first_view(request):
    return Response({"Detail": "Hello world"})

class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class OrderView(ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


class CartView(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        # Get the data
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        
        # Get validated data
        shipping_address = serializer.validated_data['shipping_address']
        payment_method = serializer.validated_data['payment_method']
        
        try:
            # transaction.atomic() ensures all database operations succeed together or fail together.
            # Without atomic = Buying items one by one. if you fail on item 3, you still have items 1-2 in your cart
            # With atomic = All items scanned together at checkout. if any item fails, entire transaction cancels
            with transaction.atomic():  
                # 1. Get user's cart
                cart = Cart.objects.get(user=request.user)
                # get all cart items from the cart of user with optimization
                cart_items = cart.items.select_related('product').all()

                # 2. Validate cart items
                # Check if the cart items is not empty
                if not cart_items:
                    return Response({"error": "Cart is empty"})
                # check if available and stock quantity
                total_amount = 0
                for item in cart_items:
                    if not item.product.is_available:
                        return Response({"error": f"{item.product.name} is no longer available"})
                    if item.product.stock_quantity < item.quantity:
                        return Response({"error": f"Not enough stock for {item.product.name} stock left {item.product.stock_quantity}"})
                    
                    # calculate the total amout from the products
                    total_amount += item.quantity * item.product.price
                
                # 3. Create order
                order = Order.objects.create(
                    customer = request.user,
                    status = 'pending',
                    total_amount = total_amount,
                    shipping_address = shipping_address,
                    payment_method = payment_method,
                    payment_status='pending'
                )

                # 4. Convert cart items to order items
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order = order,
                        product = cart_item.product,
                        quantity = cart_item.quantity,
                        price_at_purchase = cart_item.product.price,
                        size = cart_item.size,
                        color = cart_item.color
                    )

                    # 5. Update inventory
                    cart_item.product.stock_quantity -= cart_item.quantity
                    cart_item.product.save()

                # 6. Clear cart
                cart.items.all().delete()

                # 7. Return order details
                return Response({
                "success": True,
                "message": "Order created successfully",
                "order_number": order.order_number,
                "total_amount": str(total_amount),
                "order_id": order.id
                })
            
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"})
        except  Exception as e:
            return Response({"error": f"Checkout failed: {str(e)}"})

# Payment request 
class PaymentView(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    # Insted of taking data for normal payment object with all fields, we only take order id for now
    def create(self, request):
        order_id = request.data.get('order_id')

        # Now we need to create the payment intent for the received order
        try:
            # first we get the order of which we are going to process the payment
            order = Order.objects.get(id=order_id, customer=request.user)

            # now we create Stripe PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=int(order.total_amount * 100),
                currency='usd',
                metadata={
                    'order_id': order.id,
                    'customer_id': request.user.id
                }
            )

            # create a payment object 
            payment = Payment.objects.create(
                order = order,
                stripe_payment_intent_id=intent.id,
                amount=order.total_amount
            )

            serializer = self.get_serializer(payment)
            response_data = serializer.data
            response_data['client_secret'] = intent.client_secret
            return Response(response_data)
                    
        except Order.DoesNotExist:
            return Response({"error": "Order not found"})

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """
        Confirm payment status
        POST /api/payment/{id}/confirm/
        """
        payment = self.get_object()
        
        # Check payment status with Stripe
        intent = stripe.PaymentIntent.retrieve(payment.stripe_payment_intent_id)
        
        if intent.status == 'succeeded':
            payment.status = 'completed'
            payment.save()
            
            # Update order status
            payment.order.payment_status = 'paid'
            payment.order.status = 'processing'
            payment.order.save()
            
            return Response({
                "success": True,
                "message": "Payment confirmed successfully",
                "order_status": payment.order.status
            })
        else:
            return Response({
                "error": f"Payment not completed. Status: {intent.status}"
            })