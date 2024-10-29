from django.urls import path
from .views import add_to_cart_modal, ShoppingCartView

app_name = 'purchasing'

urlpatterns = [
    path('add-to-cart-modal/<int:product_id>/', add_to_cart_modal, name='add_to_cart_modal'),
    path('shopping-cart/', ShoppingCartView.as_view(), name='shopping_cart'),
]