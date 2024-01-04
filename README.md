[![Python 3.12](https://img.shields.io/badge/python-3.12-green.svg)](https://www.python.org/downloads/release/python-3120/)
# ozon-outloader
## Описание
Данный сервис является выгрузчиком товаров на площадку [OZON](https://www.ozon.ru/). Является непосредственной частью системы
Markets-Bridge.

*Данный сервис является очень временным решением, и будет либо переписан, либо неиспользован в будущем, т.к. на данный момент из-за
него сервис [Markets-Bridge](https://github.com/qckzzi/markets-bridge-drf-app) перегружен ответственностью.

Его задачи:
1. Получает JSON данные, которые перенаправляются в OZON (что априори является некорректной работой, в будущем из [Markets-Bridge](https://github.com/qckzzi/markets-bridge-drf-app)
будет вырезана подсистема выгрузки данных, такие интеграции должны реализовываться смежно от DRF системы и получать данные по доступному API);
2. Валидирует данные по правилам OZON;
3. Записывает результат в логи [Markets-Bridge](https://github.com/qckzzi/markets-bridge-drf-app).

## Установка
### Конфигурация системы
Для функционирования системы необходимы:
- Запущенный instance [Markets-Bridge](https://github.com/qckzzi/markets-bridge-drf-app);
- [RabbitMQ server](https://www.rabbitmq.com/download.html);
- Python, поддерживаемой версии (разработка велась на 3.12.0).

### Установка проекта
Клонируем проект в необходимую директорию:
```shell
git clone git@github.com:qckzzi/ozon-outloader.git
```
```shell
cd ozon-outloader
```
Создадим виртуальное окружение:
```shell
python3 -m venv venv
```
(или любым другим удобным способом)

Активируем его:
```shell
. venv/bin/activate
```
Установим зависимости:

(для разработки)
```shell
pip install -r DEV_REQUIREMENTS.txt
```
(для деплоя)
```shell
pip install -r REQUIREMENTS.txt
```
В корневой директории проекта необходимо скопировать файл ".env.example", переименовать
его в ".env" и заполнить в соответствии с вашей системой.

Запуск сервиса:
```shell
python3 src/main.py
```
## Разработка

Для внесения изменений в кодовую базу необходимо инициализировать pre-commit git hook.
Это можно сделать командой в терминале, находясь в директории проекта:
```shell
pre-commit install
```
Это необходимо для поддержания 
единого кодстайла в проекте. При каждом коммите будет запущен форматировщик.