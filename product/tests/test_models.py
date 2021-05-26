""" test for product app"""
# Create your tests here.

from django.test import TestCase

from product.models import bulk_insert_product_category, \
    Product, Category, \
    get_product_by_id, \
    get_subsitut_for_product


class TestProductApp(TestCase):
    """
    Class for test models for product app
    """

    def setUp(self):
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

    def test_get_product_by_id(self):
        """
        test get product by id for the url '/products/<id_product>'
        """

        id_test_not_found = 8682

        id_product_test = Product.objects.filter(name__icontains='Pizza test').first().id

        query_by_id = get_product_by_id(id_product_test)
        self.assertEqual(query_by_id.name, 'Pizza test')

        query_by_id_not_found = get_product_by_id(id_test_not_found)
        self.assertEqual(query_by_id_not_found, None)

    def test_get_substitut(self):
        """
        test get substitut
        """

        product = "Pizza test"
        get_substitute_products = get_subsitut_for_product(product)
        expected_products = ['Pizza fromage', 'Pizza fromage meilleur', 'Pizza 5 fromage']

        substitute_products = get_substitute_products[1]

        for substitute_product in substitute_products:
            self.assertIn(substitute_product.name, expected_products)

        get_wrong_substitute_products = get_subsitut_for_product('toto')
        self.assertEqual(get_wrong_substitute_products, False)
