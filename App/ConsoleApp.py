import fire

from Client import Client


client = Client()


def new(path: str, storage_name: str):
    return client.new(path, storage_name)


def add(storage_name: str, key: str, value: str):
    return client.add(storage_name, key, value)


def set(storage_name: str, key: str, value: str):
    return client.set(storage_name, key, value)


def get(storage_name: str, key: str):
    return client.get(storage_name, key)


def login(login: str, password: str):
    client.login(login, password)
    pass


if __name__ == "__main__":
    fire.Fire()
