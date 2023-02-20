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

accounts = Conf.Config.reader_csv("/Users/lilong/Documents/Test_Api/Address/Top/GOERLI.csv",10)

# safe
@allure.feature("Transfers!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # GOERLI
            ("GOERLI safe2-2账户批量转账 nativecoin 余额不足","GOERLI","GoerliETH","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xBA900f26FDe478A75E4752813df547DbB2dE1414",accounts,"0.000000000000000021",400,2102001),
            ("GOERLI safe2-2账户批量转账 nativecoin 手续费不足","GOERLI","GoerliETH","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xBA900f26FDe478A75E4752813df547DbB2dE1414",accounts,"0.00000000000000002",400,2100000),
            ("GOERLI safe2-2账户批量转账 erc20coin 余额不足","GOERLI","USDCC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xBA900f26FDe478A75E4752813df547DbB2dE1414",accounts,"0.11",400,2102001),
            ("GOERLI safe2-2账户批量转账 erc20coin 手续费不足","GOERLI","USDCC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xBA900f26FDe478A75E4752813df547DbB2dE1414",accounts,"0.001",400,2100000),
        ]
    elif env_type == 1: #生产
        test_data = []

    @allure.story("Safe Transfers Batch Fail!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,privatekey,from_add,to_add,amount,status_code,code', test_data)
    def test_custodial(self,test_title,networkCode,symbol,privatekey,from_add,to_add,amount,status_code,code):

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
            del balance,quantity
            del balance,quantity

        with allure.step("构建交易——instructions"):
            recipients = []
            for i in range(len(accounts)):
                recipients.append(
                    {
                        "to":accounts[i],
                        "amount":amount
                    }
                )
            body = {
                "networkCode":networkCode,
                "type":"MULTI_TRANSFER",
                "body":{
                    "from":from_add,
                    "symbol":symbol,
                    "recipients":recipients
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