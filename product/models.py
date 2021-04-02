""" Models postgres"""
from typing import Union
from django.db import models

from product.config.config import logger


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    image_product = models.CharField(max_length=255, null=True)
    stores = models.CharField(max_length=200, null=True)
    url = models.CharField(max_length=255, null=True)
    nutriscore = models.CharField(max_length=20, null=True)
    image_reperes_nutrionnels = models.CharField(max_length=255, null=True)
    category = models.ManyToManyField(Category)


def delete_all_data_in_tables():
    Product.objects.all().delete()
    Category.objects.all().delete()
    logger.info("Toutes les données ont étaient éffacés")


def bulk_insert_product_category(list_product: list):
    """
    insert all product and ur categories
    """
    # Creation de deux objet (product & category) pour bulk insert

    logger.info(f"Il y a {len(list_product)} produit")
    number_product_insert = 0
    number_product_update = 0
    for product in list_product:

        product_obj, created = Product.objects.get_or_create(
            name=product['name'],
        )
        if created:
            number_product_insert += 1
        if not product_obj.image_product == product['image_product'] and \
                not product_obj.stores == product['stores'] and \
                not product_obj.url == product['url'] and \
                not product_obj.nutriscore == product['nutriscore'] and \
                not product_obj.image_reperes_nutrionnels == product['image_reperes_nutrionnels']:
            number_product_update += 1

        product_obj.image_product = product['image_product']
        product_obj.stores = product['stores']
        product_obj.url = product['url']
        product_obj.nutriscore = product['nutriscore']
        product_obj.image_reperes_nutrionnels = product['image_reperes_nutrionnels']
        product_obj.save()

        # Creation des categories
        categories_obj = []
        for category in product['categories_product']:
            obj, created = Category.objects.get_or_create(
                name=category
            )
            if obj:
                categories_obj.append(obj)
            elif created:
                categories_obj.append(obj)
            product_obj.category.add(obj)

    logger.info(f"il y a {number_product_insert} qui ont étaient inséré")


def get_id_product_by_name(product_name: str) -> Union[int, None]:
    """
    get product with name
    :param product_name: name product enter into search bar
    :type product_name: str
    """
    query = Product.objects.filter(name__icontains=product_name).values().first()

    if query is None:
        return query
    if query['id']:
        return query['id']


def get_product_by_id(id_product: int) -> Union[dict, None]:
    """
    get product with id
    :param id_product: id product
    :type product_name: int
    """
    try:
        int(id_product)
    except ValueError as e:
        return None
    query = Product.objects.filter(pk=id_product).values().first()

    return query
