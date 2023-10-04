from Compressors.IValueCompressor import IValueCompressor


class DefaultCompressor(IValueCompressor):
    def __init__(self):
        ...

    def compress(self, byte_array) -> bytes:
        return byte_array

    def decompress(self, byte_array) -> bytes:
        return byte_array
