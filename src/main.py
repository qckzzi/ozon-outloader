#!/usr/bin/env python
"""Основной модуль запуска загрузчика."""
import requests

import config
from markets_bridge.services import (
    Fetcher,
)


def main():
    products = Fetcher.get_products()
    headers = {'Client-Id': config.ozon_client_id, 'Api-Key': config.ozon_api_key}
    response = requests.post(config.ozon_product_import_url, headers=headers, json=products)
    print(response.json()['result'])


if __name__ == '__main__':
    main()
