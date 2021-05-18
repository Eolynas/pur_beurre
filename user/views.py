""" All view User app"""
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseNotFound, Http404
from django.shortcuts import render
from django.template import loader
from django.views import generic, View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from user.forms import RegisterUserForm
from product.forms import SearchProduct, SearchProductNavBar
from product.models import get_product_by_id, get_subsitut_for_product, save_product_for_user, get_product_save_user

from base64 import b64encode


class RegisterUser(generic.TemplateView):
    """
    page signUP
    """

    template_name = 'user/register.html'

    def post(self, request, *args, **kwargs):
        """
        post in register page (after submit)
        """
        form = RegisterUserForm(request.POST, request.FILES)
        if form.is_valid():

            user = form.save(request)
            if user is False:
                info = "Erreur lors de l'upload de l'image"
                return render(request, self.template_name, {'form': form, 'info': info})
            login(request, user)
            return HttpResponseRedirect('/index')

        return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        """
        get in result page (before submit)
        """
        form = RegisterUserForm()
        return render(request, self.template_name, {'form': form})


class LoginView(generic.TemplateView):
    """
    page signIn
    """

    template_name = 'user/login.html'

    def get(self, request, *args, **kwargs):
        """
        get in login page (before login)
        """
        form = AuthenticationForm()
        return render(request, self.template_name, context={"form": form})

    def post(self, request, **kwargs):
        """
        get in login page (after submit login)
        """
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = request.POST.get('username', False)
            password = request.POST.get('password', False)
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')

        return render(request, self.template_name, context={"form": form})


class LogoutView(generic.RedirectView):
    """
    A view that logout user and redirect to homepage.
    """

    def get(self, request, *args, **kwargs):
        """
        get in logout page
        """
        logout(request)
        return HttpResponseRedirect('/')


class DashboardUser(generic.TemplateView):
    """
    page my accompte
    """

    template_name = 'user/dashboard_user.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        get in dashboard page
        """
        form_navbar = SearchProductNavBar
        image = None
        header = {'h1': f"Bonjour {request.user.first_name}"}
        try:
            if isinstance(request.user.profile.image, memoryview):
                image = b64encode(request.user.profile.image).decode('ascii')

            return render(request, self.template_name, {'user': request.user,
                                                        'header': header,
                                                        'image': image,
                                                        'form_navbar': form_navbar})
        except:
            return render(request, self.template_name, {'user': request.user,
                                                        'header': header,
                                                        'image': image,
                                                        'form_navbar': form_navbar})


class MyProducts(generic.TemplateView):
    """
    view for save products by user
    """
    template_name = 'products/result.html'

    @method_decorator(login_required(login_url='/accounts/login/'))
    def get(self, request, *args, **kwargs):
        """
        get in product page
        """
        form_navbar = SearchProductNavBar
        save_product_by_user = get_product_save_user(request.user)

        header = {'h1': 'Vos produits sauvegardé'}
        return render(request, self.template_name, {'substitut_products': save_product_by_user,
                                                    'myproduct': True,
                                                    'header': header,
                                                    'user': request.user,
                                                    'form_navbar': form_navbar})