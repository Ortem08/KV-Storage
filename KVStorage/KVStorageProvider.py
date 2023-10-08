import os

from Index.CachedIndexRepository import CachedIndexRepository
from Index.IndexRepository import IndexRepository
from KVStorage.IKVStorageProvider import IKVStorageProvider
from KVStorage.KVStorage import KVStorage
from KVStorageResponse import KVStorageResponse
from ValueStorage.CachedValueRepository import CachedValueRepository
from ValueStorage.ValueRepository import ValueRepository


class KVStorageProvider(IKVStorageProvider):
    def __init__(self, storages_path: str = 'storages', storages_list_name: str = 'storages_list'):
        self._storages_path = storages_path
        self._storages_list_name = storages_list_name

        self._storages = {}
        with open(os.path.join(self._storages_path, self._storages_list_name), 'w+') as f:
            for storage_name in f.readlines():
                ind_rep = CachedIndexRepository(IndexRepository(os.path.join(self._storages_path, storage_name)))
                val_rep = CachedValueRepository(ValueRepository(os.path.join(self._storages_path, storage_name)))

                storage = KVStorage(ind_rep, val_rep)
                self._storages[storage_name] = storage

    def get(self, storage_name: str):
        if not self._storages.__contains__(storage_name):
            raise ValueError(f"Unknown storage name [{storage_name}]")

        return self._storages[storage_name]

    def add(self, storage_name: str):
        if self._storages.__contains__(storage_name):
            raise ValueError(f'Storage [{storage_name}] already exists')

        ind_rep = CachedIndexRepository(IndexRepository(os.path.join(self._storages_path, storage_name)))
        val_rep = CachedValueRepository(ValueRepository(os.path.join(self._storages_path, storage_name)))

        storage = KVStorage.new_storage(ind_rep, val_rep)

        with open(os.path.join(self._storages_path, self._storages_list_name), 'a') as f:
            f.write(storage_name)

        self._storages[storage_name] = storage
