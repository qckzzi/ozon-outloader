#!/usr/bin/env python
import json
import logging

import pika
import requests

import config


_headers = {'Client-Id': config.ozon_client_id, 'Api-Key': config.ozon_api_key}


def callback(ch, method, properties, body):
    try:
        message = json.loads(body)

        processing_map = {
            'LOAD_PRODUCTS': load_products,
            'UPDATE_PRODUCT_PRICES' : update_product_prices,
            'UPDATE_PRODUCT_STOCKS' : update_product_stocks,
        }

        processing_function = processing_map[message['method']]

        logging.info(f'Products was received for "{message["method"].lower()}" action.')

        products = message['products']
        processing_function(products)

    except KeyError as e:
        logging.exception(f'Body validation error: {e}')
        return
    except Exception as e:
        logging.exception(f'There was a problem: {e}')
        return


def load_products(products: dict):
    response = requests.post(config.ozon_product_import_url, headers=_headers, json=products)
    response.raise_for_status()
    logging.info(f'Import result: {response.json()['result']}')


def update_product_prices(products: dict):
    response = requests.post(config.ozon_update_product_prices_url, headers=_headers, json=products)
    response.raise_for_status()
    logging.info(f'Prices update result: {response.json()['result']}')


def update_product_stocks(products: dict):
    response = requests.post(config.ozon_update_product_stocks_url, headers=_headers, json=products)
    response.raise_for_status()
    logging.info(f'Stocks update result: {response.json()['result']}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

    connection_parameters = pika.ConnectionParameters(host='localhost', heartbeat=300, blocked_connection_timeout=300)
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.queue_declare('outloading')
    channel.basic_consume('outloading', callback, auto_ack=True)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.close()
        connection.close()
