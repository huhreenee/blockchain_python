from pymerkle import MerkleTree, verify_inclusion, verify_consistency

class Block:
    def __init__(self):
        self.index = 0
        self.previousHash = ""
        self.hash = ""
        self.nonce = 0
        self.transactions = []
        self.merkleRootHash = ""

    def key(self):
        return f"{repr(self.transactions)}{str(self.index)}{str(self.previousHash)}{str(self.nonce)}"

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def __str__(self):
        return f"Previous Hash:{self.previousHash}, merkleRootHash:{self.merkleRootHash}, Nonce:{self.nonce}, Number of Transactions:{len(self.transactions)}"
    
    def generate_merkle_tree(self):
        tree = MerkleTree()
        for t in [t.encode('ASCII') for t in [b.txnHash for b in self.transactions]]:
            tree.append_entry(t)
        return tree