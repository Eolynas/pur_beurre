from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader


def index(request):
    title = "Pur Beurre"
    # JUSTE METTRE LE NOMS DE L'APP ET LE NOMS DU FICHIER HTML (il trouve le chemin tout seul visiblement)
    template = loader.get_template('products/index.html')
    return HttpResponse(template.render({'title': title}))

def legal(request):
    title = "Mention légale"
    # JUSTE METTRE LE NOMS DE L'APP ET LE NOMS DU FICHIER HTML (il trouve le chemin tout seul visiblement)
    template = loader.get_template('products/mention_legale.html')
    return HttpResponse(template.render({'title': title}))