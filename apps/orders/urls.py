from django.urls import path
from .views import (
    OrderListCreateView, PositionsView, 
    OrderSellView, OrderBuyView, SecondaryMarketListView
)

urlpatterns = [
    path('orders', OrderListCreateView.as_view(), name='order-list-create'),
    path('positions', PositionsView.as_view(), name='positions'),
    path('orders/sell/<uuid:order_id>', OrderSellView.as_view(), name='order-sell'),
    path('orders/buy/<uuid:order_id>', OrderBuyView.as_view(), name='order-buy'),
    path('secondary-market', SecondaryMarketListView.as_view(), name='secondary-market'),
]
