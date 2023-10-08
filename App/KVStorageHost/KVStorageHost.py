from flask import Flask

from Infrastructure.IHost import IHost
from App.KVStorageHost.KVStorageController import KVStorageController
from KVStorage.KVStorageProvider import KVStorageProvider
from KVStorage.KVStorageService import KVStorageService


class KVStorageHost(IHost):
    def __init__(self,
                 host: str = '127.0.0.1',
                 port: int = 8000):
        self._host = host
        self._port = port

        self._app = Flask(__name__)

        self._controllers = [
            KVStorageController(self._app, KVStorageService(KVStorageProvider()))
        ]

    def run(self):
        self._app.run(self._host, self._port)
