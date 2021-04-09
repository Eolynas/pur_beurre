from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.Index.as_view()),
    path('index/', views.Index.as_view(), name="index"),
    path('legal/', views.Legal.as_view(), name="legal"),
    path('products/<int:id_product>/', views.ProductInfo.as_view(extra_context={'title': 'name'})),
    path('results/', views.Result.as_view(extra_context={'title': 'results'}), name="results"),
    path('listproducts/', views.AllProducts.as_view(), name="allProducts"),
    path('accounts/login/', views.LoginView.as_view(), name="login"),
    path('accounts/logout/', views.LogoutView.as_view(), name="logout"),
    path('accounts/dashboard/', views.DashboardUser.as_view(), name="dashboardUser"),
    # path('/accounts/signup/', views.SignUp.as_view(), name="signup"),
    # path('product_result/', views.ProductResult.as_view(extra_context={'title': 'Mention Légale'}),
    #      name="product_result")
]
