import json
import random
import string
from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))))
from Common import Http, Conf
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))

# custodial
@allure.feature("Transfers Success!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # GOERLI
            # ("GOERLI Custodial账户转账 nativecoin","GOERLI","goerliETH","0xcc7a54ec1d39d1cf7b35f2b3b92031ad5fc7b6ca",["0xa7A9E710f9A3B4184D4F8B7d379CEC262f2382c2"],["0x64"]),
            ("GOERLI Custodial账户批量转账 nativecoin","GOERLI","goerliETH","0xcc7a54ec1d39d1cf7b35f2b3b92031ad5fc7b6ca",["0xa7A9E710f9A3B4184D4F8B7d379CEC262f2382c2","0x9d055026eb8d83ef561d5d8084f2dd02e7ad2c17"],["0x64","0x1"]),
        ]
    elif env_type == 1: #生产
        test_data = []

    @allure.story("Custodial Transfers Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,from_add,to_adds,values', test_data)
    def test_custodial(self,test_title,networkCode,symbol,from_add,to_adds,values):

        if len(to_adds) == 1: #普通转账
            payload = {
                "from":from_add,
                "to":to_adds[0],
                "value":values[0]
                }
            type = "TRANSACTION"
        elif len(to_adds) > 1: #批量转账
            calls =[]
            for i in range(len(to_adds)):
                call = {
                    "to":to_adds[i],
                    "value":values[i]
                }
                calls.append(call)

            payload = {
                "from":from_add,
                "calls":calls
                }
            type = "MULTISEND_TRANSACTION"

        with allure.step("构建交易——transactions"):
            body = {
                "networkCode":networkCode,
                "payload":payload,
                "type":type
            }
            transfer = Http.HttpUtils.transactions(body)
            assert transfer.status_code == 200
            assert transfer.json()["statusDesc"] == "SIGNED"

            id = transfer.json()["id"]

        with allure.step("rebuilde交易"):
            params = {

            }
            re = Http.HttpUtils.rebuild(id,params)
            assert re.status_code == 200

        with allure.step("广播交易"):
            send = Http.HttpUtils.send(id)
            assert send.status_code == 200
            assert send.json()["statusDesc"] == "PENDING"

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')