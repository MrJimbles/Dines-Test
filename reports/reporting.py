from django.db.models import F
from inventory.models import Inventory, Transaction
from inventory.serializers import InventorySerializer

from .serializers import TransReportSerializer


class EOD_Reports:
    def transactions(rep_date):
        # Grab all transactions for the specified day and serialize it
        trans = Transaction.objects.select_related("product").filter(date=rep_date)

        serializer = TransReportSerializer(trans, many=True)
        # Create a sum of all transaction values for an end of day take
        total_sales = sum(x.value for x in trans)
        return {"total_sales": total_sales, "transactions": serializer.data}

    def low_stock():
        # Grab all low stock, comparing current stock to the low notifier
        inv = Inventory.objects.select_related("product").filter(
            stock__lte=F("low_notifier")
        )
        serializer = InventorySerializer(inv, many=True)
        return serializer.data

    def all_stock():
        # Grab all stock
        inv = Inventory.objects.select_related("product").all()
        serializer = InventorySerializer(inv, many=True)
        return serializer.data
