from django.conf.urls import url
from django.urls import path

from . import views # import views so we can use them in urls.


urlpatterns = [
    url(r'^$', views.index), # "/store" will call the method "index" in "views.py"
    path('store/', views.index), # "/store" will call the method "index" in "views.py"
]