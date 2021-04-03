from django.core.management.base import BaseCommand, CommandError

from product.open_food_fact import recover_data_api_open_food_fact
from product.config import config
from product.models import bulk_insert_product_category
from product.config.config import logger


class Command(BaseCommand):
    help = 'Insert data from API Open Food Fact'

    def handle(self, *args, **kwargs):
        """
        function main:
        - run methode for get data in api open food fact
        - insert data api in table db
        """
        # bulk_insert_product_category()
        configparser = config.config
        list_categories = configparser['API_OFF']['list_categories'].split(",")
        recover_api = recover_data_api_open_food_fact.RecoverApi()
        for category in list_categories:
            # del space in list
            category = category.strip()
            logger.info("===================")
            logger.info(f"Insertion pour la catégorie {category}")
            logger.info("===================")
            list_product = recover_api.get_product(category=category)
            # bulk insert product
            if len(list_product) > 0:
                bulk_insert_product_category(list_product=list_product)



