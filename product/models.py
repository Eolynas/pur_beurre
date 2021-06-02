""" Models postgres"""
from typing import Tuple, Union

from django.contrib.auth.models import User
from django.db import models

from tools import logger


class Category(models.Model):
    """
    models category for product
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)


class Product(models.Model):
    """
    models product
    """

    name = models.CharField(max_length=200, unique=True)
    image_product = models.CharField(max_length=255, null=True)
    stores = models.CharField(max_length=200, null=True)
    url = models.CharField(max_length=255, null=True)
    nutriscore = models.CharField(max_length=20, null=True)
    image_nutrient_benchmarks = models.CharField(max_length=255, null=True)
    category = models.ManyToManyField(Category, related_name="products")
    user_save = models.ManyToManyField(User, related_name="user_save_products")


def delete_all_data_in_tables():
    """
    for delete table (use in developement only)
    """
    Product.objects.all().delete()
    Category.objects.all().delete()
    logger.info("Toutes les données ont étaient éffacés")


def bulk_insert_product_category(list_product: list):
    """
    insert all product and ur categories
    """
    logger.info(f"Il y a {len(list_product)} produit")
    number_product_insert = 0
    number_product_update = 0
    for product in list_product:

        product_obj, created = Product.objects.get_or_create(
            name=product["name"],
        )
        if created:
            number_product_insert += 1
        if (
                not product_obj.image_product == product["image_product"]
                and not product_obj.stores == product["stores"]
                and not product_obj.url == product["url"]
                and not product_obj.nutriscore == product["nutriscore"]
                and not product_obj.image_nutrient_benchmarks == product["image_reperes_nutrionnels"]
        ):
            number_product_update += 1

        product_obj.image_product = product["image_product"]
        product_obj.stores = product["stores"]
        product_obj.url = product["url"]
        product_obj.nutriscore = product["nutriscore"]
        product_obj.image_nutrient_benchmarks = product["image_reperes_nutrionnels"]
        product_obj.save()

        for category in product["categories_product"]:
            categories_obj = []
            obj, _ = Category.objects.get_or_create(name=category)
            categories_obj.append(obj)
            product_obj.category.add(obj)

    logger.info(f"il y a {number_product_insert} qui ont étaient inséré")


def get_product_by_id(id_product: int) -> Union[Product, None]:
    """
    get product with id
    :param id_product: id product
    :type product_name: int
    """
    try:
        query = Product.objects.get(pk=id_product)
        return query
    except Product.DoesNotExist:
        return None


def get_subsitut_for_product(product: str) -> Union[Tuple[str, list], bool]:
    """
    get subsitut at product
    :param product: Product at changed
    :return: product_initial_info.name: object product
    :return: choise_substitute_products: list object product
    """
    max_substitute = 6
    product_initial_info = Product.objects.filter(name__icontains=product).first()
    if not product_initial_info:
        return False
    categories_at_product_initial = product_initial_info.category.all()

    substitute_products = []
    for category in categories_at_product_initial.all():
        list_product_by_category = []
        products = category.products.all()
        for product in products:
            if (
                    product not in substitute_products
                    and product.nutriscore.lower()
                    <= product_initial_info.nutriscore.lower()
                    and not product.name == product_initial_info.name
            ):
                list_product_by_category.append(product)
                substitute_products.append(product)

    nbr_products_in_list = len(substitute_products)

    if nbr_products_in_list > max_substitute:
        return product_initial_info, substitute_products[:max_substitute]

    return product_initial_info, substitute_products


def save_product_for_user(id_product: int, user: User):
    """
    Save product adding by user
    """
    product = get_product_by_id(id_product)

    if not product:
        return False
    product.user_save.add(user)
    product.save()
    return True


def get_product_save_user(user):
    """
    get all product save by user
    """
    user_product_save = user.user_save_products.all()

    return user_product_save

# def get_all_name_products():
#     """
#     get all name product for autocomplete
#     /!\ /!\ NOT IMPLEMENTED FOR A FUTURE VERSION /!\ /!\
#     """
#     print("stop")
#     all_products = Product.objects.all().values('name')
#     return all_products
