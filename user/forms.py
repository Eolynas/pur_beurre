""" Form for product app"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from user.models import Profile


class RegisterUserForm(UserCreationForm):
    """
    form for signup new users
    """
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Pseudo',
                                                                            'class': 'fadeIn first'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                                          'class': 'fadeIn second'}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Prénom',
                                                                               'class': 'fadeIn third'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'noms',
                                                                              'class': 'fadeIn second'}))

    image = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class': 'image_form'}))

    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe',
                                                                                 'class': 'fadeIn fourth'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'saisissez de nouveau votre mot de passe',
               'class': 'fadeIn fourth'}))

    class Meta:
        """
        Class meta
        """
        model = User
        fields = ("username", "first_name", "last_name", "email", "image", "password1")

    def save(self, commit=True):
        """
        for save user with form register
        """
        user = super(RegisterUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
            try:
                profile = Profile(user=user)
                profile.image = self.cleaned_data["image"].file.read()
                profile.save()
            except:
                user.delete()
                return False

        return user

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size / 1000000 > 2:
                raise ValidationError("Image trop large (>2mb)")
            return image
        raise ValidationError("Couldn't read uploaded image")
