import requests

import config
from markets_bridge.types import (
    MBProduct,
)


class Fetcher:
    @staticmethod
    def get_products() -> list[MBProduct]:
        products = requests.get(config.mb_products_url).json()

        return products
