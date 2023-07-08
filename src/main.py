import asyncio
import uvicorn

from config.config import config

from api import app as app_fastapi
from scheduler import app as app_rocketry
from db.database import SessionLocal
from db.block_entity import get_all_blocks, save_block
from domain.blockchain import create_genesis_block


class Server(uvicorn.Server):
    """Customized uvicorn.Server

    Uvicorn server overrides signals and we need to include
    Rocketry to the signals."""

    def handle_exit(self, sig: int, frame) -> None:
        app_rocketry.session.shut_down()
        return super().handle_exit(sig, frame)


def start_db():
    with SessionLocal() as session:
        print("DB:", session)
        result = get_all_blocks(session)
        if len(result) > 0:
            session.close()
        else:
            print("DB: Creating genesis block")
            save_block(session, create_genesis_block())


async def main():
    "Run scheduler and the API"

    server = Server(
        config=uvicorn.Config(
            app_fastapi, workers=1, loop="asyncio", port=config.port, reload=True
        )
    )

    api = asyncio.create_task(server.serve())
    sched = asyncio.create_task(app_rocketry.serve())

    start_db()

    await asyncio.wait([sched, api])


if __name__ == "__main__":
    asyncio.run(main())
