import fire

from Client import Client

client = Client()


def new(storage_name: str, storage_type: str = 'Std', mem_limit: int = 0):
    return client.new(storage_name, storage_type, mem_limit)


def add(storage_name: str, key: str, value: str):
    return client.add(storage_name, key, value)


def add_with_ttl(storage_name: str, key: str, value: str, ttl: int):
    return client.add_with_ttl(storage_name, key, value, ttl)


def set(storage_name: str, key: str, value: str):
    return client.set(storage_name, key, value)


def get(storage_name: str, key: str):
    return client.get(storage_name, key)


def get_by_key_prefix(storage_name: str, key_prefix: str):
    return client.get_by_key_prefix(storage_name, key_prefix)


def get_all_keys(storage_name: str):
    return client.get_all_keys(storage_name)


def get_by_key_in_any_register(storage_name: str, key: str):
    return client.get_by_key_in_any_register(storage_name, key)


def delete(storage_name: str, key: str):
    return client.delete(storage_name, key)


def login(login: str, password: str):
    client.login(login, password)
    pass


if __name__ == "__main__":
    fire.Fire()
