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
from Common import Conf, Httpcore
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))

# safe
@allure.feature("Transfers Success!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            #CLV
            # ("CLV 2-2多签账户转账","CLV","CLV",["7967c43bd3f3874ccfa6ff6ceda5faa8c699ad0fe2be33f44c8bb8abcb23a2fd","7cc57c9ab4d60f6991dd32827927266c90a7c165db6c71ea344c86a05e582b68"],"5EwMcCvUPD7RKUTs86NoLPame9oCg8edtdKCdbcsxTFL3aTQ","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","0.000123456"),
            ("CLV 2-3多签账户转账","CLV","CLV",["7967c43bd3f3874ccfa6ff6ceda5faa8c699ad0fe2be33f44c8bb8abcb23a2fd","7cc57c9ab4d60f6991dd32827927266c90a7c165db6c71ea344c86a05e582b68"],"5HnsmbUfRH37XVXhz1JpDcyGHRmDZJNwnd2SP2M2urS6v71U","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","0.00023456"),
        ]
    elif env_type == 1: #生产
        test_data = []

    @allure.story("Custodial Transfers Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,privatekey,from_add,to_add,amount', test_data)
    def test_custodial(self,test_title,networkCode,symbol,privatekey,from_add,to_add,amount):

        with allure.step("查询账户holder信息"):
            holder = Httpcore.HttpCoreUtils.holder(networkCode=networkCode,symbol=symbol,address=from_add)
            assert holder.status_code ==200
            quantity = holder.json()["list"][0]["quantity"]

        with allure.step("构建交易——instructions"):
            body = {
                "networkCode":networkCode,
                "type":"transfer",
                "body":{
                    "from":from_add,
                    "to":to_add,
                    "symbol":symbol,
                    "amount":amount
                },
                "transactionParams":{
                    "memo":''.join(random.sample(string.ascii_letters + string.digits, 10))
                }
            }
            transfer = Httpcore.HttpCoreUtils.core_instructions(body)
            assert transfer.status_code == 200
            assert transfer.json()["_embedded"]["transactions"][0]["statusDesc"] == "BUILDING"

            id = transfer.json()["_embedded"]["transactions"][0]["id"]
            requiredSignings = transfer.json()["_embedded"]["transactions"][0]["requiredSignings"]
            signatures = []
            for i in range(len(requiredSignings)):
                hash = requiredSignings[i]["hash"]
                publickeys = requiredSignings[i]["publicKeys"]
                for j in range(len(publickeys)):
                    signature = {
                        "hash":hash,
                        "publicKey":publickeys[j],
                        "signature":Conf.Config.sign(privatekey[j],hash)

                    }
                    signatures.append(signature)

        with allure.step("签名交易"):
            sign  =Httpcore.HttpCoreUtils.core_sign(id,signatures)
            assert sign.status_code == 200

        with allure.step("广播交易"):
            send = Httpcore.HttpCoreUtils.core_send(id)
            assert send.status_code == 200
            assert send.json()["statusDesc"] == "PENDING"
            hash = send.json()["hash"]

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')