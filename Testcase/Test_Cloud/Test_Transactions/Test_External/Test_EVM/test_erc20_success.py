import json
import random
import string
from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))))
from Common import Http, Conf
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))

# custodial
@allure.feature("Transfers Success!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # GOERLI
            ("GOERLI Custodial账户转账 erc20coin","GOERLI","0x1eC2CE6108240118Ff2c66eC8AFAC28618D7e066",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da"],"0xe525e7cd17f6dc950492755a089e452fd5d9d44f","0xa7A9E710f9A3B4184D4F8B7d379CEC262f2382c2","0x64"),
        ]
    elif env_type == 1: #生产
        test_data = []

    @allure.story("Custodial Transfers Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,tokenaddress,privatekey,from_add,to_add,amount', test_data)
    def test_custodial(self,test_title,networkCode,tokenaddress,privatekey,from_add,to_add,amount):

        with allure.step("构建交易——transactions"):
            body = {
                "networkCode":networkCode,
                "payload":{
                    "from":from_add,
                    "to":tokenaddress,
                    "inputRequest":{
                        "to":to_add,
                        "value":amount
                    }
                },
                "type":"TOKEN_TRANSFER_TRANSACTION"
            }
            transfer = Http.HttpUtils.transactions(body)
            assert transfer.status_code == 200
            assert transfer.json()["statusDesc"] == "BUILDING"

            id = transfer.json()["id"]
            requiredSignings = transfer.json()["requiredSignings"]

            signatures = []
            for i in range(len(requiredSignings)):
                hash = requiredSignings[i]["hash"]
                signature = {
                    "hash":hash,
                    "publicKey":requiredSignings[i]["publicKeys"][0],
                    "signature":Conf.Config.sign(privatekey[0],hash)

                }
                signatures.append(signature)

        with allure.step("Sign交易"):
            sign = Http.HttpUtils.sign(id,signatures)
            assert sign.status_code == 200

        # with allure.step("rebuilde交易"):
        #     params = {

        #     }
        #     re = Http.HttpUtils.rebuild(id,params)
        #     assert re.status_code == 200

        with allure.step("广播交易"):
            send = Http.HttpUtils.send(id)
            assert send.status_code == 200
            assert send.json()["statusDesc"] == "PENDING"

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')