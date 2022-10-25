from rest_framework import serializers
from .models import Inventory, Transaction


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        depth = 1
        fields = ["id", "product", "stock", "low_notifier"]


class InventoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        depth = 1
        fields = ["id", "product", "stock"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "product", "amount", "date", "value"]


class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "product", "amount", "date"]

    def stock_check(self, inv):
        # Used to validate there is enough stock to process the transaction
        if 0 < self.data.get("amount") <= inv.stock:
            return True
        else:
            raise serializers.ValidationError(
                {"amount": "Not enough stock to process transaction"}
            )
