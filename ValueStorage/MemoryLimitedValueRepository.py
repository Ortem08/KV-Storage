import os.path

from Infrastructure.CursorDir.ICursor import ICursor
from Infrastructure.CursorDir.InMemoryCurosr import InMemoryCursor
from ValueStorage.IValueRepository import IValueRepository


class MemoryLimitedValueRepository(IValueRepository):
    def __init__(self, value_repository: IValueRepository, memory_limit_in_mb: int = 1024):
        self._value_repository = value_repository
        self._memory_limit_in_mb = memory_limit_in_mb

        self._current_memory_consumption = 0
        for file_path in self._value_repository.get_file_paths():
            if os.path.exists(file_path):
                self._current_memory_consumption += os.path.getsize(file_path) / 2 ** 32

        self._in_memory_storage = []

    def add(self, value: bytes) -> ICursor:
        if len(value) / 2 ** 32 + self._current_memory_consumption > self._memory_limit_in_mb:
            self._in_memory_storage.append(value)
            return InMemoryCursor(len(self._in_memory_storage) - 1)

        return self._value_repository.add(value)

    def set(self, value: bytes, old_cursor: ICursor) -> ICursor:
        if old_cursor.type == 'InMemory':
            self._in_memory_storage[old_cursor.index] = value
            return old_cursor

        if len(value) / 2 ** 32 + self._current_memory_consumption > self._memory_limit_in_mb:
            self._in_memory_storage.append(value)
            self._value_repository.mark_removed(old_cursor)
            return InMemoryCursor(len(self._in_memory_storage) - 1)

        return self._value_repository.set(value)

    def get(self, pointer: ICursor) -> bytes:
        if pointer.type == 'InMemory':
            return self._in_memory_storage[pointer.index]

        return self._value_repository.get(pointer)

    def mark_removed(self, old_cursor: ICursor):
        if old_cursor.type == 'InMemory':
            self._in_memory_storage.remove(self._in_memory_storage[old_cursor.index])
            return
        self._value_repository.mark_removed(old_cursor)

    def get_file_paths(self) -> []:
        return self._value_repository.get_file_paths()
