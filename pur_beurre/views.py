from django.http import HttpResponse
from django.template import loader

# def index(request):
#     message = "Salut tout le monde !"
#     return HttpResponse(message)

def index(request):
    ...
    template = loader.get_template('index.html')
    return HttpResponse(template.render(request=request))