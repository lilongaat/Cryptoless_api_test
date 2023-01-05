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
from Common import Http, Conf, Httpcore
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))


@allure.feature("Transfers Success!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # MATIC
            ("MATIC SWAP:MATIC->USDC","MATIC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0x25f7f610a1dc5f674a5e2bb9c2846be076814cd7","MATIC","USDC","1","0.00012"),
            # ("MATIC SWAP:USDC->MATIC","MATIC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0x25f7f610a1dc5f674a5e2bb9c2846be076814cd7","USDC","MATIC","1","0.000011"),
        ]
    elif env_type == 1: #生产
        test_data = []

    @allure.story("Custodial Transfers Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,privatekey,address,from_coin,to_coin,slippage,fromamount', test_data)
    def test_custodial(self,test_title,networkCode,privatekey,address,from_coin,to_coin,slippage,fromamount):

        with allure.step("core查询账户holder信息"):
            holder = Http.HttpUtils.holders(networkCode=networkCode,symbol=from_coin,address=address)
            assert holder.status_code ==200
            quantity = holder.json()["list"][0]["quantity"]

        with allure.step("core构建交易——instructions"):
            body = {
                "networkCode":networkCode,
                "type":"swap",
                "body":{
                    "address":address,
                    "from":from_coin,
                    "to":to_coin,
                    "fromAmount":fromamount,
                    "slippage":slippage
                },
                "transactionParams":{
                    "memo":''.join(random.sample(string.ascii_letters + string.digits, 10))
                }
            }
            transfer = Http.HttpUtils.instructions(body)
            assert transfer.status_code == 200
            assert transfer.json()["_embedded"]["transactions"][0]["statusDesc"] == "SIGNING"

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
            sign = Http.HttpUtils.sign(id,signatures)
            assert sign.status_code == 200

        with allure.step("广播交易"):
            send = Http.HttpUtils.send(id)
            assert send.status_code == 200
            assert send.json()["statusDesc"] == "PENDING"

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')