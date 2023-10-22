from App.KVStorageHost.KVStorageResponse import KVStorageResponse
from App.TokenExpiredError import TokenExpiredError
from KVStorage.IKVStorageProvider import IKVStorageProvider


class KVStorageService:
    def __init__(self, kv_storage_provider: IKVStorageProvider):
        self._storage_provider = kv_storage_provider

    def new(self, storage_name: str, storage_type: str, mem_limit: int = 0):
        try:
            self._storage_provider.add(storage_name, storage_type, mem_limit)
            return KVStorageResponse(None, None, None)
        except ValueError as ex:
            return KVStorageResponse(None, None, str(ex))
        except TokenExpiredError as ex:
            return KVStorageResponse(None, None, f'Expired, exception: [{str(ex)}]')
        except Exception as ex:
            return KVStorageResponse(None, None, str(ex))

    def get(self, storage_name: str, key: str) -> KVStorageResponse:
        try:
            storage = self._storage_provider.get(storage_name)
            return KVStorageResponse(key, storage.get(key), None)
        except ValueError as ex:
            print(ex)
            return KVStorageResponse(key, None, f'Unknown storage [{storage_name}], exception: [{str(ex)}]')
        except KeyError:
            return KVStorageResponse(key, None, f'Unknown key [{key}] for [{storage_name}] storage')
        except TokenExpiredError as ex:
            return KVStorageResponse(key, None, f'Expired, exception: [{str(ex)}]')
        except Exception as ex:
            return KVStorageResponse(key, None, f'Unknown error [{str(ex)}]')

    def add(self, storage_name: str, key: str, value: str) -> KVStorageResponse:
        try:
            storage = self._storage_provider.get(storage_name)
            storage.add(key, value)
            return KVStorageResponse(key, None, None)
        except ValueError as ex:
            return KVStorageResponse(key, None, f'Unknown storage [{storage_name}], exception: [{str(ex)}]')
        except TokenExpiredError as ex:
            return KVStorageResponse(key, None, f'Expired, exception: [{str(ex)}]')
        except Exception as ex:
            return KVStorageResponse(key, None, f'Unknown error [{str(ex)}]')

    def set(self, storage_name: str, key: str, value: str) -> KVStorageResponse:
        try:
            storage = self._storage_provider.get(storage_name)
            storage.set(key, value)
            return KVStorageResponse(key, None, None)
        except ValueError as ex:
            return KVStorageResponse(key, None, f'Unknown storage [{storage_name}], exception: [{str(ex)}]')
        except TokenExpiredError as ex:
            return KVStorageResponse(key, None, f'Expired, exception: [{str(ex)}]')
        except Exception as ex:
            return KVStorageResponse(key, None, f'Unknown error [{str(ex)}]')
