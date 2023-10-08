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

    def add(self, key: str, value: str, storage_name: str) -> None:
        params = {
            'key': f'{key}',
            'storage_name': f'{storage_name}'
        }
        response = requests.post(f'{Client.URL}/add', params=params, data=value)

        pass

    def set(self, key: str, value: str, storage_name: str) -> None:
        params = {
            'key': f'{key}',
            'storage_name': f'{storage_name}'
        }
        response = requests.post(f'{Client.URL}/set', params=params, data=value)

        pass

    def get(self, key: str, storage_name: str) -> str:
        params = {
            'key': f'{key}',
            'storage_name': f'{storage_name}'
        }
        response = requests.get(f'{Client.URL}/get', params=params)

        return response.json()
