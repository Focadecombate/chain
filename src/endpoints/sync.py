from pydantic import BaseModel
import requests
from fastapi import APIRouter, Depends, HTTPException

from domain.blockchain import Blockchain
from domain.block import Block
from config.config import config
from domain.sync_file import (
    get_file_contents,
    write_address_to_file,
)
from db.database import SessionLocal
from db.get_db import get_db
from db.block_entity import get_all_blocks, save_block

router = APIRouter()


class SyncResponse(BaseModel):
    sync_addresses: list[str]
    our_url: str


class AddSyncAddress(BaseModel):
    address: str


class SyncBlocks(BaseModel):
    blocks: list[Block]


@router.post("/address")
def add_sync_address(data: AddSyncAddress) -> SyncResponse:
    file = get_file_contents()

    address_exists = file.addresses.issubset(set().add(data.address))

    if address_exists:
        raise HTTPException(status_code=409, detail="Node already exists")

    write_address_to_file(data.address)

    return list_sync_addresses()


@router.get("/")
def list_sync_addresses() -> SyncResponse:
    addresses = get_file_contents()

    return {
        "sync_addresses": list(addresses.addresses),
        "our_url": config.our_url,
    }


@router.post("/blockchain")
def receive_blockchain(
    received_chain: SyncBlocks,
    db: SessionLocal = Depends(get_db),
):
    blocks = get_all_blocks(session=db)
    blocks.sort(key=lambda block: block.timestamp)
    blockchain = Blockchain(blocks=blocks)

    for block in received_chain.blocks:
        block_exists = blockchain.block_exists(block.hash)

        if block_exists is not None:
            continue

        try:
            print(
                f"Adding block, hash: {block.hash} previous_hash: {block.previous_hash}"
            )
            
            save_block(block=block, session=db)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail=str(e))

    return {"blocks": blockchain.chain}


@router.post("/start")
async def sync_blockchain(
    db: SessionLocal = Depends(get_db),
):
    blocks = get_all_blocks(session=db)
    blocks.sort(key=lambda block: block.timestamp)
    blockchain = Blockchain(blocks=blocks)
    print("Syncing blockchain")

    chain = SyncBlocks(blocks=blockchain.chain).json()

    addresses = get_file_contents()

    for address in addresses.addresses:
        if address == config.our_url:
            continue

        print(f"Syncing with {address}")
        response = requests.request(
            method="POST",
            url=f"{address}/sync/blockchain",
            data=chain,
            headers={"Content-Type": "application/json"},
        )

        return response.json()
