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

# custodial 超过最大fee，失败转账
@allure.feature("Transfers!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # GOERLI
            ("GOERLI Custodial账户转账 nativecoin rebuild Maxfee","GOERLI","GoerliETH","0xcc7a54ec1d39d1cf7b35f2b3b92031ad5fc7b6ca","0xbdb3bd7b3f3daeadc58d00ef5f15ed9a476b8fe3","0.000000000000000001",28571428592428,28571428572428,400,2102003),
            ("GOERLI Custodial账户转账 erc20coin rebuild Maxfee","GOERLI","USDCC","0xcc7a54ec1d39d1cf7b35f2b3b92031ad5fc7b6ca","0xbdb3bd7b3f3daeadc58d00ef5f15ed9a476b8fe3","0.123",28571428592428,28571428572428,400,2102003),
            ("GOERLI Custodial账户转账 nativecoin rebuild feepoor","GOERLI","GoerliETH","0x57d8daBDF8C9eD5D9FF512F1033576303Ff9Aa20","0xbdb3bd7b3f3daeadc58d00ef5f15ed9a476b8fe3","0.0001",200000000000,150000000000,400,2100000),
        ]
    elif env_type == 1: #生产
        test_data = [
            # MATIC
            ("MATIC Custodial账户转账 erc20coin rebuild Maxfee","MATIC","USDC","0xe458fd3e2515d42cbcd52a89b52fb662bf052143","0x3d7f18ad2cea9b59e54dfaf09b327c1ccd899591","0.000123",28571428592428,28571428572428,400,2102003),
            ("MATIC Custodial账户转账 nativecoin rebuild Maxfee","MATIC","MATIC","0xe458fd3e2515d42cbcd52a89b52fb662bf052143","0x3d7f18ad2cea9b59e54dfaf09b327c1ccd899591","0.00012",28571428592428,28571428572428,400,2102003),
        ]

    @allure.story("Custodial Transfers Fail Maxfee!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,from_add,to_add,amount,maxFeePerGas,maxPriorityFeePerGas,status_code,code', test_data)
    def test_custodial(self,test_title,networkCode,symbol,from_add,to_add,amount,maxFeePerGas,maxPriorityFeePerGas,status_code,code):

        with allure.step("查询from账户holder信息"):
            holder = Http.HttpUtils.holders(networkCode=networkCode,symbol=symbol,address=from_add)
            assert holder.status_code ==200

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
            assert transfer.json()["_embedded"]["transactions"][0]["statusDesc"] == "SIGNED"

            id = transfer.json()["_embedded"]["transactions"][0]["id"]

        with allure.step("rebuild交易"):
            params = {
                    "maxFeePerGas":hex(maxFeePerGas),
                    "maxPriorityFeePerGas":hex(maxPriorityFeePerGas),
                }
            rebuild = Http.HttpUtils.rebuild(id,params)
            assert rebuild.status_code == status_code
            assert rebuild.json()["code"] == code


if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')