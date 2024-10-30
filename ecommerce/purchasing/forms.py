from django import forms
from .models import PrePurchase


class PrePurchaseForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop("product", None)
        super().__init__(*args, **kwargs)

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        # Check if the quantity requested is greater than available stock
        if self.product and quantity > self.product.quantity:
            raise forms.ValidationError(f"Only {self.product.quantity} units available in stock.")

        return quantity

    class Meta:
        model = PrePurchase
        fields = ["quantity"]
