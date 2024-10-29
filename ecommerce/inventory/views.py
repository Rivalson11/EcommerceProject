from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from core.mixins import AdminRequiredMixin
from .forms import ProductForm

from .models import Product


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/products.html'  # Specify the template
    context_object_name = 'products'  # Name for the list in the template
    paginate_by = 10  # Optional: add pagination if there are many products

    def get_queryset(self):
        return Product.objects.prefetch_related('categories').all()


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'inventory/product_detail.html'  # Template to render
    context_object_name = 'product'  # Use 'product' as the context variable


class ProductCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Product
    template_name = 'inventory/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('inventory:products')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductEditView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "inventory/product_edit.html"

    def get_success_url(self):
        return reverse_lazy('inventory:products')


class ProductDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Product
    template_name = "inventory/product_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy('inventory:products')