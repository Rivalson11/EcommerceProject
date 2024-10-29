from django.urls import path
from .views import add_to_cart_modal

app_name = 'purchasing'

urlpatterns = [
    path('add-to-cart-modal/<int:product_id>/', add_to_cart_modal, name='add_to_cart_modal'),
]