from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Market
from .serializers import MarketSerializer, MarketCreateSerializer, ResolveMarketSerializer


class MarketListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        market_status = request.query_params.get('status', 'active')
        qs = Market.objects.all()
        if market_status == 'active':
            qs = qs.filter(resolved=False)
        elif market_status == 'resolved':
            qs = qs.filter(resolved=True)
        return Response({'markets': MarketSerializer(qs, many=True).data})

    def post(self, request):
        if not (request.user.is_authenticated and request.user.is_admin_user):
            return Response({'error': 'Admin requis.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = MarketCreateSerializer(data=request.data)
        if serializer.is_valid():
            market = serializer.save()
            return Response(MarketSerializer(market).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarketDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, market_id):
        try:
            market = Market.objects.get(pk=market_id)
        except Market.DoesNotExist:
            return Response({'error': 'Marché introuvable.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(MarketSerializer(market).data)


class ResolveMarketView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, market_id):
        if not request.user.is_admin_user:
            return Response({'error': 'Admin requis.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            market = Market.objects.select_for_update().get(pk=market_id)
        except Market.DoesNotExist:
            return Response({'error': 'Marché introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        if market.resolved:
            return Response({'error': 'Ce marché est déjà résolu.'}, status=status.HTTP_409_CONFLICT)

        serializer = ResolveMarketSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        winner_idx = serializer.validated_data['winnerIdx']

        # Mise à jour du marché
        # Le signal handle_market_resolution dans signals.py se déclenchera
        # automatiquement lors de cet appel à .save()
        market.resolved = True
        market.winner_idx = winner_idx
        market.save()

        return Response({
            'marketId': market_id,
            'resolved': True,
            'winnerIdx': winner_idx,
            'message': 'Le marché a été résolu. Les paiements sont traités automatiquement.'
        })
