import os
import pytest
from Infrastructure.CursorDir.Cursor import Cursor
from ValueStorage.ValueRepository import ValueRepository

value_storage = ValueRepository('', 'test_storage.svl')


@pytest.mark.parametrize(
    "str_value",
    [
        "Hi, my name is Sandre Ayzykin",
        "Привет, меня зовут Сандрй Айзыки123",
        ""
    ])
def test_add(str_value):
    value = str_value.encode()
    actual_cursor = value_storage.add(value)
    with open('test_storage.svl', 'r') as f:
        file_len = len(f.read())

    assert actual_cursor.len == file_len
    assert actual_cursor.index == 0
    os.remove(value_storage._file_path)


@pytest.mark.parametrize(
    "str_value",
    [
        "Hi, my name is Sandre Ayzykin",
        "Привет, меня зовут Сандрй Айзыки123",
        ""
    ])
def test_get_returns_same_what_added(str_value):
    value = str_value.encode()
    cursor = value_storage.add(value)

    actual_value = value_storage.get(cursor)
    assert actual_value == value
    os.remove(value_storage._file_path)


@pytest.mark.parametrize(
    "cur_ind, cur_len",
    [
        # (0, 30), хз как узнать длину файла
        # (5, 29),
        (-1, 29),
        (0, -1)
    ])
def test_raises_if_bad_cursor(cur_ind, cur_len):
    value = "Hi, my name is Sandre Ayzykin".encode()
    value_storage.add(value)

    with pytest.raises(ValueError):
        value_storage.get(Cursor(cur_ind, cur_len))

    os.remove(value_storage._file_path)


def test_get_by_cursor():
    value1 = "Hi, my name is Sandre Ayzykin".encode()
    value2 = "Привет, меня зовут Сандрй Айзыки123".encode()
    value3 = "wassUp".encode()
    cur1 = value_storage.add(value1)
    cur2 = value_storage.add(value2)
    cur3 = value_storage.add(value3)

    actual1 = value_storage.get(cur1)
    actual3 = value_storage.get(cur3)
    actual2 = value_storage.get(cur2)

    assert actual1 == value1
    assert actual2 == value2
    assert actual3 == value3

    os.remove(value_storage._file_path)


def test_set():
    value = "Hi, my name is Sandre Ayzykin".encode()
    old_cursor = value_storage.add(value)
    new_value = "Привет, меня зовут Сандрй Айзыки123".encode()
    new_cursor = value_storage.set(new_value, old_cursor)

    with open('unused.crs', 'r') as f:
        cursor_json = f.read().strip()

    assert cursor_json == old_cursor.to_json()
    assert new_value == value_storage.get(new_cursor)

    os.remove(value_storage._file_path)
    os.remove(value_storage._unused_cursor_path)
