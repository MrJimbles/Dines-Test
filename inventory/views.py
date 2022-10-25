from rest_framework.generics import ListAPIView, ListCreateAPIView, UpdateAPIView

from .models import Inventory, Transaction
from .serializers import (
    InventorySerializer,
    InventoryUpdateSerializer,
    TransactionCreateSerializer,
    TransactionSerializer,
)


# Returns a list of all products and their stock levels
class AllInventory(ListAPIView):
    queryset = Inventory.objects.select_related("product").all()
    serializer_class = InventorySerializer

# Allows user to modify the inventory, overwrites the update in order to ensure that the stock does not drop below zero and that the model is incremented by the request rather than replaced.
class ModifyInventory(UpdateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventoryUpdateSerializer
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        try:
            request_mod = int(request.data.get("stock"))
        except:
            request_mod = False
        if request_mod:
            instance = self.get_object()
            modifier_stock = instance.stock + request_mod
            request.data["stock"] = modifier_stock
        return super(ModifyInventory, self).update(request, *args, **kwargs)

# Allows user to create a transaction, overwriting the create in order to ensure that there is enough stock for the order to be created.
class CreateTransaction(ListCreateAPIView):
    queryset = Transaction.objects.select_related("product").all()
    serializer_class = TransactionCreateSerializer

    def create(self, request, *args, **kwargs):
        temp_serializer = self.get_serializer(data=request.data)
        if temp_serializer.is_valid():
            inv = Inventory.objects.get(product=request.data.get("product"))
            if (
                temp_serializer.stock_check(inv)
                and int(temp_serializer.validated_data.get("amount")) > 0
            ):
                inv.stock -= temp_serializer.validated_data.get("amount")
                request.data["value"] = (
                    temp_serializer.validated_data.get("amount") * inv.product.price
                )
                inv.save()
                self.serializer_class = TransactionSerializer

        return super().create(request, *args, **kwargs)
