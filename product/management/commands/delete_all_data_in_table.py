from django.core.management.base import BaseCommand
from product.models import delete_all_data_in_tables


class Command(BaseCommand):
    help = 'Insert data from API Open Food Fact'

    def handle(self, *args, **kwargs):
        delete_all_data_in_tables()



