import json
import random
import string
from time import sleep
from decimal import Decimal
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
from Common import Httpcore, Conf
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))


@allure.feature("Transfer Success!")
class Test_transfer_success:
    if env_type == 0: #测试
        test_data = [
            ("GOERLI普通账户转账nativecoin",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da"],"GOERLI","0xe525e7cd17f6dc950492755a089e452fd5d9d44f","0xa7A9E710f9A3B4184D4F8B7d379CEC262f2382c2","0x64"),
            # ("MATIC普通账户转账nativecoin",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da"],"MATIC","0xe525e7cd17f6dc950492755a089e452fd5d9d44f","0xa7A9E710f9A3B4184D4F8B7d379CEC262f2382c2","0x64"),
        ]
    elif env_type == 1: #生产
        test_data = []

    @allure.story("Transfer Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,networkCode,fromaddress,toaddress,value', test_data)
    def test_custodial(self,test_title,privatekey,networkCode,fromaddress,toaddress,value):

        with allure.step("查询holders"):
            holder = Httpcore.HttpCoreUtils.holder(networkCode=networkCode,address=fromaddress)
            assert holder.status_code == 200

        with allure.step("Build交易"):
            body = {
                    "networkCode": networkCode,
                    "payload": {
                        "from": fromaddress,
                        "to": toaddress,
                        "value": value
                    },
                    "type": "TRANSACTION"
                }

            ts = Httpcore.HttpCoreUtils.core_build(body)
            assert ts.status_code == 200
            id = ts.json()["id"]
            requiredSignings = ts.json()["requiredSignings"]
            signatures = []
            for i in range(len(requiredSignings)):
                hash = requiredSignings[i]["hash"]
                publickey = requiredSignings[i]["publicKeys"][0]
                signature = {
                    "hash":hash,
                    "publicKey":publickey,
                    "signature":Conf.Config.sign(privatekey[0],hash)

                }
                signatures.append(signature)

        with allure.step("Sign交易"):
            sign = Httpcore.HttpCoreUtils.core_sign(id,signatures)
            assert sign.status_code == 200

        with allure.step("广播交易"):
            send = Httpcore.HttpCoreUtils.core_send(id)
            assert send.status_code == 200

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')