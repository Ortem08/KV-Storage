import hashlib
import json
from datetime import datetime, timedelta

from Infrastructure.CursorDir.CursorParser import CursorParser
from Infrastructure.CursorDir.ICursor import ICursor


class Index:
    def __init__(self, key: str, cursor: ICursor, left: ICursor, right: ICursor, ttl: int = -1):
        self.key = key
        self.cursor = cursor
        self.left = left
        self.right = right

        self.expires_at = None
        if ttl != -1:
            self.expires_at = datetime.now() + timedelta(0, ttl)

        self.hash = Index.get_hash(key)

    def to_json(self) -> str:
        expires_at = 'infinite'
        if self.expires_at is not None:
            expires_at = self.expires_at.strftime("%m/%d/%Y, %H:%M:%S")

        return json.dumps({'key': self.key,
                           'cursor': self.cursor.to_json(),
                           'left': self.left.to_json(),
                           'right': self.right.to_json(),
                           'expires': expires_at})

    @staticmethod
    def from_json(str_in_json: str) -> 'Index':
        values = json.loads(str_in_json)
        index = Index(
            values['key'].strip(),
            CursorParser.parse(values['cursor']),
            CursorParser.parse(values['left']),
            CursorParser.parse(values['right']))
        if values['expires'] == 'infinite':
            index.expires_at = None
        else:
            index.expires_at = datetime.strptime(values['expires'], "%m/%d/%Y, %H:%M:%S")

        return index

    @staticmethod
    def get_hash(key: str) -> str:
        hash_evaluator = hashlib.sha256()
        hash_evaluator.update(key.encode())
        return hash_evaluator.hexdigest()
