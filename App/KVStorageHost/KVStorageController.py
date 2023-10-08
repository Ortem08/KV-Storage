from flask import request

from KVStorage.KVStorageService import KVStorageService


class KVStorageController:
    def __init__(self, app, kv_storage_service: KVStorageService):
        self._kv_storage_service = kv_storage_service
        self._app = app

        @self._app.post("/new")
        def new():
            args = request.args
            return self._kv_storage_service.new(args.get("storage_name")).to_json()

        @self._app.post("/add")
        def add():
            args = request.args
            return self._kv_storage_service.add(
                args.get("storage_name"),
                args.get("key"),
                request.data.decode()).to_json()

        @self._app.post("/set")
        def set():
            args = request.args
            return (self._kv_storage_service.set(
                args.get("storage_name"),
                args.get("key"),
                request.data.decode())
                    .to_json())

        @self._app.get("/get")
        def get():
            args = request.args
            return (self._kv_storage_service.get(
                args.get("storage_name"),
                args.get("key"),)
                    .to_json())
