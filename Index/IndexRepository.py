from Infrastructure.CursorDir.Cursor import Cursor
from Index.Index import Index
from Index.IIndexRepository import IIndexRepository
from Infrastructure.CursorDir import ICursor


class IndexRepository(IIndexRepository):
    def __init__(self, path: str):
        self._path = path
        self._indexes_filename = "indexes"

        self._file_path = path.join([self._path, self._indexes_filename])

    def add(self, key: str, cursor: ICursor):
        ind_to_add = Index(key, cursor, Cursor(), Cursor())
        with open(self._file_path, "a") as f:
            cursor_to_new_index = IndexRepository.append_index(f, ind_to_add)

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
                        IndexRepository.set_index(f, current_index, current_index_str_len)
                        break
                else:
                    if current_index.key == key:
                        raise Exception

                    right_ind = current_index.right
                    if not right_ind.is_null():
                        current_index_str_len, current_index = IndexRepository.get_index(f, right_ind)
                        continue
                    else:
                        current_index.right = cursor_to_new_index
                        IndexRepository.set_index(f, current_index, current_index_str_len)
                        break
        pass

    def get(self, key) -> ICursor:
        ind_to_find = Index(key, Cursor(), Cursor(), Cursor())
        with open(self._file_path, 'r') as f:
            current_index_str = f.readline()
            current_index = Index.from_json(current_index_str)
            while True:
                if current_index.hash > ind_to_find.hash:
                    left_ind = current_index.left
                    if left_ind.is_null():
                        break
                    else:
                        _, current_index = IndexRepository.get_index(f, left_ind)
                        continue
                else:
                    if current_index.key == key:
                        return current_index.cursor

                    right_ind = current_index.right
                    if right_ind.is_null():
                        break
                    else:
                        _, current_index = IndexRepository.get_index(f, right_ind)
                        continue
        return None

    @staticmethod
    def get_index(f, cursor: Cursor):
        f.seek(cursor.index)
        current_index_str = f.read(cursor.len)
        current_index_str_len = len(current_index_str)
        current_index = Index.from_json(current_index_str)
        return current_index_str_len, current_index

    @staticmethod
    def set_index(f, current_index, current_index_str_len):
        f.seek(f.tell() - current_index_str_len)
        f.write(current_index.to_json())
        pass

    @staticmethod
    def append_index(f, ind_to_add: Index):
        ind_json = ind_to_add.to_json()
        f.write(ind_json)

        return Cursor(f.tell() - len(ind_json), len(ind_json))
