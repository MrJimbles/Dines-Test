from django.core.validators import MinValueValidator
from django.db import models
from products.models import Product
from datetime import date


# Create your models here.
# Inventory requires a link to the product, the amount of stock and additionally for reporting it requires a notifier for when stock needs reordering
class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    low_notifier = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.product} - {self.stock}"


# Transactions requires a link to the product, the amount of the transaction, the date of the transaction and the total value of the transaction
class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    amount = models.IntegerField(validators=[MinValueValidator(0)])
    date = models.DateField(default=date.today)
    value = models.FloatField()

    def __str__(self):
        return f"{self.amount} of units sold of product {self.product} - {self.date}"
