from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.Index.as_view()),
    path('index/', views.Index.as_view(), name="index"),
    path('legal/', views.Legal.as_view(), name="legal"),
    path('products/<int:id_product>/', views.ProductInfo.as_view(extra_context={'title': 'name'}), name="products"),
    path('products/save/', views.SaveProduct.as_view(), name="product_save"),
    path('products/results/', views.Result.as_view(extra_context={'title': 'results'}), name="results"),
]
