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

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxNTczOTM3MDIxNzEzNzc2NjQyIiwiZXhwIjoxNjY0Njk1NjE2LCJpYXQiOjE2NjQwOTA4MTYsInVzZXJJZCI6MTU3MzkzNzAyMTcxMzc3NjY0Mn0.TfkTJsH4rp4FCmciMn1BUVlnev1JPI7glaTUjyVUz8M"
web3token = "eyJib2R5IjoiV2ViMyBUb2tlbiBWZXJzaW9uOiAyXG5Ob25jZTogMTU3MzkzNzAyMTcxMzc3NjY0MlxuSXNzdWVkIEF0OiBTdW4sIDI1IFNlcCAyMDIyIDA3OjI2OjQyIEdNVFxuRXhwaXJhdGlvbiBUaW1lOiBXZWQsIDIyIFNlcCAyMDMyIDA3OjI2OjQyIEdNVCIsInNpZ25hdHVyZSI6IjB4MDdhMzI4M2IxY2JmNWRkOTQwNTFhNWM5NjYxNWM4NTY5ZDQ0ZGEzZTJkODIzZGI4NzE5YjA0YWUwYmRhZWE4NzY4OTZiZGY5ZjEzZTU3YWUxMDRjNTExZDMwODQwMTgxMjE5Zjg1Y2ExZTkwNTIwYzgxMjRlM2I3MjAwNmI1YjUxYiJ9"

# custodial
@allure.feature("Stake_Success!")
class Test_stake_success:
    test_data = [
        # IRIS网络
        ("Custodial账户IRIS质押","IRIS","IRIS","stake","iaa1kfmz96l3hfltxdzdhrcxw2dg6wfp852w6xwaxe",str(Conf.Config.random_amount(4))),
        # ("Custodial账户IRIS赎回","IRIS","IRIS","unstake","iaa1kfmz96l3hfltxdzdhrcxw2dg6wfp852w6xwaxe",str(Conf.Config.random_amount(5))),
        # ("Custodial账户IRIS赎回","IRIS","IRIS","claim","iaa1kfmz96l3hfltxdzdhrcxw2dg6wfp852w6xwaxe",0),
    ]

    @allure.story("Custodial_Stake_Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,type,address,amount', test_data)
    def test_custodial(self,test_title,networkCode,symbol,type,address,amount):

        with allure.step("查询From账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,address,web3token)
            assert holders.status_code == 200

        with allure.step("查询账户staking信息"):
            staking = Http.HttpUtils.get_staking(networkCode,symbol,address)
            assert staking.status_code == 200

        with allure.step("构建交易——instructions"):
            if type == "claim":
                body = {
                    "delegator":address,
                    "coinSymbol":symbol,
                }
            else:
                body = {
                    "delegator":address,
                    "coinSymbol":symbol,
                    "amount":amount
                }
            transactionParams = {
                "memo":''.join(random.sample(string.ascii_letters + string.digits, 10))
            }
            stake = Http.HttpUtils.instructions(type,body,networkCode,[],transactionParams,token)

            assert stake.status_code == 200
            assert stake.json()["_embedded"]["transactions"][0]["status"] == "PENDING"

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')