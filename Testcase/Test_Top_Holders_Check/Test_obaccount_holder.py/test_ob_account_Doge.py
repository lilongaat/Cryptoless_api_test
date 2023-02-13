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

env_type = int(ReadConfig().get_env('type'))
if env_type == 0: # Debug
    ob_token = ReadConfig().get_debug('ob_token')
elif env_type == 1: # Release
    ob_token = ReadConfig().get_release('ob_token')




@allure.feature("Accounts Balances!")
class Test_accounts_balances():
    accounts = Conf.Config.reader_csv("/Users/lilong/Documents/Test_Api/Address/Top/DOGE.csv",1)

    @allure.story("DOGE Rich_address(Top-100) Balances Check!")
    @allure.title('查询账户余额-{address}')
    @pytest.mark.parametrize('address', accounts)
    def test_account_balance(self, address):

        with allure.step("dogechain.info查询地址余额"):
            response = Httpexplore.DOGE.balance(address)
            assert response.status_code == 200
            balance = Decimal(response.json())

        with allure.step("Graphql查询地址余额"):
            graphql = Graphql.Graphql.getAccountByAddress("DOGE",address,"DOGE")
            assert graphql.status_code == 200
            amount = Decimal(graphql.json()["data"]["getAccountByAddress"]["amount"])

        with allure.step("系统查询地址余额"):
            holder = Http.HttpUtils.holders("DOGE","DOGE",address,ob_token)
            assert holder.status_code == 200
            if len(holder.json()["list"]) == 0:
                quantity = 0
            else:
                quantity = (Decimal(holder.json()["list"][0]['quantity']))

        with allure.step("验证地址余额:explore,Graphql相差小于0.1"):
            assert abs(balance - amount) < 0.1,"explore!=Graphql"
        
        with allure.step("验证地址余额:explore,Graphql相差小于0.1"):
            assert abs(balance - quantity) < 0.1,"explore!=holder"
            del balance,amount,quantity

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')