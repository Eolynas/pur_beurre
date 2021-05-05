""" All view Product app"""
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseNotFound, Http404
from django.shortcuts import render
from django.template import loader
from django.views import generic, View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from .forms import SearchProduct, RegisterUserForm, SearchProductNavBar
from product.models import get_id_product_by_name, get_product_by_id, get_subsitut_for_product, get_all_name_products, save_product_for_user, get_product_save_user

from PIL import Image
import io
from base64 import b64encode

class Index(View):
    """
    Page index url/ or url/index
    """
    template_name = 'products/index.html'
    form_class = SearchProduct
    form_navbar = SearchProductNavBar

    def get(self, request):

        return render(request, self.template_name, {'form': self.form_class, 'form_navbar': self.form_navbar})


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
    """
    view for url after research
    """
    template_name = 'products/result.html'
    substitute_products = {}
    form_class = SearchProduct

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        substitute_products = {}
        if form.is_valid():
            form_navbar = SearchProductNavBar
            result_form = form.print_form()
            result = get_subsitut_for_product(result_form['product'])
            if result is False:
                info_product = f"le produit {result_form['product']} n'est pas présent dans notre base de donnée"
                return render(request, self.template_name, {'info': "Aucun produit trouvé",
                                                            'product_not_found': info_product,
                                                            'form_navbar': form_navbar})
            substitute_products['initial_product'] = result[0]
            substitute_products['substitut_products'] = result[1]
            substitute_products['product_save_for_user'] = None
            if request.user.is_authenticated:
                substitute_products['product_save_for_user'] = get_product_save_user(request.user)

            return render(request, self.template_name, {'initial_product': substitute_products['initial_product'],
                                                        'substitut_products': substitute_products['substitut_products'],
                                                        'product_save_for_user': substitute_products['product_save_for_user'],
                                                        'form_navbar': form_navbar})


class RegisterUser(generic.TemplateView):
    """
    page signUP
    """

    template_name = 'products/register.html'

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST, request.FILES)
        if form.is_valid():

            user = form.save(request)
            # profile = profile_form.save(commit = False)
            # profile.user = user
            # profile.save(request)
            if user is False:
                info = "Erreur lors de l'upload de l'image"
                return render(request, self.template_name, {'form': form, 'info': info})
            else:
                login(request, user)
            return HttpResponseRedirect('/index')
        else:
            return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        form = RegisterUserForm()
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
                return HttpResponseRedirect('/')

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
    def get(self, request, *args, **kwargs):
        form_navbar = SearchProductNavBar
        # user = {}
        # user['user'] = request.user
        # imageStream = io.BytesIO(request.user.profile.image)
        image = None

        try:
            if isinstance(request.user.profile.image, memoryview):
                # user['image'] = b64encode(request.user.profile.image).decode('ascii')
                image = b64encode(request.user.profile.image).decode('ascii')
            # return render(request, self.template_name, user)
            header = {'h1': 'Bonjour', 'h4': 'ca va'}
            return render(request, self.template_name, {'user': request.user,
                                                        'image': image,
                                                        'form_navbar': form_navbar})
        except:
            return render(request, self.template_name, {'user': request.user,
                                                        'image': image,
                                                        'form_navbar': form_navbar})


class SaveProduct(View):
    """
    save product by user
    """
    # template_name = 'products/dashboardUser.html'

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):

        product_id = request.POST['product_id']

        result = save_product_for_user(product_id, user=request.user)
        if not result:
            raise Http404("Une erreur s'est produite lors de la sauvegarde de votre produit")
        print(result)
        return HttpResponseRedirect('/accounts/products/')


class MyProducts(generic.TemplateView):
    """
    view for save products by user
    """
    template_name = 'products/result.html'

    @method_decorator(login_required(login_url='/accounts/login/'))
    def get(self, request, *args, **kwargs):
        form_navbar = SearchProductNavBar
        save_product_by_user = get_product_save_user(request.user)
        # product_id = request.POST['product_id']
        # result = save_product_for_user(product_id, user=request.user)
        # print(result)

        return render(request, self.template_name, {'substitut_products': save_product_by_user,
                                                    'myproduct': True,
                                                    'user': request.user,
                                                    'form_navbar': form_navbar})

# class AllProducts(generic.View):
#     """
#     View for all products in the form of JSON
#     she is there to do the autocompletion
#     /!\ /!\ NOT IMPLEMENTED FOR A FUTURE VERSION /!\ /!\
#     """
#
#     def get(self, request, *args, **kwargs):
#         data = get_all_name_products()
#         dict_products = {}
#         dict_products['products'] = data
#         list_products = []
#         for product in data:
#             list_products.append(product['name'])
#         dict_products['products'] = list_products
#
#         return JsonResponse(dict_products, safe=True)
