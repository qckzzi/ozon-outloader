#!/usr/bin/env python
"""Основной модуль запуска загрузчика."""
from markets_bridge.services import (
    Fetcher,
)


def main():
    products = Fetcher.get_products()
    ...


if __name__ == '__main__':
    main()
