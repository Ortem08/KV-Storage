import json


class KVStorageResponse:
    def __init__(self, key: str, value: str, error: str):
        self._key = key
        self._value = value
        self._error = error

    def to_json(self) -> str:
        return json.dumps({"key": self._key, "value": self._value, "error": self._error})

    @staticmethod
    def from_json(json_str: str) -> 'KVStorageResponse':
        values = json.loads(json_str)

        return KVStorageResponse(values["key"], values["value"], values["error"])

    @staticmethod
    def from_dict(values: {}) -> 'KVStorageResponse':
        return KVStorageResponse(values["key"], values["value"], values["error"])
