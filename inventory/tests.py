import json

from django.urls import reverse
from numpy import product
from products.models import Product
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Inventory

# Create your tests here.
class InventoryManagementCase(APITestCase):

    inv_url = reverse("all-inventory")

    def inv_specific(self, num):
        return reverse("modify-inventory", kwargs={"id": num})

    def setUp(self):
        # Create test products
        self.product_1 = Product.objects.create(
            name="Toast", price="10.00", category="Food"
        )
        self.product_2 = Product.objects.create(
            name="Beans", price="7.25", category="Food"
        )
        # Create Inventory entries for test products
        self.inventory_1 = Inventory.objects.create(
            product=self.product_1, stock=5, low_notifier=3
        )
        self.inventory_2 = Inventory.objects.create(
            product=self.product_2, stock=2, low_notifier=4
        )

    def test_list_all_stock(self):
        # Run a get on inventory url
        response = self.client.get(self.inv_url)

        # Check that we recieve a 200 code and check the JSON of the response is as expected
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            [
                {
                    "id": 1,
                    "product": {
                        "id": 1,
                        "name": "Toast",
                        "price": 10.0,
                        "category": "Food",
                    },
                    "stock": 5,
                    "low_notifier": 3,
                },
                {
                    "id": 2,
                    "product": {
                        "id": 2,
                        "name": "Beans",
                        "price": 7.25,
                        "category": "Food",
                    },
                    "stock": 2,
                    "low_notifier": 4,
                },
            ],
        )

    def test_increment_stock(self):
        # Run a put on inventory url for inventory 1
        response = self.client.put(
            self.inv_specific(1),
            json.dumps({"stock": 1}),
            content_type="application/json",
        )

        # Check that we recieve a 200 and that the response is as expected
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["stock"], 6)

    def test_decrement_stock(self):
        # Run a put on inventory url for inventory 2
        response = self.client.put(
            self.inv_specific(2),
            json.dumps({"stock": -1}),
            content_type="application/json",
        )

        # Check that we recieve a 200 and that the response is as expected
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["stock"], 1)

    def test_decrement_past_zero(self):
        # Run a put on inventory url for inventory 2
        response = self.client.put(
            self.inv_specific(2),
            json.dumps({"stock": -30}),
            content_type="application/json",
        )

        # Check that we recieve a Bad Request code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_increment_not_a_number(self):
        # Run a put on inventory url for inventory 2
        response = self.client.put(
            self.inv_specific(2),
            json.dumps({"stock": "thirty"}),
            content_type="application/json",
        )

        # Check that we recieve a Bad Request code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TransactionCase(APITestCase):
    trans_url = reverse("create-transaction")

    def setUp(self):
        # Create test products
        self.product_1 = Product.objects.create(
            name="Toast", price="10.00", category="Food"
        )
        self.product_2 = Product.objects.create(
            name="Beans", price="7.25", category="Food"
        )
        # Create Inventory entries for test products
        self.inventory_1 = Inventory.objects.create(
            product=self.product_1, stock=5, low_notifier=3
        )
        self.inventory_2 = Inventory.objects.create(
            product=self.product_2, stock=2, low_notifier=4
        )

    def test_create_transaction(self):
        # Post transaction to transaction url for product 1
        response = self.client.post(
            self.trans_url,
            json.dumps({"product": 1, "amount": 1, "date": "2022-10-25"}),
            content_type="application/json",
        )

        # Check that we recieve a 201 created and that the response is as expected
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content),
            {"id": 1, "product": 1, "amount": 1, "date": "2022-10-25", "value": 10.0},
        )

        # Check that product 1 has decremented to 4 in stock
        self.inventory_1.refresh_from_db()
        self.assertEqual(self.inventory_1.stock, 4)

    def test_transaction_not_enough_stock(self):
        # Post transaction to transaction url for product 1
        response = self.client.post(
            self.trans_url,
            json.dumps({"product": 1, "amount": 200, "date": "2022-10-25"}),
            content_type="application/json",
        )

        # Check that we recieve a 400 bad request and that the response is as expected
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {"amount": "Not enough stock to process transaction"},
        )

        # Check that product 1 has not decremented to 4 in stock
        self.inventory_1.refresh_from_db()
        self.assertEqual(self.inventory_1.stock, 5)

    def test_transaction_string(self):
        # Post transaction to transaction url for product 1
        response = self.client.post(
            self.trans_url,
            json.dumps({"product": 1, "amount": "twenty", "date": "2022-10-25"}),
            content_type="application/json",
        )

        # Check that we recieve a 400 bad request and that the response is as expected
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content), {"amount": ["A valid integer is required."]}
        )

        # Check that product 1 has not decremented to 4 in stock
        self.inventory_1.refresh_from_db()
        self.assertEqual(self.inventory_1.stock, 5)

    def test_transaction_product_string(self):
        # Post transaction to transaction url for product 1
        response = self.client.post(
            self.trans_url,
            json.dumps({"product": "one", "amount": 1, "date": "2022-10-25"}),
            content_type="application/json",
        )

        # Check that we recieve a 400 bad request and that the response is as expected
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {"product": ["Incorrect type. Expected pk value, received str."]},
        )

    def test_transaction_negative(self):
        # Post transaction to transaction url for product 1
        response = self.client.post(
            self.trans_url,
            json.dumps({"product": 1, "amount": -1, "date": "2022-10-25"}),
            content_type="application/json",
        )

        # Check that we recieve a 400 bad request and that the response is as expected
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {"amount": ["Ensure this value is greater than or equal to 0."]},
        )
