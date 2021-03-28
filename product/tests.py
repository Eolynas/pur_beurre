""" test for product app"""
# Create your tests here.
from unittest.mock import patch, MagicMock

from django.test import TestCase

from product.models import bulk_insert_product_category
from product.open_food_fact.recover_data_api_open_food_fact import RecoverApi


class TestProductApp(TestCase):

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
                        'stores': 'Auchan',
                        'url': 'https://fr.openfoodfacts.org',
                        'nutriscore_score': 8,
                        'categories_product': 'pizza, fromage'
                    }
                ],
            'count': 1

        }
        url = 'https://fr.openfoodfacts.org/category/pizza.json'
        mock_get.get = MagicMock()
        mock_get.get.return_value.json.return_value = product_example
        recover_api = RecoverApi()
        product = recover_api.get_product(category='pizza')
        self.assertEqual(product[0]["nutriscore_score"], 8)

    def test_insert_data_in_db(self):
        """
        test insert data (product & category) in db
        """
        example_dict_product = [
            {'name': 'Pizza 4 fromage',
             'stores': None,
             'url': 'https://fr.openfoodfacts.org/produit/0001217',
             'nutriscore_score': 11, 'categories_product': ['fr:Pizza aux 4 fromages']
             },
            {'name': 'Pizza reine',
             'stores': 'Auchan',
             'url': 'https://fr.openfoodfacts.org/produit/0001218',
             'nutriscore_score': 9, 'categories_product': ['fr:Pizza reine']
             }
        ]
        insert = bulk_insert_product_category(example_dict_product)
        self.assertEqual(insert.status_code, 200)
