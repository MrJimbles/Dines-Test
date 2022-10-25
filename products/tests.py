import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Product


class ProductCheckCase(APITestCase):

    product_url = reverse("product-view")

    def setUp(self):
        # Create test products
        self.product_1 = Product.objects.create(
            name="Toast", price="10.00", category="Food"
        )
        self.product_2 = Product.objects.create(
            name="Beans", price="7.25", category="Food"
        )
        self.product_3 = Product.objects.create(
            name="Car", price="1000.00", category="Vehicle"
        )

    def test_list_all_products(self):
        # Run a get on product url
        response = self.client.get(self.product_url)

        # Check that we recieve a 200 code and check the JSON of the response is as expected
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            [
                {"id": 1, "name": "Toast", "price": 10.0, "category": "Food"},
                {"id": 2, "name": "Beans", "price": 7.25, "category": "Food"},
                {"id": 3, "name": "Car", "price": 1000.0, "category": "Vehicle"},
            ],
        )

    def test_product_search(self):
        # Run a get on product url providing a url query to search the name
        response = self.client.get(self.product_url + "?search=Toast")

        # Check that we recieve a 200 code and check the JSON of the response is as expected
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            [{"id": 1, "name": "Toast", "price": 10.0, "category": "Food"}],
        )

    def test_category_search(self):
        # Run a get on product url providing a url query to search the category
        response = self.client.get(self.product_url + "?search=Food")

        # Check that we recieve a 200 code and check the JSON of the response is as expected
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            [
                {"id": 1, "name": "Toast", "price": 10.0, "category": "Food"},
                {"id": 2, "name": "Beans", "price": 7.25, "category": "Food"},
            ],
        )
