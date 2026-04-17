from rest_framework import serializers
from .models import Market


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = (
            'id', 'title', 'event_date', 'option_a', 'option_b',
            'price_a_sats', 'price_b_sats', 'votes_a', 'votes_b',
            'resolved', 'winner_idx', 'created_at',
        )


class MarketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ('id', 'title', 'event_date', 'option_a', 'option_b')

    def create(self, validated_data):
        from django.conf import settings
        payout = getattr(settings, 'PAYOUT_PER_SHARE_SATS', 10000)
        # Par défaut, cote = 10 donc prix = payout / 10
        default_price = payout // 10
        validated_data['price_a_sats'] = default_price
        validated_data['price_b_sats'] = default_price
        return super().create(validated_data)


class ResolveMarketSerializer(serializers.Serializer):
    winnerIdx = serializers.IntegerField()

    def validate_winnerIdx(self, value):
        if value not in (0, 1):
            raise serializers.ValidationError("winnerIdx doit être 0 ou 1.")
        return value
