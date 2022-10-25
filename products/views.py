import django
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from .models import Product
from .serializers import ProductSerializer


# Returns a list of all products, uses django_filters in order to facilitate searching
class ProductView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ("id", "name", "category")
    search_fields = ("id", "name", "category")
