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
    ARCHIVE_PRODUCTS_MAX = 100
    PRODUCT_LIST_FILTER_VALUES_COUNT_MAX = 1000

    @classmethod
    def get_sending_method_by_operation_type(cls, operation_type: str):
        method_for_operation_type_map = {
            OperationType.LOAD_PRODUCTS: cls.send_products,
            OperationType.UPDATE_PRODUCT_PRICES: cls.update_product_prices,
            OperationType.UPDATE_PRODUCT_STOCKS: cls.update_product_stocks,
            OperationType.ARCHIVE_PRODUCTS: cls.archive_products,
        }

        return method_for_operation_type_map[operation_type]

    @classmethod
    def send_products(cls, products: dict, headers: dict):
        pointer_range = range(0, len(products['items']), cls.PRODUCT_IMPORT_MAX)

        for i in pointer_range:
            products_range = dict(items=products['items'][i:i+cls.PRODUCT_IMPORT_MAX])

            cls.send_request_to_ozon(
                url=config.ozon_product_import_url,
                body=products_range,
                headers=headers,
                result_message='Import result: ',
            )

    @classmethod
    def update_product_prices(cls, products: dict, headers: dict):
        pointer_range = range(0, len(products['prices']), cls.PRICE_UPDATE_MAX)

        for i in pointer_range:
            products_range = dict(prices=products['prices'][i:i+cls.PRICE_UPDATE_MAX])

            cls.send_request_to_ozon(
                url=config.ozon_update_product_prices_url,
                body=products_range,
                headers=headers,
                result_message='Prices update result: ',
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

    @classmethod
    def archive_products(cls, products: dict, headers: dict):
        product_ids = products['product_ids']
        product_ids_in_ozon = []

        pointer_range = range(0, len(product_ids), cls.PRODUCT_LIST_FILTER_VALUES_COUNT_MAX)

        for i in pointer_range:
            product_ids_range = product_ids[i:i+cls.PRODUCT_LIST_FILTER_VALUES_COUNT_MAX]
            product_list_request_body = dict(
                filter=dict(
                    offer_id=list(map(lambda x: str(x), product_ids_range)),
                ),
                last_id='',
                limit=1000,
            )

            product_list_response_json = cls.send_request_to_ozon(
                url=config.ozon_product_list_url,
                body=product_list_request_body,
                headers=headers,
            )
            product_list_result = product_list_response_json['result']
            product_list_items = product_list_result['items']
            product_ids_in_ozon.extend([item['product_id'] for item in product_list_items])

        pointer_range = range(0, len(product_ids_in_ozon), cls.ARCHIVE_PRODUCTS_MAX)

        for i in pointer_range:
            archive_products_request_body = dict(product_id=product_ids_in_ozon[i:i+cls.STOCK_UPDATE_MAX])

            cls.send_request_to_ozon(
                url=config.ozon_archive_product_url,
                body=archive_products_request_body,
                headers=headers,
                result_message='Archive result: ',
            )

    @staticmethod
    def send_request_to_ozon(url: str, body: dict, headers: dict, result_message: str | None = None) -> dict:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        response_json = response.json()

        if result_message:
            result = f'{result_message}{response_json["result"]}'

            write_log_entry(result)
            logging.info(result)

        return response_json
