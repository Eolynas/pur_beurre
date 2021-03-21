""" main file for recover data api and insert / update in db"""

import sys

from product.models import Category, Product
# import recover_data_api_open_food_fact
from product.open_food_fact import recover_data_api_open_food_fact
from product.config import config


def main():
    """
    function main:
    - run methode for get data in api open food fact
    - insert data api in table db
    """
    configparser = config.config
    list_categories = configparser['API_OFF']['list_categories'].split(",")
    recover_api = recover_data_api_open_food_fact.RecoverApi()
    for category in list_categories:
        print("===================")
        print(category)
        print("===================")
        list_product = recover_api.get_product(category=category)



if __name__ == "__main__":
    main()