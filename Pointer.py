from Infrastructure.IPointer import IPointer


class Pointer(IPointer):
    def __init__(self):
        self.index = 0
        self.last_len = 0

    def to_byte_array(self) -> bytes:
        ...

    def from_byte_array(self, byte_array) -> IPointer:
        ...
