from django.test import Client, TestCase


class TestViews(TestCase):
    """
    test all views for product App
    """

    def test_index(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/index')
        self.assertEqual(response.status_code, 301)

    def test_legal(self):
        response = self.client.get('/legal')
        self.assertEqual(response.status_code, 200)

    def test_ProductInfo(self):
        response = self.client.get('/products/1')
        self.assertEqual(response.status_code, 200)