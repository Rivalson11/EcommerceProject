from django.test import TestCase
from django.urls import reverse

from users.models import User


class UserLoginTest(TestCase):
    def setUp(self):
        # Create a user for login testing
        self.user = User.objects.create_user(username="loginuser", password="password123")

    def test_user_login(self):
        # Attempt login with correct credentials
        response = self.client.post(reverse('login'), {
            'username': 'loginuser',
            'password': 'password123'
        })

        # Check for a successful login and redirect
        self.assertEqual(response.status_code, 302)  # Redirect after login
        self.assertRedirects(response, reverse('inventory:products'))