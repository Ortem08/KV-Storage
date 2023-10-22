from Index.IIndexRepository import IIndexRepository
from Infrastructure.CursorDir import ICursor


class CachedIndexRepository(IIndexRepository):
    def __init__(self, index_repository: IIndexRepository):
        self._repository = index_repository
        self._cache = {}

    def init(self) -> None:
        self._repository.init()

    def add(self, key: str, cursor: ICursor, ttl: int = -1) -> None:
        self._repository.add(key, cursor, ttl)

        if ttl == -1:
            self._cache[key] = cursor
        pass

    def set(self, key: str, cursor: ICursor) -> None:
        if not self._cache.__contains__(key) or not self._cache[key] == cursor:
            self._repository.set(key, cursor)
            self._cache[key] = cursor
        pass

    def get(self, key) -> ICursor:
        if self._cache.__contains__(key):
            return self._cache[key]

        cursor = self._repository.get(key)
        if cursor is not None:
            self._cache[key] = cursor
        return cursor

    def get_all_keys(self) -> []:
        for key in self._repository.get_all_keys():
            yield key
