# inventory/views.py
from django.views.generic.list import ListView
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'inventory/product_list.html'  # Specify the template
    context_object_name = 'products'  # Name for the list in the template
    paginate_by = 10  # Optional: add pagination if there are many products
