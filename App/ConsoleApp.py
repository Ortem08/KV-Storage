import fire

from Client import Client

client = Client()


def new(path: str, storage_name: str):
    client.new(path, storage_name)
    pass


def add(storage_name: str, key: str, value: str):
    client.add(storage_name, key, value)
    pass


def set(storage_name: str, key: str, value: str):
    client.set(storage_name, key, value)
    pass


def get(storage_name: str, key: str):
    return client.get(storage_name, key)
    pass


if __name__ == "__main__":
    fire.Fire()
