'''wallet setup'''      # wallet address and private key
ADDR = ''
PRIVATE_KEY= ''

'''stake your available stables into these pools'''         # 1 if yes, 0 if don't
USDT = 1
USDC = 1
DAI = 1
USDC = 1

'''compound to'''       # all claimed ptp will be compounded to this coin.
TO = 'usdte'            # options: 'usdte', 'usdce', 'daie', 'mim'

'''others'''
COMPOUND_FREQ = 86400   # time (seconds) between each compounding run. default: 86400 (1 day)
TX_INTERVALS = 30       # time (seconds) between each transaction. >30 is best just in case avax is congested
CLAIM_VEPTP = 1        # 1 if yes, 0 if no
