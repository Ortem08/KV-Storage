import datetime
import json
from json import JSONEncoder

import jwt


class Token:
    SECRET_KEY = 'VERYSECRET'

    def __init__(self, current_token):
        self.token = current_token

    @staticmethod
    def create_token(login: str, password: str) -> 'Token':
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)

        payload = {
            'login': login,
            'password': password,
            'expiration_date': expiration_date
        }

        token = jwt.encode(payload, Token.SECRET_KEY, algorithm='HS256', json_encoder=DateTimeEncoder)
        token_with_date = Token(token)
        return token_with_date

    def to_json(self) -> str:
        return json.dumps(
            {"token": self.token})

    def get_token_expiration_date(self) -> datetime:
        decoded_token = jwt.decode(self.token, Token.SECRET_KEY, algorithms='HS256')
        expiration_date = datetime.datetime.strptime(decoded_token['expiration_date'], '%Y-%m-%dT%H:%M:%S.%f')

        return expiration_date


class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)
