import os.path
import time
import uuid

from InMemoryLog import InMemoryLog
from Index.IndexRepository import IndexRepository
from Infrastructure.CursorDir.Cursor import Cursor

test_folder = 'Tests/IndexRepository_Tests_Folder'


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


def test_get_all_keys():
    file_name = generate_test_file_name()
    rep = IndexRepository(test_folder, file_name)
    rep.init()

    rep.add("key1", Cursor(1, 1))
    rep.add("key2", Cursor(2, 2))
    rep.add("key3", Cursor(3, 3))
    rep.add("key4", Cursor(4, 4))

    t = {'key1', 'key2', 'key3', 'key4'}
    for key in rep.get_all_keys():
        t.remove(key)

    os.remove(os.path.join(test_folder, file_name))

    assert len(t) == 0


def test_ttl():
    file_name = generate_test_file_name()
    rep = IndexRepository(test_folder, file_name)
    rep.init()

    rep.add("key1", Cursor(1, 1), 1)
    rep.add("key2", Cursor(2, 2), 100)
    rep.add("key3", Cursor(3, 3), 2)
    rep.add("key4", Cursor(4, 4), 100)

    time.sleep(5)

    assert rep.get("key1") is None
    assert len(InMemoryLog.read_new()) != 0
    assert_cursors(rep.get("key2"), Cursor(2, 2))
    assert rep.get("key3") is None
    assert len(InMemoryLog.read_new()) != 0
    assert_cursors(rep.get("key4"), Cursor(4, 4))

    os.remove(os.path.join(test_folder, file_name))


def test_remove():
    file_name = generate_test_file_name()
    rep = IndexRepository(test_folder, file_name)
    rep.init()

    rep.add("key1", Cursor(1, 1))
    rep.add("key2", Cursor(2, 2))
    rep.add("key3", Cursor(3, 3))
    rep.add("key4", Cursor(4, 4))

    rep.remove("key2")

    assert rep.get("key2") is None

    assert_cursors(rep.get('key1'), Cursor(1, 1))
    assert_cursors(rep.get('key3'), Cursor(3, 3))
    assert_cursors(rep.get('key4'), Cursor(4, 4))

    os.remove(os.path.join(test_folder, file_name))
