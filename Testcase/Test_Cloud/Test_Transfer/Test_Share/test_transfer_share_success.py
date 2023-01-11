from decimal import Decimal
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
from Common import Http, Httpexplore, Conf
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))

# share
@allure.feature("Transfers Success!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # BTC
            ("BTC 2-2share账户转账","BTC","BTC",["320e15269f5d12054ff67dbe1e7984c6af2f58db8f4ca3f429e98fe6a01c9e47","b61190f8b2fcb4754ff8527f083bb3df68bf89285d7c5e428276f5f4572b7abe"],"tb1q4t8jtp4fwjg4spfjh7ux5ckhrallj652kwrj48gcvd0rt5g9ea3q4vlm33","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq","0.000001"),
            ("BTC 3-4share账户转账","BTC","BTC",["320e15269f5d12054ff67dbe1e7984c6af2f58db8f4ca3f429e98fe6a01c9e47","cb9a013a1eb2aa7e5ce8303f7700c8b6da6bc661ec0c3cb72954be0e09532ad7","b61190f8b2fcb4754ff8527f083bb3df68bf89285d7c5e428276f5f4572b7abe"],"tb1qear90rkncgh46gdh39k42y77xpd6uawfkxh0xw8puz6jdmsys8hs66yacu","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq","0.000001"),

            # GOERLI
            ("GOERLI 2-2share账户转账 nativecoin","GOERLI","GoerliETH",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d"],"0x24ca55d569ca99ae648949147ccb3e0024ec1098","0xa7A9E710f9A3B4184D4F8B7d379CEC262f2382c2","0.00012"),
            ("GOERLI 2-2share账户转账 erc20coin","GOERLI","USDCC",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d"],"0x24ca55d569ca99ae648949147ccb3e0024ec1098","0xa7A9E710f9A3B4184D4F8B7d379CEC262f2382c2","0.000123"),
            ("GOERLI 3-4share账户转账 nativecoin","GOERLI","GoerliETH",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","7534dc589c84575f6fb1478e19b1a982a45d8712133996be167455258b7caec1","0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d"],"0xe10e947a35a06eecab6ab6cba14936720bfab54a","0xa7A9E710f9A3B4184D4F8B7d379CEC262f2382c2","0.00012"),
            ("GOERLI 3-4share账户转账 erc20coin","GOERLI","USDCC",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","7534dc589c84575f6fb1478e19b1a982a45d8712133996be167455258b7caec1","0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d"],"0xe10e947a35a06eecab6ab6cba14936720bfab54a","0xa7A9E710f9A3B4184D4F8B7d379CEC262f2382c2","0.000123"),

            # MATIC
            # ("MATIC 2-2share账户转账 nativecoin","MATIC","MATIC",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d"],"0xa374f6ac3df090035f9a3b0993b5eeddad29b949","0x3d7f18ad2cea9b59e54dfaf09b327c1ccd899591","0.00012"),
            # ("MATIC 2-2share账户转账 erc20coin","MATIC","USDC",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d"],"0xa374f6ac3df090035f9a3b0993b5eeddad29b949","0x3d7f18ad2cea9b59e54dfaf09b327c1ccd899591","0.000123"),

            # IRIS
            ("IRIS 2-2shared账户转账","IRIS","IRIS",["d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b","e560c8c3353414a3339f17001c563cd816be808799889aa3827ea5465124a790"],"iaa1xul5lny6qp9vqqj42q9lm9rpy0lyafr80fx3h2","iaa15h0lvaa6slvj0hg4d64548j2c5fds2zv8tkvgs","0.000015"),
            ("IRIS 3-4shared账户转账","IRIS","IRIS",["d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b","e560c8c3353414a3339f17001c563cd816be808799889aa3827ea5465124a790","dfa7ef6ccec876014f4a5b00393404268d8de04ef190fdc14383fd8be8afc708"],"iaa15kv39f7hepkqlsyqx5v8ye28743xnfrkzngfgu","iaa15h0lvaa6slvj0hg4d64548j2c5fds2zv8tkvgs","0.000015"),

            # CLV
            ("CLV 2-2shared账户转账","CLV","CLV",["7967c43bd3f3874ccfa6ff6ceda5faa8c699ad0fe2be33f44c8bb8abcb23a2fd","7cc57c9ab4d60f6991dd32827927266c90a7c165db6c71ea344c86a05e582b68"],"5EwMcCvUPD7RKUTs86NoLPame9oCg8edtdKCdbcsxTFL3aTQ","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","0.000016"),
            ("CLV 3-4shared账户转账","CLV","CLV",["7967c43bd3f3874ccfa6ff6ceda5faa8c699ad0fe2be33f44c8bb8abcb23a2fd","7cc57c9ab4d60f6991dd32827927266c90a7c165db6c71ea344c86a05e582b68","b7eb71a716e21bbc82bce03318c386cacb64b2b8eab0b341749b4aed92fc5136"],"5DyVmFJSPXRu4Ufv1Q46y1w7MejCpS5VrLvJwXKNMppzg9Nk","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","0.0000161"),
        ]
    elif env_type == 1: #生产
        test_data = []

    @allure.story("Custodial Transfers Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,privatekey,from_add,to_add,amount', test_data)
    def test_custodial(self,test_title,networkCode,symbol,privatekey,from_add,to_add,amount):

        with allure.step("浏览器查询from账户balance信息"):
            balance = Httpexplore.Balances_explore.query(networkCode,from_add,symbol)
                
        with allure.step("查询from账户holder信息"):
            holder = Http.HttpUtils.holders(networkCode=networkCode,symbol=symbol,address=from_add)
            assert holder.status_code ==200
            quantity = Decimal(holder.json()["list"][0]["quantity"])

        logger.debug("浏览器查询账户balance为:" + str(balance))
        logger.debug("查询账户holder为:" + str(quantity))

        with allure.step("账户余额相等验证 浏览器查询==holder"):
            assert balance == quantity

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
            transfer = Http.HttpUtils.instructions(body)
            assert transfer.status_code == 200
            assert transfer.json()["_embedded"]["transactions"][0]["statusDesc"] == "BUILDING"

            id = transfer.json()["_embedded"]["transactions"][0]["id"]
            requiredSignings = transfer.json()["_embedded"]["transactions"][0]["requiredSignings"]
            signatures = []
            for i in range(len(requiredSignings)):
                hash = requiredSignings[i]["hash"]
                publickeys = requiredSignings[i]["publicKeys"]
                threshold = requiredSignings[i]["threshold"]
                for j in range(threshold):
                    signature = {
                        "hash":hash,
                        "publicKey":publickeys[j],
                        "signature":Conf.Config.sign(privatekey[j],hash)

                    }
                    signatures.append(signature)

        with allure.step("签名交易"):
            sign  =Http.HttpUtils.sign(id,signatures)
            assert sign.status_code == 200

        with allure.step("广播交易"):
            send = Http.HttpUtils.send(id)
            assert send.status_code == 200
            assert send.json()["statusDesc"] == "PENDING"

            hash = send.json()["hash"]

        # logger.error("\n\n"+networkCode+"--"+symbol+"--"+test_title+"\n"+from_add+"--"+quantity+"\n"+hash+"\n\n")

        with allure.step("通过id查询交易记录"):
            sleep(30)
            for n in range(10):
                transaction = Http.HttpUtils.transactions_byid(id)
                assert transaction.status_code == 200
                statusDesc = transaction.json()["statusDesc"]
                if statusDesc == "SETTLED" and len(transaction.json()["balanceChanges"]) > 0:
                    break
                else:
                    sleep(30)
            sleep(5)

        with allure.step("浏览器查询from账户balance信息"):
            balance = Httpexplore.Balances_explore.query(networkCode,from_add,symbol)
                
        with allure.step("查询from账户holder信息"):
            holder = Http.HttpUtils.holders(networkCode=networkCode,symbol=symbol,address=from_add)
            assert holder.status_code ==200
            quantity = Decimal(holder.json()["list"][0]["quantity"])

        logger.debug("浏览器查询账户balance为:" + str(balance))
        logger.debug("查询账户holder为:" + str(quantity))

        with allure.step("账户余额相等验证 浏览器查询==holder"):
            assert balance == quantity


if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')