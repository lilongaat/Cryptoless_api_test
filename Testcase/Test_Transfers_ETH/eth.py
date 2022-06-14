import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
from Common import Http, Conf
from Common.Loguru import logger


network = "ETH"
prkey = "1dfb5db671e7d68dda061d8a7e79a57ed9e27449d6e934c3286978ee2873a435"
publickey = ["02b2a4911e34a182981cb37df1ab2f05b39b9977e0699e15a0f59711367c5454ac"]
add = "0x44d9Ea428C4C1D097947A683439a60105281AAD7"
amunt = "0.0000002"
res = Http.HttpUtils.post_transfers(network,network,publickey,add,add,amunt)

hash = res[5][0]['hash']
signature = Conf.Config.sign(prkey,hash)

signatures = [
    {
        "hash":res[5][0]['hash'],
        "publickey":publickey[0],
        "signature":signature
    }
]
print(signatures)

sig = Http.HttpUtils.post_sign_transfers(res[1],res[2],res[3],res[4],res[5],res[6],signatures=signatures)