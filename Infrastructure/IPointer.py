from abc import ABC, abstractmethod


class IPointer(ABC):
    @abstractmethod
    def to_byte_array(self) -> bytes:
        ...

    @abstractmethod
    def from_byte_array(self, byte_array: bytes) -> 'IPointer':
        ...
