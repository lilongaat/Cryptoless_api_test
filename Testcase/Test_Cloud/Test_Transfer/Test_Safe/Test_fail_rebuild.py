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

# safe
@allure.feature("Transfers!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # GOERLI
            ("GOERLI safe账户转账 nativecoin 交易不能Rebuild","GOERLI","GoerliETH","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0x9D055026eB8D83eF561D5D8084F2DD02e7AD2C17","0xa7a9e710f9a3b4184d4f8b7d379cec262f2382c2","0.00012",400,2300000),
            ("GOERLI safe账户转账 erc20coin 交易不能Rebuild","GOERLI","USDCC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0x9D055026eB8D83eF561D5D8084F2DD02e7AD2C17","0xa7a9e710f9a3b4184d4f8b7d379cec262f2382c2","0.00123",400,2300000),

            # MATIC
            ("MATIC safe账户转账 nativecoin 交易不能Rebuild","MATIC","MATIC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0x585eab16d5494f01bae462d4719d12214a443eec","0x3d7f18ad2cea9b59e54dfaf09b327c1ccd899591","0.000012",400,2300000),
            ("MATIC safe账户转账 erc20coin 交易不能Rebuild","MATIC","USDC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0x585eab16d5494f01bae462d4719d12214a443eec","0x3d7f18ad2cea9b59e54dfaf09b327c1ccd899591","0.00123",400,2300000),
        ]
    elif env_type == 1: #生产
        test_data = [
            # ETH

            # BSC 太贵了暂时不开
            # ("BSC safe账户转账nativecoin","BSC","BNB","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x49624761fca25f4782f88dc67aac8e8a48f54411","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.0000014",400,2300000),
            # ("BSC safe账户转账erc20coin","BSC","USDC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x49624761fca25f4782f88dc67aac8e8a48f54411","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.00000141",400,2300000),

            # MATIC
            ("MATIC safe账户转账nativecoin","MATIC","MATIC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x66c1d34c273cc09df9072f49aeba4b09e017bc5c","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.0000015",400,2300000),
            ("MATIC safe账户转账erc20coin","MATIC","USDC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x66c1d34c273cc09df9072f49aeba4b09e017bc5c","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.000151",400,2300000),
        ]

    @allure.story("safe Transfers Fail!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,privatekey,from_add,to_add,amount,status_code_check,code_check', test_data)
    def test_custodial(self,test_title,networkCode,symbol,privatekey,from_add,to_add,amount,status_code_check,code_check):

        with allure.step("浏览器查询from账户balance信息"):
            balance = Httpexplore.Balances_explore.query(networkCode,from_add,symbol)
                
        with allure.step("查询from账户holder信息"):
            holder = Http.HttpUtils.holders(networkCode=networkCode,symbol=symbol,address=from_add)
            assert holder.status_code ==200
            quantity = Decimal(holder.json()["list"][0]["quantity"])

        logger.debug("浏览器查询账户balance为:" + str(balance))
        logger.debug("查询账户holder为:" + str(quantity))

        with allure.step("账户余额相等验证 浏览器查询==holder"):
            assert balance == quantity

        with allure.step("构建交易——instructions"):
            body = {
                "networkCode":networkCode,
                "type":"transfer",
                "body":{
                    "from":from_add,
                    "to":to_add,
                    "symbol":symbol,
                    "amount":amount
                },
                "transactionParams":{
                    "memo":''.join(random.sample(string.ascii_letters + string.digits, 10))
                }
            }
            transfer = Http.HttpUtils.instructions(body)
            assert transfer.status_code == 200
            id = transfer.json()["_embedded"]["transactions"][0]["id"]

        with allure.step("rebuild交易"):
            params = {}
            rebuild = Http.HttpUtils.rebuild(id,params)
            assert rebuild.status_code == status_code_check
            assert rebuild.json()["code"] == code_check

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')