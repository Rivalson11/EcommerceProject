from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Product


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/product_list.html'  # Specify the template
    context_object_name = 'products'  # Name for the list in the template
    paginate_by = 10  # Optional: add pagination if there are many products

class ProductDetailView(DetailView):
    model = Product
    template_name = 'inventory/product_detail.html'  # Template to render
    context_object_name = 'product'  # Use 'product' as the context variable
