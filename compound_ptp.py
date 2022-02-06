import config
from utils.avax_platypus_utils import claim_veptp, check_available_stables_and_stake, claim_ptp_from_all_pools
from utils.avax_traderjoe_utils import swap_ptp
import time
import logging

logging.basicConfig(filename='logs/ptp_compounder.log', encoding='utf-8', level=logging.DEBUG, force=True)



def main():
    info = {
        'sender_address': config.ADDR,
        'private': config.PRIVATE_KEY,
        'to':   config.TO,
        'usdte': {'deposit':config.USDT, 'addr':'0xc7198437980c041c805A1EDcbA50c1Ce5db95118', 'balance': 0, 'ptp_balance': 0, 'ptp_pool': '0000000000000000000000000000000000000000000000000000000000000000'},
        'usdce': {'deposit':config.USDC, 'addr':'0xA7D7079b0FEaD91F3e65f86E8915Cb59c1a4C664', 'balance': 0, 'ptp_balance': 0, 'ptp_pool': '0000000000000000000000000000000000000000000000000000000000000001'},
        'daie': {'deposit':config.DAI, 'addr':'0xd586E7F844cEa2F87f50152665BCbc2C279D8d70', 'balance': 0, 'ptp_balance': 0, 'ptp_pool': '0000000000000000000000000000000000000000000000000000000000000002'},
        'usdc': {'deposit':config.DAI, 'addr':'0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E', 'balance': 0, 'ptp_balance': 0, 'ptp_pool': '0000000000000000000000000000000000000000000000000000000000000004'},
        'intervals': config.TX_INTERVALS
    }
    #
    while 1:
    if config.CLAIM_VEPTP == 1:
        claim_veptp(info)
        time.sleep(info['intervals'])

    claim_ptp_from_all_pools(info)
    swap_ptp(info)
    check_available_stables_and_stake(info)
    time.sleep(config.COMPOUND_FREQ)

if __name__ == '__main__':
    main()
