from abc import ABC, abstractmethod


class ICursor(ABC):
    def __init__(self, cursor_type: str):
        self.type = cursor_type

    @abstractmethod
    def to_json(self) -> bytes:
        ...

    @abstractmethod
    def is_null(self) -> bool:
        ...