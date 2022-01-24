from web3 import Web3

def get_w3_rpc(link):
    w3 = Web3(Web3.HTTPProvider(link))
    return w3
