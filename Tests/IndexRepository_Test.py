import os.path
import uuid

from Index.IndexRepository import IndexRepository
from Infrastructure.CursorDir.Cursor import Cursor

test_folder = 'IndexRepository_Tests_Folder'


def assert_files(actual: str, expected: str):
    with open(actual, 'r') as f:
        lines_actual = f.readlines()
    os.remove(actual)

    with open(expected) as f:
        lines_expected = f.readlines()

    assert len(lines_actual) == len(lines_expected)
    for i in range(len(lines_actual)):
        assert lines_actual[i] == lines_expected[i]


def assert_cursors(actual: Cursor, expected: Cursor):
    assert actual.len == expected.len
    assert actual.index == expected.index


def generate_test_file_name() -> str:
    return str(uuid.uuid4())


def test_add():
    rep = IndexRepository(test_folder, generate_test_file_name())
    rep.init()

    rep.add("key1", Cursor(1, 1))
    rep.add("key2", Cursor(2, 2))
    rep.add("key3", Cursor(3, 3))
    rep.add("key4", Cursor(4, 4))

    assert_files(rep._file_path, os.path.join(test_folder, 'test_add_expected'))


def test_set():
    rep = IndexRepository(test_folder, generate_test_file_name())
    rep.init()

    rep.add("key1", Cursor(1, 1))
    rep.add("key2", Cursor(2, 2))
    rep.add("key3", Cursor(3, 3))
    rep.add("key4", Cursor(4, 4))

    rep.set("key2", Cursor(22, 22))

    assert_files(rep._file_path, os.path.join(test_folder, 'test_set_expected'))


def test_get():
    rep = IndexRepository(test_folder, 'test_get_file')

    assert_cursors(rep.get('root_index'), Cursor(0, 0))

    assert_cursors(rep.get('key1'), Cursor(1, 1))
    assert_cursors(rep.get('key2'), Cursor(2, 2))
    assert_cursors(rep.get('key3'), Cursor(3, 3))
    assert_cursors(rep.get('key4'), Cursor(4, 4))




