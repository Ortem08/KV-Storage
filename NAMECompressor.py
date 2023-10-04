from Infrastructure.IValueCompressor import IValueCompressor


class NAMECompressor(IValueCompressor):
    def __init__(self):
        ...

    def compress(self, byte_array) -> bytes:
        return byte_array

    def decompress(self, byte_array) -> bytes:
        return byte_array
