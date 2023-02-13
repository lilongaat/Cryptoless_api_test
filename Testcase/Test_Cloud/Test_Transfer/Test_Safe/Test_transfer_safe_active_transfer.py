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
from Common import Http, Httpexplore, Httpcore, Conf
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))

# safe
@allure.feature("Transfers!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # GOERLI 创建后 激活+转账
            ("GOERLI safe账户转账 nativecoin","GOERLI","GoerliETH","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113","0xacd5c6a98407469856b47d333309ed814fc64ebe","0xa7a9e710f9a3b4184d4f8b7d379cec262f2382c2","0.00023"),
            ("GOERLI safe账户转账 erc20coin","GOERLI","USDCC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113","0xacd5c6a98407469856b47d333309ed814fc64ebe","0xa7a9e710f9a3b4184d4f8b7d379cec262f2382c2","0.000123"),
        ]
    elif env_type == 1: #生产
        test_data = [
            # ETH

            # BSC

            # MATIC
        ]

    @allure.story("Safe Transfers&Active Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,privatekey,publickey,from_add,to_add,amount', test_data)
    def test_custodial(self,test_title,networkCode,symbol,privatekey,publickey,from_add,to_add,amount):

        with allure.step("创建安全账户"):
            acc = Http.HttpUtils.create_safe_account("safe",networkCode,publickey)
            assert acc.status_code == 200
            assert acc.json()["status"] == "inactive"
            from_add = acc.json()["address"]

        with allure.step("母账户转账nativecoin到多签账户"):
            Httpcore.HttpCoreUtils.core_parent_account_transfer_nativecoin(networkCode,from_add,"4000000000000000")

        with allure.step("母账户转账erc20coin:USDC到多签账户"):
            Httpcore.HttpCoreUtils.core_parent_account_transfer_erc20coin(networkCode,"0x1eC2CE6108240118Ff2c66eC8AFAC28618D7e066",from_add,"1000000000000000000")

        sleep(15)
        logger.debug("\n"+"safe账户" +"\n"+ from_add+"\n\n")

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
            del balance,quantity

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

        with allure.step("广播交易"):
            send = Http.HttpUtils.send(id)
            assert send.status_code == 200
            assert send.json()["statusDesc"] == "PENDING"

            hash = send.json()["hash"]

        
        # logger.debug("\n\n"+networkCode+"--"+symbol+"--"+test_title+"\n"+from_add+"--"+quantity+"\n"+hash+"\n\n")

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
            del balance,quantity

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')