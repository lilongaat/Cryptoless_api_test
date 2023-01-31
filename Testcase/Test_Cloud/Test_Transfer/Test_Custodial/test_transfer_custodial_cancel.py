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
from Common import Http, Conf
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))

# custodial
@allure.feature("Transfers!")
class Test_transfers_fail:
    if env_type == 0: #测试
        test_data = [
            # BTC
            ("BTC Custodial账户转账cancel","BTC","BTC","tb1q7ymdm79ryug7vttw4jrf87pdcmn67n3p9rgc5x","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq","0.000008"),

            # GOERLI
            ("GOERLI Custodial账户转账 nativecoin cancel","GOERLI","GoerliETH","0xcc7a54ec1d39d1cf7b35f2b3b92031ad5fc7b6ca","0xa7A9E710f9A3B4184D4F8B7d379CEC262f2382c2","0.00012"),
            ("GOERLI Custodial账户转账 erc20coin cancel","GOERLI","USDCC","0xcc7a54ec1d39d1cf7b35f2b3b92031ad5fc7b6ca","0xa7A9E710f9A3B4184D4F8B7d379CEC262f2382c2","0.000123"),

            #IRIS
            ("IRIS Custodial账户转账cancel","IRIS","IRIS","iaa1q2eql0hjd345tfxnzat6s7jfpwg3jansv8krwe","iaa1q2eql0hjd345tfxnzat6s7jfpwg3jansv8krwe","0.000123"),

            #CLV
            ("CLV Custodial账户转账cancel","CLV","CLV","5G8W1b7pWa7zzcYAWomTaX2zmP1SHE7JDEGvQTdGh45d83te","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","0.0000014"),
        ]
    elif env_type == 1: #生产
        test_data = []

    @allure.story("Custodial Transfers Cancel!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_custodial(self,test_title,networkCode,symbol,from_add,to_add,amount):

        # with allure.step("查询账户holder信息"):
        #     holder = Http.HttpUtils.holders(networkCode=networkCode,symbol=symbol,address=from_add)
        #     assert holder.status_code ==200
        #     quantity = holder.json()["list"][0]["quantity"]

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

        with allure.step("取消交易"):
            cancel = Http.HttpUtils.cancel(id)
            assert cancel.status_code == 200
            assert cancel.json()['status'] == 7
            assert cancel.json()['statusDesc'] == "CANCELED"

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')