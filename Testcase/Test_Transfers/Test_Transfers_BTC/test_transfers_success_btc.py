import json
from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Conf
from Common.Loguru import logger


@allure.feature("Transfers_Success!")
class Test_transfers_success_btc():
    test_data = [
        # 测试
        ("正常转账!",["dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b"],["022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"],"BTC","BTC","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun",Conf.Config.random_amount(2)),
    ]

    @allure.story("Transfers_BTC_Success!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_address(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        with allure.step("构建交易——transfers"):
            res = Http.HttpUtils.post_transfers(networkCode,symbol,PublicKeys,from_add,to_add,amount)
            assert res[0].status_code == 200

        # signatures = []
        # for i in range(len(res[5])):
        #     signature = Conf.Config.sign(privatekey[0],res[5][i]['hash'])
        #     logger.info(signature)
        #     signatures.append(
        #         {
        #         "hash":res[5][i]['hash'],
        #         "publickey":PublicKeys[0],
        #         "signature":signature
        #     }
        #     )

        # with allure.step("签名交易——sign"):
        #     sig = Http.HttpUtils.post_sign_transfers(res[1],res[2],res[3],res[4],res[5],res[6],signatures)
        #     assert sig.status_code == 200

        # with allure.step("广播交易——send"):
        #     send = Http.HttpUtils.post_send_transfers(res[3])
        #     assert send.status_code == 200

        # with allure.step("查询关联交易记录——balance-transactions by hash"):
        #     sleep(10)
        #     hash = json.loads(send.text)["hash"]
        #     transcations = Http.HttpUtils.get_transactions_byhash(hash)
        #     assert transcations.status_code == 200

        #     # BTC自己转自己一条交易记录
        #     if (from_add == to_add):
        #         assert len(transcations.json()) == 1
        #     else:
        #         assert len(transcations.json()) == 2

