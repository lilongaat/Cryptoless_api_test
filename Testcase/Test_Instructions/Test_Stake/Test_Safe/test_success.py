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

# safe
@allure.feature("Stake_Success!")
class Test_stake_success:
    if env_type == 0: #测试
        test_data = [
            # IRIS网络2-2
            # ("Safe2-2账户IRIS质押",["d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b"],"IRIS","IRIS","stake","iaa1x5m8vh53addgrdtnsxc07tryn46f9d7x4q3p40",str(Conf.Config.random_amount(4))),
            # ("Safe2-2账户IRIS赎回",["d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b"],"IRIS","IRIS","unstake","iaa1x5m8vh53addgrdtnsxc07tryn46f9d7x4q3p40",str(Conf.Config.random_amount(5))),
            # ("Safe2-2账户IRIS赎回",["d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b"],"IRIS","IRIS","claim","iaa1x5m8vh53addgrdtnsxc07tryn46f9d7x4q3p40",0),
            # IRIS网络2-3
            ("Safe2-3账户IRIS质押",["d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b"],"IRIS","IRIS","stake","iaa1rflt7r2qz7sv83dtt3kgek5a05g9dghshkjjdu",str(Conf.Config.random_amount(4))),
            # ("Safe2-3账户IRIS赎回",["d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b"],"IRIS","IRIS","unstake","iaa1rflt7r2qz7sv83dtt3kgek5a05g9dghshkjjdu",str(Conf.Config.random_amount(5))),
            # ("Safe2-3账户IRIS赎回",["d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b"],"IRIS","IRIS","claim","iaa1rflt7r2qz7sv83dtt3kgek5a05g9dghshkjjdu",0),
            # CLV网络
            # ("Safe2-2账户CLV质押",["426a6690c29c5ee0052712c1fda0cc38691f3faf2a571f4b04c9705bbf3f921b"],"CLV","CLV","stake","5Eud43L2RufGoFQpsJjeGYPiyKdYd5JMNWy81RjzeBknXHgG",str(Conf.Config.random_amount(4))),
            # ("Safe2-2账户CLV赎回",["426a6690c29c5ee0052712c1fda0cc38691f3faf2a571f4b04c9705bbf3f921b"],"CLV","CLV","unstake","5Eud43L2RufGoFQpsJjeGYPiyKdYd5JMNWy81RjzeBknXHgG",str(Conf.Config.random_amount(5))),
            # ("Safe2-2账户CLV赎回",["426a6690c29c5ee0052712c1fda0cc38691f3faf2a571f4b04c9705bbf3f921b"],"CLV","CLV","claim","5Eud43L2RufGoFQpsJjeGYPiyKdYd5JMNWy81RjzeBknXHgG",0),
        ]
    if env_type == 1: #生产
        test_data = [
            # IRIS网络2-2
            ("Safe2-2账户IRIS质押",["a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c"],"IRIS","IRIS","stake","iaa1mmdw5mw2nw9wvqrzjzarkt46pkfn2n5hwpwz0w",str(Conf.Config.random_amount(4))),
            # ("Safe2-2账户IRIS赎回",["a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c"],"IRIS","IRIS","unstake","iaa1mmdw5mw2nw9wvqrzjzarkt46pkfn2n5hwpwz0w",str(Conf.Config.random_amount(5))),
            # ("Safe2-2账户IRIS赎回",["a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c"],"IRIS","IRIS","claim","iaa1mmdw5mw2nw9wvqrzjzarkt46pkfn2n5hwpwz0w",0),
            # IRIS网络2-3
            # ("Safe2-3账户IRIS质押",["a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c"],"IRIS","IRIS","stake","iaa1n367xt7536vhcxrnjx60na77afw2dzecxlmnah",str(Conf.Config.random_amount(4))),
            # ("Safe2-3账户IRIS赎回",["a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c"],"IRIS","IRIS","unstake","iaa1n367xt7536vhcxrnjx60na77afw2dzecxlmnah",str(Conf.Config.random_amount(5))),
            # ("Safe2-3账户IRIS赎回",["a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c"],"IRIS","IRIS","claim","iaa1n367xt7536vhcxrnjx60na77afw2dzecxlmnah",0),
            # CLV网络
            # ("Safe2-2账户CLV质押",["426a6690c29c5ee0052712c1fda0cc38691f3faf2a571f4b04c9705bbf3f921b"],"CLV","CLV","stake","5Eud43L2RufGoFQpsJjeGYPiyKdYd5JMNWy81RjzeBknXHgG",str(Conf.Config.random_amount(4))),
            # ("Safe2-2账户CLV赎回",["426a6690c29c5ee0052712c1fda0cc38691f3faf2a571f4b04c9705bbf3f921b"],"CLV","CLV","unstake","5Eud43L2RufGoFQpsJjeGYPiyKdYd5JMNWy81RjzeBknXHgG",str(Conf.Config.random_amount(5))),
            # ("Safe2-2账户CLV赎回",["426a6690c29c5ee0052712c1fda0cc38691f3faf2a571f4b04c9705bbf3f921b"],"CLV","CLV","claim","5Eud43L2RufGoFQpsJjeGYPiyKdYd5JMNWy81RjzeBknXHgG",0),
        ]

    @allure.story("Custodial_Stake_Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,networkCode,symbol,type,address,amount', test_data)
    def test_custodial(self,test_title,privatekey,networkCode,symbol,type,address,amount):

        with allure.step("查询From账户holders信息——holders"):
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

        with allure.step("签名交易——sign"):
            sign = Http.HttpUtils.sign(id,signatures,serialized)
            assert sign.status_code == 200
            assert sign.json()["status"] == "SIGNED"

            id = stake.json()["_embedded"]["transactions"][0]["id"]

        with allure.step("广播交易"):
            send = Http.HttpUtils.send(id)
            assert send.status_code == 200
            assert send.json()["status"] == "PENDING"

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')