import requests

from IClient import IClient
from Token import Token


class Client(IClient):
    URL = 'http://127.0.0.1:8000'
    SECRET_KEY = ''
    TOKEN = None

    def __init__(self):
        try:
            with open('token', 'r') as f:
                Client.TOKEN = Token(f.read())
        except FileNotFoundError:
            self.login(input('Логин: '), input('Пароль: '))

    def new(self, path: str, storage_name: str, storage_type: str, mem_limit: int = 0) -> None:
        params = {
            'path': f'{path}',
            'storage_name': f'{storage_name}',
            'token': f'{self.TOKEN.token}',
            'storage_type': f'{storage_type}',
            'mem_limit': f'{mem_limit}'
        }

        response = requests.post(f'{Client.URL}/new', params=params)

        return response.json()

    def add(self, storage_name: str, key: str, value: str) -> None:
        params = {
            'storage_name': f'{storage_name}',
            'key': f'{key}',
            'token': f'{self.TOKEN.token}'
        }
        response = requests.post(f'{Client.URL}/add', params=params, data=value)

        return response.json()

    def add_with_ttl(self, storage_name: str, key: str, value: str, ttl: int) -> None:
        params = {
            'storage_name': f'{storage_name}',
            'key': f'{key}',
            'ttl': f'{ttl}',
            'token': f'{self.TOKEN.token}'
        }
        response = requests.post(f'{Client.URL}/add_with_ttl', params=params, data=value)

        return response.json()

    def set(self, storage_name: str, key: str, value: str) -> None:
        params = {
            'storage_name': f'{storage_name}',
            'key': f'{key}',
            'token': f'{self.TOKEN.token}'
        }
        response = requests.post(f'{Client.URL}/set', params=params, data=value)

        return response.json()

    def get(self, storage_name: str, key: str) -> str:
        params_get = {
            'storage_name': f'{storage_name}',
            'key': f'{key}',
            'token': f'{self.TOKEN.token}'
        }
        #
        # params_get_pref = {
        #     'storage_name': f'{storage_name}',
        #     'key_prefix': f'{key}',
        #     'token': f'{self.TOKEN.token}'
        # }

        response = requests.get(f'{Client.URL}/get', params=params_get)
        # if response.json()['value'].__contains__("Key not found"):
        #     response = requests.get(f'{Client.URL}/get', params=params_get_pref)

        return response.json()

    def get_by_key_prefix(self, storage_name: str, key_prefix: str) -> str:
        params = {
            'storage_name': f'{storage_name}',
            'key_prefix': f'{key_prefix}',
            'token': f'{self.TOKEN.token}'
        }

        response = requests.get(f'{Client.URL}/get_by_key_prefix', params=params)

        return response.json()

    def get_all_keys(self, storage_name: str) -> str:
        params = {
            'storage_name': f'{storage_name}',
            'token': f'{self.TOKEN.token}'
        }
        response = requests.get(f'{Client.URL}/get_all_keys', params=params)

        return response.json()

    def get_by_key_in_any_register(self, storage_name: str, key: str):
        params = {
            'storage_name': f'{storage_name}',
            'token': f'{self.TOKEN.token}',
            'key': key
        }
        response = requests.get(f'{Client.URL}/get_by_key_in_any_register', params=params)

        return response.json()

    def delete(self, storage_name: str, key: str) -> str:
        params = {
            'storage_name': f'{storage_name}',
            'key': f'{key}',
            'token': f'{self.TOKEN.token}'
        }
        response = requests.post(f'{Client.URL}/delete', params=params)

        return response.json()

    def login(self, login: str, password: str) -> None:
        params = {
            'login': f'{login}',
            'password': f'{password}'
        }
        response = requests.post(f'{Client.URL}/login', params=params)

        Client.TOKEN = Token(response.json()['token'])
        with open('token', 'w') as f:
            f.write(Client.TOKEN.token)
        print('Success')

        pass
