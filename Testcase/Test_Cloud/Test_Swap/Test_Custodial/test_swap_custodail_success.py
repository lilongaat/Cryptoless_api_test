from decimal import Decimal
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
from Common import Http, Httpexplore, Conf
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))

# custodail
@allure.feature("Swap!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # MATIC 
            ("MATIC custodail账户 SWAP:MATIC-USDC","MATIC","0x651a23f7bed98b52c7829ad668a4836c48064850","MATIC","USDC","1","0.00012"),
            ("MATIC custodail账户 SWAP:USDC-MATIC","MATIC","0x651a23f7bed98b52c7829ad668a4836c48064850","USDC","MATIC","1","0.00012"),
            ("MATIC custodail账户 SWAP:USDC-USDT","MATIC","0x651a23f7bed98b52c7829ad668a4836c48064850","USDC","USDT","1","0.00012"),
            ("MATIC custodail账户 SWAP:USDT-USDC","MATIC","0x651a23f7bed98b52c7829ad668a4836c48064850","USDT","USDC","1","0.00012"),
        ]
    elif env_type == 1: #生产
        test_data = [
            # MATIC 
            ("MATIC custodail账户 SWAP:MATIC-USDC","MATIC","0xe458fd3e2515d42cbcd52a89b52fb662bf052143","MATIC","USDC","1","0.000012"),
            ("MATIC custodail账户 SWAP:USDC-MATIC","MATIC","0xe458fd3e2515d42cbcd52a89b52fb662bf052143","USDC","MATIC","1","0.000012"),
            ("MATIC custodail账户 SWAP:USDC-USDT","MATIC","0xe458fd3e2515d42cbcd52a89b52fb662bf052143","USDC","USDT","1","0.000012"),
            ("MATIC custodail账户 SWAP:USDT-USDC","MATIC","0xe458fd3e2515d42cbcd52a89b52fb662bf052143","USDT","USDC","1","0.000012"),
        ]

    @allure.story("Custodial Swap Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,address,from_coin,to_coin,slippage,fromamount', test_data)
    def test_custodial(self,test_title,networkCode,address,from_coin,to_coin,slippage,fromamount):

        with allure.step("浏览器查询from账户balance信息"):
            balance = Httpexplore.Balances_explore.query(networkCode,address,from_coin)
                
        with allure.step("查询from账户holder信息"):
            holder = Http.HttpUtils.holders(networkCode=networkCode,symbol=from_coin,address=address)
            assert holder.status_code ==200
            quantity = Decimal(holder.json()["list"][0]["quantity"])

        logger.debug("浏览器查询账户balance为:" + str(balance))
        logger.debug("查询账户holder为:" + str(quantity))

        with allure.step("账户余额相等验证 浏览器查询==holder"):
            assert balance == quantity


        with allure.step("构建交易——instructions"):
            body = {
                "networkCode":networkCode,
                "type":"swap",
                "body":{
                    "address":address,
                    "from":from_coin,
                    "to":to_coin,
                    "fromAmount":fromamount,
                    "slippage":slippage
                },
                "transactionParams":{
                    "memo":''.join(random.sample(string.ascii_letters + string.digits, 10))
                }
            }
            transfer = Http.HttpUtils.instructions(body)
            assert transfer.status_code == 200
            assert transfer.json()["_embedded"]["transactions"][0]["statusDesc"] == "SIGNED"

            id = transfer.json()["_embedded"]["transactions"][0]["id"]

        with allure.step("广播交易"):
            send = Http.HttpUtils.send(id)
            assert send.status_code == 200
            assert send.json()["statusDesc"] == "PENDING"

        with allure.step("通过id查询交易记录"):
            sleep(30)
            for n in range(10):
                transaction = Http.HttpUtils.transactions_byid(id)
                assert transaction.status_code == 200
                statusDesc = transaction.json()["statusDesc"]
                if statusDesc == "SETTLED" and len(transaction.json()["balanceChanges"]) > 0:
                    break
                else:
                    sleep(30)
            sleep(5)


        with allure.step("浏览器查询from账户balance信息"):
            balance = Httpexplore.Balances_explore.query(networkCode,address,from_coin)
                
        with allure.step("查询from账户holder信息"):
            holder = Http.HttpUtils.holders(networkCode=networkCode,symbol=from_coin,address=address)
            assert holder.status_code ==200
            quantity = Decimal(holder.json()["list"][0]["quantity"])

        logger.debug("浏览器查询账户balance为:" + str(balance))
        logger.debug("查询账户holder为:" + str(quantity))

        with allure.step("账户余额相等验证 浏览器查询==holder"):
            assert balance == quantity

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')