import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Conf

# 测试
prkey = "49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"
publickey = ["033511e38fd373c4515ada4826616146b4c3def47da9907b59d9555b19134dd683"]
add = "iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u"
amount = '0.001'

res = Http.HttpUtils.post_transfers("IRIS","IRIS",publickey,add,'iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u',amount)

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