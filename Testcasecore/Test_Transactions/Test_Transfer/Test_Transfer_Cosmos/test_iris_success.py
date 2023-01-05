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
            ("IRIS普通账户转账",["d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b"],"0260fbc9e026fe789a5a3c26289577719900c6046dc1d9ac1471b8eb08d15d0de4","IRIS","iaa1ed68xf6453t7u4ttsmphdrwqflx2l90e6ymuaq","iaa1ed68xf6453t7u4ttsmphdrwqflx2l90e6ymuaq","40"),
        ]
    elif env_type == 1: #生产
        test_data = []

    @allure.story("Transfer Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,publicKey,networkCode,fromaddress,toaddress,amount', test_data)
    def test_custodial(self,test_title,privatekey,publicKey,networkCode,fromaddress,toaddress,amount):

        with allure.step("Build交易"):
            body = {
                    "networkCode": networkCode,
                    "payload": {
                        "from": fromaddress,
                        "to": toaddress,
                        "pubKey":publicKey,
                        "amount":{
                            "denom":"uiris",
                            "amount":amount
                        },
                        "params":{
                            "fee":{
                                "gasPrice":"0.2uiris",
                            }
                        },
                    "memo": "mnwVYt5UjZ",
                    },
                    "type": "TRANSFER_TRANSACTION"
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
    print(path)
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')