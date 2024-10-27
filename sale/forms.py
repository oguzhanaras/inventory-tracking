# sales/forms.py
from django import forms
from .models import Sale, SaleItem
from inventory.models import Product

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = []

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Satılacak miktar'}),
        }
