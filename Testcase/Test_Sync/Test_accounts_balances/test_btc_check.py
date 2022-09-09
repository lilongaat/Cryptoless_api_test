import json
from time import sleep
from decimal import Decimal
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Conf, Httpexplore, Graphql
from Common.Loguru import logger

Authorization = "eyJzaWduYXR1cmUiOiIweGU4YzU0YjkzYTRlZDBmM2UxY2FkMDVjMDQzZmQzY2U0MjUwNTExNzY4MGY4NWViMmViMzAzZjQ5ZjNhMGFmYjU1OWExOWQxNDg2OTI1YTM0YzFmYTMxNWYzMzhjYTRhNGM2NzY0YjNmNjhiODMxY2VkMmZlNGUxOGVkMWVkNTMwMWMiLCJib2R5IjoiV2ViMyBUb2tlbiBWZXJzaW9uOiAyXG5Ob25jZTogNDE0NDU2MDhcbklzc3VlZCBBdDogVGh1LCAyNSBBdWcgMjAyMiAxMTozMjoyMCBHTVRcbkV4cGlyYXRpb24gVGltZTogTW9uLCAyNSBBdWcgMjA0MiAxMTozMjoyMCBHTVQifQ=="

@allure.feature("Accounts Balances!")
class Test_accounts_balances():
    accounts = Conf.Config.reader_csv("/Users/lilong/Documents/Test_Api/Address/Top/BTC.csv",100)

    @allure.story("BTC Rich_address(Top-100) Balances Check!")
    @allure.title('查询账户余额-{address}')
    @pytest.mark.parametrize('address', accounts)
    def test_account_balance(self, address):

        with allure.step("btc.com查询地址余额"):
            response = Httpexplore.BTC.balance(address)
            assert response.status_code == 200
            balance = Decimal(response.json()["data"]["balance"])/Decimal(10**8)

        with allure.step("Graphql查询地址余额"):
            graphql = Graphql.Graphql.getAccountByAddress("BTC",address,"BTC")
            assert graphql.status_code == 200
            amount = Decimal(graphql.json()["data"]["getAccountByAddress"]["amount"])

        with allure.step("系统查询地址余额"):
            holder = Http.HttpUtils.get_holders("BTC","BTC",address,Authorization)
            assert holder.status_code == 200
            quantity = Decimal(holder.json()[0]['quantity'])

        with allure.step("验证地址余额:explore==Graphql"):
            assert balance == amount,"explore!=Graphql"
        
        with allure.step("验证地址余额:explore==holder"):
            assert balance == quantity,"explore!=holder"

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')