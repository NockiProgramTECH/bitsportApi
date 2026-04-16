from django.urls import path
from .views import OrderListCreateView, PositionsView

urlpatterns = [
    path('orders', OrderListCreateView.as_view(), name='order-list-create'),
    path('positions', PositionsView.as_view(), name='positions'),
]
