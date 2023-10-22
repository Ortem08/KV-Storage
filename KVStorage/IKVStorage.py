from abc import ABC, abstractmethod

from Index.IIndexRepository import IIndexRepository
from ValueStorage.IValueRepository import IValueRepository


class IKVStorage(ABC):
    @staticmethod
    @abstractmethod
    def new_storage(
            index_repository: IIndexRepository,
            value_repository: IValueRepository) -> 'IKVStorage':
        ...

    @abstractmethod
    def add(self, key: str, value: str, ttl: int = -1) -> None:
        ...

    @abstractmethod
    def set(self, key: str, value: str) -> None:
        ...

    @abstractmethod
    def get(self, key: str) -> str:
        ...

    @abstractmethod
    def get_all_keys(self) -> []:
        ...
