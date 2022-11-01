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


# custodial
@allure.feature("Transfers_Success!")
class Test_transfers_success:
    test_data = [
        # IRIS网络
        ("Custodial账户IRIS质押","IRIS","IRIS","iaa1tpm89pqldl2fcte86xqv4328tyywdyz6x2u47a",str(Conf.Config.random_amount(4)))
        #CLV网络
        # ("Custodial账户CLV转账","CLV","CLV","5Cp9xGyehSAeLBmuVxWdoFYvXkjnVDGX8ZWU5mGVUR8FzyaT","5CvuzcexRrvsinqq2N7hmQyE9iXk26XNpE18ZEbyMaKtmPL9",str(Conf.Config.random_amount(4))),
        # ("Custodial账户CLV转账","CLV","CLV","5Cp9xGyehSAeLBmuVxWdoFYvXkjnVDGX8ZWU5mGVUR8FzyaT","5Cp9xGyehSAeLBmuVxWdoFYvXkjnVDGX8ZWU5mGVUR8FzyaT",str(Conf.Config.random_amount(4))),
    ]

    @allure.story("Custodial_Transfers_Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,address,amount', test_data)
    def test_custodial(self,test_title,networkCode,symbol,address,amount):

        with allure.step("查询账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,address)
            assert holders.status_code == 200

        with allure.step("查询账户质押信息——delegations"):
            staking = Http.HttpUtils.get_staking(networkCode,symbol,address)
            assert staking.status_code == 200

        with allure.step("构建质押交易——instructions"):
            body = {
                "delegator":address,
                "symbol":symbol,
                "amount":amount
            }
            transactionParams = {
                "memo":''.join(random.sample(string.ascii_letters + string.digits, 10))
            }
            transfer = Http.HttpUtils.instructions("stake",body,networkCode,[],transactionParams)

            assert transfer.status_code == 200
        #     assert transfer.json()["_embedded"]["transactions"][0]["status"] == "PENDING"
        #     assert transfer.json()["body"]["symbol"] == symbol
        #     assert transfer.json()["body"]["amount"] == amount
        #     assert transfer.json()["body"]["from"] == from_add
        #     assert transfer.json()["body"]["to"] == to_add
        #     sleep(30)

        # with allure.step("查询From账户holders信息——holders"):
        #     holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
        #     assert holders.status_code == 200

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')