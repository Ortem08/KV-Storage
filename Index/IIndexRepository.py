from abc import abstractmethod, ABC

from Infrastructure.CursorDir import ICursor


class IIndexRepository(ABC):
    @abstractmethod
    def init(self) -> None:
        ...

    @abstractmethod
    def add(self, key: str, cursor: ICursor, ttl: int = -1) -> None:
        ...

    @abstractmethod
    def set(self, key: str, cursor: ICursor) -> None:
        ...

    @abstractmethod
    def get(self, key) -> ICursor:
        ...

    @abstractmethod
    def get_all_keys(self) -> []:
        ...

    @abstractmethod
    def remove(self, key: str) -> ICursor:
        ...
