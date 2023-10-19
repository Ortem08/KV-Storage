import json

from Infrastructure.CursorDir.ICursor import ICursor


class Cursor(ICursor):
    def __init__(self, index=0, len=0):
        super().__init__('Single')
        if len < 0 or index < 0:
            raise ValueError

        self.index = index
        self.len = len

    def to_json(self) -> str:
        return json.dumps(
            {
                'type': self._type,
                'index': str(self.index),
                'len': str(self.len)
            })

    def is_null(self) -> bool:
        return self.len == 0
