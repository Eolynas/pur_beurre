""" Models postgres"""
from typing import Union, Tuple

from django.db import models

from tools import logger
from random import choice
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


# class UserProfil(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     image = models.ImageField(null=True)
#
#     def __str__(self):
#         return "%s's profile" % self.user


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # profile_image = models.FileField()
    name_animals = models.CharField(max_length=255, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    image_product = models.CharField(max_length=255, null=True)
    stores = models.CharField(max_length=200, null=True)
    url = models.CharField(max_length=255, null=True)
    nutriscore = models.CharField(max_length=20, null=True)
    image_reperes_nutrionnels = models.CharField(max_length=255, null=True)
    category = models.ManyToManyField(Category, related_name='products')
    user_save = models.ManyToManyField(User, related_name='user_save_products')

    def __str__(self):
        return self.name


def delete_all_data_in_tables():
    Product.objects.all().delete()
    Category.objects.all().delete()
    logger.info("Toutes les données ont étaient éffacés")

    # def bulk_insert_product_category():
    #     """
    #     insert all product and ur categories
    #     """
    #     # Creation de deux objet (product & category) pour bulk insert
    #
    #     p1 = Product.objects.create(name="Pizza fromage",
    #                                 image_product="https://image.fr",
    #                                 stores="OpenClassrooms",
    #                                 url=None,
    #                                 nutriscore="D",
    #                                 image_reperes_nutrionnels="https://image_repere.fr")
    #
    #     p1.save()
    #     c1 = Category.objects.create(name='Pizza')
    #     c1.save()
    #     p1.category.add(c1)
    #     c2 = Category.objects.create(name='Fromage')
    #     c2.save()
    #     p1.category.add(c2)
    #
    #     get = Product.objects.filter(pk=221)
    #     print(get)

    """
    AttributeError: 'function' object has no attribute 'value'
>>> Category.objects.filter(product__name='Pizza fromage').all.values()
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: 'function' object has no attribute 'values'
>>> Category.objects.filter(product__name='Pizza fromage').all().value()
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: 'QuerySet' object has no attribute 'value'
>>> Category.objects.filter(product__name='Pizza fromage').all().values()
<QuerySet [{'id': 312, 'name': 'Pizza'}, {'id': 313, 'name': 'Fromage'}]>

    """


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
        # categories_obj = []
        for category in product['categories_product']:
            categories_obj = []
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


def get_product_by_id(id_product: int) -> Union[Product, None]:
    """
    get product with id
    :param id_product: id product
    :type product_name: int
    """
    try:
        int(id_product)
    except ValueError as e:
        return None
    query = Product.objects.filter(pk=id_product).first()

    return query


def get_subsitut_for_product(product: str) -> Union[Tuple[str, list], bool]:
    """
    get subsitut at product
    :param product: Product at changed
    :return: product_initial_info.name: object product
    :return: choise_substitute_products: list object product
    """

    # recovery of the product & categories sought by the user
    product_initial_info = Product.objects.filter(name__icontains=product).first()
    if not product_initial_info:
        return False
    categories_at_product_initial = product_initial_info.category.all()

    substitute_products = []
    for index, category in enumerate(categories_at_product_initial.all()):
        list_product_by_category = []
        products = category.products.all()
        for product in products:
            if not product in substitute_products \
                    and product.nutriscore.lower() <= product_initial_info.nutriscore.lower() \
                    and not product.name == product_initial_info.name:
                list_product_by_category.append(product)
                substitute_products.append(product)

    nbr_products_in_list = len(substitute_products)

    if nbr_products_in_list > 6:
        # method to randomly choose 6 products
        # choise_substitute_products = []
        # for x in range(6):
        #     choise = choice(substitute_products)
        #     choise_substitute_products.append(choise)
        #     substitute_products.remove(choise)
        #
        # print(choise_substitute_products)
        #
        # return product_initial_info, choise_substitute_products
        return product_initial_info, substitute_products[:6]

    return product_initial_info, substitute_products


def save_product_for_user(id_product: int, user: User):
    """
    Save product adding by user
    """
    product = get_product_by_id(id_product)
    result = product.user_save.add(user)
    product.save()


def get_product_save_user(user):
    """
    get all product save by user
    """
    user_product_save = Product.objects.filter(user_save=user.id).all()

    return user_product_save


def get_all_name_products():
    """
    get all name product for autocomplete
    /!\ /!\ NOT IMPLEMENTED FOR A FUTURE VERSION /!\ /!\
    """
    print("stop")
    all_products = Product.objects.all().values('name')
    return all_products
