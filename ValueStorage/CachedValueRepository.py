from Infrastructure.CursorDir.ICursor import ICursor
from ValueStorage.IValueRepository import IValueRepository


class CachedValueRepository(IValueRepository):
    bytes_in_mb = 2 ** 32

    def __init__(self, value_repository: IValueRepository, cache_value_limit_in_mb: int = 1):
        self._value_repository = value_repository
        self._cache_value_limit_in_mb = cache_value_limit_in_mb

        self._cache = {}

    def add(self, value: bytes) -> ICursor:
        cursor = self._value_repository.add(value)
        if self.should_store_in_cache(len(value)):
            self._cache[cursor] = value

        return cursor

    def set(self, value: bytes, old_cursor: ICursor) -> ICursor:
        cursor = self._value_repository.set(value, old_cursor)
        self._cache.pop(old_cursor)
        if self.should_store_in_cache(len(value)):
            self._cache[cursor] = value

        return cursor

    def get(self, pointer: ICursor) -> bytes:
        if self._cache.__contains__(pointer):
            return self._cache[pointer]

        value = self._value_repository.get(pointer)
        if self.should_store_in_cache(len(value)):
            self._cache[pointer] = value
        return value

    def mark_removed(self, old_cursor: ICursor):
        self._value_repository.mark_removed(old_cursor)

    def should_store_in_cache(self, value_len_in_b: int) -> bool:
        return value_len_in_b / CachedValueRepository.bytes_in_mb < self._cache_value_limit_in_mb

    def get_file_paths(self) -> []:
        return self._value_repository.get_file_paths()
