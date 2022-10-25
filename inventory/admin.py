from django.contrib import admin

from .models import Inventory, Transaction

# Register your models here.
admin.site.register(Inventory)
admin.site.register(Transaction)
