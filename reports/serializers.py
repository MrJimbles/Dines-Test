from inventory.models import Transaction
from rest_framework import serializers


class TransReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        depth = 1
        fields = ["id", "product", "amount", "value"]
