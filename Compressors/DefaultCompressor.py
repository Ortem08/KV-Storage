import zlib

from Compressors.IValueCompressor import IValueCompressor


class DefaultCompressor(IValueCompressor):
    def __init__(self):
        ...

    def compress(self, byte_array) -> bytes:
        return zlib.compress(byte_array, level=9)

    def decompress(self, byte_array) -> bytes:
        return zlib.decompress(byte_array)
