import os
import io
import hashlib
import pickle

from block import Block
from blockchain import Blockchain
from transaction import Transaction
from generate_rsa_keypair import keypair_gen


MAX_TXNS = 2
CURRENT_DIRECTORY = os.getcwd()
ADMIN_INITIAL_BALANCE = 1000000
ADMIN_HASH = '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'
BLOCK_FILE_FOLDER = 'BlockFile'


def store_blocks(blocks, account_holders):
    block_path = os.path.join(CURRENT_DIRECTORY, BLOCK_FILE_FOLDER)
    if not os.path.exists(block_path):
        os.mkdir(block_path)
    for block in blocks:
        if block.hash:
            file_name = os.path.join(block_path, block.hash)
            with io.open(file_name, 'wb') as f:
                pickle.dump(block, f, pickle.HIGHEST_PROTOCOL)

    if account_holders:
        with io.open(os.path.join(block_path, 'metadata'), 'wb') as f:
            pickle.dump(account_holders, f, pickle.HIGHEST_PROTOCOL)


def retrieve_blocks():
    blockchain = Blockchain()
    account_holders = {}
    block_path = os.path.join(CURRENT_DIRECTORY, BLOCK_FILE_FOLDER)
    if not os.path.exists(block_path):
        return blockchain, account_holders
    for file in os.listdir(block_path):
        if file == 'metadata':
            with io.open(os.path.join(block_path, 'metadata'), 'rb') as f:
                account_holders = pickle.load(f)
            continue
        with io.open(os.path.join(block_path, file), 'rb') as f:
            blockchain.add_block(pickle.load(f))

    return blockchain, account_holders


def find_all_accounts(blocks):
    accounts = {}
    for block in blocks:
        for txn in block.transactions:
            accounts[txn.fromm] = True
            accounts[txn.to] = True
    return accounts.keys()


def findAccountBalance(blocks, account_name):
    if account_name == ADMIN_HASH:
        return ADMIN_INITIAL_BALANCE
    account_balance = 0
    for block in blocks:
        for txn in block.transactions:
            if txn.fromm == account_name:
                account_balance -= txn.amount

            if txn.to == account_name:
                account_balance += txn.amount
    return account_balance


def findAccountBalanceForBlock(transactions, account_name):
    if account_name == ADMIN_HASH:
        return ADMIN_INITIAL_BALANCE
    account_balance = 0

    for txn in transactions:
        if txn.fromm == account_name:
            account_balance = account_balance - txn.amount

        if txn.to == account_name:
            account_balance = account_balance + txn.amount
    return account_balance


def print_balance_sheet(blockchain, account_holders):
    print('Blockchain Structure: ')
    for block in blockchain.blocks:
        print(f'Block : {block.hash} : [')
        print(block)
        for transaction in block.transactions:
            print(transaction)
        print(']', end='\n\n')

    print('Balance Sheet: ')
    account_names = find_all_accounts(blockchain.blocks)
    for account in account_names:
        print(account + ' = ' + str(findAccountBalance(blockchain.blocks, account)))
    print(account_holders)


def blockchain_handler():
    account_holders = {}
    blockchain, account_holders = retrieve_blocks()

    if len(blockchain.blocks) < 2:
        block = Block()
        blockchain = Blockchain(block)
    txns = []

    while True:
        allow = input('Type y to proceed: ')
        if allow != 'y':
            break
        else:
            debit_account = input('Debit Account: ')
            credit_account = input('Credit Account: ')
            if debit_account not in account_holders and debit_account != 'admin':
                account_holders[debit_account] = hashlib.sha256(keypair_gen()).hexdigest()

            if credit_account not in account_holders:
                account_holders[credit_account] = hashlib.sha256(keypair_gen()).hexdigest()

            credit_account_pkey = account_holders[credit_account]

            if debit_account != 'admin':
                debit_account_pkey = account_holders[debit_account]
            else:
                debit_account_pkey = hashlib.sha256(debit_account.encode('utf-8')).hexdigest()

            try:
                amount = int(input('Amount: '))
            except ValueError as e:
                print('Enter valid amount')
                continue

            if amount < 0:
                print('Enter valid amount')
                continue

            account_balance = findAccountBalance(blockchain.blocks, debit_account_pkey) + findAccountBalanceForBlock(txns, debit_account_pkey)

            if account_balance < amount:
                print('Invalid transaction, please try again')
                continue

            txns.append(Transaction(debit_account_pkey, credit_account_pkey, amount))

            if len(txns) >= MAX_TXNS:
                block = blockchain.get_next_block(txns)
                blockchain.add_block(block)
                txns = []

    if txns:
        block = blockchain.get_next_block(txns)
        blockchain.add_block(block)
        txns = []

    print_balance_sheet(blockchain, account_holders)
    store_blocks(blockchain.blocks, account_holders)


def __init__():
    blockchain_handler()


if __name__ == '__main__':
    __init__()
