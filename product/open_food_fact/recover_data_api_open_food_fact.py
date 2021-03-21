import requests


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
            number_page_requetes_get = 2
            page = 1
            list_list_product = []
            while len(list_list_product) <= 100:

                query_2 = requests.get(f'https://fr.openfoodfacts.org/category/{category}.json?page={page}').json()

                for product in query_2['products']:
                    product_list = {}

                    product_list['name'] = product.get("product_name_fr")

                    product_list['stores'] = product.get("stores")

                    product_list['url'] = product.get("url")

                    product_list['nutriscore_score'] = product.get("nutriscore_score")

                    product_list['categories_product'] = product.get("categories", "").split(",")

                    list_list_product.append(product_list)
                page += 1

            return list_list_product

        except:
            print("Une erreur c'est produite pendant la requete GET")


if __name__ == "__main__":
    RecoverApi().get_product("Pizza")

