import os

from Index.CachedIndexRepository import CachedIndexRepository
from Index.IndexRepository import IndexRepository
from KVStorage.IKVStorageProvider import IKVStorageProvider
from KVStorage.KVStorage import KVStorage
from ValueStorage.CachedValueRepository import CachedValueRepository
from ValueStorage.MemoryLimitedValueRepository import MemoryLimitedValueRepository
from ValueStorage.ValueRepository import ValueRepository


class KVStorageProvider(IKVStorageProvider):
    def __init__(self, storages_path: str = 'storages', storages_list_name: str = 'storages_list'):
        self._storages_path = storages_path
        self._storages_list_name = storages_list_name

        self._storages = {}
        with open(os.path.join(self._storages_path, self._storages_list_name), 'r') as f:
            for storage_info in f.readlines():
                particles = [p for p in storage_info.replace('\n', '').split(' ') if p.strip()]
                storage_name = particles[0]
                print(particles)

                ind_rep = CachedIndexRepository(IndexRepository(os.path.join(self._storages_path, storage_name)))
                val_rep = CachedValueRepository(ValueRepository(os.path.join(self._storages_path, storage_name)))
                if len(particles) > 1:
                    val_rep = MemoryLimitedValueRepository(val_rep, int(particles[1]))

                storage = KVStorage(ind_rep, val_rep)
                self._storages[storage_name] = storage

    def get(self, storage_name: str):
        print(storage_name)
        print(self._storages)
        if not self._storages.__contains__(storage_name):
            raise ValueError(f"Unknown storage name [{storage_name}]")

        return self._storages[storage_name]

    def add(self, storage_name: str, storage_type: str, mem_limit: int = 0):
        if self._storages.__contains__(storage_name):
            raise ValueError(f'Storage [{storage_name}] already exists')

        storage_path = os.path.join(self._storages_path, storage_name)
        os.mkdir(storage_path)

        ind_rep = CachedIndexRepository(IndexRepository(storage_path))
        val_rep = CachedValueRepository(ValueRepository(storage_path))

        if storage_type == 'MemoryLimited':
            val_rep = MemoryLimitedValueRepository(val_rep, mem_limit)

        storage = KVStorage.new_storage(ind_rep, val_rep)

        with open(os.path.join(self._storages_path, self._storages_list_name), 'a') as f:
            if storage_type == 'MemoryLimited':
                f.write(f'{storage_name} {mem_limit}\n')
            else:
                f.write(f'{storage_name} \n')

        self._storages[storage_name] = storage
