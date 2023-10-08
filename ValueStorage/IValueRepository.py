from abc import abstractmethod, ABC
from Infrastructure.CursorDir.Cursor import Cursor


class IValueRepository(ABC):
    @abstractmethod
    def add(self, value: bytes) -> Cursor:
        ...

    @abstractmethod
    def set(self, value: bytes, old_cursor: Cursor) -> Cursor:
        ...

    @abstractmethod
    def get(self, pointer: Cursor) -> bytes:
        ...
