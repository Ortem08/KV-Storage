from abc import ABC, abstractmethod


class IValueCompressor(ABC):
    @abstractmethod
    def compress(self, byte_array: bytes) -> bytes:
        ...

    @abstractmethod
    def decompress(self, byte_array: bytes) -> bytes:
        ...
