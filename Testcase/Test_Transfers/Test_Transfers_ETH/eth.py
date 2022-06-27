import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
from Common import Http, Conf
from Common.Loguru import logger

Authorization = "eyJzaWduYXR1cmUiOiIweDNkMWQzN2M3YmU4ODFjYTE5OGNjYWU4N2RiZGJjYTBmODZiZWEyZjliMWJjMDIxYWRjZjg5MjQxMTgxZGU3ZDY3YTA0MTliNjgzMzBiYmQyYmExYWRkNzliYzFkYWQ3YmE2YWY1ZjFjZDBhNWNmYjViNTEwZmYyMDc3M2EyZTAyMWIiLCJib2R5IjoiV2ViMyBUb2tlbiBWZXJzaW9uOiAyXG5Ob25jZTogNjk3ODAwNlxuSXNzdWVkIEF0OiBXZWQsIDE1IEp1biAyMDIyIDAwOjIxOjM1IEdNVFxuRXhwaXJhdGlvbiBUaW1lOiBTdW4sIDE1IEp1biAyMDQyIDAwOjIxOjM1IEdNVCJ9"
prkey = "9365d91088ca52629cd2f22bb14fda4efecf8905d53734e115cb9e1c8bb5b580"
publickey = ["032e6841694b2b247971b85db1786d723438c0a2f04aa719af7204348b7d3822d0"]
add = "0xB231eCF7c613473FcE444d6F394256083a671Db8"
amunt = "0.0000002"

res = Http.HttpUtils.post_transfers("ETH-RINKEBY","ETH",publickey,add,add,amunt,Authorization)
print(json.dumps(res))
print(res[3],res[8])

hash = res[5][0]['hash']
signature = Conf.Config.sign(prkey,hash)

signatures = [
    {
        "hash":res[5][0]['hash'],
        "publickey":publickey[0],
        "signature":signature
    }
]
# print(json.dumps(signatures))



sig = Http.HttpUtils.post_sign_transfers(res[1],res[2],res[3],res[4],res[5],res[6],signatures,status='BUILDING',Authorization = Authorization)