""" Form for product app"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SearchProduct(forms.Form):
    """
    Form for search product (form is in index.html)
    """
    product = forms.CharField(label='product', max_length=100,
                              widget=forms.TextInput(
                                  attrs={'placeholder': 'Produit',
                                         'class': 'form-control mr-sm-2 search-product'}))

    def print_form(self):
        print(self.cleaned_data)
        return self.cleaned_data


class SearchProductNavBar(forms.Form):
    """
    Form for search product (form is in index.html)
    """
    product = forms.CharField(label='product', max_length=100,
                              widget=forms.TextInput(
                                  attrs={'placeholder': 'Chercher',
                                         'class': 'form-control mr-sm-2 search-product-navbar'}))

    def print_form(self):
        print(self.cleaned_data)
        return self.cleaned_data


class RegisterUserForm(UserCreationForm):
    """
    form for signup new users
    """
    # pseudo = forms.CharField(max_length=100)
    # message = forms.CharField(widget=forms.Textarea)
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Pseudo',
                                                              'class': 'fadeIn first'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'fadeIn second'}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Prénom',
                                                                'class': 'fadeIn third'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'noms',
                                                               'class': 'fadeIn second'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe',
                                                               'class': 'fadeIn fourth'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'saisissez de nouveau votre mot de passe',
                                                               'class': 'fadeIn fourth'}))

    # cc_myself = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1")

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
        return user
        # if commit:
        #     user.save()
        # return user


