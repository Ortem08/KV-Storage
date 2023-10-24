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
        except KeyError as ex:
            return KVStorageResponse(key, None, f'Unknown key [{key}] for [{storage_name}] storage. '
                                                f'Inner exception: {ex}')
        except TokenExpiredError as ex:
            return KVStorageResponse(key, None, f'Expired, exception: [{str(ex)}]')
        except Exception as ex:
            return KVStorageResponse(key, None, f'Unknown error [{str(ex)}]')

    def add(self, storage_name: str, key: str, value: str, ttl: int = -1) -> KVStorageResponse:
        try:
            storage = self._storage_provider.get(storage_name)
            storage.add(key, value, ttl)
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

    def get_all_keys(self, storage_name):
        try:
            storage = self._storage_provider.get(storage_name)
            return KVStorageResponse(storage.get_all_keys(), None, None)
        except ValueError as ex:
            return KVStorageResponse(None, None, f'Unknown storage [{storage_name}], exception: [{str(ex)}]')
        except TokenExpiredError as ex:
            return KVStorageResponse(None, None, f'Expired, exception: [{str(ex)}]')
        except Exception as ex:
            return KVStorageResponse(None, None, f'Unknown error [{str(ex)}]')

    def get_by_key_prefix(self, storage_name, key_prefix):
        try:
            storage = self._storage_provider.get(storage_name)
            values = []
            for key in storage.get_all_keys():
                if key.startswith(key_prefix):
                    try:
                        values.append(f'{key}: {storage.get(key)}')
                    except KeyError:
                        pass

            return KVStorageResponse(key_prefix, values, None)
        except ValueError as ex:
            return KVStorageResponse(None, None, f'Unknown storage [{storage_name}], exception: [{str(ex)}]')
        except TokenExpiredError as ex:
            return KVStorageResponse(None, None, f'Expired, exception: [{str(ex)}]')
        except Exception as ex:
            return KVStorageResponse(None, None, f'Unknown error [{str(ex)}]')

    def get_by_key_in_any_register(self, storage_name, key_in_any_register: str):
        try:
            key_lower = key_in_any_register.lower()
            storage = self._storage_provider.get(storage_name)
            values = []
            for key in storage.get_all_keys():
                if key_lower == key.lower():
                    values.append(f'{key}: {storage.get(key)}')

            return KVStorageResponse(key_in_any_register, values, None)
        except ValueError as ex:
            return KVStorageResponse(None, None, f'Unknown storage [{storage_name}], exception: [{str(ex)}]')
        except TokenExpiredError as ex:
            return KVStorageResponse(None, None, f'Expired, exception: [{str(ex)}]')
        except Exception as ex:
            return KVStorageResponse(None, None, f'Unknown error [{str(ex)}]')

    def remove(self, storage_name: str, key: str) -> KVStorageResponse:
        try:
            storage = self._storage_provider.get(storage_name)
            storage.remove(key)
            return KVStorageResponse(key, None, None)
        except ValueError as ex:
            return KVStorageResponse(key, None, f'Unknown storage [{storage_name}], exception: [{str(ex)}]')
        except TokenExpiredError as ex:
            return KVStorageResponse(key, None, f'Expired, exception: [{str(ex)}]')
        except Exception as ex:
            print(ex)
            return KVStorageResponse(key, None, f'Unknown error [{str(ex)}]')
