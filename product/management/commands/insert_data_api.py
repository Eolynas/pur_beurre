from django.core.management.base import BaseCommand, CommandError
from product.models import Product, Category
from django.utils import timezone
from product.open_food_fact import recover_data_api_open_food_fact, insert_data_api_in_db


class Command(BaseCommand):
    help = 'Insert data from API Open Food Fact'

    def handle(self, *args, **kwargs):
        recover_api = insert_data_api_in_db.main()



