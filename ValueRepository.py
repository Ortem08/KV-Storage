from Infrastructure.IValueRepository import IValueRepository
from NAMECompressor import NAMECompressor
from Pointer import Pointer
import datetime


class ValueRepository(IValueRepository):
    def __init__(self, filename: str):
        self.filename = filename
        self.pointer = Pointer()
        self.compressor = NAMECompressor()

    def add(self, value) -> Pointer:
        with open(self.filename, "ab") as f:
            compressed_value = self.compressor.compress(value)
            f.write(compressed_value)
            self.pointer.last_len = len(compressed_value)
            self.pointer.index = f.tell() - self.pointer.last_len

        return self.pointer

    def get(self, pointer) -> bytes:
        with open(self.filename, "rb") as f:
            f.seek(pointer.index)
            compressed_value = f.read(pointer.last_len)
            return self.compressor.decompress(compressed_value)
