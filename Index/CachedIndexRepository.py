from Index.IIndexRepository import IIndexRepository
from Infrastructure.CursorDir import ICursor


class CachedIndexRepository(IIndexRepository):
    def __init__(self, index_repository: IIndexRepository):
        self.repository = index_repository
        self.cache = {}

    def add(self, key: str, cursor: ICursor) -> None:
        self.repository.add(key, cursor)

        self.cache[key] = cursor
        pass

    def set(self, key: str, cursor: ICursor) -> None:
        if not self.cache.__contains__(key) or not self.cache[key] == cursor:
            self.repository.set(key, cursor)
            self.cache[key] = cursor
        pass

    def get(self, key) -> ICursor:
        if self.cache.__contains__(key):
            return self.cache[key]

        cursor = self.repository.get(key)
        self.cache[key] = cursor
        return cursor
