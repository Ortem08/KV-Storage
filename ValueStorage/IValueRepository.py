from abc import abstractmethod, ABC

from Infrastructure.CursorDir.ICursor import ICursor


class IValueRepository(ABC):
    @abstractmethod
    def add(self, value: bytes) -> ICursor:
        ...

    @abstractmethod
    def set(self, value: bytes, old_cursor: ICursor) -> ICursor:
        ...

    @abstractmethod
    def get(self, pointer: ICursor) -> bytes:
        ...

    @abstractmethod
    def mark_removed(self, old_cursor: ICursor):
        ...

    @abstractmethod
    def get_file_paths(self) -> []:
        ...
