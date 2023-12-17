import logging

import requests

import config
from markets_bridge.utils import (
    write_log_entry,
)
from ozon.enums import (
    OperationType,
)


class OzonSender:
    """Отправитель данных в OZON."""

    PRODUCT_IMPORT_MAX = 100
    STOCK_UPDATE_MAX = 100
    PRICE_UPDATE_MAX = 1000

    @classmethod
    def get_sending_method_by_operation_type(cls, operation_type: str):
        method_for_operation_type_map = {
            OperationType.LOAD_PRODUCTS: cls.send_products,
            OperationType.UPDATE_PRODUCT_PRICES: cls.update_product_prices,
            OperationType.UPDATE_PRODUCT_STOCKS: cls.update_product_stocks,
        }

        return method_for_operation_type_map[operation_type]

    @classmethod
    def send_products(cls, products: dict, headers: dict):
        pointer_range = range(0, len(products['items']), cls.PRODUCT_IMPORT_MAX)

        for i in pointer_range:
            products_range = dict(items=products['items'][i:i+cls.PRODUCT_IMPORT_MAX])

            cls.send_request_to_ozon(
                url=config.ozon_update_product_stocks_url,
                body=products_range,
                headers=headers,
                result_message='Stocks update result: ',
            )

    @classmethod
    def update_product_prices(cls, products: dict, headers: dict):
        pointer_range = range(0, len(products['prices']), cls.PRICE_UPDATE_MAX)

        for i in pointer_range:
            products_range = dict(prices=products['prices'][i:i+cls.PRICE_UPDATE_MAX])

            cls.send_request_to_ozon(
                url=config.ozon_update_product_stocks_url,
                body=products_range,
                headers=headers,
                result_message='Stocks update result: ',
            )

    @classmethod
    def update_product_stocks(cls, products: dict, headers: dict):
        pointer_range = range(0, len(products['stocks']), cls.STOCK_UPDATE_MAX)

        for i in pointer_range:
            products_range = dict(stocks=products['stocks'][i:i+cls.STOCK_UPDATE_MAX])

            cls.send_request_to_ozon(
                url=config.ozon_update_product_stocks_url,
                body=products_range,
                headers=headers,
                result_message='Stocks update result: ',
            )

    @staticmethod
    def send_request_to_ozon(url: str, body: dict, headers: dict, result_message: str):
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        result = f'{result_message}{response.json()["result"]}'

        write_log_entry(result)
        logging.info(result)
