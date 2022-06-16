import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
from Common import Http, Conf

# 测试
prkey = "f5b815e8fba18b5cf699e29032cb110e1ac43b5a5ade15b0c6cd51c813b70fef"
publickey = ["02de74187a6253914c9eee8001e6a2c6b2d1af2545e1d3771af4a431ef031a3209"]
add = "iaa1wvmuzvyqlt76pddyk0w30glswev4kadksfa7ny"
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