from django.db import models
from inventory.models import Product
from users.models import User
from django.utils import timezone


class Purchase(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)
