"""dines_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from inventory.views import AllInventory, CreateTransaction, ModifyInventory
from products.views import ProductView
from reports.views import DayReport

urlpatterns = [
    path("admin/", admin.site.urls),
    path("products/", ProductView.as_view(), name="product-view"),
    path("inventory/", AllInventory.as_view(), name="all-inventory"),
    path("inventory/<int:id>", ModifyInventory.as_view(), name="modify-inventory"),
    path("transactions/", CreateTransaction.as_view(), name="create-transaction"),
    path("reports/", DayReport.as_view(), name="day-report"),
]
