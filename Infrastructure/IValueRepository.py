from abc import abstractmethod, ABC
from Pointer import Pointer


class IValueRepository(ABC):
    @abstractmethod
    def add(self, value: bytes) -> Pointer:
        ...

    @abstractmethod
    def get(self, pointer: Pointer) -> bytes:
        ...
