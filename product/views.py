from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader


def index(request):
    message = "Salut tout le monde !"
    # JUSTE METTRE LE NOMS DE L'APP ET LE NOMS DU FICHIER HTML (il trouve le chemin tout seul visiblement)
    template = loader.get_template('product/index.html')
    return HttpResponse(template.render(request=request))