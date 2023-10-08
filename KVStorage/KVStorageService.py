import os

from Index.CachedIndexRepository import CachedIndexRepository
from Index.IndexRepository import IndexRepository
from KVStorage.IKVStorageProvider import IKVStorageProvider
from KVStorage.KVStorage import KVStorage
from KVStorageResponse import KVStorageResponse
from ValueStorage.CachedValueRepository import CachedValueRepository
from ValueStorage.ValueRepository import ValueRepository


class KVStorageService:
    def __init__(self, kv_storage_provider: IKVStorageProvider):
        self._storage_provider = kv_storage_provider

    def new(self, storage_name: str):
        try:
            self._storage_provider.add(storage_name)
            return KVStorageResponse(None, None, None)
        except ValueError as ex:
            return KVStorageResponse(None, None, str(ex))
        except Exception as ex:
            return KVStorageResponse(None, None, str(ex))

    def get(self, storage_name: str, key: str) -> KVStorageResponse:
        try:
            storage = self._storage_provider.get(storage_name)
            return KVStorageResponse(key, storage.get(key), None)
        except ValueError as ex:
            return KVStorageResponse(key, None, f'Unknown storage [{storage_name}], exception: [{str(ex)}]')
        except KeyError:
            return KVStorageResponse(key, None, f'Unknown key [{key}] for [{storage_name}] storage')
        except Exception as ex:
            return KVStorageResponse(key, None, f'Unknown error [{str(ex)}]')

    def add(self, storage_name: str, key: str, value: str) -> KVStorageResponse:
        try:
            storage = self._storage_provider.get(storage_name)
            storage.add(key, value)
            return KVStorageResponse(key, None, None)
        except ValueError as ex:
            return KVStorageResponse(key, None, f'Unknown storage [{storage_name}], exception: [{str(ex)}]')
        except Exception as ex:
            return KVStorageResponse(key, None, f'Unknown error [{str(ex)}]')

    def set(self, storage_name: str, key: str, value: str) -> KVStorageResponse:
        try:
            storage = self._storage_provider.get(storage_name)
            storage.set(key, value)
            return KVStorageResponse(key, None, None)
        except ValueError as ex:
            return KVStorageResponse(key, None, f'Unknown storage [{storage_name}], exception: [{str(ex)}]')
        except Exception as ex:
            return KVStorageResponse(key, None, f'Unknown error [{str(ex)}]')
