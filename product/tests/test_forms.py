""" TEST FOR FORMS"""

from django.test import TestCase

from product.forms import SearchProduct


class TestSearchProduct(TestCase):
    """
    test search product with search bar (index.html)
    """

    def test_search_product(self):
        """
        test search product with search bar (index.html)
        """

        form = SearchProduct()
        self.assertTrue(
            form.fields['product'].label is None or form.fields['product'].label == 'product')

        """
        CE QUE JE DOIS TESTER
    
        - User -> Entre le produit dans la barre de recherche
            - ENTER -> CREATION DE LA REQUETE POST
        - Récuperation dans la route du form "POST"
        - Vérifier si les données sont bien envoyée
    
        ------ TEST A FAIRE -------
        - validation des données (si pas d'injection xss ou autres)
        - validation des données non vide
    

    """
