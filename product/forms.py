""" Form for product app"""
from django import forms


class SearchProduct(forms.Form):
    """
    Form for search product (form is in index.html)
    """

    product = forms.CharField(
        label="product",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Produit",
                "class": "form-control mr-sm-2 search-product",
            }
        ),
    )

    def print_form(self):
        print(self.cleaned_data)
        return self.cleaned_data


class SearchProductNavBar(forms.Form):
    """
    Form for search product (form is in index.html)
    """

    product = forms.CharField(
        label="product",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Chercher",
                "class": "form-control mr-sm-2 search-product-navbar",
            }
        ),
    )
