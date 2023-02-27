from web3 import Web3,eth,HTTPProvider
from ens import ens,ENS
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loguru import logger
from Config.readconfig import ReadConfig

env_type = int(ReadConfig().get_env('type'))
if env_type == 0: # Debug
    Provider_GOERLI = ReadConfig().get_debug('Provider_goerli')
elif env_type == 1: # Release
    Provider_ETH = ReadConfig().get_release('Provider_ETH')


w3 = Web3(Web3.HTTPProvider(Provider_GOERLI, request_kwargs={'timeout': 60}))
# print(w3.isConnected())

address = "0xC29E1815E7cf466b55ed5fCceD090656A3F36300"

blocknumber = eth.Eth(w3).blockNumber
balances = eth.Eth(w3).getBalance(address,"latest")

