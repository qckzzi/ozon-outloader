#!/usr/bin/env python
import json
import logging

import pika

from markets_bridge.utils import (
    write_log_entry,
)
from ozon.utils import (
    OzonSender,
)


def callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        operation_type = message['method']

        logging.info(f'Products was received for "{operation_type.lower()}" action.')

        sending_function = OzonSender.get_sending_method_by_operation_type(operation_type)

        products = message['products']
        headers = _get_headers(products.pop('personal_area'))
        sending_function(products, headers)

    except KeyError as e:
        error = f'Body validation error: {e}'
        write_log_entry(error)
        logging.error(error)
        return
    except Exception as e:
        error = f'There was a problem: {e}'
        write_log_entry(error)
        logging.exception(error)
        return


def _get_headers(personal_area_variables: list[dict]):
    headers = {}

    for variable in personal_area_variables:
        headers.update({variable['key']: variable['value']})

    return {variable['key']: variable['value'] for variable in personal_area_variables}


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

    connection_parameters = pika.ConnectionParameters(host='localhost', heartbeat=300, blocked_connection_timeout=300)
    with pika.BlockingConnection(connection_parameters) as connection:
        channel = connection.channel()
        channel.queue_declare('outloading')
        channel.basic_consume('outloading', callback, auto_ack=True)
        channel.start_consuming()
