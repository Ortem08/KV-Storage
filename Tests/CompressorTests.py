import pytest
from Compressors.DefaultCompressor import DefaultCompressor

compressor = DefaultCompressor()


def test_compress():
    byte_array = 'Hi, my name is Sandre Ayzykin'.encode()
    compressed_data = compressor.compress(byte_array)
    decompressed_data = compressor.decompress(compressed_data)
    assert byte_array == decompressed_data
