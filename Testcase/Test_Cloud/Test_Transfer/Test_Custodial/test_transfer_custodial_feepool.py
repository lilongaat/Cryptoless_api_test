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

# custodial
@allure.feature("Transfers!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # BTC
            ("BTC Custodial账户转账 fee=0","BTC","BTC","tb1q5qe4xx0uc300fdqq5xe5mj6ku7x3m0y7epehkn","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","0.0001",400,2102004),
            ("BTC Custodial账户转账 fee<minfee","BTC","BTC","tb1q5qe4xx0uc300fdqq5xe5mj6ku7x3m0y7epehkn","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","0.00009801",400,2102004),

            # GOERLI
            ("GOERLI Custodial账户转账 nativecoin 手续费不给","GOERLI","GoerliETH","0x57d8daBDF8C9eD5D9FF512F1033576303Ff9Aa20","0xbdb3bd7b3f3daeadc58d00ef5f15ed9a476b8fe3","0.001",400,2100000),
            ("GOERLI Custodial账户转账 nativecoin 手续费不足","GOERLI","GoerliETH","0x57d8daBDF8C9eD5D9FF512F1033576303Ff9Aa20","0xbdb3bd7b3f3daeadc58d00ef5f15ed9a476b8fe3","0.000999999999",400,2100000),
            ("GOERLI Custodial账户转账 erc20coin 手续费不足","GOERLI","USDCC","0x0b4f0984f8341bf707e520080dd393e6c53e0262","0xbdb3bd7b3f3daeadc58d00ef5f15ed9a476b8fe3","5",400,2100000),

            # IRIS
            ("IRIS Custodial账户转账 手续费不给","IRIS","IRIS","iaa1h4a85el0w6hp38smxt5rn0qzxpwsy3r70gz4pj","iaa15h0lvaa6slvj0hg4d64548j2c5fds2zv8tkvgs","0.1",400,2100000),
            ("IRIS Custodial账户转账 手续费不足","IRIS","IRIS","iaa1h4a85el0w6hp38smxt5rn0qzxpwsy3r70gz4pj","iaa15h0lvaa6slvj0hg4d64548j2c5fds2zv8tkvgs","0.09999",400,2100000),

            # CLV
            ("CLV Custodial账户转账 手续费不给","CLV","CLV","5DUeheqqCmPHcFXLm54QEecJWYbWbVj5oKKkUZ3poyk5Vxv2","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","0.1",400,2100000),
            ("CLV Custodial账户转账 手续费不足","CLV","CLV","5DUeheqqCmPHcFXLm54QEecJWYbWbVj5oKKkUZ3poyk5Vxv2","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","0.09999",400,2100000),
        ]
    elif env_type == 1: #生产
        test_data = [
            # MATIC
        ]

    @allure.story("Custodial Transfers Fail Feepool!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,from_add,to_add,amount,status_code,code', test_data)
    def test_custodial(self,test_title,networkCode,symbol,from_add,to_add,amount,status_code,code):

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
            assert transfer.status_code == status_code
            assert transfer.json()["code"] == code
            


if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')