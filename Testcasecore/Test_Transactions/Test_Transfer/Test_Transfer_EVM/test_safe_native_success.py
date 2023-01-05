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
            #test_title                    #privatekey                                                                                                                            #publickey                                                                                                                                  #networkCode#privatekey_send                                                #publickey_send                                                      #address_send                                #from                                        #to                                          #value  #paytype
            # ("GOERLI多签账户自付转账nativecoin",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d"],["0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113","03c420167aaf4fc7106646b2fe485519e5569ceb1584ae31d62537e349a4e4b5a9"],"GOERLI","9cbca176aff8c48ebd9a27c31455e34ebc86e25a17e22b3d65a716fc851ada38","0326288a7bbff5dc672bfec0a0a02ccae3eeb3e93a0294c8e0f534c97438de0fce","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0xc06c78af1668fe747875698bec4b645982409945","0x6490C1b13A4576128159576F9d3acadF79e8dd6f","0x64","1"),
            ("GOERLI多签账户代付转账nativecoin",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d"],["0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113","03c420167aaf4fc7106646b2fe485519e5569ceb1584ae31d62537e349a4e4b5a9"],"GOERLI","9cbca176aff8c48ebd9a27c31455e34ebc86e25a17e22b3d65a716fc851ada38","0326288a7bbff5dc672bfec0a0a02ccae3eeb3e93a0294c8e0f534c97438de0fce","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0xc06c78af1668fe747875698bec4b645982409945","0x6490C1b13A4576128159576F9d3acadF79e8dd6f","0x64","2"),

            # ("MATIC多签账户转账nativecoin",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d"],["0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113","03c420167aaf4fc7106646b2fe485519e5569ceb1584ae31d62537e349a4e4b5a9"],"MATIC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113","0xe525E7cd17f6Dc950492755A089E452fd5d9d44f","0x6490C1b13A4576128159576F9d3acadF79e8dd6f","0x6490C1b13A4576128159576F9d3acadF79e8dd6f","0x64"),
        ]
    elif env_type == 1: #生产
        test_data = []

    @allure.story("Transfer Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,publickey,networkCode,privatekey_send,publickey_send,sendaddress,fromaddress,toaddress,value,payType', test_data)
    def test_custodial(self,test_title,privatekey,publickey,networkCode,privatekey_send,publickey_send,sendaddress,fromaddress,toaddress,value,payType):

        with allure.step("查询holders"):
            holder = Httpcore.HttpCoreUtils.holder(networkCode=networkCode,address=fromaddress)
            assert holder.status_code == 200

        with allure.step("Build交易"):
            body = {
                    "networkCode": networkCode,
                    "payload": {
                        "from": fromaddress,
                        "to":toaddress,
                        "value":value,
                        "senderPublicKey":publickey_send,
                        "payType":payType
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
                for j in range(len(requiredSignings[i]["publicKeys"])):
                    publickey = requiredSignings[i]["publicKeys"][j]
                    signature = {
                        "hash":hash,
                        "publicKey":publickey,
                        "signature":Conf.Config.sign(privatekey[j],hash)

                    }
                    signatures.append(signature)

        with allure.step("Sign交易"):
            sign = Httpcore.HttpCoreUtils.core_sign(id,signatures)
            assert sign.status_code == 200

        if payType == "2":
                id_ = sign.json()["id"]
                hash_ = sign.json()["requiredSignings"][0]["hash"]

                signatures_ = [{
                            "hash":hash_,
                            "publicKey":publickey_send,
                            "signature":Conf.Config.sign(privatekey_send,hash_)

                        }]

                with allure.step("Send Sign交易"):
                    sign_ = Httpcore.HttpCoreUtils.core_sign(id,signatures_)
                    assert sign_.status_code == 200

                with allure.step("广播交易"):
                    send = Httpcore.HttpCoreUtils.core_send(id_)
                    assert send.status_code == 200
        else:
            with allure.step("广播交易"):
                send = Httpcore.HttpCoreUtils.core_send(id)
                assert send.status_code == 200

        

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')