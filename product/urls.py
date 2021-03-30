from django.conf.urls import url
from django.urls import path, re_path

from . import views # import views so we can use them in urls.


urlpatterns = [
    url(r'^$', views.index),
    path('products/', views.index),
    path('legal/', views.legal),
]