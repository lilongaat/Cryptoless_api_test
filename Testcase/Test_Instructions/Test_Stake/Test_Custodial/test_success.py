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

# custodial
@allure.feature("Stake Success!")
class Test_stake_success:
    if env_type == 0: #测试
        test_data = [
            # IRIS网络
            # ("Custodial账户IRIS质押","IRIS","IRIS","stake","iaa1vywcfmff44nlhud05nlzlpw0hrlxenptn9ff7r",str(Conf.Config.random_amount(4))),
            # ("Custodial账户IRIS赎回","IRIS","IRIS","unstake","iaa1vywcfmff44nlhud05nlzlpw0hrlxenptn9ff7r",str(Conf.Config.random_amount(5))),
            ("Custodial账户IRISclaim","IRIS","IRIS","claim","iaa1vywcfmff44nlhud05nlzlpw0hrlxenptn9ff7r",0),
            # CLV网络
            # ("Custodial账户IRIS质押","CLV","CLV","stake","5CFStFse5QY5dyfeHeTDSnMeBBRgxXse2D8k1TUbM67HeA9h",str(Conf.Config.random_amount(4))),
            # ("Custodial账户IRIS赎回","CLV","CLV","unstake","5CFStFse5QY5dyfeHeTDSnMeBBRgxXse2D8k1TUbM67HeA9h",str(Conf.Config.random_amount(5))),
            # ("Custodial账户IRISclaim","CLV","CLV","claim","5CFStFse5QY5dyfeHeTDSnMeBBRgxXse2D8k1TUbM67HeA9h",0),
        ]
    if env_type == 1: #生产
        test_data = [
            # IRIS网络
            ("Custodial账户IRIS质押","IRIS","IRIS","stake","iaa1yvgc6tjuetv6hzchnvnqg4r09ltzk8ld6m0vcu",str(Conf.Config.random_amount(4))),
            # ("Custodial账户IRIS赎回","IRIS","IRIS","unstake","iaa1yvgc6tjuetv6hzchnvnqg4r09ltzk8ld6m0vcu",str(Conf.Config.random_amount(5))),
            # ("Custodial账户IRISclaim","IRIS","IRIS","claim","iaa1yvgc6tjuetv6hzchnvnqg4r09ltzk8ld6m0vcu",0),
            # CLV网络
            # ("Custodial账户CLV质押","CLV","CLV","stake","5DiDtDkGFJ4CtgdEnGHaWU3JwSmCro26FozcqyTY8Brk3KSo",str(Conf.Config.random_amount(4))),
            # ("Custodial账户CLV赎回","CLV","CLV","unstake","5DiDtDkGFJ4CtgdEnGHaWU3JwSmCro26FozcqyTY8Brk3KSo",str(Conf.Config.random_amount(5))),
            # ("Custodial账户CLVclaim","CLV","CLV","claim","5DiDtDkGFJ4CtgdEnGHaWU3JwSmCro26FozcqyTY8Brk3KSo",0),
        ]

    @allure.story("Custodial_Stake_Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,type,address,amount', test_data)
    def test_custodial(self,test_title,networkCode,symbol,type,address,amount):

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
            assert stake.json()["_embedded"]["transactions"][0]["status"] == "SIGNED"

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