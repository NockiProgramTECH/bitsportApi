from django.urls import path
from .views import BalanceView, DepositView, WithdrawView, DemoResetView

urlpatterns = [
    path('balance', BalanceView.as_view(), name='wallet-balance'),
    path('deposit', DepositView.as_view(), name='wallet-deposit'),
    path('withdraw', WithdrawView.as_view(), name='wallet-withdraw'),
    path('../demo/reset', DemoResetView.as_view(), name='demo-reset'),
]
