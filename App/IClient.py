from abc import ABC, abstractmethod


class IClient(ABC):
    @abstractmethod
    def new(self, path: str, storage_name: str, storage_type: str, mem_limit: int = 0) -> None:
        ...

    @abstractmethod
    def add(self, storage_name: str, key: str, value: str) -> None:
        ...

    @abstractmethod
    def set(self, storage_name: str, key: str, value: str) -> None:
        ...

    @abstractmethod
    def get(self, storage_name: str, key: str) -> str:
        ...
