import json
from web3 import Web3

def load_contract(w3, address, abi):
    return w3.eth.contract(address=address, abi=abi)
