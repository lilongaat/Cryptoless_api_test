import json
from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
from Common import Http, Conf
from Common.Loguru import logger


@allure.feature("Transfers_IRIS_Success!")
class Test_transfers_eth:
    test_data = [
        # 测试
        {"privatekey":["44298f449dab3993e9965a32c1c4e1d99c1fcece7e228b348516924cecc88f18"],"PublicKeys":["032de47c91516ffd2985965935841fa8243894b003886a1f478682da74a848db58"],"networkCode":"IRIS","symbol":"IRIS","from":"iaa13cq3lkmheswkz4d00vu4663267aw6tqjep3jy4","to":"iaa13cq3lkmheswkz4d00vu4663267aw6tqjep3jy4","amount":1},
    ]

    @allure.testcase("Transfers_IRIS,单签地址转账!")
    @pytest.mark.parametrize('param', test_data)
    def test_transfers_address(self, param):
        privatekey = list(param.values())[0][0]
        PublicKeys = list(param.values())[1][0]
        networkCode = list(param.values())[2]
        symbol = list(param.values())[3]
        from_add = list(param.values())[4]
        to_add = list(param.values())[5]
        amount = list(param.values())[6]

        # transfers
        res = Http.HttpUtils.post_transfers(networkCode,symbol,PublicKeys,from_add,to_add,amount)
        # logger.info(res[0])

        signature = Conf.Config.sign(privatekey,res[5][0]['hash'])
        # logger.info(signature)

        signatures = [
            {
                "hash":res[5][0]['hash'],
                "publickey":PublicKeys,
                "signature":signature
            }
        ]
        # logger.info(signatures)

        sig = Http.HttpUtils.post_sign_transfers(res[1],res[2],res[3],res[4],res[5],res[6],signatures)
        # logger.info(sig)

        send = Http.HttpUtils.post_send_transfers()
