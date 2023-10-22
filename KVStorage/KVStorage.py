from InMemoryLog import InMemoryLog
from Index.IIndexRepository import IIndexRepository
from KVStorage.IKVStorage import IKVStorage
from ValueStorage.IValueRepository import IValueRepository


class KVStorage(IKVStorage):
    def __init__(
            self,
            index_repository: IIndexRepository,
            value_repository: IValueRepository):

        self._index_repository = index_repository
        self._value_repository = value_repository
        self._in_memory_context = {}

    @staticmethod
    def new_storage(
            index_repository: IIndexRepository,
            value_repository: IValueRepository):
        index_repository.init()
        return KVStorage(index_repository, value_repository)

    def add(self, key: str, value: str) -> None:
        cursor = self._value_repository.add(value.encode('UTF-8'))

        if cursor.type == 'InMemory':
            self._in_memory_context[key] = cursor
            InMemoryLog.info(f"Storage memory {self._value_repository._memory_limit_in_mb} overflowed. "
                             f"Value with key {key} was added to memory. "
                             f"It will be lost with shutdown.")
            return
        self._index_repository.add(key, cursor)

    def set(self, key: str, value: str) -> None:
        if key in self._in_memory_context.keys():
            old_cursor = self._in_memory_context[key]
            cursor = self._value_repository.set(value.encode('UTF-8'), old_cursor)
            self._in_memory_context[key] = cursor
        else:
            old_cursor = self._index_repository.get(key)
            cursor = self._value_repository.set(value.encode('UTF-8'), old_cursor)
            self._index_repository.set(key, cursor)

    def get(self, key: str) -> str:
        if key in self._in_memory_context.keys():
            cursor = self._in_memory_context[key]
        else:
            cursor = self._index_repository.get(key)

        if cursor is None:
            raise Exception(f'Key not found [{key}]')

        return self._value_repository.get(cursor).decode('UTF-8')

    def get_all_keys(self) -> []:
        keys = [key for key in self._index_repository.get_all_keys()]
        return keys
