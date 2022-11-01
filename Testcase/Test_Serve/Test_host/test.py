import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from Common import Httprpc
from Common.Loguru import logger


host_infura = "https://mainnet.infura.io/v3/5d6fbdc545934723b28072344efcf9e5"

hash = "0xae0a3ed35b1d18e240ffa3593d85ee84c34bb45b10c676be335cac162255c2bf"

infura = Httprpc.HttpRpcEth_Utils.eth_getTransactionByHash(host_infura,hash)
assert infura.status_code == 200