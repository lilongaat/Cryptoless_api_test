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
            #IRIS
            # ("IRIS 质押","IRIS","IRIS","stake",["d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b","e560c8c3353414a3339f17001c563cd816be808799889aa3827ea5465124a790"],"iaa1xul5lny6qp9vqqj42q9lm9rpy0lyafr80fx3h2","0.00123"),
            # ("IRIS 解除质押","IRIS","IRIS","un_stake",["d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b","e560c8c3353414a3339f17001c563cd816be808799889aa3827ea5465124a790"],"iaa1xul5lny6qp9vqqj42q9lm9rpy0lyafr80fx3h2","0.0012"),
            # ("IRIS 提取奖励","IRIS","IRIS","claim",["d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b","e560c8c3353414a3339f17001c563cd816be808799889aa3827ea5465124a790"],"iaa1xul5lny6qp9vqqj42q9lm9rpy0lyafr80fx3h2",""),

            #CLV
            ("CLV 质押","CLV","CLV","stake",["7967c43bd3f3874ccfa6ff6ceda5faa8c699ad0fe2be33f44c8bb8abcb23a2fd","7cc57c9ab4d60f6991dd32827927266c90a7c165db6c71ea344c86a05e582b68"],"5EwMcCvUPD7RKUTs86NoLPame9oCg8edtdKCdbcsxTFL3aTQ","0.00123"),
            # ("CLV 解除质押","CLV","CLV","un_stake",["7967c43bd3f3874ccfa6ff6ceda5faa8c699ad0fe2be33f44c8bb8abcb23a2fd","7cc57c9ab4d60f6991dd32827927266c90a7c165db6c71ea344c86a05e582b68"],"5EwMcCvUPD7RKUTs86NoLPame9oCg8edtdKCdbcsxTFL3aTQ","0.00123"),
            # ("CLV 提取奖励","CLV","CLV","claim",["7967c43bd3f3874ccfa6ff6ceda5faa8c699ad0fe2be33f44c8bb8abcb23a2fd","7cc57c9ab4d60f6991dd32827927266c90a7c165db6c71ea344c86a05e582b68"],"5EwMcCvUPD7RKUTs86NoLPame9oCg8edtdKCdbcsxTFL3aTQ",""),
        ]
    elif env_type == 1: #生产
        test_data = []

    @allure.story("Custodial Transfers Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,type,privatekey,address,amount', test_data)
    def test_custodial(self,test_title,networkCode,symbol,type,privatekey,address,amount):

        with allure.step("core查询账户holder信息"):
            holder = Httpcore.HttpCoreUtils.holder(networkCode=networkCode,symbol=symbol,address=address)
            assert holder.status_code ==200
            quantity = holder.json()["list"][0]["quantity"]

        with allure.step("core查询账户质押信息"):
            delegated = Httpcore.HttpCoreUtils.core_delegators(networkCode,address)
            assert delegated.status_code ==200
            delegated = delegated.json()[0]["staked"]

        with allure.step("core构建交易——stake"):
            if type == "stake" or type == "un_stake":
                body_ = {
                    "delegator":address,
                    "coinSymbol":symbol,
                    "amount":amount
                }
            elif type == "claim":
                body_ = {
                    "delegator":address,
                    "coinSymbol":symbol
                }
            body = {
                "networkCode":networkCode,
                "type":type,
                "body":body_
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
            sign = Httpcore.HttpCoreUtils.core_sign(id,signatures)
            assert sign.status_code == 200

        with allure.step("广播交易"):
            send = Httpcore.HttpCoreUtils.core_send(id)
            assert send.status_code == 200
            assert send.json()["statusDesc"] == "PENDING"

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')