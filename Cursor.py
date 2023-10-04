from Infrastructure.ICursor import ICursor


class Cursor(ICursor):
    def __init__(self, index=0, len=0):
        self.index = index
        self.len = len

    def to_byte_array(self) -> bytes:
        ...

    def from_byte_array(self, byte_array) -> ICursor:
        ...
