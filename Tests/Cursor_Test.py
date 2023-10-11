import os

import pytest

from Infrastructure.CursorDir.Cursor import Cursor
from ValueStorage.ValueRepository import ValueRepository

value_storage = ValueRepository('', 'test_storage.svl')


@pytest.mark.parametrize(
    "cur_ind, cur_len",
    [
        (-1, 29),
        (0, -1)
    ])
def test_raises_if_bad_cursor(cur_ind, cur_len):
    value = "Hi, my name is Sandre Ayzykin".encode()
    value_storage.add(value)

    with pytest.raises(ValueError):
        value_storage.get(Cursor(cur_ind, cur_len))

    os.remove(value_storage._file_path)
