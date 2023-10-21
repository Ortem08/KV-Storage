import os
import uuid

from Index.CachedIndexRepository import CachedIndexRepository
from Index.IndexRepository import IndexRepository
from Infrastructure.CursorDir.Cursor import Cursor

test_folder = 'CachedIndexRepository_Tests_Folder'


def assert_cursors(actual: Cursor, expected: Cursor):
    assert actual.len == expected.len
    assert actual.index == expected.index


def generate_test_file_name() -> str:
    return str(uuid.uuid4())


def test_add_should_be_added_to_cache():
    rep = IndexRepository(test_folder, generate_test_file_name())
    cached_rep = CachedIndexRepository(rep)
    cached_rep.init()

    cached_rep.add("key", Cursor(1, 12))

    os.remove(rep._file_path)

    assert cached_rep._cache.__contains__("key")
    assert_cursors(cached_rep._cache["key"], Cursor(1, 12))


def test_set_should_be_changed_in_cache():
    rep = IndexRepository(test_folder, generate_test_file_name())
    cached_rep = CachedIndexRepository(rep)
    cached_rep.init()

    cached_rep.add("key", Cursor(1, 12))
    cached_rep.set("key", Cursor(2, 23))

    os.remove(rep._file_path)

    assert cached_rep._cache.__contains__("key")
    assert_cursors(cached_rep._cache["key"], Cursor(2, 23))


def test_get_should_add_to_cache():
    rep = IndexRepository(test_folder, generate_test_file_name())
    cached_rep = CachedIndexRepository(rep)
    cached_rep.init()

    cached_rep.add("key", Cursor(1, 12))

    cached_rep._cache.pop("key")
    assert not cached_rep._cache.__contains__("key")

    cached_rep.get("key")

    os.remove(rep._file_path)

    assert cached_rep._cache.__contains__("key")
    assert_cursors(cached_rep._cache["key"], Cursor(1, 12))


def test_get_should_get_from_cache():
    rep = IndexRepository(test_folder, generate_test_file_name())
    cached_rep = CachedIndexRepository(rep)
    cached_rep.init()

    cached_rep.add("key", Cursor(1, 12))

    cached_rep._cache["key"] = Cursor(2, 23)

    os.remove(rep._file_path)

    assert cached_rep._cache.__contains__("key")
    assert_cursors(cached_rep._cache["key"], Cursor(2, 23))