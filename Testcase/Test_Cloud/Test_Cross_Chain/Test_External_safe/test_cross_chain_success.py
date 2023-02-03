import json
import random
import string
from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
from Common import Http, Conf
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))

# extarnal
@allure.feature("Transfers Success!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # MATIC 
            # ("MATIC SWAP:MATIC-USDC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xe525E7cd17f6Dc950492755A089E452fd5d9d44f","MATIC","USDC","0x3d7f18ad2cea9b59e54dfaf09b327c1ccd899591","BSC","USDT","1","0.000012"),
        ]
    elif env_type == 1: #生产
        test_data = [
            # BSC——MATIC
            ("CrossChain USDC BSC(普通账户)-MATIC(普通账户)","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","BSC","USDC","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","MATIC","13"),
            # ("CrossChain USDC MATIC(普通账户)-BSC(普通账户)","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","MATIC","USDC","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","BSC","12.8"),

            # ("CrossChain USDC BSC(普通账户)-MATIC(安全账户)","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","BSC","USDC","0x66c1d34c273cc09df9072f49aeba4b09e017bc5c","MATIC","13"),
            # ("CrossChain USDC MATIC(安全账户)-BSC(普通账户)","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x66c1d34c273cc09df9072f49aeba4b09e017bc5c","MATIC","USDC","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","BSC","12.8"),
        ]

    @allure.story("Custodial Transfers Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,fromaddress,networkCode,symbol,toaddress,toNetworkCode,amount', test_data)
    def test_custodial(self,test_title,privatekey,fromaddress,networkCode,symbol,toaddress,toNetworkCode,amount):

        with allure.step("查询from账户holder信息"):
            holder = Http.HttpUtils.holders(networkCode=networkCode,symbol=symbol,address=fromaddress)
            assert holder.status_code ==200
            quantity = holder.json()["list"][0]["quantity"]

        with allure.step("构建交易——instructions"):
            body = {
                "networkCode":networkCode,
                "type":"CROSS_CHAIN",
                "body":{
                    "from":fromaddress,
                    "to":toaddress,
                    "symbol":symbol,
                    "amount":amount,
                    "toNetworkCode":toNetworkCode
                }
            }
            transfer = Http.HttpUtils.instructions(body)
            assert transfer.status_code == 200

            id = transfer.json()["_embedded"]["transactions"][0]["id"]
            requiredSignings = transfer.json()["_embedded"]["transactions"][0]["requiredSignings"]
            signatures = []
            for i in range(len(requiredSignings)):
                hash = requiredSignings[i]["hash"]
                publickey = requiredSignings[i]["publicKeys"][0]
                signature = {
                    "hash":hash,
                    "publicKey":publickey,
                    "signature":Conf.Config.sign(privatekey,hash)

                }
                signatures.append(signature)

        with allure.step("签名交易"):
            sign  =Http.HttpUtils.sign(id,signatures)
            assert sign.status_code == 200

        with allure.step("广播交易"):
            send = Http.HttpUtils.send(id)
            assert send.status_code == 200
            assert send.json()["statusDesc"] == "PENDING"

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')