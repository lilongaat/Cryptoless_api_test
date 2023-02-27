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
            ("MATIC custodail账户 SWAP:MATIC-USDC 超出余额","MATIC","0x651a23f7bed98b52c7829ad668a4836c48064850","MATIC","USDC","1","100",400,2102001),
            ("MATIC custodail账户 SWAP:MATIC-USDC 超出精度","MATIC","0x651a23f7bed98b52c7829ad668a4836c48064850","MATIC","USDC","1","0.0000000000000000001",400,2100000),
            ("MATIC custodail账户 SWAP:USDC-MATIC 超出余额","MATIC","0x651a23f7bed98b52c7829ad668a4836c48064850","USDC","MATIC","1","10000",400,2102001),
            ("MATIC custodail账户 SWAP:USDC-MATIC 超出精度","MATIC","0x651a23f7bed98b52c7829ad668a4836c48064850","USDC","MATIC","1","0.0000001",400,2100000),
            ("MATIC custodail账户 SWAP:MATIC-USDC 手续费不足","MATIC","0x8a38e85dd7dd796b819447a2b120dfd3e5af3a98","MATIC","USDC","1","0.00001",400,2100000),
            ("MATIC custodail账户 SWAP:USDC-MATIC 手续费不足","MATIC","0x8a38e85dd7dd796b819447a2b120dfd3e5af3a98","USDC","MATIC","1","0.001",400,2100000),
            ("MATIC custodail账户 SWAP:USDC-MATIC 滑点值格式错误","MATIC","0x651a23f7bed98b52c7829ad668a4836c48064850","USDC","MATIC","0.9","0.00001",400,2300000),
            ("MATIC custodail账户 SWAP:USDC-MATIC 滑点值没有","MATIC","0x651a23f7bed98b52c7829ad668a4836c48064850","USDC","MATIC","","0.00001",400,2300000),
            ("MATIC custodail账户 SWAP:USDC-MATIC 滑点值太小","MATIC","0x651a23f7bed98b52c7829ad668a4836c48064850","USDC","MATIC","0","0.00001",400,2300000),
            ("MATIC custodail账户 SWAP:USDC-MATIC 滑点值太大","MATIC","0x651a23f7bed98b52c7829ad668a4836c48064850","USDC","MATIC","51","0.00001",400,2300000),
            ("MATIC custodail账户 SWAP 资产不存在","MATIC","0x651a23f7bed98b52c7829ad668a4836c48064850","USDC","UU","1","0.00001",400,2200000),
        ]
    elif env_type == 1: #生产
        test_data = [
            # # MATIC 
            ("MATIC custodail账户 SWAP:MATIC-USDC 超出余额","MATIC","0xe458fd3e2515d42cbcd52a89b52fb662bf052143","MATIC","USDC","1","100",400,2102001),
            ("MATIC custodail账户 SWAP:MATIC-USDC 超出精度","MATIC","0xe458fd3e2515d42cbcd52a89b52fb662bf052143","MATIC","USDC","1","0.0000000000000000001",400,2100000),
            ("MATIC custodail账户 SWAP:USDC-MATIC 超出余额","MATIC","0xe458fd3e2515d42cbcd52a89b52fb662bf052143","USDC","MATIC","1","10000",400,2102001),
            ("MATIC custodail账户 SWAP:USDC-MATIC 超出精度","MATIC","0xe458fd3e2515d42cbcd52a89b52fb662bf052143","USDC","MATIC","1","0.0000001",400,2100000),
            ("MATIC custodail账户 SWAP:MATIC-USDC 手续费不足","MATIC","0xd1f031ee103fb6bc93c2f68160422136fabdb5b0","MATIC","USDC","1","0.001",400,2100000),
            ("MATIC custodail账户 SWAP:USDC-MATIC 手续费不足","MATIC","0xd1f031ee103fb6bc93c2f68160422136fabdb5b0","USDC","MATIC","1","0.001",400,2100000),
            ("MATIC custodail账户 SWAP:USDC-MATIC 滑点值格式错误","MATIC","0xe458fd3e2515d42cbcd52a89b52fb662bf052143","USDC","MATIC","0.9","0.00001",400,2300000),
            ("MATIC custodail账户 SWAP:USDC-MATIC 滑点值没有","MATIC","0xe458fd3e2515d42cbcd52a89b52fb662bf052143","USDC","MATIC","","0.00001",400,2300000),
            ("MATIC custodail账户 SWAP:USDC-MATIC 滑点值太小","MATIC","0xe458fd3e2515d42cbcd52a89b52fb662bf052143","USDC","MATIC","0","0.00001",400,2300000),
            ("MATIC custodail账户 SWAP:USDC-MATIC 滑点值太大","MATIC","0xe458fd3e2515d42cbcd52a89b52fb662bf052143","USDC","MATIC","51","0.00001",400,2300000),
            ("MATIC custodail账户 SWAP 资产不存在","MATIC","0xe458fd3e2515d42cbcd52a89b52fb662bf052143","USDC","UU","1","0.00001",400,2200000),
        ]

    @allure.story("Custodial Swap Fail!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,address,from_coin,to_coin,slippage,fromamount,status_code,code', test_data)
    def test_custodial(self,test_title,networkCode,address,from_coin,to_coin,slippage,fromamount,status_code,code):
  
        with allure.step("查询from账户holder信息"):
            holder = Http.HttpUtils.holders(networkCode=networkCode,symbol=from_coin,address=address)
            assert holder.status_code ==200

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
            assert transfer.status_code == status_code
            assert transfer.json()["code"] == code
            

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')