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

    def set(self, storage_name: str, key: str, value: str) -> None:
        params = {
            'storage_name': f'{storage_name}',
            'key': f'{key}',
            'token': f'{self.TOKEN.token}'
        }
        response = requests.post(f'{Client.URL}/set', params=params, data=value)

        return response.json()

    def get(self, storage_name: str, key: str) -> str:
        params = {
            'storage_name': f'{storage_name}',
            'key': f'{key}',
            'token': f'{self.TOKEN.token}'
        }
        response = requests.get(f'{Client.URL}/get', params=params)

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
