import hashlib


class Transaction:
    def __init__(self, fromm, to, amount):
        self.fromm = fromm
        self.to = to
        self.amount = amount
        txn = str(fromm) + str(to) + str(amount)
        self.txnHash = hashlib.sha256(txn.encode('utf-8')).hexdigest()

    def __str__(self):
        return f"From : {self.fromm}, To: {self.to}, Amount: {self.amount}, TxnHash: {self.txnHash}"
