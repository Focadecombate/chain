import hashlib
import datetime

from pydantic import BaseModel


class CreateBlock(BaseModel):
    timestamp: datetime.datetime
    data: str
    previous_hash: str


class Block(CreateBlock):
    hash: str

    class Config:
        orm_mode = True


def calculate_hash(block: CreateBlock) -> str:
    sha = hashlib.sha256()
    sha.update(
        str(block.timestamp).encode("utf-8")
        + str(block.data).encode("utf-8")
        + str(block.previous_hash).encode("utf-8")
    )
    return sha.hexdigest()


def create_block(data: str, previous_hash: str) -> Block:
    to_create = CreateBlock(
        data=data, previous_hash=previous_hash, timestamp=datetime.datetime.now()
    )
    return Block(
        **to_create.dict(),
        hash=calculate_hash(to_create),
    )
