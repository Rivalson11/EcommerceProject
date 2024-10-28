from django.urls import path
from . import views
from .views import ProductListView

urlpatterns = [
    path('product/<int:pk>/', ProductListView.as_view(), name='products'),
]