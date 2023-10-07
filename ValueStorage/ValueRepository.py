from ValueStorage.IValueRepository import IValueRepository
from Compressors.DefaultCompressor import DefaultCompressor
from Infrastructure.CursorDir.Cursor import Cursor


class ValueRepository(IValueRepository):
    def __init__(self, filename: str):
        self.filename = filename
        self.compressor = DefaultCompressor()

    def add(self, value) -> Cursor:
        with open(self.filename, "ab") as f:
            compressed_value = self.compressor.compress(value)
            f.write(compressed_value)

            pointer = Cursor(f.tell() - len(compressed_value),
                             len(compressed_value))

        return pointer

    def get(self, pointer) -> bytes:
        with open(self.filename, "rb") as f:
            f.seek(pointer.index)
            compressed_value = f.read(pointer.len)
            return self.compressor.decompress(compressed_value)
