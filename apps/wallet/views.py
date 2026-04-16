import uuid
from django.conf import settings
from django.db import transaction
from django.db.models import F
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.authentication.models import User
from .serializers import DepositSerializer, WithdrawSerializer


def balance_response(user):
    sats = user.balance_sats
    return {
        'balanceSats': sats,
        'balanceBTC': f'{sats / 100_000_000:.8f}',
    }


class BalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.refresh_from_db()
        return Response(balance_response(request.user))


class DepositView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        if not settings.DEBUG:
            return Response(
                {'error': 'Dépôt manuel désactivé en production.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = DepositSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        amount = serializer.validated_data['amountSats']
        User.objects.filter(pk=request.user.pk).update(balance_sats=F('balance_sats') + amount)
        request.user.refresh_from_db()
        return Response(balance_response(request.user))


class WithdrawView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = WithdrawSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        amount = serializer.validated_data['amountSats']
        address = serializer.validated_data['address']

        user = User.objects.select_for_update().get(pk=request.user.pk)
        if user.balance_sats < amount:
            return Response(
                {'error': 'Solde insuffisant.'},
                status=status.HTTP_402_PAYMENT_REQUIRED,
            )

        User.objects.filter(pk=user.pk).update(balance_sats=F('balance_sats') - amount)
        user.refresh_from_db()

        # En mode réel, envoyer via LNbits / Electrum ici
        simulated_txid = uuid.uuid4().hex

        return Response({
            'txid': simulated_txid,
            'address': address,
            'amountSats': amount,
            'remainingBalanceSats': user.balance_sats,
        })


class DemoResetView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        if not settings.DEBUG:
            return Response({'error': 'Endpoint désactivé en production.'}, status=status.HTTP_403_FORBIDDEN)

        from apps.orders.models import Order
        Order.objects.filter(user=request.user, status='open').delete()
        User.objects.filter(pk=request.user.pk).update(
            balance_sats=settings.DEMO_INITIAL_BALANCE_SATS
        )
        return Response({
            'message': 'Demo reset successful',
            'newBalanceSats': settings.DEMO_INITIAL_BALANCE_SATS,
        })
