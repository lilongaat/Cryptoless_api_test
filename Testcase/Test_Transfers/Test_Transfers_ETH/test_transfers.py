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


@allure.feature("Transfers_ETH_Success!")
class Test_transfers_eth:
    test_data = [
        # 测试
        {"privatekey":["1dfb5db671e7d68dda061d8a7e79a57ed9e27449d6e934c3286978ee2873a435"],"PublicKeys":["02b2a4911e34a182981cb37df1ab2f05b39b9977e0699e15a0f59711367c5454ac"],"networkCode":"ETH","symbol":"ETH","from":"0x44d9Ea428C4C1D097947A683439a60105281AAD7","to":"0x44d9Ea428C4C1D097947A683439a60105281AAD7","amount":Conf.Config.random_amount(18)},
        # 生产
        # {"privatekey":["b62cb712741b7e6f60b54728b6fb071c32feb1cd14e8e2c1b08c92230d650e95"],"PublicKeys":["02488e3f6edb86a6a5e5fe457c71b9d5e40d75558231bfb1489e62694044490fc8"],"networkCode":"ETH","symbol":"ETH","from":"0x8591589a1D9e21073084329Dde89aB745c0F5A2e","to":"0x8591589a1D9e21073084329Dde89aB745c0F5A2e","amount":Conf.Config.random_amount(18)},
    ]

    @allure.testcase("Transfers_ETH,单签地址转账!")
    @pytest.mark.parametrize('param', test_data)
    def test_transfers_address(self, param):
        privatekey = list(param.values())[0][0]
        PublicKeys = list(param.values())[1]
        networkCode = list(param.values())[2]
        symbol = list(param.values())[3]
        from_add = list(param.values())[4]
        to_add = list(param.values())[5]
        amount = list(param.values())[6]

        logger.info(privatekey)

        # transfers
        res = Http.HttpUtils.post_transfers(networkCode,symbol,PublicKeys,from_add,to_add,amount)
        logger.info(res[0])

        signature = Conf.Config.sign(privatekey,res[5][0]['hash'])
        logger.info(signature)

        signatures = [
            {
                "hash":res[5][0]['hash'],
                "publickey":PublicKeys[0],
                "signature":signature
            }
        ]
        logger.info(signatures)

        sig = Http.HttpUtils.post_sign_transfers()
        # logger.info(sig)

        # send = Http.HttpUtils.post_send_transfers()
