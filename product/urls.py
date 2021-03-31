from django.conf.urls import url
from django.urls import path, re_path, include

from . import views # import views so we can use them in urls.


urlpatterns = [
    url(r'^$', views.index),
    path('products/', views.index, name="index"),
    # path('legal/', views.Legal),
    path('legal/', views.Legal.as_view(extra_context={'title': 'Mention Légale'}), name="legal")
]