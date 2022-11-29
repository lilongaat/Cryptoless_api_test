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
    accounts = Conf.Config.reader_csv("/Users/lilong/Documents/Test_Api/Address/Top/ETH.csv",100)

    @allure.story("ETH Rich_address(Top-100) Balances Check!")
    @allure.title('查询账户余额-{address}')
    @pytest.mark.parametrize('address', accounts)
    def test_account_balance(self, address):

        with allure.step("etherscan.com查询地址余额"):
            response = Httpexplore.ETH.balance(address)
            assert response.status_code == 200
            balance = Decimal(response.json()["result"])/Decimal(10**18)

        with allure.step("Graphql查询地址余额"):
            graphql = Graphql.Graphql.getAccountByAddress("ETH",address,"ETH")
            assert graphql.status_code == 200
            amount = Decimal(graphql.json()["data"]["getAccountByAddress"]["amount"])/Decimal(10**18)

        with allure.step("系统查询地址余额"):
            holder = Http.HttpUtils.holders("ETH","ETH",address,ob_token)
            assert holder.status_code == 200
            if len(holder.json()) == 0:
                quantity = 0
            else:
                quantity = (Decimal(holder.json()[0]['quantity']))

        with allure.step("验证地址余额:explore==Graphql"):
            assert balance == amount,"explore!=Graphql"
        
        with allure.step("验证地址余额:explore==holder"):
            assert balance == quantity,"explore!=holder"

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')