from django.db.models import FloatField, ExpressionWrapper, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import F
from django.db.models import FloatField, ExpressionWrapper, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView

from .forms import PrePurchaseForm
from .models import Product, ShoppingCart, PrePurchase
from .models import Purchase


class MyPurchasesView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = "purchasing/my_purchases.html"
    context_object_name = "purchases"

    def get_queryset(self):
        qs = Purchase.objects.filter(customer=self.request.user).select_related('product').order_by('-date')
        qs = qs.annotate(total_value=ExpressionWrapper(F("product__price") * F("quantity"), output_field=FloatField()))
        return qs


class AddToCartModalView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        form = PrePurchaseForm(initial={"quantity": 1})
        return render(
            request,
            "purchasing/prepurchase_form.html",
            {"form": form, "product": product},
        )

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart, created = ShoppingCart.objects.get_or_create(customer=request.user)
        form = PrePurchaseForm(request.POST, product=product)

        if form.is_valid():
            quantity_to_add = form.cleaned_data["quantity"]

            with transaction.atomic():
                # Update or create PrePurchase entry
                prepurchase, created = PrePurchase.objects.get_or_create(
                    shopping_cart=cart,
                    product=product,
                    defaults={"customer": request.user, "quantity": quantity_to_add},
                )

                if not created:
                    # If it exists, update the quantity atomically
                    prepurchase.quantity = F("quantity") + quantity_to_add
                    prepurchase.save()

                # Reduce product stock
                product.quantity = F("quantity") - quantity_to_add
                product.save(update_fields=["quantity"])

            return JsonResponse({"success": True, "message": "Item added to cart"})
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)


class CartItemDeleteView(LoginRequiredMixin, DeleteView):
    model = PrePurchase
    template_name = "purchasing/cart_item_confirm_delete.html"
    context_object_name = "cart_item"

    def get_success_url(self):
        return reverse_lazy("purchasing:shopping_cart")

    def get_queryset(self):
        # Ensure only items in the user's cart can be deleted
        return super().get_queryset().filter(shopping_cart__customer=self.request.user)

    def form_valid(self, form):
        # Retrieve the cart item to be deleted
        self.object = self.get_object()
        product = self.object.product
        quantity_to_restock = self.object.quantity

        product.quantity = F("quantity") + quantity_to_restock
        product.save()
        return super().form_valid(form)


class ShoppingCartView(LoginRequiredMixin, ListView):
    model = PrePurchase
    template_name = "purchasing/shopping_cart.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        cart, created = ShoppingCart.objects.get_or_create(customer=self.request.user)
        # Retrieve PrePurchase items related to the user's cart
        qs = cart.prepurchase_set.all().annotate(
            total_price=ExpressionWrapper(F("product__price") * F("quantity"), output_field=FloatField())
        )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_value"] = context["cart_items"].aggregate(grand_total=Sum("total_price"))["grand_total"]
        return context


class PurchaseView(LoginRequiredMixin, View):
    template_name = "purchasing/purchase_confirmation.html"
    success_url = reverse_lazy("purchasing:purchase_complete")

    def get(self, request, *args, **kwargs):
        # Retrieve the cart and cart items
        cart = get_object_or_404(ShoppingCart, customer=request.user)
        cart_items = cart.prepurchase_set.all().annotate(
            total_price=ExpressionWrapper(F("product__price") * F("quantity"), output_field=FloatField())
        )

        # Calculate the total cart value
        total_value = cart_items.aggregate(grand_total=Sum("total_price"))["grand_total"]

        # Render the confirmation page
        return render(
            request,
            self.template_name,
            {"cart_items": cart_items, "total_value": total_value},
        )

    def post(self, request, *args, **kwargs):
        # Retrieve the cart and cart items
        cart = get_object_or_404(ShoppingCart, customer=request.user)
        cart_items = cart.prepurchase_set.all()

        # Process the purchase in an atomic transaction
        with transaction.atomic():
            # Create Purchase entries for each PrePurchase item in the cart
            purchases = [
                Purchase(
                    customer=request.user,
                    product=item.product,
                    quantity=item.quantity,
                )
                for item in cart_items
            ]
            Purchase.objects.bulk_create(purchases)  # Save all purchases in bulk

            for item in cart_items:
                item.product.popularity_score = F("popularity_score") + item.quantity
                item.product.save(update_fields=["popularity_score"])

            # Delete the PrePurchase items and the ShoppingCart
            cart_items.delete()
            cart.delete()

        # Redirect to the "Purchase Complete" page
        return redirect(self.success_url)
