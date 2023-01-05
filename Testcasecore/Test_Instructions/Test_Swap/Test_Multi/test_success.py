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
            # 0x3ae919f24e9d5651dca65facd2948316fdbc4d85
            # ("MATIC SWAP:MATIC->USDC","MATIC",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d"],"0x3ccd8840a33ea13fd527a018af04efdfa37faade","MATIC","USDC","1","0.00012",2,"9cbca176aff8c48ebd9a27c31455e34ebc86e25a17e22b3d65a716fc851ada38","0326288a7bbff5dc672bfec0a0a02ccae3eeb3e93a0294c8e0f534c97438de0fce"),
            # ("MATIC SWAP:USDC->MATIC","MATIC",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d"],"0x3ccd8840a33ea13fd527a018af04efdfa37faade","USDC","MATIC","1","0.000123",2,"9cbca176aff8c48ebd9a27c31455e34ebc86e25a17e22b3d65a716fc851ada38","0326288a7bbff5dc672bfec0a0a02ccae3eeb3e93a0294c8e0f534c97438de0fce"),

            # MATIC 激活+swap
            ("MATIC SWAP:MATIC->USDC","MATIC",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d"],"0x52367b0a7527e0f1fcdec85700c6e2af61977ae7","MATIC","USDC","1","0.00012",2,"9cbca176aff8c48ebd9a27c31455e34ebc86e25a17e22b3d65a716fc851ada38","0326288a7bbff5dc672bfec0a0a02ccae3eeb3e93a0294c8e0f534c97438de0fce"),
            # ("MATIC SWAP:USDC->MATIC","MATIC",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d"],"0x52367b0a7527e0f1fcdec85700c6e2af61977ae7","USDC","MATIC","1","0.000123",2,"9cbca176aff8c48ebd9a27c31455e34ebc86e25a17e22b3d65a716fc851ada38","0326288a7bbff5dc672bfec0a0a02ccae3eeb3e93a0294c8e0f534c97438de0fce"),
        ]
    elif env_type == 1: #生产
        test_data = []

    @allure.story("Custodial Transfers Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,privatekey,address,from_coin,to_coin,slippage,fromamount,paytype,privatekey_send,publickey_send', test_data)
    def test_custodial(self,test_title,networkCode,privatekey,address,from_coin,to_coin,slippage,fromamount,paytype,privatekey_send,publickey_send):

        with allure.step("core查询账户holder信息"):
            holder = Httpcore.HttpCoreUtils.holder(networkCode=networkCode,symbol=from_coin,address=address)
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
                "paytype":paytype,
                "senderPublicKey":publickey_send,
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
                publicKeys = requiredSignings[i]["publicKeys"]
                for j in range(len(publicKeys)):
                    signature = {
                        "hash":hash,
                        "publicKey":publicKeys[j],
                        "signature":Conf.Config.sign(privatekey[j],hash)

                    }
                    signatures.append(signature)

        with allure.step("签名交易"):
            sign = Httpcore.HttpCoreUtils.core_sign(id,signatures)
            assert sign.status_code == 200

        if paytype == 1 or paytype == 2:
            id = sign.json()["id"]
            requiredSignings = sign.json()["requiredSignings"]
            signatures = {
                        "hash":requiredSignings[0]["hash"],
                        "publicKey":requiredSignings[0]["publicKeys"][0],
                        "signature":Conf.Config.sign(privatekey_send,requiredSignings[0]["hash"])

                    }

            sign_ = Httpcore.HttpCoreUtils.core_sign(id,signatures)
            assert sign_.status_code == 200
        elif paytype == 3:
            pass

        with allure.step("广播交易"):
            send = Httpcore.HttpCoreUtils.core_send(id)
            assert send.status_code == 200
            assert send.json()["statusDesc"] == "PENDING"

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')