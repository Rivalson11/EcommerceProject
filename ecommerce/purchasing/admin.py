from django.contrib import admin

from purchasing.models import Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'quantity', 'date')
    list_filter = ('date', 'product')
