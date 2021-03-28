""" Models postgres"""
from django.db import models
from product.config.config import logger


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)


class Product(models.Model):
    name = models.CharField(max_length=200)
    stores = models.CharField(max_length=200, null=True)
    url = models.CharField(max_length=255, null=True)
    nutriscore = models.CharField(max_length=20, null=True)
    category = models.ManyToManyField(Category)


# class ProductCategory(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)

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
    for product in list_product:


        # Creation d'un produit
        # prod = Product(
        #     name=product['name'],
        #     stores=product['stores'],
        #     url=product['url'],
        #     nutriscore=product['nutriscore_score'],
        # )
        # prod.save()
        product_obj, created = Product.objects.get_or_create(
            name=product['name'],
            stores=product['stores'],
            url=product['url'],
            nutriscore=product['nutriscore_score']
        )
        if created:
            number_product_insert += 1


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
        # Product.objects.bulk_create(object_product)
        # product_obj.save()
        # product_obj.category(categories_obj)

    # Product.objects.bulk_create(object_product)
    # Product.objects.set(obj_categories)

