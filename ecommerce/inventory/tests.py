
from django.test import TestCase
from django.urls import reverse
from model_bakery import baker  # Using model_bakery instead of model_mommy

from inventory.models import Product, ProductCategories
from purchasing.models import PrePurchase
from users.models import User


class ProductListViewTest(TestCase):
    def setUp(self):
        # Create test products using model_bakery
        self.products = baker.make(Product, _quantity=5)

    def test_product_list_view(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse('inventory:products'))
        self.assertEqual(response.status_code, 200)

        # Check that all products appear in the response context
        for product in self.products:
            self.assertContains(response, product.name)

    def test_redirect_on_no_login(self):

        response = self.client.get(reverse('inventory:products'))
        self.assertEqual(response.status_code, 302)


class AddToCartModalViewTest(TestCase):
    def setUp(self):
        # Create a user and log in
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

        # Create a product for testing
        self.product = baker.make(Product, quantity=10)

    def test_add_to_cart(self):
        # Define the quantity to add
        quantity_to_add = 3

        # Send POST request to add the product to the cart
        response = self.client.post(
            reverse('purchasing:add_to_cart_modal', args=[self.product.id]),
            {'quantity': quantity_to_add}
        )

        # Check response status
        self.assertEqual(response.status_code, 200)

        # Check if a PrePurchase object was created with the correct values
        self.assertTrue(PrePurchase.objects.filter(
            shopping_cart__customer=self.user,
            product=self.product,
            quantity=quantity_to_add
        ).exists())


class ProductCreateViewTest(TestCase):
    def setUp(self):
        # Create a user and give them staff privileges
        self.staff_user = User.objects.create_user(username="adminuser", password="adminpass")
        self.staff_user.is_staff = True
        self.staff_user.save()

        # Log in as the staff user
        self.client.login(username="adminuser", password="adminpass")
        self.category = ProductCategories.objects.create(name='TestCategory')

    def test_product_create_view(self):
        # Define product data for creation
        product_data = {
            'product_id': 'NewProduct',
            'name': 'New Product',
            'categories': self.category.id,
            'price': 100.00,
            'quantity': 5,
            'popularity_score': 10
        }

        # Send POST request to create the new product
        response = self.client.post(reverse('inventory:product_add'), data=product_data)

        if response.context and 'form' in response.context:
            print("Form errors:", response.context['form'].errors)
        # Check for redirect after creation
        self.assertEqual(response.status_code, 302)  # Should redirect after creation

        # Verify the product was created in the database
        self.assertTrue(Product.objects.filter(name='New Product', price=100.00).exists())