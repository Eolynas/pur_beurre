""" test for product app"""
# Create your tests here.

from django.test import TestCase

from product.models import bulk_insert_product_category, \
    Product, Category, \
    get_id_product_by_name, \
    get_product_by_id, \
    get_subsitut_for_product


class TestProductApp(TestCase):

    def setUp(self):
        # product_object = Product()
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
        p1.category.add(c1)
        p1.category.add(c3)

        p2 = Product.objects.create(name="Pizza fromage",
                                    image_product="https://image.fr",
                                    stores="OpenClassrooms",
                                    url='https://masuperpizza.fr',
                                    nutriscore="C",
                                    image_reperes_nutrionnels="https://image_repere.fr")

        p2.category.add(c1)
        p2.category.add(c2)
        p2.category.add(c3)

        p3 = Product.objects.create(name="Pizza fromage meilleur",
                                    image_product="https://image.fr",
                                    stores="OpenClassrooms",
                                    url='https://masuperpizza.fr',
                                    nutriscore="A",
                                    image_reperes_nutrionnels="https://image_repere.fr")

        p3.category.add(c1)
        p3.category.add(c2)
        p3.category.add(c4)

        product_toto = 'toto'

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
        print(query)
        int(query)

        # query = Product.objects.filter(name__icontains='Pizza').values().first()
        query = get_id_product_by_name('Pizza')
        print(query)
        int(query)
        # self.assertEqual(query, int)

        query = get_id_product_by_name('sqdqsdqsdqsd')
        self.assertEqual(query, None)

    def test_get_product_by_id(self):
        """
        test get product by id for the url '/products/<id_product>'
        """

        id_test_1 = 5
        id_test_2 = 8682
        id_test_3 = 'pizza'
        id_test_4 = False
        id_test_5 = None

        # TODO: Peut-on tester avec un str ? car j'ai un typeError alors que l'except est géré

        query_by_id = get_product_by_id(id_test_1)
        self.assertEqual(query_by_id['name'], 'Pizza test')

        query_by_id = get_product_by_id(id_test_2)
        self.assertEqual(query_by_id['name'], None)

    def test_get_substitut(self):
        """
        test get substitut
        """

        product = "Pizza test"
        substitute_products = get_subsitut_for_product(product)
        expected_products = ['Pizza fromage', 'Pizza fromage meilleur']

        for substitute_product in substitute_products:
            self.assertIn(substitute_product.name, expected_products)
