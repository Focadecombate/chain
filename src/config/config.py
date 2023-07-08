from os import getenv
from uuid import uuid4

from pydantic import BaseModel

str_port = getenv("UVICORN_PORT")
port = int(str_port) if str_port else 8000
id = getenv("SERVER_ID")

our_url = f"http://localhost:{port}" if port else "http://localhost:8000"
our_id = id if id else str(uuid4())

class Config(BaseModel):
    our_url: str
    our_id: str
    port: int

config = Config(our_url=our_url, our_id=our_id, port=port)