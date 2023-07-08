from rocketry import Rocketry

from domain.ping import check_cluster_health
from domain.sync_file import get_file_contents

app = Rocketry(execution="async")


@app.task("every 5 seconds")
async def health_check():
    addresses = get_file_contents().addresses
    check_cluster_health(addresses)


if __name__ == "__main__":
    app.run()
