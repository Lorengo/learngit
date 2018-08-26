import web3
from web3 import Web3


# create web3 object
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))


def send_transaction(from_adress,to_adress,value,gas_price,gas_limit,privatekey):
    txn=dict(nonce=web3.eth.getTransactionCount(from_adress),
    to=to_adress,
    value=value,
    gasPrice=gas_price,
    gas=gas_limit,
    data=b'',)
    privatekey=privatekey
    signed_txn=web3.eth.account.signTransaction(txn,privatekey)
    txn_hash=web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return txn_hash