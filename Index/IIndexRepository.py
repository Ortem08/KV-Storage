from abc import abstractmethod, ABC
from Infrastructure.CursorDir import ICursor


class IIndexRepository(ABC):
    @abstractmethod
    def add(self, key: str, cursor: ICursor) -> bool:
        ...

    @abstractmethod
    def get(self, key) -> ICursor:
        ...
