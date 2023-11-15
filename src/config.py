import os

from dotenv import (
    load_dotenv,
)


load_dotenv()

# Markets-Bridge
mb_domain = os.getenv('MB_DOMAIN')

if not mb_domain:
    raise ValueError('Не ')

mb_login = os.getenv('MB_LOGIN')
mb_password = os.getenv('MB_PASSWORD')

if not (mb_login and mb_password):
    raise ValueError('MB_LOGIN and MB_PASSWORD not set for Markets-Bridge authentication')

mb_token_url = mb_domain + 'api/token/'
mb_token_refresh_url = mb_token_url + 'refresh/'
mb_system_environments_url = mb_domain + 'api/v1/common/system_environments/'
mb_logs_url = mb_domain + 'api/v1/common/logs/'


# OZON
ozon_domain = 'https://api-seller.ozon.ru/'
ozon_product_import_url = ozon_domain + 'v2/product/import'
ozon_update_product_prices_url = ozon_domain + 'v1/product/import/prices'
ozon_update_product_stocks_url = ozon_domain + 'v1/product/import/stocks'

ozon_client_id = os.getenv('OZON_CLIENT_ID')
ozon_api_key = os.getenv('OZON_API_KEY')

if not (ozon_client_id and ozon_api_key):
    raise ValueError('Не заданы Client-Id и Api-Key для доступа к api озона.')
