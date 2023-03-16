import os
import io
import hashlib
import json
from OpenSSL import crypto
import pickle

from block import Block
from blockchain import Blockchain
from transaction import Transaction
from generate_rsa_keypair import keypair_gen


MAX_TXNS = 2
CURRENT_DIRECTORY = os.getcwd()


def store_blocks(blocks, account_holders):
    block_path = os.path.join(CURRENT_DIRECTORY, 'block_file')
    if not os.path.exists(block_path):
        os.mkdir(block_path)
    for block in blocks:
        if block.hash:
            file_name = os.path.join(block_path, block.hash)
            print(file_name)
            with io.open(file_name, 'wb') as f:
                pickle.dump(block, f, pickle.HIGHEST_PROTOCOL)
            # print(block)
            # print(block.hash)
            # file_name = hashlib.sha256(str(block))

    if account_holders:
        with io.open(os.path.join(block_path, 'metadata'), 'wb') as f:
            pickle.dump(account_holders, f, pickle.HIGHEST_PROTOCOL)


def retrieve_blocks(blockchain):
    account_holders = {}
    block_path = os.path.join(CURRENT_DIRECTORY, 'block_file')
    if not os.path.exists(block_path):
        return
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
    if account_name == '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918':
        return 1000000
    account_balance = 0
    for block in blocks:
        for txn in block.transactions:
            if txn.fromm == account_name:
                account_balance -= txn.amount

            if txn.to == account_name:
                account_balance += txn.amount
    return account_balance


def findAccountBalanceForBlock(transactions, account_name):
    if account_name == '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918':
        return 1000000
    account_balance = 0

    for txn in transactions:
        if txn.fromm == account_name:
            account_balance = account_balance - txn.amount

        if txn.to == account_name:
            account_balance = account_balance + txn.amount
    return account_balance


def print_balance_sheet(blockchain, account_holders):
    # print(blockchain.blocks)
    print('Balance Sheet: ')
    account_names = find_all_accounts(blockchain.blocks)
    for account in account_names:
        print(account + ' = ' + str(findAccountBalance(blockchain.blocks, account)))
    print(account_holders)


def blockchain_handler():
    account_holders = {}
    block = Block()
    blockchain = Blockchain(block)
    txns = []

    blockchain, account_holders = retrieve_blocks(blockchain)

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
                print('Enter validdd amount')
                continue

            # account_balance = findAccountBalance(blockchain.blocks,
            #                                      hashlib.sha256(debit_account_pkey).hexdigest())\
            #                   + findAccountBalanceForBlock(txns,
            #                                                hashlib.sha256(debit_account_pkey).hexdigest())
            account_balance = findAccountBalance(blockchain.blocks, debit_account_pkey) + findAccountBalanceForBlock(txns, debit_account_pkey)

            if account_balance < amount:
                print('Invalid transaction, please try again')
                continue


            # transaction = Transaction(hashlib.sha256(debit_account_pkey).hexdigest(),
            #                           hashlib.sha256(credit_account_pkey).hexdigest(), amount)

            transaction = Transaction(debit_account_pkey, credit_account_pkey, amount)

            txns.append(transaction)

            if len(txns) >= MAX_TXNS:
                block = blockchain.get_next_block(txns)
                blockchain.add_block(block)
                block = Block()
                txns = []

    if not txns:
        block = blockchain.get_next_block(txns)
        blockchain.add_block(block)
        txns = []

    print_balance_sheet(blockchain, account_holders)

    store_blocks(blockchain.blocks, account_holders)


def __init__():
    blockchain_handler()


if __name__ == '__main__':
    __init__()



