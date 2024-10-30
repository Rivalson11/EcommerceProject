from django.urls import path
from django.views.generic import TemplateView

from .views import (
    ShoppingCartView,
    PurchaseView,
    CartItemDeleteView,
    AddToCartModalView, MyPurchasesView,
)

app_name = "purchasing"

urlpatterns = [
    path(
        "add-to-cart-modal/<int:product_id>/",
        AddToCartModalView.as_view(),
        name="add_to_cart_modal",
    ),
    path("shopping-cart/", ShoppingCartView.as_view(), name="shopping_cart"),
    path("purchase/", PurchaseView.as_view(), name="purchase"),
    path(
        "purchase-complete/",
        TemplateView.as_view(template_name="purchasing/purchase_complete.html"),
        name="purchase_complete",
    ),
    path(
        "cart/item/<int:pk>/delete/",
        CartItemDeleteView.as_view(),
        name="cart_item_delete",
    ),
    path('my-purchases/', MyPurchasesView.as_view(), name='my_purchases'),
]
