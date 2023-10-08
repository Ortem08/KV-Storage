import os

from Compressors.DefaultCompressor import DefaultCompressor
from Infrastructure.CursorDir.Cursor import Cursor
from ValueStorage.IValueRepository import IValueRepository


class ValueRepository(IValueRepository):
    def __init__(self, path: str, filename='storage.svl'):
        self._path = path
        self._filename = filename
        self._unused_cursor_name = 'unused.crs'
        self._file_path = os.path.join(self._path, self._filename)
        self._unused_cursor_path = os.path.join(self._path, self._unused_cursor_name)

        self.compressor = DefaultCompressor()

    def add(self, value) -> Cursor:
        with open(self._file_path, "ab") as f:
            compressed_value = self.compressor.compress(value)
            f.write(compressed_value)

            cursor = Cursor(f.tell() - len(compressed_value),
                            len(compressed_value))

        return cursor

    def set(self, value, old_cursor) -> Cursor:
        with open(self._unused_cursor_path, 'a') as u:
            u.write(old_cursor.to_json() + '\n')

        return self.add(value)

    def get(self, cursor) -> bytes:
        with open(self._file_path, "rb") as f:
            f.seek(cursor.index)
            compressed_value = f.read(cursor.len)
            return self.compressor.decompress(compressed_value)
