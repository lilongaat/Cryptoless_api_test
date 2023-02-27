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
from Common import Http, Conf, Httpexplore
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))


@allure.feature("Swap!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # MATIC
            ("MATIC safe2-2 激活+SWAP:MATIC->USDC 未支持","MATIC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xb6655b550d7f53e2d9731df849ad484d369d3932","MATIC","USDC","1","0.0000002",400,2102001),
            ("MATIC safe2-2 激活+SWAP:USDC->MATIC 未支持","MATIC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xb6655b550d7f53e2d9731df849ad484d369d3932","USDC","MATIC","1","0.20000",400,2102005),
            ("MATIC safe2-2 激活+SWAP:MATIC->USDC 未支持","MATIC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xb6655b550d7f53e2d9731df849ad484d369d3932","MATIC","USDC","1","0.00000009999",400,2102005),
            ("MATIC safe2-2 激活+SWAP:USDC->MATIC 未支持","MATIC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xb6655b550d7f53e2d9731df849ad484d369d3932","USDC","MATIC","1","0.01",400,2102005),

            # ("MATIC safe2-3 激活+SWAP:MATIC->USDC 余额不足","MATIC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xc29e1815e7cf466b55ed5fcced090656a3f36300","MATIC","USDC","1","0.00002",400,2102001),
            # ("MATIC safe2-3 激活+SWAP:USDC->MATIC 余额不足","MATIC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xc29e1815e7cf466b55ed5fcced090656a3f36300","USDC","MATIC","1","0.21",400,2102001),
        ]
    elif env_type == 1: #生产
        test_data = [
            # MATIC
            ("MATIC safe2-2 激活+SWAP:MATIC->USDC 未支持","MATIC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0xe4b6def3fe8008830f08707eb63eb362e9aa3b61","MATIC","USDC","1","0.00041378165394182",400,2102001),
            ("MATIC safe2-2 激活+SWAP:USDC->MATIC 未支持","MATIC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0xe4b6def3fe8008830f08707eb63eb362e9aa3b61","USDC","MATIC","1","0.20000",400,2102005),
            ("MATIC safe2-2 激活+SWAP:MATIC->USDC 未支持","MATIC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0xe4b6def3fe8008830f08707eb63eb362e9aa3b61","MATIC","USDC","1","0.00041378",400,2102005),
            ("MATIC safe2-2 激活+SWAP:USDC->MATIC 未支持","MATIC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0xe4b6def3fe8008830f08707eb63eb362e9aa3b61","USDC","MATIC","1","0.05",400,2102005),

            # ("MATIC safe2-3 SWAP:MATIC->USDC 余额不足","MATIC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x3b9570c5a0a689d2b05c229fea25527f744ef2fe","MATIC","USDC","1","0.00041378165394182",400,2102001),
            # ("MATIC safe2-3 SWAP:USDC->MATIC 余额不足","MATIC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x3b9570c5a0a689d2b05c229fea25527f744ef2fe","USDC","MATIC","1","0.20000",400,2102001),
            # ("MATIC safe2-3 SWAP:MATIC->USDC 手续费不足","MATIC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x3b9570c5a0a689d2b05c229fea25527f744ef2fe","MATIC","USDC","1","0.00041378",400,2100000),
            # ("MATIC safe2-3 SWAP:USDC->MATIC 手续费不足","MATIC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x3b9570c5a0a689d2b05c229fea25527f744ef2fe","USDC","MATIC","1","0.05",400,2100000),
        ]

    @allure.story("Safe Swap Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,privatekey,address,from_coin,to_coin,slippage,fromamount,status_code,code', test_data)
    def test_custodial(self,test_title,networkCode,privatekey,address,from_coin,to_coin,slippage,fromamount,status_code,code):

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
            del balance,quantity

        with allure.step("core构建交易——instructions"):
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
            assert transfer.status_code == status_code
            assert transfer.json()["code"] == code

            


if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')