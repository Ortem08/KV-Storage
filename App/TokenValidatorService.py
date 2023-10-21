import datetime

from App.Token import Token


class TokenValidatorService:
    def __init__(self, users: {}):
        self._users = users

    def get_token(self, login: str, password: str) -> Token:
        if login not in self._users or password != self._users[login]:
            raise ValueError("Wrong login info")

        return Token.create_token(login, password)

    @staticmethod
    def validate_token(token: Token) -> bool:
        if token.get_token_expiration_date() < datetime.datetime.utcnow():
            return False

        return True
