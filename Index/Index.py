import json
import hashlib

from Infrastructure.CursorDir.CursorParser import CursorParser
from Infrastructure.CursorDir.ICursor import ICursor


class Index:
    key_size = 16

    def __init__(self, key: str, cursor: ICursor, left: ICursor, right: ICursor):
        self.key = key
        self.cursor = cursor
        self.left = left
        self.right = right

        self.hash = Index.get_hash(key)

    def to_json(self) -> str:
        return json.dumps({'key': self.key.ljust(Index.key_size, ' '),
                           'cursor': self.cursor.to_json(),
                           'left': self.left.to_json(),
                           'right': self.right.to_json()})

    @staticmethod
    def from_json(str_in_json: str) -> 'Index':
        values = json.loads(str_in_json)
        return Index(
            values['key'].strip(),
            CursorParser.parse(values['cursor']),
            CursorParser.parse(values['left']),
            CursorParser.parse(values['right']))

    @staticmethod
    def get_hash(key: str) -> str:
        hash_evaluator = hashlib.sha256()
        hash_evaluator.update(key.encode())
        return hash_evaluator.hexdigest()

