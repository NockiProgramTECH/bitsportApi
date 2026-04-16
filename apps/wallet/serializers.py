from rest_framework import serializers


class DepositSerializer(serializers.Serializer):
    amountSats = serializers.IntegerField(min_value=1)


class WithdrawSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=100)
    amountSats = serializers.IntegerField(min_value=1)

    def validate_address(self, value):
        # Validation basique adresse Bitcoin (mainnet / testnet / bech32)
        if not (value.startswith('bc1') or value.startswith('1') or
                value.startswith('3') or value.startswith('tb1')):
            raise serializers.ValidationError("Adresse Bitcoin invalide.")
        return value
