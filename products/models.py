from django.db import models

# Create your models here.
# Products requires a product name, a price and a category
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    category = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.category}"
