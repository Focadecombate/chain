from sqlalchemy import Column, String
from sqlalchemy.orm import Session

from domain.block import Block

from .database import Base


class BlockEntity(Base):
    __tablename__ = "blocks"

    hash = Column(String, primary_key=True, unique=True, index=True)
    data = Column(String)
    timestamp = Column(String)
    previous_hash = Column(String)


def save_block(session: Session, block: Block):
    db_block = BlockEntity(**block.dict())
    session.add(db_block)
    session.commit()
    session.refresh(db_block)
    return db_block


def get_block_by_hash(session: Session, hash: str):
    return session.query(BlockEntity).get(hash)


def get_all_blocks(session: Session):
    return session.query(BlockEntity).all()
