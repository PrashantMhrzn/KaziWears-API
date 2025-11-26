from django.urls import path, include
from .views import first_view, ProductView, OrderView, CategoryView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'products', ProductView)
router.register(r'category', CategoryView)
router.register(r'orders', OrderView)

urlpatterns = [
    path('', include(router.urls)),
    # path('category/', CategoryView.as_view({'get': 'list'})),
    # path('products/', ProductView.as_view({'get': 'list'})),
    # path('orders/', OrderView.as_view({'get': 'list'})),
]
