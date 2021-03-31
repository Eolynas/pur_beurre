from django.conf.urls import url
from django.urls import path, re_path, include

from . import views, forms



urlpatterns = [
    path('', views.Index.as_view(extra_context={'title': 'Index'}), name="index"),
    path('index/', views.Index.as_view(extra_context={'title': 'Index'}), name="index"),
    path('legal/', views.Legal.as_view(extra_context={'title': 'Mention Légale'}), name="legal"),
    path('product_result/', views.ProductResult.as_view(extra_context={'title': 'Mention Légale'}), name="product_result")
]