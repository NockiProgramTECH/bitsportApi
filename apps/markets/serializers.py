from rest_framework import serializers
from .models import Market


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = (
            'id', 'title', 'event_date', 'option_a', 'option_b',
            'price_a_sats', 'price_b_sats', 'resolved', 'winner_idx', 'created_at',
        )


class MarketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ('id', 'title', 'event_date', 'option_a', 'option_b', 'price_a_sats', 'price_b_sats')

    def validate(self, data):
        if data['price_a_sats'] + data['price_b_sats'] != 100000:
            raise serializers.ValidationError(
                "La somme price_a_sats + price_b_sats doit être égale à 100 000 sats."
            )
        return data


class ResolveMarketSerializer(serializers.Serializer):
    winnerIdx = serializers.IntegerField()

    def validate_winnerIdx(self, value):
        if value not in (0, 1):
            raise serializers.ValidationError("winnerIdx doit être 0 ou 1.")
        return value
