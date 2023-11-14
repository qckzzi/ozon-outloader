import requests

import config


class Singleton:
    _instance = None
    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance


class Accesser(Singleton):
    def __init__(self):
        self.refresh_token = None
        self.access_token = None

        self.update_jwt()

    def update_jwt(self):
        login_data = {
            'username': config.mb_login,
            'password': config.mb_password
        }

        response = requests.post(config.mb_token_url, data=login_data)
        response.raise_for_status()
        token_data = response.json()
        self.access_token = token_data['access']
        self.refresh_token = token_data['refresh']

    def update_access_token(self):
        body = {'refresh': {self.refresh_token}}

        response = requests.post(config.mb_token_refresh_url, json=body)

        try:
            response.raise_for_status()
        except Exception:
            self.update_jwt()

        token_data = response.json()
        self.access_token = token_data['access']
