from django.db import models
from inventory.models import Product
from users.models import User
from django.utils import timezone


class Purchase(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(default=timezone.now)
