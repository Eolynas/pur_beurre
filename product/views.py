""" All view Product app"""
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views import generic, View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import SearchProduct
from product.models import get_id_product_by_name, get_product_by_id, get_subsitut_for_product, get_all_name_products


class Index(View):
    """
    Page index url/ or url/index
    """
    template_name = 'products/index.html'
    form_class = SearchProduct

    def get(self, request):

        return render(request, self.template_name, {'form': self.form_class})


class Legal(generic.TemplateView):
    """
    Page mention legal url/legal
    """
    template_name = 'products/mention_legale.html'


class ProductInfo(generic.TemplateView):
    """
    Page product url/product/<id>
    """
    template_name = 'products/product.html'

    def get_context_data(self, *args, **kwargs):
        product = get_product_by_id(kwargs['id_product'])
        if product:
            context = super(ProductInfo, self).get_context_data(*args, **kwargs)
            context['name'] = product.name
            context['image_product'] = product.image_product
            context['stores'] = product.stores
            context['url'] = product.url
            context['nutriscore'] = product.nutriscore
            context['image_reperes_nutrionnels'] = product.image_reperes_nutrionnels
            return context


class Result(generic.FormView, generic.TemplateView):
    template_name = 'products/result.html'
    substitute_products = {}
    form_class = SearchProduct

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        substitute_products = {}
        if form.is_valid():
            result_form = form.print_form()
            result = get_subsitut_for_product(result_form['product'])
            substitute_products['initial_product'] = result[0]
            substitute_products['substitut_products'] = result[1]

            return render(request, self.template_name, substitute_products)


class AllProducts(generic.View):

    def get(self, request, *args, **kwargs):
        data = get_all_name_products()
        dict_products = {}
        dict_products['products'] = data
        list_products = []
        for product in data:
            list_products.append(product['name'])
        dict_products['products'] = list_products

        return JsonResponse(dict_products, safe=True)


class SignUp(generic.TemplateView):
    """
    page signUP
    """

    template_name = 'products/signup.html'

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/index')

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})


class LoginView(generic.TemplateView):
    """
    page signIn
    """

    template_name = 'products/login.html'

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, self.template_name, context={"form": form})

    def post(self, request, **kwargs):
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = request.POST.get('username', False)
            password = request.POST.get('password', False)
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                print(request, f"You are now logged in as {username}")
                return HttpResponseRedirect('/')
            else:
                print(request, "Invalid username or password.")
        else:
            print(request, "Invalid username or password.")

        return render(request, self.template_name, context={"form": form})


class LogoutView(generic.RedirectView):
    """
    A view that logout user and redirect to homepage.
    """

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')


class DashboardUser(generic.TemplateView):
    """
    page my accompte
    """

    template_name = 'products/dashboardUser.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



