from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Product, ShoppingCart, PrePurchase
from .forms import PrePurchaseForm
from django.db.models import F


@login_required
def add_to_cart_modal(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = ShoppingCart.objects.get_or_create(customer=request.user)

    if request.method == 'POST':
        form = PrePurchaseForm(request.POST)
        if form.is_valid():
            if PrePurchase.objects.filter(shopping_cart=cart, product=product).exists():
                PrePurchase.objects.filter(shopping_cart=cart, product=product).update(quantity=F('quantity') + form.cleaned_data['quantity'])
            else:
                prepurchase = form.save(commit=False)
                prepurchase.customer = request.user
                prepurchase.shopping_cart = cart
                prepurchase.product = product
                prepurchase.save()
            return JsonResponse({'success': True, 'message': 'Item added to cart'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    else:
        form = PrePurchaseForm(initial={'quantity': 1})

    return render(request, 'purchasing/prepurchase_form.html', {'form': form, 'product': product})
