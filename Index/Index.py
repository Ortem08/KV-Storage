import json
import hashlib

from Infrastructure.CursorDir.CursorParser import CursorParser
from Infrastructure.CursorDir.ICursor import ICursor


class Index:
    key_len = 16
    hash_len = 16

    def __init__(self, key: str, cursor: ICursor, left: ICursor, right: ICursor):
        self.key = key
        self.cursor = cursor
        self.left = left
        self.right = right

        hash_evaluator = hashlib.sha256()
        hash_evaluator.update(self.key.encode())
        self.hash = hash_evaluator.hexdigest()

    def to_json(self) -> str:
        return json.dumps({'key': self.key.ljust(Index.key_len, ' '),
                           'hash': self.hash,
                           'cursor': self.cursor.to_json(),
                           'left': self.left.to_json(),
                           'right': self.right.to_json()})

    @staticmethod
    def from_json(str_in_json: str):
        values = json.loads(str_in_json)
        return Index(
            values['key'].strip(),
            CursorParser.parse(values['cursor']),
            CursorParser.parse(values['left']),
            CursorParser.parse(values['right']))
