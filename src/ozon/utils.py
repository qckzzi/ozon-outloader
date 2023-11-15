import logging

import requests

import config
from markets_bridge.utils import (
    get_ozon_api_key,
    get_ozon_client_id,
    write_log_entry,
)
from ozon.enums import (
    OperationType,
)


class OzonSender:
    """Отправитель данных в OZON."""

    @classmethod
    def get_sending_method_by_operation_type(cls, operation_type: str):
        method_for_operation_type_map = {
            OperationType.LOAD_PRODUCTS: cls.send_products,
            OperationType.UPDATE_PRODUCT_PRICES: cls.update_product_prices,
            OperationType.UPDATE_PRODUCT_STOCKS: cls.update_product_stocks,
        }

        return method_for_operation_type_map[operation_type]

    @classmethod
    def send_products(cls, products: dict):
        cls.send_request_to_ozon(
            url=config.ozon_product_import_url,
            body=products,
            result_message='Import result: ',
        )

    @classmethod
    def update_product_prices(cls, products: dict):
        cls.send_request_to_ozon(
            url=config.ozon_update_product_prices_url,
            body=products,
            result_message='Prices update result: ',
        )

    @classmethod
    def update_product_stocks(cls, products: dict):
        cls.send_request_to_ozon(
            url=config.ozon_update_product_stocks_url,
            body=products,
            result_message='Stocks update result: ',
        )


    @staticmethod
    def send_request_to_ozon(url: str, body: dict, result_message: str):
        response = requests.post(url, headers=_get_headers(), json=body)
        response.raise_for_status()
        result = f'{result_message}{response.json()['result']}'

        write_log_entry(result)
        logging.info(result)


def _get_headers():
    client_id = get_ozon_client_id()
    ozon_api_key = get_ozon_api_key()

    return {'Client-Id': client_id, 'Api-Key': ozon_api_key}