import os

import pytest

from ValueStorage.MemoryLimitedValueRepository import MemoryLimitedValueRepository
from ValueStorage.ValueRepository import ValueRepository


def test_store_in_file_get_should_return_correctly():
    value_storage = MemoryLimitedValueRepository(ValueRepository('', 'test_storage.svl'), 1 / (2 ** 31))
    cursor = value_storage.add('1'.encode('UTF-8'))

    file_exists = os.path.exists(value_storage.get_file_paths()[0])
    value = value_storage.get(cursor)
    os.remove(value_storage.get_file_paths()[0])
    assert file_exists
    assert value == b'1'


def test_store_in_memory_get_should_return_correctly():
    value_storage = MemoryLimitedValueRepository(ValueRepository('', 'test_storage.svl'), 1 / (2 ** 31))
    cursor = value_storage.add('123123123'.encode('UTF-8'))

    assert not os.path.exists(value_storage.get_file_paths()[0])
    assert value_storage.get(cursor) == b'123123123'