""" All view Product app"""
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View, generic

from product.forms import SearchProduct, SearchProductNavBar
from product.models import (
    Product,
    get_product_by_id,
    get_product_save_user,
    get_subsitut_for_product,
    save_product_for_user,
    delete_product_save
)


class Index(View):
    """
    Page index url/ or url/index
    """

    template_name = "products/index.html"
    form_class = SearchProduct
    form_navbar = SearchProductNavBar

    def get(self, request):
        """
        get in home page
        """

        header = {
            "h1": "Du gras oui, mais de qualité",
            "h4": "Trouvez un produit de substitution pour ceux que vous consommez tous les jours",
        }
        return render(
            request,
            self.template_name,
            {
                "form": self.form_class,
                "form_navbar": self.form_navbar,
                "header": header,
            },
        )


class Legal(View):
    """
    Page mention legal url/legal
    """

    template_name = "products/mention_legale.html"
    form_navbar = SearchProductNavBar

    def get(self, request):
        """
        get in legal page
        """
        header = {"h1": "Mentions légales"}
        return render(
            request,
            self.template_name,
            {"header": header, "form_navbar": self.form_navbar},
        )


class ProductInfo(generic.TemplateView):
    """
    Page product url/product/<id>
    """

    template_name = "products/product.html"

    def get(self, request, **kwargs):
        """
        get in product page
        """
        product = get_product_by_id(kwargs["id_product"])
        form_navbar = SearchProductNavBar
        if product:
            header = {
                "h1": "Du gras oui, mais de qualité",
                "h4": "Trouvez un produit de substitution pour ceux que vous consommez tous les jours",
            }
            return render(
                request,
                self.template_name,
                {"header": header, "product": product, "form_navbar": form_navbar},
            )
        header = {"h1": "Produit non trouvé"}
        return render(
            request, self.template_name, {"header": header, "form_navbar": form_navbar}
        )


class Result(generic.TemplateView):
    """
    view for url after research
    """

    template_name = "products/result.html"
    substitute_products = {}
    form_class = SearchProduct

    def post(self, request, *args, **kwargs):
        """
        post in result page
        """
        form = self.form_class(request.POST)
        substitute_products = {}
        if form.is_valid():
            form_navbar = SearchProductNavBar
            result_form = form.print_form()
            result = get_subsitut_for_product(result_form["product"])
            if result is False:
                header = {
                    "h1": f"le produit {result_form['product']} n'est pas présent dans notre base de donnée"
                }
                info_product = f"le produit {result_form['product']} n'est pas présent dans notre base de donnée"
                return render(
                    request,
                    self.template_name,
                    {
                        "header": header,
                        "title": "produit non trouvé",
                        "product_not_found": info_product,
                        "form_navbar": form_navbar,
                    },
                )
            substitute_products["initial_product"] = result[0]
            substitute_products["substitut_products"] = result[1]
            substitute_products["product_save_for_user"] = None
            if request.user.is_authenticated:
                substitute_products["product_save_for_user"] = get_product_save_user(
                    request.user
                )

            header = {"h1": result[0].name}
            return render(
                request,
                self.template_name,
                {
                    "initial_product": substitute_products["initial_product"],
                    "header": header,
                    "title": result[0].name,
                    "substitut_products": substitute_products["substitut_products"],
                    "product_save_for_user": substitute_products[
                        "product_save_for_user"
                    ],
                    "form_navbar": form_navbar,
                },
            )


class SaveProduct(View):
    """
    save product by user
    """

    @method_decorator(login_required(login_url="/accounts/login/"))
    def dispatch(self, request, *args, **kwargs):
        """
        post in login page
        """

        product_id = request.POST["product_id"]

        result = save_product_for_user(product_id, user=request.user)
        if not result:
            raise Http404(
                "Une erreur s'est produite lors de la sauvegarde de votre produit"
            )
        print(result)
        return HttpResponseRedirect("/accounts/products/")


class ListProducts(View):
    """
    page for display, filter ALL product
    """

    queryset = Product.objects.all()
    template_name = "products/list_product.html"

    def get(self, request):
        """
        get in legal page
        """
        header = {"h1": "Listes des produits"}
        queryset = Product.objects.all()
        return render(
            request,
            self.template_name,
            {"products": queryset, "header": header},
        )


class DeleteProductSave(View):
    """
    Delete save Product in dashboard
    """

    @method_decorator(login_required(login_url="/accounts/login/"))
    def post(self, request, *args, **kwargs):
        """
        post for delete product save
        """

        product_id = request.POST["product_id"]

        result = delete_product_save(user=request.user, product_id=product_id)
        if not result:
            raise Http404(
                "Une erreur s'est produite lors de la sauvegarde de votre produit"
            )
        print(result)
        return HttpResponseRedirect("/accounts/products/")

