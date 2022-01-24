This repository helps you to compound $PTP from the liquidity pools on platypus.finance into a stablecoin of your choice. Please read the disclaimer before proceeding.

# Disclaimer
This repository was made so that i wouldn't have to manually compound my $ptp everyday. It's a learning experience for me too. This exposes your wallet's private key in the config file. Use this repository only if you understand what you are doing and at your own risk! I will not be responsible for any possible losses.

# What this repository does in specific terms
1. Claims your vePTP if the option is turned on in `config.py`.
2. Claims all your reward $PTP from the pools.
3. Market sells all your claimed $PTP to the stablecoin defined in `config.py` via trader joe. There is no slippage used (as im not using an oracle).
4. Then stakes available stable coins in your wallet into the pools. You can indicate which stablecoins to stake in `config.py`.

This repository assumes all tokens are all already approved. This repository does NOT take care of token approvals. If you are unsure what how to go perform token approvals, simply just go through the whole staking process once for your stablecoins on platypus.finance.


# Prerequisite
`python>3.8`
`pip install web3`

# Setting Up
1. git clone this repo
2. `cd ptp_compounder`
3. Modify/change the `config.py` parameters using your text editor
4. After setting up, run `nohup python compound_ptp.py &` for the python script to run in the background.

Alternatively, you can use `screen` instead of the `nohup`. Depends on your preference.

## Config parameters
1. `ADDR`         - your wallet public address
2. `PRIVATE_KEY`  - your wallet private key. IMPORTANT!
3. `USDT`         - Stake all USDT.e in your wallet into the USDT.e pool
4. `USDC`         - Stake all USDC.e in your wallet into the USDC.e pool
5. `DAI`          - Stake all DAI.e in your wallet into the DAI.e pool
6. `MIM`          - Stake all MIM in your wallet into the MIM pool
3. `TO`           - coin that your this script will sell to on trader joe. options: 'usdte', 'usdce', 'daie', 'mim'
4. `COMPOUND_FREQ`- time (seconds) between each compounding run. default: 86400 (1 day)
5. `TX_INTERVALS` - time (seconds) between each transaction. > 30 is best just in case avax is congested. default: 30
6. `CLAIM_VEPTP`    - Claim $VEPTP before compounding?   1 if yes, 0 if no

# Donations
If this repository has helped you in any way, and if you would like to support me, you can send me any crypto on any EVM chain at `0xC986B1Aa3bFD11069e1e1bC67C712895Bc5DbC40` or sending me UST at `poohbear.ust`
