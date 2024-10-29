from django import forms
from .models import PrePurchase

class PrePurchaseForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = PrePurchase
        fields = ['quantity']
