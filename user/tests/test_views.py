""" Test for user views"""
from django.contrib.auth.models import User
from django.test import TestCase

from product.models import Category, Product


class TestViews(TestCase):
    """
    test all views for product App
    """

    def setUp(self):
        self.user_bob = User.objects.create_user(
            username="bob", first_name="bob", password="toto2021"
        )
        self.user_bob.save()
        self.user_roger = User.objects.create_user("roger")
        self.user_roger.save()

        add_category_1 = Category.objects.create(name="Pizza")
        add_category_2 = Category.objects.create(name="Fromage")
        add_category_3 = Category.objects.create(name="Test")
        add_category_4 = Category.objects.create(name="Test_2")

        add_product_1 = Product.objects.create(
            name="Pizza test",
            image_product="https://image.fr",
            stores="OpenClassrooms",
            url=None,
            nutriscore="D",
            image_nutrient_benchmarks="https://image_repere.fr",
        )
        add_product_1.save()
        add_product_1.category.add(add_category_1, add_category_3)

        add_product_2 = Product.objects.create(
            name="Pizza fromage",
            image_product="https://image.fr",
            stores="OpenClassrooms",
            url="https://masuperpizza.fr",
            nutriscore="C",
            image_nutrient_benchmarks="https://image_repere.fr",
        )

        add_product_2.category.add(add_category_1, add_category_2, add_category_3)

        add_product_3 = Product.objects.create(
            name="Pizza fromage meilleur",
            image_product="https://image.fr",
            stores="OpenClassrooms",
            url="https://masuperpizza.fr",
            nutriscore="A",
            image_nutrient_benchmarks="https://image_repere.fr",
        )

        add_product_3.category.add(add_category_1, add_category_2, add_category_4)

        add_product_4 = Product.objects.create(
            name="Pizza 5 fromage",
            image_product="https://image.fr",
            stores="OpenClassrooms",
            url="https://masuperpizza.fr",
            nutriscore="A",
            image_nutrient_benchmarks="https://image_repere.fr",
        )
        add_product_4.category.add(add_category_1, add_category_2, add_category_4)

    def test_register(self):
        """
        Test RegisterUser (/accounts/login/)
        - status_code (200)
        - if method is get -> display form
        - if method is post -> valid login
        - if method is post -> error login
        - test template
        """
        response = self.client.get("/accounts/register/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", str(response.content))
        self.assertTemplateUsed(response, "user/register.html")

        response = self.client.post(
            "/accounts/register/",
            {
                "username": "Eddy",
                "first_name": "Eddy",
                "email": "edddd@yahoo.fr",
                "password1": ":mdp202020",
                "password2": ":mdp202020",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        # ----------- ERROR ----------- #
        response = self.client.post(
            "/accounts/register/",
            {
                "username": "Eddy-Test",
                "first_name": "Eddy",
                "email": "eddddy@yahoo.fr",
                "password1": ":mdp202020",
                "password2": ":mdp202029",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/register.html")

    def test_login_view(self):
        """
        Test RegisterUser (/accounts/login/)
        - status_code (200)
        - if method is get -> display form
        - if method is post -> valid login
        - if method is post -> error login
        """
        # ----------- GET ----------- #
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", str(response.content))
        self.assertTemplateUsed(response, "user/login.html")

        # ----------- POST ----------- #

        response = self.client.post(
            "/accounts/login/", {"username": "bob", "password": "toto2021"}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Bonjour bob", str(response.content))
        self.assertTemplateUsed(response, "products/index.html")

        # ----------- ERROR ----------- #

        # Error password
        response = self.client.post(
            "/accounts/login/", {"username": "bob", "password": "toto2020"}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        error_msg = (
            "Saisissez un nom d’utilisateur et un mot de passe valides. Remarquez que chacun "
            "de ces champs est sensible à la casse (différenciation des majuscules/minuscules)"
        )
        self.assertIn(error_msg, response.content.decode("utf-8"))
        self.assertTemplateUsed(response, "user/login.html")

    def test_dashboard_user(self):
        """
        Test RegisterUser (/accounts/login/)
        - status_code (200)
        - if method is get -> not authenticated
        - if method is get -> authenticated
        """
        # ----------- GET NOT AUTHENTIFICATED ----------- #
        response = self.client.get("/accounts/dashboard/")
        self.assertEqual(response.status_code, 302)

        # ----------- GET AUTHENTIFICATED ----------- #
        self.client.force_login(User.objects.get_or_create(username="roger")[0])
        response = self.client.get("/accounts/dashboard/")
        # self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """
        Test logout
        """
        self.client.force_login(User.objects.get_or_create(username="bob")[0])
        response = self.client.get("/accounts/logout/")
        self.assertEqual(response.status_code, 302)
