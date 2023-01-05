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
from Common import Http, Conf, Httpcore
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))

# safe
@allure.feature("Transfers Success!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # GOERLI
            ("GOERLI share账户转账 nativecoin",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d"],["0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113","03c420167aaf4fc7106646b2fe485519e5569ceb1584ae31d62537e349a4e4b5a9"],"GOERLI","goerliETH","0x24ca55d569ca99ae648949147ccb3e0024ec1098",["0x24ca55d569ca99ae648949147ccb3e0024ec1098"],["0x64"]),
            # ("GOERLI share账户批量转账 nativecoin",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d"],["0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113","03c420167aaf4fc7106646b2fe485519e5569ceb1584ae31d62537e349a4e4b5a9"],"GOERLI","goerliETH","0x24ca55d569ca99ae648949147ccb3e0024ec1098",["0x24ca55d569ca99ae648949147ccb3e0024ec1098","0x24ca55d569ca99ae648949147ccb3e0024ec1098","0x24ca55d569ca99ae648949147ccb3e0024ec1098"],["0x0","0x1","0x64"]),
        ]
    elif env_type == 1: #生产
        test_data = []

    @allure.story("Safe Transfers Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,publickey,networkCode,symbol,from_add,to_adds,values', test_data)
    def test_safe(self,test_title,privatekey,publickey,networkCode,symbol,from_add,to_adds,values):

        if len(to_adds) == 1: #普通转账
            payload = {
                "from":from_add,
                "to":to_adds[0],
                "value":values[0]
                }
            type = "TRANSACTION"
        elif len(to_adds) > 1: #批量转账
            calls =[]
            for i in range(len(to_adds)):
                call = {
                    "to":to_adds[i],
                    "value":values[i]
                }
                calls.append(call)

            payload = {
                "from":from_add,
                "calls":calls
                }
            type = "MULTISEND_TRANSACTION"


        with allure.step("构建交易——transactions"):
                body = {
                    "networkCode":networkCode,
                    "payload":payload,
                    "type":type
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
                        "publicKey":requiredSignings[i]["publicKeys"][i],
                        "signature":Conf.Config.sign(privatekey[i],hash)

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