import os

from Index.IIndexRepository import IIndexRepository
from Index.IndexTree import IndexTree
from Infrastructure.CursorDir import ICursor


class IndexRepository(IIndexRepository):
    def __init__(self, path: str, indexes_filename: str = "indexes", max_index_size_in_bytes: int = 512):
        self._file_path = os.path.join(path, indexes_filename)

        self._index_tree = IndexTree(path, indexes_filename, max_index_size_in_bytes)

    def init(self) -> None:
        self._index_tree.init()

    def add(self, key: str, cursor: ICursor, ttl: int = -1) -> None:
        self._index_tree.add(key, cursor, ttl)

    def set(self, key: str, cursor: ICursor) -> None:
        self._index_tree.set(key, cursor)

    def get(self, key) -> ICursor:
        index_got = self._index_tree.get(key)
        if index_got is None:
            return None
        return index_got.cursor

    def get_all_keys(self) -> []:
        return self._index_tree.get_all_keys()

    def remove(self, key: str) -> ICursor:
        return self._index_tree.remove(key).cursor
