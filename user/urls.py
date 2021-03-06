from django.urls import path

from user import views

urlpatterns = [
    path("accounts/login/", views.LoginView.as_view(), name="login"),
    path("accounts/logout/", views.LogoutView.as_view(), name="logout"),
    path("accounts/dashboard/", views.DashboardUser.as_view(), name="dashboardUser"),
    path("accounts/register/", views.RegisterUser.as_view(), name="register"),
    path("accounts/products/", views.MyProducts.as_view(), name="myproduct"),
    path("accounts/changepassword/", views.ChangePassword.as_view(), name="changePassword"),
]
