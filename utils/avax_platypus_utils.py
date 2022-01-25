from utils.node_utils import get_w3_rpc
from utils.contract_utils import load_contract
import json
import time
import random
import logging

from web3.middleware import geth_poa_middleware

w3 = get_w3_rpc('https://api.avax.network/ext/bc/C/rpc')
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

logging.info(f'Connected: {w3.isConnected()}')

platypus_proxy_abi = json.loads('[{"inputs":[{"internalType":"address","name":"initialLogic","type":"address"},{"internalType":"address","name":"initialAdmin","type":"address"},{"internalType":"bytes","name":"_data","type":"bytes"}],"stateMutability":"payable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"stateMutability":"payable","type":"fallback"},{"inputs":[],"name":"admin","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"implementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"}],"name":"upgradeTo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"stateMutability":"payable","type":"function"},{"stateMutability":"payable","type":"receive"}]')

platypus_proxy_contract = load_contract(w3=w3, address=w3.toChecksumAddress('0xB0523f9F473812FB195Ee49BC7d2ab9873a98044'), abi=platypus_proxy_abi)


def check_available_stables_and_stake(info):
    info = get_all_stables_balance(info)
    for stable in ['usdte', 'usdce', 'daie', 'mim']:
        if info[stable]['deposit']:
            if info[stable]['balance'] > 0:
                logging.info(f"{time.ctime(time.time())}: Depositing {info[stable]['balance']} {stable}")
                time.sleep(info['intervals'])
                deposit_stable(info['sender_address'], info['private'], info[stable]['addr'], info[stable]['balance'])
                time.sleep(info['intervals'])

            info = get_all_plp_balance(info)
            if info[stable]['ptp_balance'] > 0:
                logging.info(f"{time.ctime(time.time())}: Staking {info[stable]['ptp_balance']} {stable}")
                time.sleep(info['intervals'])
                stake_plp(info['sender_address'], info['private'], info[stable]['ptp_pool'], info[stable]['ptp_balance'])
                time.sleep(info['intervals'])

    #update balances
    info = get_all_stables_balance(info)
    return info


def claim_ptp_from_all_pools(info):
    addr = info['sender_address']
    pkey = info['private']
    nonce = w3.eth.get_transaction_count(addr)
    tx = {
                'chainId': 43114,
                'to': '0xB0523f9F473812FB195Ee49BC7d2ab9873a98044',
                'from': addr,
                'data': '0x4ed73d28000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000003',
                'gas': 500000,
                'gasPrice': w3.toWei(26,'gwei'),
                'nonce': nonce,
                }

    signed_txn = w3.eth.account.sign_transaction(tx, private_key=pkey)
    w3.eth.send_raw_transaction(signed_txn.rawTransaction)


ptp_coin_abi = json.loads('[{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"address","name":"minter_","type":"address"},{"internalType":"uint256","name":"mintingAllowedAfter_","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"minter","type":"address"},{"indexed":false,"internalType":"address","name":"newMinter","type":"address"}],"name":"MinterChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"DOMAIN_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"rawAmount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"minimumTimeBetweenMints","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"rawAmount","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"mintCap","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"minter","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"mintingAllowedAfter","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"rawAmount","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"minter_","type":"address"}],"name":"setMinter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"rawAmount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"src","type":"address"},{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"rawAmount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]')
ptp_coin_contract = load_contract(w3=w3, address=w3.toChecksumAddress('0x22d4002028f537599bE9f666d1c4Fa138522f9c8'), abi=ptp_coin_abi)

def get_ptp_balance(addr):
    return ptp_coin_contract.functions.balanceOf(addr).call()



def claim_veptp(info):
    logging.info(f'{time.ctime(time.time())}: Claiming $vePTP')
    addr, pkey = info['sender_address'], info['private']
    nonce = w3.eth.get_transaction_count(addr)
    tx = {
                'chainId': 43114,
                'to': '0x5857019c749147EEE22b1Fe63500F237F3c1B692',
                'type': '0x2',
                'from': addr,
                'data': '0x4e71d92d',
                'gas': 500000,
                'maxFeePerGas': w3.toWei(26,'gwei'),
                'maxPriorityFeePerGas': w3.toWei(26,'gwei'),
                'nonce': nonce,
                }

    signed_txn = w3.eth.account.sign_transaction(tx, private_key=pkey)
    w3.eth.send_raw_transaction(signed_txn.rawTransaction)

stable_coin_abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"chainId","type":"uint256"}],"name":"AddSupportedChainId","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"contractAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"supplyIncrement","type":"uint256"}],"name":"AddSwapToken","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"newBridgeRoleAddress","type":"address"}],"name":"MigrateBridgeRole","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"address","name":"feeAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"feeAmount","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"originTxId","type":"bytes32"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"contractAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"supplyDecrement","type":"uint256"}],"name":"RemoveSwapToken","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"chainId","type":"uint256"}],"name":"Unwrap","type":"event"},{"inputs":[{"internalType":"uint256","name":"chainId","type":"uint256"}],"name":"addSupportedChainId","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"contractAddress","type":"address"},{"internalType":"uint256","name":"supplyIncrement","type":"uint256"}],"name":"addSwapToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burnFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"chainIds","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newBridgeRoleAddress","type":"address"}],"name":"migrateBridgeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"feeAddress","type":"address"},{"internalType":"uint256","name":"feeAmount","type":"uint256"},{"internalType":"bytes32","name":"originTxId","type":"bytes32"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"contractAddress","type":"address"},{"internalType":"uint256","name":"supplyDecrement","type":"uint256"}],"name":"removeSwapToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"swap","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"swapSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"chainId","type":"uint256"}],"name":"unwrap","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
usdce_coin_contract = load_contract(w3=w3, address=w3.toChecksumAddress('0xA7D7079b0FEaD91F3e65f86E8915Cb59c1a4C664'), abi=stable_coin_abi)
usdte_coin_contract = load_contract(w3=w3, address=w3.toChecksumAddress('0xc7198437980c041c805A1EDcbA50c1Ce5db95118'), abi=stable_coin_abi)
daie_coin_contract = load_contract(w3=w3, address=w3.toChecksumAddress('0xd586E7F844cEa2F87f50152665BCbc2C279D8d70'), abi=stable_coin_abi)
mim_coin_contract = load_contract(w3=w3, address=w3.toChecksumAddress('0x130966628846BFd36ff31a822705796e8cb8C18D'), abi=stable_coin_abi)





def get_all_stables_balance(info):
    addr=info['sender_address']
    info['usdce']['balance'] = usdce_coin_contract.functions.balanceOf(addr).call()
    info['usdte']['balance'] = usdte_coin_contract.functions.balanceOf(addr).call()
    info['daie']['balance'] = daie_coin_contract.functions.balanceOf(addr).call()
    info['mim']['balance']= mim_coin_contract.functions.balanceOf(addr).call()

    return info


def deposit_stable(addr, pkey, stable, balance):

    data = '0x90d25074' #function hex

    #1st field
    data += stable.lstrip('0x').zfill(64) #stable contract

    #2nd field
    stable_amt = hex(balance).lstrip('0x').zfill(64)
    data += stable_amt #64 length hex amount of stable to deposit

    #3rd field
    data += addr.lstrip('0x').zfill(64) #wallet address

    #4th field
    now = hex(int(time.time() + 1000000)).lstrip('0x').zfill(64)
    data += now #time i think
    assert (len(data)==266)



    nonce = w3.eth.get_transaction_count(addr)
    tx = {
                'chainId': 43114,
                'type': '0x2',
                'to': '0x66357dCaCe80431aee0A7507e2E361B7e2402370',
                'from': addr,
                'data': data,
                'gas': 500000,
                'maxFeePerGas': w3.toWei(26,'gwei'),
                'maxPriorityFeePerGas': w3.toWei(26,'gwei'),
                'nonce': nonce,
                }

    signed_txn = w3.eth.account.sign_transaction(tx, private_key=pkey)

    w3.eth.send_raw_transaction(signed_txn.rawTransaction)

#
plp_abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"chainId","type":"uint256"}],"name":"AddSupportedChainId","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"contractAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"supplyIncrement","type":"uint256"}],"name":"AddSwapToken","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"newBridgeRoleAddress","type":"address"}],"name":"MigrateBridgeRole","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"address","name":"feeAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"feeAmount","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"originTxId","type":"bytes32"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"contractAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"supplyDecrement","type":"uint256"}],"name":"RemoveSwapToken","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"chainId","type":"uint256"}],"name":"Unwrap","type":"event"},{"inputs":[{"internalType":"uint256","name":"chainId","type":"uint256"}],"name":"addSupportedChainId","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"contractAddress","type":"address"},{"internalType":"uint256","name":"supplyIncrement","type":"uint256"}],"name":"addSwapToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burnFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"chainIds","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newBridgeRoleAddress","type":"address"}],"name":"migrateBridgeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"feeAddress","type":"address"},{"internalType":"uint256","name":"feeAmount","type":"uint256"},{"internalType":"bytes32","name":"originTxId","type":"bytes32"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"contractAddress","type":"address"},{"internalType":"uint256","name":"supplyDecrement","type":"uint256"}],"name":"removeSwapToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"swap","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"swapSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"chainId","type":"uint256"}],"name":"unwrap","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
usdte_plp_contract = load_contract(w3=w3, address=w3.toChecksumAddress('0x0D26D103c91F63052Fbca88aAF01d5304Ae40015'), abi=plp_abi)
usdce_plp_contract = load_contract(w3=w3, address=w3.toChecksumAddress('0x909B0ce4FaC1A0dCa78F8Ca7430bBAfeEcA12871'), abi=plp_abi)
daie_plp_contract = load_contract(w3=w3, address=w3.toChecksumAddress('0xc1Daa16E6979C2D1229cB1fd0823491eA44555Be'), abi=plp_abi)
mim_plp_contract = load_contract(w3=w3, address=w3.toChecksumAddress('0x6220BaAd9D08Dee465BefAE4f82ee251cF7c8b82'), abi=plp_abi)


def get_all_plp_balance(info):
    addr=info['sender_address']
    info['usdce']['ptp_balance'] = usdce_plp_contract.functions.balanceOf(addr).call()
    info['usdte']['ptp_balance'] = usdte_plp_contract.functions.balanceOf(addr).call()
    info['daie']['ptp_balance'] = daie_plp_contract.functions.balanceOf(addr).call()
    info['mim']['ptp_balance']= mim_plp_contract.functions.balanceOf(addr).call()

    return info

def stake_plp(addr, pkey, pool, balance):
    data = '0xe2bbb158' #function hex

    #1st field
    data += pool #usdce pool

    #2nd field
    plp_amt = hex(balance).lstrip('0x').zfill(64)
    data += plp_amt #64 length hex amount of usdc plp to deposit



    nonce = w3.eth.get_transaction_count(addr)
    tx = {
                'chainId': 43114,
                'type': '0x2',
                'to': '0xB0523f9F473812FB195Ee49BC7d2ab9873a98044',
                'from': addr,
                'data': data,
                'gas': 500000,
                'maxFeePerGas': w3.toWei(26,'gwei'),
                'maxPriorityFeePerGas': w3.toWei(26,'gwei'),
                'nonce': nonce,
                }

    signed_txn = w3.eth.account.sign_transaction(tx, private_key=pkey)

    w3.eth.send_raw_transaction(signed_txn.rawTransaction)
