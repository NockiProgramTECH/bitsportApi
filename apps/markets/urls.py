from django.urls import path
from .views import MarketListView, MarketDetailView, ResolveMarketView

urlpatterns = [
    path('markets', MarketListView.as_view(), name='market-list'),
    path('markets/<str:market_id>', MarketDetailView.as_view(), name='market-detail'),
    path('markets/<str:market_id>/resolve', ResolveMarketView.as_view(), name='market-resolve'),
]
