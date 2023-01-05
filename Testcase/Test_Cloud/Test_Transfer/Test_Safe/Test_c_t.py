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

# safe
@allure.feature("Transfers Success!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # GOERLI
            # ("GOERLI Safe创建+转入coin",["0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113"],[""],"GOERLI","0x1eC2CE6108240118Ff2c66eC8AFAC28618D7e066"),
            # ("GOERLI Safe创建+转入coin",[""],[""],"GOERLI","0x1eC2CE6108240118Ff2c66eC8AFAC28618D7e066"),

            # MATIC
            # ("MATIC Safe创建+转入coin",["0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113"],[],"MATIC","0x2791bca1f2de4661ed88a30c99a7a9449aa84174"),
        ]
    elif env_type == 1: #生产
        test_data = []

    @allure.story("Safe Transfers Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,publickey,recovery,networkCode,tokenaddress', test_data)
    def test_safe(self,test_title,publickey,recovery,networkCode,tokenaddress):

        with allure.step("创建安全账户"):
            acc = Http.HttpUtils.create_safe_account("safe",networkCode,publickey[0],recovery[0])
            assert acc.status_code == 200
            assert acc.json()["status"] == "inactive"
            from_add = acc.json()["address"]

        with allure.step("母账户转账nativecoin到多签账户"):
            Httpcore.HttpCoreUtils.core_parent_account_transfer_nativecoin(networkCode,from_add,"4000000000000000")

        with allure.step("母账户转账erc20coin:USDC到多签账户"):
            Httpcore.HttpCoreUtils.core_parent_account_transfer_erc20coin(networkCode,tokenaddress,from_add,"1000000000000000000")

        logger.error("\n"+"safe账户" +"\n"+ from_add+"\n\n")
        


if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')