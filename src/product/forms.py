from django.forms import forms, ModelForm, CharField, TextInput, Textarea, BooleanField, CheckboxInput
from django import forms
from product.models import Variant, Product, ProductVariantPrice


class VariantForm(ModelForm):
    class Meta:
        model = Variant
        fields = '__all__'
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'active': CheckboxInput(attrs={'class': 'form-check-input', 'id': 'active'})
        }

# class ProductUpdateForm(ModelForm):
#     price = forms.FloatField()
#     stock = forms.FloatField()
#     class Meta:
#         model = Product
#         fields = ['title', 'description', 'price', 'stock']

class ProductUpdateForm(ModelForm):
    class Meta:
        model = Product
        fields = ['title',  'description']

class ProductVariantPriceUpdateForm(ModelForm):
    class Meta:
        model = ProductVariantPrice
        fields = ['price', 'stock']