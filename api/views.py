from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from .models import Category, Product, Order, OrderItem, User
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer

# Create your views here.
@api_view(['GET'])
def first_view(request):
    return Response({"Detail": "Hello world"})

class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer