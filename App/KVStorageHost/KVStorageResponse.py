import json


class KVStorageResponse:
    def __init__(self, key: str, value: str, error: str, token: str = None):
        self._token = token
        self._key = key
        self._value = value
        self._error = error

    def to_json(self) -> str:
        return json.dumps({"token": self._token, "key": self._key, "value": self._value, "error": self._error})

    @staticmethod
    def from_json(json_str: str) -> 'KVStorageResponse':
        values = json.loads(json_str)

        return KVStorageResponse(values["token"], values["key"], values["value"], values["error"])

    @staticmethod
    def from_dict(values: {}) -> 'KVStorageResponse':
        return KVStorageResponse(values["token"], values["key"], values["value"], values["error"])
