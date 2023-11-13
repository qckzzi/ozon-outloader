import os

from dotenv import (
    load_dotenv,
)


load_dotenv()


# OZON
ozon_domain = 'https://api-seller.ozon.ru/'
ozon_product_import_url = ozon_domain + 'v2/product/import'
ozon_update_product_prices_url = ozon_domain + 'v1/product/import/prices'
ozon_update_product_stocks_url = ozon_domain + 'v1/product/import/stocks'

ozon_client_id = os.getenv('OZON_CLIENT_ID')
ozon_api_key = os.getenv('OZON_API_KEY')

if not (ozon_client_id and ozon_api_key):
    raise ValueError('Не заданы Client-Id и Api-Key для доступа к api озона.')
