import sys

import requests

from tools import logger
import os


class RecoverApi:
    """
    request for get apî data
    """

    def get_product(self, category) -> list:
        """
        get api data for category list
        :param category: list: category
        :return: json: product list
        """
        try:
            page = 1
            list_list_product = []
            while True:
                query = requests.get(f'https://fr.openfoodfacts.org/category/{category}.json?page={page}').json()
                if int(query['count']) == 0:
                    logger.info(f"Aucune données dans l'API pour la catégory {category}")
                    return list_list_product

                for product in query['products']:
                    product_list = {}
                    if product.get("product_name_fr") and \
                            product.get("image_url") and \
                            product.get("stores") and \
                            product.get("url") and \
                            product.get("nutriscore_grade") and \
                            product.get("image_nutrition_url") and \
                            product.get("categories"):
                        product_list['name'] = product.get("product_name_fr").strip()

                        product_list['image_product'] = product.get("image_url")

                        product_list['stores'] = product.get("stores", '').strip()

                        product_list['url'] = product.get("url", '').strip()

                        product_list['nutriscore'] = product.get("nutriscore_grade")

                        product_list['image_reperes_nutrionnels'] = product.get("image_nutrition_url")

                        product_list['categories_product'] = product.get("categories", "").split(",")

                        list_list_product.append(product_list)
                page += 1

                if query['page_count'] == page:
                    return list_list_product

        except AttributeError as e:
            logger.info("stop")
            logger.error("Une erreur c'est produite pendant la requete GET")
            logger.error(e)
            sys.exit()


if __name__ == "__main__":
    RecoverApi().get_product("Pizza")
