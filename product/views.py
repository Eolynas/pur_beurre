from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView


def index(request):
    title = "Pur Beurre"
    # JUSTE METTRE LE NOMS DE L'APP ET LE NOMS DU FICHIER HTML (il trouve le chemin tout seul visiblement)
    template = loader.get_template('products/index.html')
    return HttpResponse(template.render({'title': title}))


# def legal(request):
#     title = "Mention légale"
#     # JUSTE METTRE LE NOMS DE L'APP ET LE NOMS DU FICHIER HTML (il trouve le chemin tout seul visiblement)
#     template = loader.get_template('products/mention_legale.html')
#     return HttpResponse(template.render({'title': title}))


class Legal(TemplateView):
    template_name = 'products/mention_legale.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super(Legal, self).get_context_data(*args, **kwargs)
    #     context['title'] = 'Mention legale'
    #     return context


