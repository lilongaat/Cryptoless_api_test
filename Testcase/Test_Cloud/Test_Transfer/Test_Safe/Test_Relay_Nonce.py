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

# safe
@allure.feature("Transfers Success!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # GOERLI
            # ("GOERLI 多个safe账户构建+签名交易后同时广播","GOERLI","GoerliETH","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da",["0xf4c4b7803447dc6d3a00ed765e10fdb1bfa1ec23","0xacd5c6a98407469856b47d333309ed814fc64ebe","0x1dc8b303498e3fe1b4cc6f5ecf3b2976eaceae36","0x79f255cec4b987a4b4fd10858bc815a3b6134006","0x2bf894ab121035107337049d16ce793f161979a0"],"","0x2B0EfCF16EC1E4C5eD82dBB4Fce9B4811485e650",str(Conf.Config.random_amount(8))),
            ("GOERLI 多个safe账户构建+签名交易后,另外一个safe账户完成一笔交易后,同时广播之前的已签名交易","GOERLI","GoerliETH","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da",["0xf4c4b7803447dc6d3a00ed765e10fdb1bfa1ec23","0xacd5c6a98407469856b47d333309ed814fc64ebe","0x1dc8b303498e3fe1b4cc6f5ecf3b2976eaceae36","0x79f255cec4b987a4b4fd10858bc815a3b6134006","0x2bf894ab121035107337049d16ce793f161979a0"],"0xa491f7d4d19c4e3907910be05f19e78fbd97412b","0x2B0EfCF16EC1E4C5eD82dBB4Fce9B4811485e650",str(Conf.Config.random_amount(8))),
        ]
    elif env_type == 1: #生产
        test_data = [
            # ETH

            # BSC 

            # MATIC
        ]

    @allure.story("Custodial Transfers Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,privatekey,from_adds,from_other,to_add,amount', test_data)
    def test_custodial(self,test_title,networkCode,symbol,privatekey,from_adds,from_other,to_add,amount):

        ids = []
        hashs = []
        for n in range(len(from_adds)):

            with allure.step("浏览器查询from账户balance信息"):
                balance = Httpexplore.Balances_explore.query(networkCode,from_adds[n],symbol)
                    
            with allure.step("查询from账户holder信息"):
                holder = Http.HttpUtils.holders(networkCode=networkCode,symbol=symbol,address=from_adds[n])
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
                        "from":from_adds[n],
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
                # assert transfer.json()["_embedded"]["transactions"][0]["statusDesc"] == "SIGNING"

                id = transfer.json()["_embedded"]["transactions"][0]["id"]
                requiredSignings = transfer.json()["_embedded"]["transactions"][0]["requiredSignings"]
                signatures = []
                for i in range(len(requiredSignings)):
                    hash = requiredSignings[i]["hash"]
                    publickey = requiredSignings[i]["publicKeys"][0]
                    signature = {
                        "hash":hash,
                        "publicKey":publickey,
                        "signature":Conf.Config.sign(privatekey,hash)

                    }
                    signatures.append(signature)

            with allure.step("签名交易"):
                sign  =Http.HttpUtils.sign(id,signatures)
                assert sign.status_code == 200
                ids.append(id)

        logger.debug(ids)

        if len(from_other) == 0:
            pass
        else:
            with allure.step("构建交易——instructions"):
                body = {
                    "networkCode":networkCode,
                    "type":"transfer",
                    "body":{
                        "from":from_other,
                        "to":to_add,
                        "symbol":symbol,
                        "amount":amount
                    }
                }
                transfer = Http.HttpUtils.instructions(body)
                assert transfer.status_code == 200
                assert transfer.json()["_embedded"]["transactions"][0]["statusDesc"] == "SIGNING"

                id = transfer.json()["_embedded"]["transactions"][0]["id"]
                requiredSignings = transfer.json()["_embedded"]["transactions"][0]["requiredSignings"]
                signatures = []
                for i in range(len(requiredSignings)):
                    hash = requiredSignings[i]["hash"]
                    publickey = requiredSignings[i]["publicKeys"][0]
                    signature = {
                        "hash":hash,
                        "publicKey":publickey,
                        "signature":Conf.Config.sign(privatekey,hash)

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

        for m in range(len(ids)):
            with allure.step("广播交易"):
                send = Http.HttpUtils.send(ids[m])
                assert send.status_code == 200
                assert send.json()["statusDesc"] == "PENDING"

                hash = send.json()["hash"]
                hashs.append(hash)

        logger.debug(hashs)

        for i in range(len(ids)):
            with allure.step("通过id查询交易记录"):
                sleep(30)
                for n in range(10):
                    transaction = Http.HttpUtils.transactions_byid(ids[i])
                    assert transaction.status_code == 200
                    statusDesc = transaction.json()["statusDesc"]
                    if statusDesc == "SETTLED" and len(transaction.json()["balanceChanges"]) > 0:
                        break
                    else:
                        sleep(30)
                sleep(5)

        for j in range(len(from_adds)):
            with allure.step("浏览器查询from账户balance信息"):
                balance = Httpexplore.Balances_explore.query(networkCode,from_adds[j],symbol)
                    
            with allure.step("查询from账户holder信息"):
                holder = Http.HttpUtils.holders(networkCode=networkCode,symbol=symbol,address=from_adds[j])
                assert holder.status_code ==200
                quantity = Decimal(holder.json()["list"][0]["quantity"])

            logger.debug("浏览器查询账户balance为:" + str(balance))
            logger.debug("查询账户holder为:" + str(quantity))

            with allure.step("账户余额相等验证 浏览器查询==holder"):
                assert balance == quantity

        logger.debug("<-----并发交易ids---->")
        logger.debug(ids)
        logger.debug("<-----并发交易hashs---->")
        logger.debug(hashs)

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')