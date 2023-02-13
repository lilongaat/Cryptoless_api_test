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
            # GOERLI
            # ("GOERLI 2-2多签账户+代付+不指定签名key+指定外部sender+转账nativecoin","GOERLI","GoerliETH",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d"],[],"0x0ff50b272f22a7ded84fd2b6dc1c98f039165fd2","0x2B0EfCF16EC1E4C5eD82dBB4Fce9B4811485e650","0.00012",1,"9cbca176aff8c48ebd9a27c31455e34ebc86e25a17e22b3d65a716fc851ada38","0326288a7bbff5dc672bfec0a0a02ccae3eeb3e93a0294c8e0f534c97438de0fce"),
            # ("GOERLI 2-2多签账户+自付+不指定签名key+指定外部sender+转账nativecoin","GOERLI","GoerliETH",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d"],[],"0x0ff50b272f22a7ded84fd2b6dc1c98f039165fd2","0x2B0EfCF16EC1E4C5eD82dBB4Fce9B4811485e650","0.00012",2,"9cbca176aff8c48ebd9a27c31455e34ebc86e25a17e22b3d65a716fc851ada38","0326288a7bbff5dc672bfec0a0a02ccae3eeb3e93a0294c8e0f534c97438de0fce"),
            # ("GOERLI 2-2多签账户+自付+指定第一个签名key+指定自己sender+转账nativecoin","GOERLI","GoerliETH",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d"],["0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113"],"0x0ff50b272f22a7ded84fd2b6dc1c98f039165fd2","0x2B0EfCF16EC1E4C5eD82dBB4Fce9B4811485e650","0.00012",2,"dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113"),
            # ("GOERLI 2-2多签账户+自付+指定第二个签名key+指定自己sender+转账nativecoin","GOERLI","GoerliETH",["0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da"],["03c420167aaf4fc7106646b2fe485519e5569ceb1584ae31d62537e349a4e4b5a9"],"0x0ff50b272f22a7ded84fd2b6dc1c98f039165fd2","0x2B0EfCF16EC1E4C5eD82dBB4Fce9B4811485e650","0.00012",2,"dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113"),
            ("GOERLI 2-2多签账户+自付+指定两个签名key+指定自己sender+转账nativecoin","GOERLI","GoerliETH",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d"],["0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113","03c420167aaf4fc7106646b2fe485519e5569ceb1584ae31d62537e349a4e4b5a9"],"0x0ff50b272f22a7ded84fd2b6dc1c98f039165fd2","0x2B0EfCF16EC1E4C5eD82dBB4Fce9B4811485e650","0.00012",2,"dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113"),
            # ("GOERLI 2-2多签账户+代付+不指定签名key+指定自己sender+转账nativecoin","GOERLI","GoerliETH",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d"],[],"0x0ff50b272f22a7ded84fd2b6dc1c98f039165fd2","0x2B0EfCF16EC1E4C5eD82dBB4Fce9B4811485e650","0.00012",1,"dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113"),
            # ("GOERLI 2-2多签账户+自付+不指定签名key+指定自己sender+转账nativecoin","GOERLI","GoerliETH",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d"],[],"0x0ff50b272f22a7ded84fd2b6dc1c98f039165fd2","0x2B0EfCF16EC1E4C5eD82dBB4Fce9B4811485e650","0.00012",2,"dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113"),
        ]
    elif env_type == 1: #生产
        test_data = []

    @allure.story("Custodial Transfers Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,privatekey,definiteSignerPublicKeys,from_add,to_add,amount,paytype,senderPrivatekey,senderPublicKey', test_data)
    def test_custodial(self,test_title,networkCode,symbol,privatekey,definiteSignerPublicKeys,from_add,to_add,amount,paytype,senderPrivatekey,senderPublicKey):

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
                    "amount":amount,
                },
                "paytype":paytype,
                "senderPublicKey":senderPublicKey,
                "definiteSignerPublicKeys":definiteSignerPublicKeys,
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
            sign  = Httpcore.HttpCoreUtils.core_sign(id,signatures)
            assert sign.status_code == 200

        with allure.step("send签名交易"):
            id = sign.json()["id"]
            requiredSignings = sign.json()["requiredSignings"]
            signatures = {
                        "hash":requiredSignings[0]["hash"],
                        "publicKey":requiredSignings[0]["publicKeys"][0],
                        "signature":Conf.Config.sign(senderPrivatekey,requiredSignings[0]["hash"])

                    }

            sign_ = Httpcore.HttpCoreUtils.core_sign(id,signatures)
            assert sign_.status_code == 200

        with allure.step("广播交易"):
            send = Httpcore.HttpCoreUtils.core_send(id)
            assert send.status_code == 200
            assert send.json()["statusDesc"] == "PENDING"

            hash = send.json()["hash"]

        
        # logger.error("\n\n"+networkCode+"--"+symbol+"--"+test_title+"\n"+from_add+"--"+quantity+"\n"+hash+"\n\n")

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')