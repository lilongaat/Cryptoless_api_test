import json
from time import sleep
from decimal import Decimal
import allure
import pytest
from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Httprpc, Httpfs, Conf, Graphql, Httpexplore
from Common.Loguru import logger
from Config.readconfig import ReadConfig

# env_type = int(ReadConfig().get_env('type'))
# if env_type == 0: # Debug
#     ob_token = ReadConfig().get_debug('ob_token')

# elif env_type == 1: # Release
#     ob_token = ReadConfig().get_release('ob_token')


ob_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxNjAzMzMxODA1MzMwNzk2NTQ1IiwiZXhwIjo0ODI0Njk5MDcxLCJpYXQiOjE2NzEwOTkwNzEsInVzZXJJZCI6MTYwMzMzMTgwNTMzMDc5NjU0NX0.LqXvFCF47GglM26lQPD8aGsPGVBaOpwrRLK18kN3B20"



@allure.feature("Accounts Balances!")
class Test_accounts_balances():
    accounts = Conf.Config.reader_csv("/Users/lilong/Documents/Test_Api/Address/Top/GOERLI.csv",1)

    @allure.story("GOERLI address(Top-10) Balances Check!")
    @allure.title('查询账户余额-{address}')
    @pytest.mark.parametrize('address', accounts)
    def test_account_balance(self, address):

        with allure.step("Graphql查询地址余额"):
            graphql = Graphql.Graphql.getAccountByAddress("GOERLI",address,"goerliETH")
            assert graphql.status_code == 200
            amount = Decimal(graphql.json()["data"]["getAccountByAddress"]["amount"])/Decimal(10**18)

        with allure.step("系统查询地址余额"):
            holder = Http.HttpUtils.holders("GOERLI","GoerliETH",address,ob_token)
            assert holder.status_code == 200
            if len(holder.json()) == 0:
                quantity = 0
            else:
                quantity = (Decimal(holder.json()[0]['quantity']))

        with allure.step("验证地址余额:Graphql==Holder"):
            assert amount == quantity,"Graphql!=Holder"
        

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')