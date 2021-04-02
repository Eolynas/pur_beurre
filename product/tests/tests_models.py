""" test for product app"""
# Create your tests here.
from unittest.mock import patch, MagicMock

from django.test import TestCase

from product.models import bulk_insert_product_category, Product, get_id_product_by_name
from product.open_food_fact.recover_data_api_open_food_fact import RecoverApi


class TestProductApp(TestCase):

    def setUp(self):
        Product.objects.create(name="Pizza test",
                               image_product="https://image.fr",
                               stores="OpenClassrooms",
                               url=None,
                               nutriscore="D",
                               image_reperes_nutrionnels="https://image_repere.fr")
        Product.objects.create(name="Pizza test 2",
                               image_product="https://image2.fr",
                               stores="OpenClassrooms",
                               url='http://url.fr',
                               nutriscore="A",
                               image_reperes_nutrionnels="https://image_repere2.fr")
        Product.objects.create(name="Fromage",
                               image_product="https://image_fromage.fr",
                               stores="Fromage City",
                               url="y'en a pas",
                               nutriscore="B",
                               image_reperes_nutrionnels="https://image_repere.fr")

    @patch("product.open_food_fact.recover_data_api_open_food_fact.requests")
    def test_recover_api_open_food_fact(self, mock_get):
        """
        test recover data api open food fact
        """
        product_example = {
            'products':
                [
                    {
                        'product_name_fr': 'pizza 4 fromages',
                        'image_url': 'https://super_image.fr',
                        'stores': 'Auchan',
                        'url': 'https://fr.openfoodfacts.org',
                        'nutriscore_grade': 'E',
                        'categories_product': 'pizza, fromage',
                        'image_reperes_nutrionnels': 'https://encore_une_super_image.fr'
                    }
                ],
            'count': 1

        }
        url = 'https://fr.openfoodfacts.org/category/pizza.json'
        mock_get.get = MagicMock()
        mock_get.get.return_value.json.return_value = product_example
        recover_api = RecoverApi()
        product = recover_api.get_product(category='pizza')
        self.assertEqual(product[0]["nutriscore"], 'E')

    def test_insert_data_in_db(self):
        """
        test insert data (product & category) in db
        """
        example_dict_product = [
            {'name': 'Pizza 4 fromage',
             'image_product': 'https://fr.openfoodfacts.org/produit/0001217',
             'stores': None,
             'url': 'https://fr.openfoodfacts.org/produit/0001217',
             'nutriscore': 11,
             'image_reperes_nutrionnels': 'https://fr.openfoodfacts.org/produit/0001217',
             'categories_product': ["pizza"],
             }
        ]

        bulk_insert_product_category(example_dict_product)

        query = Product.objects.filter(name="Pizza 4 fromage").exists()

        self.assertEqual(query, True)

    def test_update_data_in_db(self):
        """
        test insert data (product & category) in db
        """
        example_dict_product_for_test_update = [
            {'name': 'pizza 4 fromages',
             'image_product': 'https://super_image.fr',
             'stores': 'Carrefour',
             'url': 'https://fr.openfoodfacts.org',
             'nutriscore': 'A',
             'categories_product': ['pizza, fromage'],
             'image_reperes_nutrionnels': 'https://encore_une_super_image.fr'
             }
        ]
        bulk_insert_product_category(example_dict_product_for_test_update)

        query = Product.objects.get(name="pizza 4 fromages")

        self.assertEqual(query.stores, 'Carrefour')

    def test_get_product_in_db(self):
        """
        test get product after research with search bar
        """
        pass

        # query = Product.objects.filter(name__icontains='pizza').values().first()
        query = get_id_product_by_name('pizza')
        self.assertEqual(query, 1)

        # query = Product.objects.filter(name__icontains='Pizza').values().first()
        query = get_id_product_by_name('Pizza')
        self.assertEqual(query, 1)

        query = get_id_product_by_name('sqdqsdqsdqsd')
        self.assertEqual(query, None)
