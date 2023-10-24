import os
import queue
from datetime import datetime
from typing import TextIO

from InMemoryLog import InMemoryLog
from Index.Index import Index
from Infrastructure.CursorDir.Cursor import Cursor
from Infrastructure.CursorDir.ICursor import ICursor


class IndexTreeNode:
    def __init__(self, index: Index, cursor: Cursor):
        self.index = index
        self.cursor = cursor
        self.hash = index.hash

    def right(self, f: TextIO):
        right_ind = self.index.right
        if not right_ind.is_null():
            return IndexTreeNode.__read__(f, right_ind)
        else:
            return None

    def left(self, f: TextIO):
        left_ind = self.index.left
        if not left_ind.is_null():
            return IndexTreeNode.__read__(f, left_ind)
        else:
            return None

    def set_left(self, f: TextIO, cursor: Cursor):
        self.index.left = cursor
        self.__change__(f)

    def set_right(self, f: TextIO, cursor: Cursor):
        self.index.right = cursor
        self.__change__(f)

    def set_index_value_cursor(self, f: TextIO, cursor: Cursor):
        self.index.cursor = cursor
        self.__change__(f)

    @staticmethod
    def __read__(f: TextIO, to_read: Cursor):
        f.seek(to_read.index)
        current_index_str = f.read(to_read.len)
        index = Index.from_json(current_index_str.strip())
        return IndexTreeNode(index, to_read)

    def __change__(self, f: TextIO):
        f.seek(self.cursor.index)
        f.write(self.index.to_json().ljust(self.cursor.len))


class IndexTree:
    def __init__(self, path: str, indexes_filename: str = "indexes", max_index_size_in_bytes: int = 512):
        self._file_path = os.path.join(path, indexes_filename)
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
        with open(self._file_path, 'r+') as f:
            current_node = IndexTree.__get_root_node__(f)
            while True:
                if current_node.hash > ind_to_add.hash:
                    left_node = current_node.left(f)
                    if left_node is None:
                        f.close()

                        new_node = self.__add_new_node__(ind_to_add)
                        with open(self._file_path, 'r+') as f_to_append:
                            current_node.set_left(f_to_append, new_node.cursor)
                        break
                    else:
                        current_node = left_node
                        continue
                else:
                    if current_node.index.key == key:
                        raise KeyError

                    right_node = current_node.right(f)
                    if right_node is None:
                        f.close()

                        new_node = self.__add_new_node__(ind_to_add)
                        with open(self._file_path, 'r+') as f_to_append:
                            current_node.set_right(f_to_append, new_node.cursor)
                        break
                    else:
                        current_node = right_node
                        continue

    def set(self, key: str, cursor: ICursor) -> None:
        with open(self._file_path, 'r+') as f:
            _, to_set, _ = IndexTree.__find_node__(f, key)
            if to_set is None:
                raise KeyError(f'Key [{key}] not found')
            if (to_set.index.expires_at is not None) and (to_set.index.expires_at < datetime.now()):
                InMemoryLog.info(f'Key [{key}] expired at [{to_set.index.expires_at}]')
                return
            to_set.set_index_value_cursor(f, cursor)

    def get(self, key: str) -> Index:
        with open(self._file_path, 'r+') as f:
            _, to_return, _ = IndexTree.__find_node__(f, key)
            if to_return is None:
                return None
            if (to_return.index.expires_at is not None) and (to_return.index.expires_at < datetime.now()):
                InMemoryLog.info(f'Key [{key}] expired at [{to_return.index.expires_at}]')
                return None
            return to_return.index

    def get_all_keys(self) -> []:
        with open(self._file_path, 'r+') as f:
            current_node = IndexTree.__get_root_node__(f)
            to_opens = queue.Queue()
            to_opens.put(current_node.left(f))
            to_opens.put(current_node.right(f))

            while to_opens.qsize() > 0:
                current_node = to_opens.get()
                if current_node is None:
                    continue

                yield current_node.index.key
                to_opens.put(current_node.left(f))
                to_opens.put(current_node.right(f))

    def remove(self, key: str) -> Index:
        with open(self._file_path, 'r+') as f:
            to_change, to_remove, is_right = IndexTree.__find_node__(f, key)

            if to_remove is None:
                raise KeyError(f'Key [{key}] not found')

            to_remove_left = to_remove.left(f)
            to_remove_right = to_remove.right(f)
            if to_remove_left is None and to_remove_right is None:
                IndexTree.__set_to_child__(f, to_change, is_right, Cursor(0, 0))
            elif to_remove_left is None:
                IndexTree.__set_to_child__(f, to_change, is_right, to_remove_right.cursor)
            elif to_remove_right is None:
                IndexTree.__set_to_child__(f, to_change, is_right, to_remove_left.cursor)
            else:
                previous = to_remove
                current = to_remove_right
                current_left = current.left(f)
                while current_left is not None:
                    previous = current
                    current = current_left
                    current_left = current.left(f)

                to_set_to_previous = Cursor(0, 0)
                current_right = current.right(f)
                if current_right is not None:
                    to_set_to_previous = current_right.cursor

                previous.set_left(f, to_set_to_previous)
                IndexTree.__set_to_child__(f, to_change, is_right, current.cursor)
                current.set_left(f, to_remove_left.cursor)
                current.set_right(f, to_remove_right.cursor)

            return to_remove.index

    @staticmethod
    def __set_to_child__(f: TextIO, to_change: IndexTreeNode, is_right: bool, cursor: Cursor):
        if is_right:
            to_change.set_right(f, cursor)
        else:
            to_change.set_left(f, cursor)

    @staticmethod
    def __find_node__(f: TextIO, key: str) -> (IndexTreeNode, IndexTreeNode, bool):
        current_node = IndexTree.__get_root_node__(f)
        prev_node = None

        is_right = False
        key_hash = Index.get_hash(key)
        while True:
            if current_node.hash > key_hash:
                left_node = current_node.left(f)
                if left_node is None:
                    return (None, None, None)
                else:
                    prev_node = current_node
                    current_node = left_node
                    is_right = False
                    continue
            else:
                if current_node.index.key == key:
                    return prev_node, current_node, is_right

                right_ind = current_node.right(f)
                if right_ind is None:
                    return (None, None, None)
                else:
                    prev_node = current_node
                    current_node = right_ind
                    is_right = True
                    continue

    @staticmethod
    def __get_root_node__(f: TextIO) -> IndexTreeNode:
        root_index_str = f.readline()
        root_index = Index.from_json(root_index_str)
        return IndexTreeNode(root_index, Cursor(0, len(root_index_str) - 1))

    def __add_new_node__(self, ind_to_add: Index) -> IndexTreeNode:
        ind_json = ind_to_add.to_json().ljust(self._max_index_size_in_bytes)
        with open(self._file_path, "a") as f:
            f.write(ind_json)
            return IndexTreeNode(ind_to_add, Cursor(f.tell() - len(ind_json), len(ind_json)))
