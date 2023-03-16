import hashlib

from block import Block


class Blockchain:
    def __init__(self, genesis_block):
        self.blocks = []
        self.add_block(genesis_block)

    def add_block(self, block):
        if self.blocks:
            block.previousHash = "0000000000000000"
            block.hash = self.generate_hash(block)

        self.blocks.append(block)

    def get_next_block(self, transactions):
        block = Block()
        for transaction in transactions:
            block.add_transaction(transaction)
        previous_block = self.get_previous_block()
        block.index = len(self.blocks)
        block.previousHash = previous_block.hash
        block.hash = self.generate_hash(block)

        return block

    def get_previous_block(self):
        return self.blocks[len(self.blocks) - 1]

    def generate_hash(self, block):
        hash = hashlib.sha256(block.key().encode('utf-8')).hexdigest()
        return hash

    # def __str__(self):
    #     return self.blocks


