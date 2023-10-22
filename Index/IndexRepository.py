import datetime
import os
import queue

from InMemoryLog import InMemoryLog
from Index.IIndexRepository import IIndexRepository
from Index.Index import Index
from Infrastructure.CursorDir import ICursor
from Infrastructure.CursorDir.Cursor import Cursor


class IndexRepository(IIndexRepository):
    def __init__(self, path: str, indexes_filename: str = "indexes", max_index_size_in_bytes: int = 512):
        self._path = path
        self._indexes_filename = indexes_filename

        self._file_path = os.path.join(self._path, self._indexes_filename)
        self._max_index_size_in_bytes = max_index_size_in_bytes

    def init(self) -> None:
        if os.path.exists(self._file_path):
            raise Exception('IndexRepository is already initiated')

        with open(self._file_path, 'w') as f:
            f.writelines(
                Index(
                    'root_index',
                    Cursor(0, 0),
                    Cursor(0, 0),
                    Cursor(0, 0))
                .to_json().ljust(self._max_index_size_in_bytes))
            f.write('\n')

    def add(self, key: str, cursor: ICursor, ttl: int = -1) -> None:
        ind_to_add = Index(key, cursor, Cursor(), Cursor(), ttl)
        with open(self._file_path, "a") as f:
            cursor_to_new_index = self.write_index(f, ind_to_add)

        with open(self._file_path, 'r+') as f:
            current_index_str = f.readline()
            current_index_str_len = len(current_index_str) + 1
            current_index = Index.from_json(current_index_str)
            while True:
                if current_index.hash > ind_to_add.hash:
                    left_ind = current_index.left
                    if not left_ind.is_null():
                        current_index_str_len, current_index = IndexRepository.get_index(f, left_ind)
                        continue
                    else:
                        current_index.left = cursor_to_new_index
                        self.set_index(f, current_index, current_index_str_len)
                        break
                else:
                    if current_index.key == key:
                        raise KeyError

                    right_ind = current_index.right
                    if not right_ind.is_null():
                        current_index_str_len, current_index = IndexRepository.get_index(f, right_ind)
                        continue
                    else:
                        current_index.right = cursor_to_new_index
                        self.set_index(f, current_index, current_index_str_len)
                        break
        pass

    def set(self, key: str, cursor: ICursor) -> None:
        key_hash = Index.get_hash(key)
        with open(self._file_path, 'r+') as f:
            root_index_str = f.readline()
            current_index_str_len = len(root_index_str) + 1
            current_index = Index.from_json(root_index_str)
            while True:
                if current_index.hash > key_hash:
                    left_ind = current_index.left
                    if left_ind.is_null():
                        break
                    else:
                        current_index_str_len, current_index = IndexRepository.get_index(f, left_ind)
                        continue
                else:
                    if current_index.key == key:
                        if current_index.expires_at is not None and current_index.expires_at < datetime.datetime.now():
                            InMemoryLog.info(f'Key [{key}] expired at [{current_index.expires_at}]')
                            return
                        self.set_index(
                            f,
                            Index(key, cursor, current_index.left, current_index.right),
                            current_index_str_len)
                        pass

                    right_ind = current_index.right
                    if right_ind.is_null():
                        break
                    else:
                        current_index_str_len, current_index = IndexRepository.get_index(f, right_ind)
                        continue
        return None

    def get(self, key) -> ICursor:
        key_hash = Index.get_hash(key)
        with open(self._file_path, 'r') as f:
            current_index_str = f.readline()
            current_index = Index.from_json(current_index_str)
            while True:
                if current_index.hash > key_hash:
                    left_ind = current_index.left
                    if left_ind.is_null():
                        break
                    else:
                        _, current_index = IndexRepository.get_index(f, left_ind)
                        continue
                else:
                    if current_index.key == key:
                        if current_index.expires_at is not None and current_index.expires_at < datetime.datetime.now():
                            InMemoryLog.info(f'Key [{key}] expired at [{current_index.expires_at}]')
                            return None
                        return current_index.cursor

                    right_ind = current_index.right
                    if right_ind.is_null():
                        break
                    else:
                        _, current_index = IndexRepository.get_index(f, right_ind)
                        continue
        return None

    def get_all_keys(self) -> []:
        with open(self._file_path, 'r') as f:
            current_index_str = f.readline()
            current_index = Index.from_json(current_index_str)
            to_open = queue.Queue()
            if not current_index.left.is_null():
                to_open.put(current_index.left)
            if not current_index.right.is_null():
                to_open.put(current_index.right)

            while to_open.qsize() > 0:
                _, current_index = IndexRepository.get_index(f, to_open.get())
                yield current_index.key

                if not current_index.left.is_null():
                    to_open.put(current_index.left)
                if not current_index.right.is_null():
                    to_open.put(current_index.right)
        return None

    @staticmethod
    def get_index(f, cursor: Cursor) -> (int, Index):
        f.seek(cursor.index)
        current_index_str = f.read(cursor.len)
        current_index = Index.from_json(current_index_str.strip())
        return cursor.len, current_index

    def set_index(self, f, current_index, current_index_str_len):
        f.seek(f.tell() - current_index_str_len)
        f.write(current_index.to_json())
        pass

    def write_index(self, f, ind_to_add: Index) -> Cursor:
        ind_json = ind_to_add.to_json().ljust(self._max_index_size_in_bytes)
        f.write(ind_json)

        return Cursor(f.tell() - len(ind_json), len(ind_json))
