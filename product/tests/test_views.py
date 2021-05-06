from django.contrib.auth.models import User
from django.test import TestCase

from django.db import models
from product.models import Product, Category


class TestViews(TestCase):
    """
    test all views for product App
    """

    def setUp(self):
        self.user_bob = User.objects.create_user(username='bob',
                                                 first_name="bob",
                                                 password="toto2021")
        self.user_bob.save()
        self.user_roger = User.objects.create_user('roger')
        self.user_roger.save()

        c1 = Category.objects.create(name='Pizza')
        c2 = Category.objects.create(name='Fromage')
        c3 = Category.objects.create(name='Test')
        c4 = Category.objects.create(name='Test_2')

        p1 = Product.objects.create(name="Pizza test",
                                    image_product="https://image.fr",
                                    stores="OpenClassrooms",
                                    url=None,
                                    nutriscore="D",
                                    image_reperes_nutrionnels="https://image_repere.fr")
        p1.save()
        p1.category.add(c1, c3)

        p2 = Product.objects.create(name="Pizza fromage",
                                    image_product="https://image.fr",
                                    stores="OpenClassrooms",
                                    url='https://masuperpizza.fr',
                                    nutriscore="C",
                                    image_reperes_nutrionnels="https://image_repere.fr")

        p2.category.add(c1, c2, c3)

        p3 = Product.objects.create(name="Pizza fromage meilleur",
                                    image_product="https://image.fr",
                                    stores="OpenClassrooms",
                                    url='https://masuperpizza.fr',
                                    nutriscore="A",
                                    image_reperes_nutrionnels="https://image_repere.fr")

        p3.category.add(c1, c2, c4)

        p4 = Product.objects.create(name="Pizza 5 fromage",
                                    image_product="https://image.fr",
                                    stores="OpenClassrooms",
                                    url='https://masuperpizza.fr',
                                    nutriscore="A",
                                    image_reperes_nutrionnels="https://image_repere.fr")
        p4.category.add(c1, c2, c4)

    def test_index(self):
        """
        Test index url
        - status_code (200, 301)
        - if login display if not user authentificated
        - if logout display if user authentificated
        """
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/index')
        self.assertEqual(response.status_code, 301)

        # Test display login / logout if user is authentificated

        loggin_user = self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.get('')
        icon_log_out = "fa-sign-out-alt"
        icon_log_in = "fa-sign-in-alt"
        self.assertIn(icon_log_out, response.content.decode("utf-8"))
        self.assertNotIn(icon_log_in, response.content.decode("utf-8"))

        self.client.logout()
        response = self.client.get('')

        self.assertIn(icon_log_in, response.content.decode("utf-8"))
        self.assertNotIn(icon_log_out, response.content.decode("utf-8"))

    def test_legal(self):
        """
        Test legal mention url (/legal/)
        - status_code (200, 301)
        """
        response = self.client.get('/legal/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/legal/')
        self.assertEqual(response.status_code, 405)

    def test_result(self):
        """
        Test result url (/results/) (after search product)
        - status_code (200)
        - if method is get
        - if method is post -> check result
        """

        response = self.client.get('/results/')
        self.assertEqual(response.status_code, 200)

        # form = SearchProduct(data={'product': 'Pizza test'})
        response = self.client.post('/results/', {'product': 'Pizza test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/result.html')
        self.assertIn('Pizza fromage', response.content.decode("utf-8"))

        response = self.client.post('/results/', {'product': 'toto'})
        self.assertEqual(response.status_code, 200)

        self.assertIn('produit non trouvé', response.content.decode("utf-8"))

    def test_register(self):
        """
        Test RegisterUser (/accounts/login/)
        - status_code (200)
        - if method is get -> display form
        - if method is post -> valid login
        - if method is post -> error login
        - test template
        """
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', str(response.content))
        self.assertTemplateUsed(response, 'products/register.html')

        response = self.client.post('/accounts/register/',
                                    {'username': 'Eddy',
                                     'first_name': 'Eddy',
                                     'email': 'edddd@yahoo.fr',
                                     'password1': ':mdp202020',
                                     'password2': ':mdp202020'}, follow=True)
        self.assertEqual(response.status_code, 200)
        # ----------- ERROR ----------- #
        response = self.client.post('/accounts/register/',
                                    {'username': 'Eddy-Test',
                                     'first_name': 'Eddy',
                                     'email': 'eddddy@yahoo.fr',
                                     'password1': ':mdp202020',
                                     'password2': ':mdp202029'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/register.html')

    def test_login_view(self):
        """
        Test RegisterUser (/accounts/login/)
        - status_code (200)
        - if method is get -> display form
        - if method is post -> valid login
        - if method is post -> error login
        """
        # ----------- GET ----------- #
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', str(response.content))
        self.assertTemplateUsed(response, 'products/login.html')

        # ----------- POST ----------- #

        response = self.client.post('/accounts/login/',
                                    {'username': 'bob',
                                     'password': 'toto2021'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bonjour bob', str(response.content))
        self.assertTemplateUsed(response, 'products/index.html')

        # ----------- ERROR ----------- #

        # Error password
        response = self.client.post('/accounts/login/',
                                    {'username': 'bob',
                                     'password': 'toto2020'}, follow=True)
        self.assertEqual(response.status_code, 200)
        error_msg = "Saisissez un nom d’utilisateur et un mot de passe valides. Remarquez que chacun de ces champs est sensible à la casse (différenciation des majuscules/minuscules)"
        self.assertIn(error_msg, response.content.decode("utf-8"))
        self.assertTemplateUsed(response, 'products/login.html')

    def test_dashboard_user(self):
        """
        Test RegisterUser (/accounts/login/)
        - status_code (200)
        - if method is get -> not authenticated
        - if method is get -> authenticated
        """
        # ----------- GET NOT AUTHENTIFICATED ----------- #
        response = self.client.get('/accounts/dashboard/')
        self.assertEqual(response.status_code, 302)

        # ----------- GET AUTHENTIFICATED ----------- #
        self.client.force_login(User.objects.get_or_create(username='roger')[0])
        response = self.client.get('/accounts/dashboard/')
        # self.assertEqual(response.status_code, 200)

    def test_product_info(self):
        """
        Test page product info
        - status_code (200)
        """

        product = Product.objects.first()
        url = f"/products/{product.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product.html')

        response = self.client.get("/products/232323/")
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """
        Test logout
        """
        self.client.force_login(User.objects.get_or_create(username='bob')[0])
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 302)

    def test_save_product(self):
        """
        Test save product
        - status_code (200) auth or not auth
        - if method is get
        - if method is post -> check result
        """
        product_test = Product.objects.first()
        response = self.client.post('/products/save/', {'product_id': product_test.id})
        self.assertEqual(response.status_code, 302)

        self.client.force_login(User.objects.get_or_create(username='bob')[0])
        response = self.client.post('/products/save/', {'product_id': product_test.id})
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/accounts/products/')
        self.assertIn(product_test.name, str(response.content))

        response = self.client.post('/products/save/', {'product_id': 999})
        self.assertEqual(response.status_code, 404)





