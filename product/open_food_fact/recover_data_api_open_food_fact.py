import sys

import requests

from product.config.config import logger, config


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
        params = {
            "action": "process",
            "json": 1,
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": category,
            "page_size": 20
        }

        try:
            page = 1
            list_list_product = []
            number_product = int(config['API_OFF']['max_product_by_category'])
            while len(list_list_product) <= number_product:
                query = requests.get(f'https://fr.openfoodfacts.org/category/{category}.json?page={page}').json()
                if int(query['count']) == 0:
                    logger.info(f"Aucune données dans l'API pour la catégory {category}")
                    return list_list_product
                elif int(query['count']) < int(config['API_OFF']['max_product_by_category']):
                    number_product = int(query['count'])

                for product in query['products']:
                    product_list = {}
                    product_list['name'] = product.get("product_name_fr").strip()

                    product_list['image_product'] = product.get("image_url")

                    product_list['stores'] = product.get("stores", '').strip()

                    product_list['url'] = product.get("url", '').strip()

                    product_list['nutriscore'] = product.get("nutriscore_grade")

                    product_list['image_reperes_nutrionnels'] = product.get("image_nutrition_url")

                    product_list['categories_product'] = product.get("categories", "").split(",")

                    list_list_product.append(product_list)
                page += 1

            return list_list_product[:number_product]

        except AttributeError as e:
            logger.info("stop")
            logger.error("Une erreur c'est produite pendant la requete GET")
            logger.error(e)
            sys.exit()


if __name__ == "__main__":
    RecoverApi().get_product("Pizza")
