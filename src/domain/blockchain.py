from domain.block import CreateBlock, calculate_hash, Block

import datetime


def create_genesis_block():
    block = CreateBlock(
        timestamp=datetime.datetime(
            2023,
            6,
            25,
            18,
            14,
        ),
        data="Genesis Block",
        previous_hash="0",
    )

    hash = calculate_hash(block)

    return Block(**block.dict(), hash=hash)


class Blockchain:
    chain: list[Block]

    def __init__(self, blocks: list[Block] = None):
        self.chain = [create_genesis_block()] if blocks is None else blocks

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block: CreateBlock):
        new_block.previous_hash = self.get_latest_block().hash
        self.chain.append(new_block)

    def add_block_from_other_node(self, new_block: Block):
        old_block = self.block_exists(new_block.previous_hash)

        print(old_block, new_block.previous_hash)

        if old_block is None:
            raise Exception("Old Block does not exist")

        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != calculate_hash(current_block):
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def block_exists(self, search_block_hash: str):
        for index, block in enumerate(self.chain):
            print(block.hash, search_block_hash)
            if block.hash == search_block_hash:
                return index, block

        return None
