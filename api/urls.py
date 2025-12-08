from django.urls import path, include
from .views import ProductView, OrderView, CategoryView, CartView, PaymentView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'products', ProductView)
router.register(r'category', CategoryView)
router.register(r'orders', OrderView, basename='order')
router.register(r'payment', PaymentView, basename='payment')
router.register(r'cart', CartView, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
]
