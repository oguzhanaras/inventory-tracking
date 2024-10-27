from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'cost_price', 'sale_price', 'quantity', 'category']
        widgets = {
            'category': forms.Select(),
        }
