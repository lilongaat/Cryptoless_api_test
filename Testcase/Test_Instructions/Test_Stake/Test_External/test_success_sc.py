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
from Common import Http, Conf
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))

# External
@allure.feature("Stake_Success!")
class Test_stake_success:
    if env_type == 0: #测试
        test_data = [
            # IRIS网络
            ("External账户IRIS质押",["d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b"],"IRIS","IRIS","stake","iaa1ed68xf6453t7u4ttsmphdrwqflx2l90e6ymuaq",str(Conf.Config.random_amount(4))),
            # ("External账户IRIS赎回",["d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b"],"IRIS","IRIS","unstake","iaa1ed68xf6453t7u4ttsmphdrwqflx2l90e6ymuaq",str(Conf.Config.random_amount(5))),
            # ("External账户IRISclaim",["d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b"],"IRIS","IRIS","claim","iaa1ed68xf6453t7u4ttsmphdrwqflx2l90e6ymuaq",0),
            # CLV网络
            ("External账户CLV质押",["7967c43bd3f3874ccfa6ff6ceda5faa8c699ad0fe2be33f44c8bb8abcb23a2fd"],"CLV","CLV","stake","5Hdmv7BeAe1XFJXso8oGMidGp186cb4uNTNMywp6fBY7UEsr",str(Conf.Config.random_amount(4))),
            # ("External账户CLV赎回",["7967c43bd3f3874ccfa6ff6ceda5faa8c699ad0fe2be33f44c8bb8abcb23a2fd"],"CLV","CLV","unstake","5Hdmv7BeAe1XFJXso8oGMidGp186cb4uNTNMywp6fBY7UEsr",str(Conf.Config.random_amount(5))),
            # ("External账户CLVclaim",["7967c43bd3f3874ccfa6ff6ceda5faa8c699ad0fe2be33f44c8bb8abcb23a2fd"],"CLV","CLV","claim","5Hdmv7BeAe1XFJXso8oGMidGp186cb4uNTNMywp6fBY7UEsr",0),
        ]
    if env_type == 1: #生产
        test_data = [
            # IRIS网络
            # ("External账户IRIS质押",["a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c"],"IRIS","IRIS","stake","iaa18j8rds5hqwp88s4qsrytq5w4eafu288cfza9th",str(Conf.Config.random_amount(4))),
            # ("External账户IRIS赎回",["a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c"],"IRIS","IRIS","unstake","iaa18j8rds5hqwp88s4qsrytq5w4eafu288cfza9th",str(Conf.Config.random_amount(5))),
            # ("External账户IRISclaim",["a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c"],"IRIS","IRIS","claim","iaa18j8rds5hqwp88s4qsrytq5w4eafu288cfza9th",0),
            # CLV网络
            # ("External账户CLV质押",["426a6690c29c5ee0052712c1fda0cc38691f3faf2a571f4b04c9705bbf3f921b"],"CLV","CLV","stake","5GF2XqzK1ERH6AGkyHz1jmMLMCVGBUEyRBxJb5TFWxhiS6EY",str(Conf.Config.random_amount(4))),
            # ("External账户CLV赎回",["426a6690c29c5ee0052712c1fda0cc38691f3faf2a571f4b04c9705bbf3f921b"],"CLV","CLV","unstake","5GF2XqzK1ERH6AGkyHz1jmMLMCVGBUEyRBxJb5TFWxhiS6EY",str(Conf.Config.random_amount(5))),
            # ("External账户CLVclaim",["426a6690c29c5ee0052712c1fda0cc38691f3faf2a571f4b04c9705bbf3f921b"],"CLV","CLV","claim","5GF2XqzK1ERH6AGkyHz1jmMLMCVGBUEyRBxJb5TFWxhiS6EY",0),
        ]

    @allure.story("Custodial_Stake_Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,networkCode,symbol,type,address,amount', test_data)
    def test_custodial(self,test_title,privatekey,networkCode,symbol,type,address,amount):

        with allure.step("查询账户holders信息"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,address)
            assert holders.status_code == 200

        with allure.step("查询账户staking信息"):
            staking = Http.HttpUtils.get_staking(networkCode,symbol,address)
            assert staking.status_code == 200

        with allure.step("构建交易——instructions"):
            if type == "claim":
                body = {
                    "delegator":address,
                    "coinSymbol":symbol,
                }
            else:
                body = {
                    "delegator":address,
                    "coinSymbol":symbol,
                    "amount":amount
                }
            transactionParams = {
                "memo":''.join(random.sample(string.ascii_letters + string.digits, 10))
            }
            stake = Http.HttpUtils.instructions(type,body,networkCode,[],transactionParams)

            assert stake.status_code == 200
            assert stake.json()["_embedded"]["transactions"][0]["status"] == "BUILDING"

            id = stake.json()["_embedded"]["transactions"][0]["id"]
            requiredSignings = stake.json()["_embedded"]["transactions"][0]["requiredSignings"]
            serialized = stake.json()["_embedded"]["transactions"][0]["serialized"]

            signatures = []
            for i in range(len(requiredSignings)):
                hash = requiredSignings[i]["hash"]
                publickey = requiredSignings[i]["publicKeys"][0]
                signature = {
                    "hash":hash,
                    "publicKey":publickey,
                    "signature":Conf.Config.sign(privatekey[0],hash)

                }
                signatures.append(signature)

        with allure.step("签名交易——instructions"):
            sign = Http.HttpUtils.sign(id,signatures,serialized)
            assert sign.status_code == 200
            assert sign.json()["status"] == "SIGNED"

            id = stake.json()["_embedded"]["transactions"][0]["id"]

        with allure.step("广播交易"):
            send = Http.HttpUtils.send(id)
            assert send.status_code == 200
            assert send.json()["status"] == "PENDING"


        sleep(20)
        with allure.step("查询账户holders信息"):
            holders_ = Http.HttpUtils.get_holders(networkCode,symbol,address)
            assert holders_.status_code == 200

        with allure.step("查询账户staking信息"):
            staking_ = Http.HttpUtils.get_staking(networkCode,symbol,address)
            assert staking_.status_code == 200

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')