import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Conf

prkey = "ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"
publickey = ["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"]
add = "0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3"
amount = "0.0000002"

res = Http.HttpUtils.post_transfers("ETH-RINKEBY","ETH",publickey,add,add,amount,Authorization=Http.Authorization_)

hash = res[5][0]['hash']
signature = Conf.Config.sign(prkey,hash)

signatures = [
    {
        "hash":res[5][0]['hash'],
        "publickey":publickey[0],
        "signature":signature
    }
]


sig = Http.HttpUtils.post_sign_transfers(res[1],res[2],res[3],res[4],res[5],res[6],signatures=signatures)

send = Http.HttpUtils.post_send_transfers(res[3])