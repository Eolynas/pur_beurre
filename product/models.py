from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)


class Product(models.Model):
    name = models.CharField(max_length=200)
    store = models.CharField(max_length=200)
    url = models.CharField(max_length=255)
    nutriscore = models.CharField(max_length=20)
    category = models.ManyToManyField(Category)




