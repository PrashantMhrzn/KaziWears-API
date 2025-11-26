from django.urls import path
from .views import first_view, ProductView, OrderView, CategoryView

urlpatterns = [
    path('', first_view),
    path('category/', CategoryView.as_view({'get': 'list'})),
    path('products/', ProductView.as_view({'get': 'list'})),
    path('orders/', OrderView.as_view({'get': 'list'})),
]
