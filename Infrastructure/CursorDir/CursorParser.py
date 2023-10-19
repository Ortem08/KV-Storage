import json

from Infrastructure.CursorDir.Cursor import Cursor
from Infrastructure.CursorDir.ICursor import ICursor


class CursorParser:
    @staticmethod
    def parse(str_in_json: str) -> ICursor:
        values = json.loads(str_in_json)
        if values['type'] == 'Single':
            return Cursor(int(values['index']), int(values['len']))
