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
@allure.feature("Stake_Fail!")
class Test_stake_fail:
    if env_type == 0: #测试
        test_data = [
            # IRIS网络
            ("Custodial账户IRIS质押手续费不足","IRIS","IRIS","stake","iaa180qh39f68devetnda4t28drsrhgxnjha5eqhus","0.000001",400,2400000),
            ("Custodial账户IRIS赎回","IRIS","IRIS","unstake","iaa180qh39f68devetnda4t28drsrhgxnjha5eqhus",str(Conf.Config.random_amount(5)),400,2400000),
            ("Custodial账户IRISclaim","IRIS","IRIS","claim","iaa180qh39f68devetnda4t28drsrhgxnjha5eqhus",0,400,2400000),

            # CLV网络
            ("Custodial账户IRIS质押","CLV","CLV","stake","5Hgu6xq1ETv3kbjBnhqZCzaDFtqUhxfFBogZuJ2RnqsoXmWk",str(Conf.Config.random_amount(6)),400,2400000),
        ]
    if env_type == 1: #生产
        test_data = [
            # IRIS网络
        ]

    @allure.story("Custodial_Stake_Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,type,address,amount,status_check,code_check', test_data)
    def test_custodial(self,test_title,networkCode,symbol,type,address,amount,status_check,code_check):

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
            assert send.status_code == status_check
            assert send.json()["code"] == code_check
            

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')