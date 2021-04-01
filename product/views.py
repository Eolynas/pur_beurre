# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views import generic, View

from .forms import SearchProduct
from product.models import get_id_product_by_name, get_product_by_id


class Index(generic.TemplateView, generic.FormView):
    template_name = 'products/index.html'
    form_class = SearchProduct

    def post(self, request, *args, **kwars):
        form = self.form_class(request.POST)
        if form.is_valid():
            name_product = form.cleaned_data['product']
            id_product = get_id_product_by_name(name_product)
            if id_product:
                return HttpResponseRedirect(f'/products/{id_product}')

    # def get_context_data(self, *args, **kwargs):
    #     context = super(AboutUs, self).get_context_data(*args, **kwargs)
    #     context['name'] = 'Gryffindor'
    #     return context


class Legal(generic.TemplateView):
    template_name = 'products/mention_legale.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super(Legal, self).get_context_data(*args, **kwargs)
    #     context['title'] = 'Mention legale'
    #     return context


# class Product(generic.TemplateView):
#     template_name = 'products/product.html'
#
#     print("stop")
#
#     # def get_context_data(self):
#     #     id_product = get_object_or_404(name=self.kwargs['id_product'])
#     #     print(id_product)

# def product(request, id_product):
#
#     product = get_product_by_id(id_product)
#     context = product
#
#     # return HttpResponse(response % id_product)
#     return render(request, 'products/product.html', context)


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


class ProductResult(generic.TemplateView):
    template_name = 'products/product.html'
    form_class = SearchProduct

    def post(self, request, *args, **kwars):
        form = self.form_class(request.POST)
        if form.is_valid():

            # context = super(ProductResult, self).get_context_data(*args, **kwargs)
            # context['name'] = form
            return render(request, self.template_name, {'product': form.cleaned_data['product']})

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductResult, self).get_context_data(*args, **kwargs)
    #     context['name'] = form
    #     return context
