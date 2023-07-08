import json
from pydantic import BaseModel


class SyncFile(BaseModel):
    addresses: set[str]


json_file = "sync.json"


def get_file_contents() -> SyncFile:
    with open(json_file, "r") as f:
        data = f.read()
        if data == "":
            return SyncFile(addresses=set())

        return SyncFile(**json.loads(data))


def write_address_to_file(address: str):
    data = get_file_contents()

    with open(json_file, "w") as f:
        if data is None:
            data = SyncFile(addresses={address})
            f.write(data.json())
            return data

        data.addresses.add(address)
        f.write(data.json())

    return data


def remove_address_from_file(address: str):
    data = get_file_contents()

    with open(json_file, "w") as f:
        data.addresses.remove(address)
        f.write(data.json())

    return data
