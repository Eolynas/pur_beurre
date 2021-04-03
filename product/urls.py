from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('index/', views.Index.as_view(extra_context={'title': 'Index'}), name="index"),
    path('legal/', views.Legal.as_view(), name="legal"),
    path('products/<int:id_product>/', views.ProductInfo.as_view(extra_context={'title': 'name'})),
    path('results/', views.Result.as_view(extra_context={'title': 'results'}), name="results"),
    # path('product_result/', views.ProductResult.as_view(extra_context={'title': 'Mention Légale'}),
    #      name="product_result")
]
