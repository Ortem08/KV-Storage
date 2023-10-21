from flask import request

from App.KVStorageHost.KVStorageResponse import KVStorageResponse
from App.Token import Token
from App.TokenExpiredError import TokenExpiredError
from KVStorage.KVStorageService import KVStorageService
from App.TokenValidatorService import TokenValidatorService


class KVStorageController:
    def __init__(self, app, kv_storage_service: KVStorageService,
                 token_validator_service: TokenValidatorService):
        self._kv_storage_service = kv_storage_service
        self._token_validator_service = token_validator_service
        self._app = app
        self._token = None

        @self._app.post("/new")
        def new():
            args = request.args

            token = Token(args.get("token"))
            if not TokenValidatorService.validate_token(token):
                return KVStorageResponse(None, None, str(TokenExpiredError())).to_json()

            kv_response = (self._kv_storage_service
                           .new(args.get("storage_name")))
            kv_response._token = token.token
            return kv_response.to_json()

        @self._app.post("/add")
        def add():
            args = request.args

            token = Token(args.get("token"))
            if not TokenValidatorService.validate_token(token):
                return KVStorageResponse(None, None, str(TokenExpiredError())).to_json()

            kv_response = self._kv_storage_service.add(
                args.get("storage_name"),
                args.get("key"),
                request.data.decode())
            kv_response._token = token.token
            return kv_response.to_json()

        @self._app.post("/set")
        def set():
            args = request.args

            token = Token(args.get("token"))
            if not TokenValidatorService.validate_token(token):
                return KVStorageResponse(None, None, str(TokenExpiredError())).to_json()

            kv_response = self._kv_storage_service.set(
                args.get("storage_name"),
                args.get("key"),
                request.data.decode())
            kv_response._token = token.token
            return kv_response.to_json()

        @self._app.get("/get")
        def get():
            args = request.args

            token = Token(args.get("token"))
            if not TokenValidatorService.validate_token(token):
                return KVStorageResponse(None, None, str(TokenExpiredError())).to_json()

            kv_response = self._kv_storage_service.get(
                args.get("storage_name"),
                args.get("key"),)
            kv_response._token = token.token
            return kv_response.to_json()

        @self._app.post("/login")
        def login():
            args = request.args
            login = args.get("login")
            password = args.get("password")
            return self._token_validator_service.get_token(login, password).to_json()
