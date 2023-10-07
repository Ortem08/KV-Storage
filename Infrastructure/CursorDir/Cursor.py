import json
from Infrastructure.CursorDir.ICursor import ICursor


class Cursor(ICursor):
    index_size = 32
    len_size = 16

    def __init__(self, index=0, len=0):
        self._type = 'single'

        self.index = index
        self.len = len

    def to_json(self) -> str:
        return json.dumps(
            {
                'type': self._type,
                'index': str(self.index).rjust(Cursor.index_size, '0'),
                'len': str(self.len).rjust(Cursor.index_size, '0')
            })

    def is_null(self) -> bool:
        return self.index == 0 and self.len == 0
