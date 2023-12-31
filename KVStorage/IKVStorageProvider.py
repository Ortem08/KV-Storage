from abc import ABC, abstractmethod


class IKVStorageProvider(ABC):
    @abstractmethod
    def get(self, storage_name: str):
        ...

    @abstractmethod
    def add(self, storage_name: str, storage_type: str, mem_limit: int = 0):
        ...
