from abc import ABC, abstractmethod


class IHost(ABC):
    @abstractmethod
    def run(self):
        ...