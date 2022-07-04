import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Conf

prkey = "dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b"
publickey = ["022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"]
add = "tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun"
amount = "0.0000002"

res = Http.HttpUtils.post_transfers("BTC","BTC",publickey,add,add,amount)

signatures = []
for i in range(len(res[5])):
    signature = Conf.Config.sign(prkey,res[5][i]['hash'])
    signatures.append(
        {
        "hash":res[5][i]['hash'],
        "publickey":publickey[0],
        "signature":signature
    }
    )

sig = Http.HttpUtils.post_sign_transfers(res[1],res[2],res[3],res[4],res[5],res[6],signatures)

send = Http.HttpUtils.post_send_transfers(res[3])