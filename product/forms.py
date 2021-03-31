""" Form for product app"""
from django import forms
from django.core.exceptions import ValidationError


class SearchProduct(forms.Form):
    """
    Form for search product (form is in index.html)
    """
    product = forms.CharField(label='product', max_length=100,
                              help_text='Entrez votre produit que vous voulez remplacer')
