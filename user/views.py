""" All view User app"""
from base64 import b64encode

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic

from product.forms import SearchProductNavBar
from product.models import get_product_save_user
from user.forms import RegisterUserForm, MyPasswordChangeForm
from django.contrib import messages


class RegisterUser(generic.TemplateView):
    """
    page signUP
    """

    template_name = "user/register.html"

    def post(self, request, *args, **kwargs):
        """
        post in register page (after submit)
        """
        form = RegisterUserForm(request.POST, request.FILES)
        if form.is_valid():

            user = form.save(request)
            if user is False:
                info = "Erreur lors de l'upload de l'image"
                return render(request, self.template_name, {"form": form, "info": info})
            login(request, user)
            return HttpResponseRedirect("/index")

        return render(request, self.template_name, {"form": form})

    def get(self, request, *args, **kwargs):
        """
        get in result page (before submit)
        """
        form = RegisterUserForm()
        return render(request, self.template_name, {"form": form})


class LoginView(generic.TemplateView):
    """
    page signIn
    """

    template_name = "user/login.html"

    def get(self, request, *args, **kwargs):
        """
        get in login page (before login)
        """
        form = AuthenticationForm()
        return render(request, self.template_name, context={"form": form})

    def post(self, request, **kwargs):
        """
        get in login page (after submit login)
        """
        form = AuthenticationForm(request, data=request.POST)
        # form = AuthenticationForm(request)
        if form.is_valid():
            username = request.POST.get("username", False)
            password = request.POST.get("password", False)
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/")

        return render(request, self.template_name, context={"form": form})


class LogoutView(generic.RedirectView):
    """
    A view that logout user and redirect to homepage.
    """

    def get(self, request, *args, **kwargs):
        """
        get in logout page
        """
        logout(request)
        return HttpResponseRedirect("/")


class DashboardUser(generic.TemplateView):
    """
    page my accompte
    """

    template_name = "user/dashboard_user.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        get in dashboard page
        """
        form_navbar = SearchProductNavBar
        image = None
        header = {"h1": f"Bonjour {request.user.first_name}"}

        if hasattr(request.user, "profile") and isinstance(
            request.user.profile.image, memoryview
        ):
            image = b64encode(request.user.profile.image).decode("ascii")

        return render(
            request,
            self.template_name,
            {
                "user": request.user,
                "header": header,
                "image": image,
                "form_navbar": form_navbar,
            },
        )


class MyProducts(generic.TemplateView):
    """
    view for save products by user
    """

    template_name = "products/result.html"

    @method_decorator(login_required(login_url="/accounts/login/"))
    def get(self, request, *args, **kwargs):
        """
        get in product page
        """
        form_navbar = SearchProductNavBar
        save_product_by_user = get_product_save_user(request.user)

        header = {"h1": "Vos produits sauvegardé"}
        return render(
            request,
            self.template_name,
            {
                "substitut_products": save_product_by_user,
                "myproduct": True,
                "header": header,
                "user": request.user,
                "form_navbar": form_navbar,
            },
        )


class ChangePassword(generic.TemplateView):
    """
    view for save products by user
    """

    template_name = "user/changepassword.html"

    @method_decorator(login_required(login_url="/accounts/login/"))
    def get(self, request, *args, **kwargs):
        """
        get in changing password page (before login)
        """
        form = MyPasswordChangeForm(request.user)

        return render(request, self.template_name, context={"form": form})

    def post(self, request, *args, **kwargs):
        """
        get in changing password page (before login)
        """
        form = MyPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # This is a VERY important step!
            update_session_auth_hash(request, user)
            messages_pws = 'Votre mot de passe a était changé avec success'
            return render(request, "user/dashboard_user.html", context={"message_psw": messages_pws})

        else:
            error = form.errors.as_data()
            list_errors = []

            for err in form.errors.as_data():
                print(form.errors[err].data[0].messages[0])
                list_errors.append(form.errors[err].data[0].messages[0])
            return render(request, self.template_name, {"form": form, "message_error": list_errors})
