from web3 import Web3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loguru import logger
from Config.readconfig import ReadConfig

env_type = int(ReadConfig().get_env('type'))
if env_type == 0: # Debug
    Provider_ETH = ReadConfig().get_debug('Provider_ETH')
elif env_type == 1: # Release
    timeout_ = int(ReadConfig().get_release('timeout'))
    url_ = ReadConfig().get_release('url')
    token = ReadConfig().get_release('token')


w3 = Web3(Web3.HTTPProvider(Provider_ETH))