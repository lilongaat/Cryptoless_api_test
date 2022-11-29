import json
import random
import string
from time import sleep
from decimal import Decimal
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
@allure.feature("Cross Chain Success!")
class Test_swap_success:
    if env_type == 0: #测试
        test_data = [
        ("正常Cross Chain(BSC(USDC)-MATIC(USDC))!","BSC","MATIC","USDC","0x4196143fA6Bcc977b15BA2a86860a3b579d1fD22","0x343d0b801Fcb032ccEB7D5411cd404816d203B91","12.5"),
        ]
    elif env_type == 1: #生产
        test_data = []

    @allure.story("Custodial Cross Chain Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,toNetworkCode,symbol,fromaddress,toaddress,amount', test_data)
    def test_custodial(self,test_title,networkCode,toNetworkCode,symbol,fromaddress,toaddress,amount):

        with allure.step("fromaddress holders信息——holder"):
            from_holder = Http.HttpUtils.get_holders(networkCode,symbol,fromaddress)
            assert from_holder.status_code == 200
            if len(from_holder.json()) == 0:
                from_holder_before = "0"
            else:
                from_holder_before = from_holder.json()[0]["quantity"]

        with allure.step("查询账户to_coin holders信息——holder"):
            to_holder = Http.HttpUtils.get_holders(toNetworkCode,symbol,toaddress)
            assert to_holder.status_code == 200
            if len(to_holder.json()) == 0:
                to_holder_before = "0"
            else:
                to_holder_before = to_holder.json()[0]["quantity"]

        with allure.step("构建交易——instructions"):
            body = {
                "from": fromaddress,
                "to": toaddress,
                "toNetworkCode":toNetworkCode,
                "symbol": symbol,
                "amount": amount
            }
            transactionParams = {
                "memo":''.join(random.sample(string.ascii_letters + string.digits, 10))
            }
            crosschain = Http.HttpUtils.instructions("CROSSCHAIN_TRANSFER",body,networkCode,[],transactionParams)

            assert crosschain.status_code == 200
            assert crosschain.json()["_embedded"]["transactions"][0]["status"] == "SIGNED"
            estimatedFee = crosschain.json()["_embedded"]["transactions"][0]["estimatedFee"]
            amount = crosschain.json()["body"]["amount"]
            id = crosschain.json()["_embedded"]["transactions"][0]["id"]

        with allure.step("广播交易"):
            send = Http.HttpUtils.send(id)
            assert send.status_code == 200
            assert send.json()["status"] == "PENDING"

        # sleep(30)


        # with allure.step("查询账户from_coin holders信息——holders"):
        #     from_holder_ = Http.HttpUtils.get_holders(networkCode,from_coin,address)
        #     assert from_holder_.status_code == 200
        #     from_holder_after = from_holder_.json()[0]["quantity"]

        # with allure.step("查询账户to_coin holders信息——holders"):
        #     to_holder_ = Http.HttpUtils.get_holders(networkCode,to_coin,address)
        #     assert to_holder_.status_code == 200
        #     to_holder_after = to_holder_.json()[0]["quantity"]

        # if from_coin == "MATIC":
        #      with allure.step("断言from_coin holder减少 手续费和swap金额"):
        #         assert Decimal(from_holder_after) == Decimal(from_holder_before) - Decimal(fromAmount) - Decimal(estimatedFee)
        # else:
        #      with allure.step("断言from_coin holder减少 swap金额"):
        #         assert Decimal(from_holder_after) == Decimal(from_holder_before) - Decimal(fromAmount)

        # with allure.step("断言to_coin holder增加 swap金额"):
        #     assert Decimal(to_holder_after) == Decimal(to_holder_before) + Decimal(toAmount)

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')