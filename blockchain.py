import hashlib
from block import Block

START_PREV_HASH = "0000000000000000"


class Blockchain:
    def __init__(self, genesis_block=None):
        self.blocks = []
        if genesis_block:
            self.add_block(genesis_block)

    def add_block(self, block):
        if not self.blocks:
            block.previousHash = START_PREV_HASH
            block.hash = self.generate_hash(block)

        self.blocks.append(block)

    def get_next_block(self, transactions):
        block = Block()
        for transaction in transactions:
            block.add_transaction(transaction)
        previous_block = self.get_previous_block()
        block.index = len(self.blocks)
        if not previous_block:
            block.previousHash = START_PREV_HASH
        else:
            block.previousHash = previous_block.hash
        block.hash = self.generate_hash(block)

        return block

    def get_previous_block(self):
        return self.blocks[len(self.blocks) - 1] or None

    def generate_hash(self, block):
        hash_key = hashlib.sha256(block.key().encode('utf-8')).hexdigest()
        return hash_key
