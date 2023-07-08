from fastapi import FastAPI

from db.database import engine, Base
from endpoints.blocks import router as blocks_router
from endpoints.sync import router as sync_router
from domain.sync_file import write_address_to_file
from config.config import config
from scheduler import app as app_rocketry

session = app_rocketry.session

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router=blocks_router, prefix="/blocks", tags=["Blocks"])
app.include_router(router=sync_router, prefix="/sync", tags=["Sync"])


@app.on_event("startup")
def join():
    print("Joining group")
    state = write_address_to_file(config.our_url)
    print(f"Joined group with state: {state}")


@app.get("/")
async def root():
    return {"health": True}
