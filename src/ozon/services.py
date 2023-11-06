import requests

import config
from ozon.types import (
    OzonProduct,
)


class Sender:
    """Отправитель данных в сервис Ozon."""

    @classmethod
    def send_products(cls, products: list[OzonProduct]):
        for product in products:
            cls.send_product(product)

    @staticmethod
    def send_product(product: OzonProduct):
        ...
        # response = requests.post(config.ozon_product_import_url, json=vars(product))
        #
        # if response.status_code == 201:
        #     print(f'The "{}" has been created.')
        # elif response.status_code == 200:
        #     print(f'The ""  already exists.')
        # else:
        #     print(f'When creating the "" , the server returned an error.')
