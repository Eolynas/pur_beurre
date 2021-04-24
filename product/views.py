""" All view Product app"""
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import render
from django.template import loader
from django.views import generic, View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from .forms import SearchProduct, RegisterUserForm
from product.models import get_id_product_by_name, get_product_by_id, get_subsitut_for_product, get_all_name_products, save_product_for_user, get_product_save_user



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
            result_form = form.print_form()
            result = get_subsitut_for_product(result_form['product'])
            if result is False:
                # return HttpResponseNotFound("<h1>Aucun produit n'a était trouvé</h1>")
                return render(request, self.template_name, {'info': "Aucun produit trouvé"})
            substitute_products['initial_product'] = result[0]
            substitute_products['substitut_products'] = result[1]
            if request.user.is_authenticated:
                substitute_products['product_save_for_user'] = get_product_save_user(request.user)

            return render(request, self.template_name, substitute_products)

    # def get(self, request, *args, **kwargs):
    #
    #     save_product_for_user(kwargs['id_product'], user=request.user)
    #
    #     return render(request, self.template_name)


class RegisterUser(generic.TemplateView):
    """
    page signUP
    """

    template_name = 'products/register.html'

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():

            user = form.save(request)
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
                print(request, f"You are now logged in as {username}")
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
    def dispatch(self, request, *args, **kwargs):
        user_product_save = {}
        user_product_save['result'] = get_product_save_user(request.user)
        user_product_save['user'] = request.user
        # return super().dispatch(*args, **kwargs)
        return render(request, self.template_name, user_product_save)


class SaveProduct(View):
    """
    save product by user
    """
    # template_name = 'products/dashboardUser.html'

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        product_id = request.POST['product_id']
        result = save_product_for_user(product_id, user=request.user)
        print(result)
        return HttpResponseRedirect('/accounts/dashboard/')
        # return redirect('dashboardUser')

        # if request.user.is_authenticated:
        #     save_product_for_user(kwargs['id_product'], user=request.user)
        #
        #     # return render(request, self.template_name)
        #     to_json = {'result': False}
        #     return HttpResponseRedirect(reverse('dashboardUser'))
        # else:
        #     return HttpResponseRedirect(reverse('login'))



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
