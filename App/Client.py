import requests

from IClient import IClient


class Client(IClient):
    URL = 'http://127.0.0.1:8000'

    def __init__(self):
        ...

    def new(self, path: str, storage_name: str) -> None:
        params = {
            'path': f'{path}',
            'storage_name': f'{storage_name}'
        }
        response = requests.post(f'{Client.URL}/new', params=params)

        pass

    def add(self, storage_name: str, key: str, value: str) -> None:
        params = {
            'storage_name': f'{storage_name}',
            'key': f'{key}'
        }
        response = requests.post(f'{Client.URL}/add', params=params, data=value)

        pass

    def set(self, storage_name: str, key: str, value: str) -> None:
        params = {
            'storage_name': f'{storage_name}',
            'key': f'{key}'
        }
        response = requests.post(f'{Client.URL}/set', params=params, data=value)

        pass

    def get(self, storage_name: str, key: str) -> str:
        params = {
            'storage_name': f'{storage_name}',
            'key': f'{key}'
        }
        response = requests.get(f'{Client.URL}/get', params=params)

        return response.json()
