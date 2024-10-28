from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('products', views.ProductListView.as_view(), name='products'),
]