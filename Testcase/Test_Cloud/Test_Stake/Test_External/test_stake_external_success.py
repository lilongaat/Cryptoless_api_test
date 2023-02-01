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
from Common import Http, Httpexplore ,Conf
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))

# External
@allure.feature("Stake!")
class Test_stake_success:
    if env_type == 0: #测试
        test_data = [
            # IRIS
            ("IRIS External账户质押","IRIS","IRIS","stake","d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b","iaa1ed68xf6453t7u4ttsmphdrwqflx2l90e6ymuaq",str(Conf.Config.random_amount(4))),
            ("IRIS External账户赎回","IRIS","IRIS","un_stake","d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b","iaa1ed68xf6453t7u4ttsmphdrwqflx2l90e6ymuaq",str(Conf.Config.random_amount(5))),
            ("IRIS External账户claim","IRIS","IRIS","claim","d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b","iaa1ed68xf6453t7u4ttsmphdrwqflx2l90e6ymuaq",0),

            # CLV
            ("CLV External账户质押","CLV","CLV","stake","7967c43bd3f3874ccfa6ff6ceda5faa8c699ad0fe2be33f44c8bb8abcb23a2fd","5Hdmv7BeAe1XFJXso8oGMidGp186cb4uNTNMywp6fBY7UEsr",str(Conf.Config.random_amount(4))),
            ("CLV External账户赎回","CLV","CLV","un_stake","7967c43bd3f3874ccfa6ff6ceda5faa8c699ad0fe2be33f44c8bb8abcb23a2fd","5Hdmv7BeAe1XFJXso8oGMidGp186cb4uNTNMywp6fBY7UEsr",str(Conf.Config.random_amount(5))),
            ("CLV External账户claim","CLV","CLV","claim","7967c43bd3f3874ccfa6ff6ceda5faa8c699ad0fe2be33f44c8bb8abcb23a2fd","5Hdmv7BeAe1XFJXso8oGMidGp186cb4uNTNMywp6fBY7UEsr",0),
        ]
    if env_type == 1: #生产
        test_data = [
            # ATOM
            ("ATOM External账户质押","ATOM","ATOM","stake","4b49226b1669a687fb4f8479fa9048f1cbb79af74529a47bae7a0c07ce97f8c6","cosmos1uxezv8wcd44hp340acnmrqhcnzau4wzhlshcag",str(Conf.Config.random_amount(4))),
            ("ATOM External账户赎回","ATOM","ATOM","un_stake","4b49226b1669a687fb4f8479fa9048f1cbb79af74529a47bae7a0c07ce97f8c6","cosmos1uxezv8wcd44hp340acnmrqhcnzau4wzhlshcag",str(Conf.Config.random_amount(5))),
            ("ATOM External账户claim","ATOM","ATOM","claim","4b49226b1669a687fb4f8479fa9048f1cbb79af74529a47bae7a0c07ce97f8c6","cosmos1uxezv8wcd44hp340acnmrqhcnzau4wzhlshcag",0),

            # IRIS
            ("IRIS External账户质押","IRIS","IRIS","stake","a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c","iaa18j8rds5hqwp88s4qsrytq5w4eafu288cfza9th",str(Conf.Config.random_amount(4))),
            ("IRIS External账户赎回","IRIS","IRIS","un_stake","a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c","iaa18j8rds5hqwp88s4qsrytq5w4eafu288cfza9th",str(Conf.Config.random_amount(5))),
            ("IRIS External账户claim","IRIS","IRIS","claim","a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c","iaa18j8rds5hqwp88s4qsrytq5w4eafu288cfza9th",0),

            # DOT

            # CLV
            ("CLV External账户质押","CLV","CLV","stake","426a6690c29c5ee0052712c1fda0cc38691f3faf2a571f4b04c9705bbf3f921b","5GF2XqzK1ERH6AGkyHz1jmMLMCVGBUEyRBxJb5TFWxhiS6EY",str(Conf.Config.random_amount(4))),
            ("CLV External账户赎回","CLV","CLV","un_stake","426a6690c29c5ee0052712c1fda0cc38691f3faf2a571f4b04c9705bbf3f921b","5GF2XqzK1ERH6AGkyHz1jmMLMCVGBUEyRBxJb5TFWxhiS6EY",str(Conf.Config.random_amount(5))),
            ("CLV External账户claim","CLV","CLV","claim","426a6690c29c5ee0052712c1fda0cc38691f3faf2a571f4b04c9705bbf3f921b","5GF2XqzK1ERH6AGkyHz1jmMLMCVGBUEyRBxJb5TFWxhiS6EY",0),
        ]

    @allure.story("External_Stake_Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,type,privatekey,address,amount', test_data)
    def test_External(self,test_title,networkCode,symbol,type,privatekey,address,amount):

        with allure.step("浏览器查询from账户balance信息"):
            balance = Httpexplore.Balances_explore.query(networkCode,address,symbol)

        with allure.step("查询from账户holder信息"):
            holder = Http.HttpUtils.holders(networkCode=networkCode,symbol=symbol,address=address)
            assert holder.status_code ==200
            quantity = Decimal(holder.json()["list"][0]["quantity"])

        logger.debug("浏览器查询账户balance为:" + str(balance))
        logger.debug("查询账户holder为:" + str(quantity))

        with allure.step("账户余额相等验证 浏览器查询==holder"):
            assert balance == quantity

        with allure.step("查询账户staking信息"):
            staking = Http.HttpUtils.staking(networkCode,address)
            assert staking.status_code == 200

        with allure.step("构建交易——instructions"):
            if type == "claim":
                body = {
                    "networkCode": networkCode,
                    "type": type,
                    "body": {
                        "delegator":address,
                        "coinSymbol":symbol
                    },
                    "transactionParams":{
                        "memo":''.join(random.sample(string.ascii_letters + string.digits, 10))
                    }
                }
            else:
                body = {
                    "networkCode": networkCode,
                    "type": type,
                    "body": {
                        "delegator":address,
                        "coinSymbol":symbol,
                        "amount":amount
                    },
                    "transactionParams":{
                        "memo":''.join(random.sample(string.ascii_letters + string.digits, 10))
                    }
                }

            stake = Http.HttpUtils.instructions(body)

            assert stake.status_code == 200
            assert stake.json()["_embedded"]["transactions"][0]["statusDesc"] == "BUILDING"

            id = stake.json()["_embedded"]["transactions"][0]["id"]
            requiredSignings = stake.json()["_embedded"]["transactions"][0]["requiredSignings"]
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
            balance = Httpexplore.Balances_explore.query(networkCode,address,symbol)
                
        with allure.step("查询from账户holder信息"):
            holder = Http.HttpUtils.holders(networkCode=networkCode,symbol=symbol,address=address)
            assert holder.status_code ==200
            quantity = Decimal(holder.json()["list"][0]["quantity"])

        logger.debug("浏览器查询账户balance为:" + str(balance))
        logger.debug("查询账户holder为:" + str(quantity))

        with allure.step("账户余额相等验证 浏览器查询==holder"):
            assert balance == quantity


        with allure.step("查询账户staking信息"):
            staking = Http.HttpUtils.staking(networkCode,address)
            assert staking.status_code == 200

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')