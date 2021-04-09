""" Form for product app"""
from django import forms
from django.core.exceptions import ValidationError


class SearchProduct(forms.Form):
    """
    Form for search product (form is in index.html)
    """
    product = forms.CharField(label='product', max_length=100,
                              widget=forms.TextInput(
                                  attrs={'placeholder': 'Produit',
                                         'class': 'form-control search-product',
                                         'id': 'products_toto'}))

    def print_form(self):
        print(self.cleaned_data)
        return self.cleaned_data

