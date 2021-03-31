# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.views import generic, View

from .forms import SearchProduct


class Index(generic.TemplateView, generic.FormView):
    template_name = 'products/index.html'
    form_class = SearchProduct

    def post(self, request, *args, **kwars):
        form = self.form_class(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/product_result')

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


class ProductResult(generic.TemplateView):
    template_name = 'products/product.html'
