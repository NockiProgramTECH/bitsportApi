from django.db import transaction
from django.db.models import F
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle

from apps.authentication.models import User
from apps.markets.models import Market
from .models import Order
from .serializers import PlaceOrderSerializer, OrderSerializer, PositionSerializer


class OrdersThrottle(UserRateThrottle):
    rate = '10/min'
    scope = 'orders'


class OrderListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_throttles(self):
        if self.request.method == 'POST':
            return [OrdersThrottle()]
        return super().get_throttles()

    def get(self, request):
        qs = Order.objects.filter(user=request.user).select_related('market')
        order_status = request.query_params.get('status', 'open')
        market_id = request.query_params.get('marketId')

        if order_status != 'all':
            if order_status == 'open':
                qs = qs.filter(status='open')
            elif order_status == 'settled':
                qs = qs.exclude(status='open')

        if market_id:
            qs = qs.filter(market_id=market_id)

        return Response({'orders': OrderSerializer(qs, many=True).data})

    @transaction.atomic
    def post(self, request):
        serializer = PlaceOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        market_id = serializer.validated_data['marketId']
        outcome_idx = serializer.validated_data['outcomeIdx']
        shares = serializer.validated_data['shares']

        # Vérifier le marché
        try:
            market = Market.objects.get(pk=market_id)
        except Market.DoesNotExist:
            return Response({'error': 'Marché introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        if market.resolved:
            return Response(
                {'error': 'Ce marché est déjà résolu, impossible de parier.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        price_per_share = market.get_price(outcome_idx)
        total_cost = shares * price_per_share

        # Vérifier le solde (avec lock)
        user = User.objects.select_for_update().get(pk=request.user.pk)
        if user.balance_sats < total_cost:
            return Response(
                {'error': f'Solde insuffisant. Requis : {total_cost} sats, disponible : {user.balance_sats} sats.'},
                status=status.HTTP_402_PAYMENT_REQUIRED,
            )

        # Débiter le solde
        User.objects.filter(pk=user.pk).update(balance_sats=F('balance_sats') - total_cost)

        # Créer l'ordre
        order = Order.objects.create(
            user=user,
            market=market,
            outcome_idx=outcome_idx,
            shares=shares,
            price_per_share_sats=price_per_share,
            status='open',
        )
        user.refresh_from_db()

        return Response(
            {
                'orderId': str(order.id),
                'marketId': market_id,
                'outcomeIdx': outcome_idx,
                'shares': shares,
                'pricePaidPerShare_sats': price_per_share,
                'totalCostSats': total_cost,
                'newBalanceSats': user.balance_sats,
                'createdAt': order.created_at,
            },
            status=status.HTTP_201_CREATED,
        )


class PositionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        positions = (
            Order.objects.filter(user=request.user, status='open')
            .select_related('market')
        )
        return Response({'positions': PositionSerializer(positions, many=True).data})
