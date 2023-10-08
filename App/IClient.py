from abc import ABC, abstractmethod


class IClient(ABC):
    @abstractmethod
    def new(self, path: str, storage_name: str) -> None:
        ...

    @abstractmethod
    def add(self, value: str, storage_name: str) -> None:
        ...

    @abstractmethod
    def set(self, key: str, value: str, storage_name: str) -> None:
        ...

    @abstractmethod
    def get(self, key: str, storage_name: str) -> str:
        ...
