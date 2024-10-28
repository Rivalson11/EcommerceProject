from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('products', views.ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
]