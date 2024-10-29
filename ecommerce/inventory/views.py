from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, When, Value, FloatField, ExpressionWrapper, Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from core.mixins import AdminRequiredMixin
from purchasing.models import ShoppingCart, PrePurchase, Purchase
from .forms import ProductForm
from .models import Product, ProductCategories

PRE_PURCHASE_WEIGHT = 0.5
PURCHASE_WEIGHT = 1


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/product_list.html'  # Specify the template
    context_object_name = 'products'  # Name for the list in the template
    paginate_by = 12  # Optional: add pagination if there are many products

    def get_queryset(self):
        return Product.objects.prefetch_related('categories').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, created = ShoppingCart.objects.get_or_create(customer=self.request.user)
        context['recommended_products'] = self.get_user_recommendations()
        context['cart_items'] = cart.prepurchase_set.all().count()
        return context

    def get_user_recommendations(self):
        purchases = Purchase.objects.filter(customer=self.request.user)
        pre_purchases = PrePurchase.objects.filter(customer=self.request.user)

        if not purchases.exists() and not pre_purchases.exists():
            return Product.objects.all().order_by('-popularity_score')[:4]

        # Step 1: Determine the user's preferred categories with weighted counts
        purchase_category_counts = purchases.values('product__categories').annotate(
            weighted_count=Sum('quantity')
        )
        pre_purchase_category_counts = pre_purchases.values('product__categories').annotate(
            weighted_count=ExpressionWrapper(Sum('quantity') * 0.5, output_field=FloatField())
        )

        # Combine weighted counts
        combined_category_counts = {}
        for entry in purchase_category_counts:
            category_id = entry['product__categories']
            combined_category_counts[category_id] = combined_category_counts.get(category_id, 0) + entry[
                'weighted_count']
        for entry in pre_purchase_category_counts:
            category_id = entry['product__categories']
            combined_category_counts[category_id] = combined_category_counts.get(category_id, 0) + entry[
                'weighted_count']

        # Step 2: Annotate each product with a weighted score based on preferred categories
        weighted_cases = [
            When(categories__id=category_id, then=Value(weight))
            for category_id, weight in combined_category_counts.items()
        ]
        annotated_products = Product.objects.annotate(
            weighted_score=Sum(
                Case(*weighted_cases, default=Value(0), output_field=FloatField())
            )
        )

        # Step 3: Order by weighted score first, then by popularity
        recommendations = annotated_products.filter(
            categories__in=combined_category_counts.keys()
        ).exclude(quantity=0).distinct().order_by('-weighted_score', '-popularity_score')[:4]

        return recommendations[:4]


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