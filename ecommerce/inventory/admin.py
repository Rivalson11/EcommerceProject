
from django.contrib import admin
from .models import Product, ProductCategories


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'popularity_score')
    search_fields = ('name', 'category')

@admin.register(ProductCategories)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)