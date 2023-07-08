from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from db.database import SessionLocal
from db.block_entity import save_block, get_all_blocks

from domain.block import Block, create_block
from domain.blockchain import Blockchain

from endpoints.sync import sync_blockchain

from pydantic import BaseModel

from db.get_db import get_db

router = APIRouter()


class createBlock(BaseModel):
    data: str
    last_hash: str


class BlockResponse(BaseModel):
    blocks: list[Block]


@router.get("/")
async def list_blocks(db: SessionLocal = Depends(get_db)) -> BlockResponse:
    blocks = get_all_blocks(session=db)

    blockchain = Blockchain(blocks=blocks)

    return {"blocks": blockchain.chain}


@router.post("/")
async def add_block(
    block: createBlock,
    background_tasks: BackgroundTasks,
    db: SessionLocal = Depends(get_db),
) -> BlockResponse:
    blocks = get_all_blocks(session=db)

    blockchain = Blockchain(blocks=blocks)

    latest_block = blockchain.get_latest_block()

    if block.last_hash != latest_block.hash:
        raise HTTPException(status_code=400, detail="Invalid last hash")

    new_block = create_block(data=block.data, previous_hash=latest_block.hash)

    blockchain.add_block(new_block=new_block)
    save_block(block=new_block, session=db)

    background_tasks.add_task(sync_blockchain, db=db)

    return {"blocks": blockchain.chain}


@router.get("/valid", operation_id="is_chain_valid")
async def is_valid(
    db: SessionLocal = Depends(get_db),
):
    blocks = get_all_blocks(session=db)

    blockchain = Blockchain(blocks=blocks)
    return {"state": "valid" if blockchain.is_chain_valid() else "invalid"}
