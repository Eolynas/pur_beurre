""" All request for database postgres"""
from product.models import Product, Category


def insert_product(product: list):
    Product