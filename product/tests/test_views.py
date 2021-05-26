""" Test for views"""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

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

        add_category_1 = Category.objects.create(name='Pizza')
        add_category_2 = Category.objects.create(name='Fromage')
        add_category_3 = Category.objects.create(name='Test')
        add_category_4 = Category.objects.create(name='Test_2')

        add_product_1 = Product.objects.create(name="Pizza test",
                                               image_product="https://image.fr",
                                               stores="OpenClassrooms",
                                               url=None,
                                               nutriscore="D",
                                               image_nutrient_benchmarks="https://image_repere.fr")
        add_product_1.save()
        add_product_1.category.add(add_category_1, add_category_3)

        add_product_2 = Product.objects.create(name="Pizza fromage",
                                               image_product="https://image.fr",
                                               stores="OpenClassrooms",
                                               url='https://masuperpizza.fr',
                                               nutriscore="C",
                                               image_nutrient_benchmarks="https://image_repere.fr")

        add_product_2.category.add(add_category_1, add_category_2, add_category_3)

        add_product_3 = Product.objects.create(name="Pizza fromage meilleur",
                                               image_product="https://image.fr",
                                               stores="OpenClassrooms",
                                               url='https://masuperpizza.fr',
                                               nutriscore="A",
                                               image_nutrient_benchmarks="https://image_repere.fr")

        add_product_3.category.add(add_category_1, add_category_2, add_category_4)

        add_product_4 = Product.objects.create(name="Pizza 5 fromage",
                                               image_product="https://image.fr",
                                               stores="OpenClassrooms",
                                               url='https://masuperpizza.fr',
                                               nutriscore="A",
                                               image_nutrient_benchmarks="https://image_repere.fr")
        add_product_4.category.add(add_category_1, add_category_2, add_category_4)

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

        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
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
        url_result = reverse('results')
        response = self.client.get(url_result)
        self.assertEqual(response.status_code, 200)

        # form = SearchProduct(data={'product': 'Pizza test'})
        response = self.client.post(url_result, {'product': 'Pizza test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/result.html')
        self.assertIn('Pizza fromage', response.content.decode("utf-8"))

        response = self.client.post(url_result, {'product': 'toto'})
        self.assertEqual(response.status_code, 200)

        self.assertIn('produit non trouvé', response.content.decode("utf-8"))

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
