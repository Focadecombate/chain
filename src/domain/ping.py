import requests

from domain.sync_file import remove_address_from_file
from config.config import config

tries = dict()


def handle_error(address: str):
    if address in tries:
        tries[address] += 1
    else:
        tries[address] = 1

    if tries[address] > 3:
        print(f"Removing {address} from cluster")
        remove_address_from_file(address)


def check_cluster_health(addresses: list[str]):
    print(f"Checking cluster health {addresses}")

    for address in list(addresses):
        if address == config.our_url:
            continue

        print(f"Checking {address}")
        try:
            response = requests.request(method="GET", url=f"{address}/")

            if not response.ok:
                handle_error(address)
                continue

            print(f"Node {address} is healthy")
        except Exception:
            handle_error(address)
