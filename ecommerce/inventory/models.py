from django.db import models
import random
import string

def generate_unique_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


class Product(models.Model):
    product_id = models.CharField(max_length=10, default=generate_unique_key, unique=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # potentially create currency model with foreign key in case of fx rates
    quantity = models.IntegerField()
    popularity_score = models.IntegerField(default=0)
    tags = models.ManyToManyField('Tag', related_name='products', blank=True)


    def __str__(self):
        return self.name


class ProductTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


