""" All view Product app"""
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views import generic, View

from .forms import SearchProduct
from product.models import get_id_product_by_name, get_product_by_id


# TODO: FONCTIONNE MAIS SANS LE FORM DE DJANGO
# class Index(generic.TemplateView):
#     template_name = 'products/index.html'
#     form_class = SearchProduct
#
#     def post(self, request, *args, **kwars):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             name_product = form.cleaned_data['product']
#             id_product = get_id_product_by_name(name_product)
#             if id_product:
#                 return HttpResponseRedirect(f'/products/{id_product}')


class Index(generic.FormView):
    template_name = 'products/index.html'
    form_class = SearchProduct
    # success_url = f'products/{cleaned_data}'

    def form_valid(self, form):
        result_form = form.print_form()
        # return super(Index, self).form_valid(form)
        id_product = get_id_product_by_name(result_form['product'])
        return HttpResponseRedirect(f'/products/{id_product}')


class Legal(generic.TemplateView):
    template_name = 'products/mention_legale.html'


class ProductInfo(generic.TemplateView):
    template_name = 'products/product.html'

    def get_context_data(self, *args, **kwargs):
        product = get_product_by_id(kwargs['id_product'])
        if product:
            context = super(ProductInfo, self).get_context_data(*args, **kwargs)
            context['name'] = product['name']
            context['image_product'] = product['image_product']
            context['stores'] = product['stores']
            context['url'] = product['url']
            context['nutriscore'] = product['nutriscore']
            context['image_reperes_nutrionnels'] = product['image_reperes_nutrionnels']
            return context


class Result(generic.TemplateView):
    template_name = 'products/result.html'

# class ProductResult(generic.TemplateView):
#     template_name = 'products/product.html'
#     form_class = SearchProduct
#
#     def post(self, request, *args, **kwars):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#
#             return render(request, self.template_name, {'product': form.cleaned_data['product']})
