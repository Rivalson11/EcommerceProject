from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import F, FloatField, ExpressionWrapper, Sum
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .forms import PrePurchaseForm
from .models import Product, ShoppingCart, PrePurchase


@login_required
def add_to_cart_modal(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = ShoppingCart.objects.get_or_create(customer=request.user)

    if request.method == 'POST':
        form = PrePurchaseForm(request.POST, product=product)
        if form.is_valid():
            quantity_to_add = form.cleaned_data['quantity']

            with transaction.atomic():
                # Update or create PrePurchase entry
                prepurchase, created = PrePurchase.objects.get_or_create(
                    shopping_cart=cart,
                    product=product,
                    defaults={'customer': request.user, 'quantity': quantity_to_add}
                )

                if not created:
                    # If it exists, update the quantity atomically
                    prepurchase.quantity = F('quantity') + quantity_to_add
                    prepurchase.save()

                # Reduce product stock
                product.quantity = F('quantity') - quantity_to_add
                product.save(update_fields=['quantity'])

            return JsonResponse({'success': True, 'message': 'Item added to cart'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    else:
        form = PrePurchaseForm(initial={'quantity': 1})

    return render(request, 'purchasing/prepurchase_form.html', {'form': form, 'product': product})


class ShoppingCartView(LoginRequiredMixin, ListView):
    model = PrePurchase
    template_name = 'purchasing/shopping_cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        cart, created = ShoppingCart.objects.get_or_create(customer=self.request.user)
        # Retrieve PrePurchase items related to the user's cart
        qs = cart.prepurchase_set.all().annotate(
            total_price=ExpressionWrapper(
                F('product__price') * F('quantity'),
                output_field=FloatField()
            )
        )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_value'] = context['cart_items'].aggregate(grand_total=Sum('total_price'))['grand_total']
        return context