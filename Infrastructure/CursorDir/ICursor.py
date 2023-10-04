from abc import ABC, abstractmethod


class ICursor(ABC):
    @abstractmethod
    def to_json(self) -> bytes:
        ...

    @abstractmethod
    def is_null(self) -> bool:
        ...