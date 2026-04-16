from django.conf import settings
from rest_framework import serializers
from .models import Order


class PlaceOrderSerializer(serializers.Serializer):
    marketId = serializers.CharField()
    outcomeIdx = serializers.IntegerField()
    shares = serializers.IntegerField(min_value=1)

    def validate_outcomeIdx(self, value):
        if value not in (0, 1):
            raise serializers.ValidationError("outcomeIdx doit être 0 ou 1.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    orderId = serializers.UUIDField(source='id', read_only=True)
    marketId = serializers.CharField(source='market_id', read_only=True)
    outcomeIdx = serializers.IntegerField(source='outcome_idx', read_only=True)
    pricePaidPerShare_sats = serializers.IntegerField(source='price_per_share_sats', read_only=True)
    totalCostSats = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    settledAt = serializers.DateTimeField(source='settled_at', read_only=True)

    class Meta:
        model = Order
        fields = (
            'orderId', 'marketId', 'outcomeIdx', 'shares',
            'pricePaidPerShare_sats', 'totalCostSats',
            'status', 'createdAt', 'settledAt',
        )

    def get_totalCostSats(self, obj):
        return obj.total_cost_sats


class PositionSerializer(serializers.ModelSerializer):
    marketId = serializers.CharField(source='market_id', read_only=True)
    marketTitle = serializers.CharField(source='market.title', read_only=True)
    outcomeName = serializers.SerializerMethodField()
    investedSats = serializers.SerializerMethodField()
    potentialPayoutSats = serializers.SerializerMethodField()
    potentialProfitSats = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'marketId', 'marketTitle', 'outcomeName', 'shares',
            'investedSats', 'potentialPayoutSats', 'potentialProfitSats', 'status',
        )

    def get_outcomeName(self, obj):
        return obj.market.get_option(obj.outcome_idx)

    def get_investedSats(self, obj):
        return obj.total_cost_sats

    def get_potentialPayoutSats(self, obj):
        return obj.shares * settings.PAYOUT_PER_SHARE_SATS

    def get_potentialProfitSats(self, obj):
        return self.get_potentialPayoutSats(obj) - obj.total_cost_sats
