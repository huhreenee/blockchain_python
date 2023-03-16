import json
# from OpenSSL import crypto


class Block:
    def __init__(self):
        self.index = 0
        self.previousHash = ""
        self.hash = ""
        self.nonce = 0
        self.transactions = []

    def key(self):
        return str(self.transactions) + str(self.index) + str(self.previousHash) + str(self.nonce)

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def __str__(self):
        return f"Hash: {self.hash}, Previous Hash: {self.previousHash}, nonce: {self.nonce}, " \
               f"index: {self.transactions}, transactions: {self.transactions}"

