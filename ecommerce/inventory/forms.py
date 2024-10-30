from django import forms
from .models import Product, ProductCategories


class ProductForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=ProductCategories.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Optional: displays categories as checkboxes
        required=True,
    )

    class Meta:
        model = Product
        fields = [
            "product_id",
            "name",
            "categories",
            "price",
            "quantity",
            "popularity_score",
        ]
