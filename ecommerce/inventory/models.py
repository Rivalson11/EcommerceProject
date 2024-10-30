from django.db import models
import random
import string
from django.utils import timezone


def generate_unique_key():
    return "".join(random.choices(string.ascii_letters + string.digits, k=10))


class ProductCategories(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.CharField(max_length=10, default=generate_unique_key, unique=True)
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField(ProductCategories)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # potentially create currency model with foreign key in case of fx rates
    quantity = models.IntegerField()
    popularity_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-popularity_score", "name"]

    def __str__(self):
        return self.name
