from django.contrib import admin

from purchasing.models import Purchase, ShoppingCart, PrePurchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'quantity', 'date')
    list_filter = ('date', 'product')

@admin.register(ShoppingCart)
class PurchaseAdmin(admin.ModelAdmin):
    pass

@admin.register(PrePurchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'quantity', 'date')
    list_filter = ('date', 'product')
