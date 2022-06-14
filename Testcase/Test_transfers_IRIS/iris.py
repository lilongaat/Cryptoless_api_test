import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
from Common import Http, Conf

# 测试
prkey = "44298f449dab3993e9965a32c1c4e1d99c1fcece7e228b348516924cecc88f18"
publickey = ["032de47c91516ffd2985965935841fa8243894b003886a1f478682da74a848db58"]
add = "iaa13cq3lkmheswkz4d00vu4663267aw6tqjep3jy4"
amount = '0.001'

# 生产
# prkey = "9f013c0dc424741a6ed4cc816d19aa706177c65bd7833a457e6777878b90ce82"
# publickey = ["02d87c076ea26a06bae0f6c25d56c7195ed26f43d84a6e14b4e4286a88d9a51884"]
# add = "iaa1jwrwsead5ehwzy9u9uw3r6cle0np04kkurrsfe"
# amount = '0.001'

res = Http.HttpUtils.post_transfers("IRIS","IRIS",publickey,add,add,amount)

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