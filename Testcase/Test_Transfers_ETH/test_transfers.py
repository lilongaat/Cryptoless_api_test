from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
from Common import Http, Httprpc, Httpfs, Conf
from Common.Loguru import logger


@allure.feature("Transfers_ETH!")
class Test_transfers_eth:
    test_data = [
        {"privatekey":["b62cb712741b7e6f60b54728b6fb071c32feb1cd14e8e2c1b08c92230d650e95"],"PublicKeys":["02488e3f6edb86a6a5e5fe457c71b9d5e40d75558231bfb1489e62694044490fc8"],"networkCode":"ETH","symbol":"ETH","from":"0x8591589a1D9e21073084329Dde89aB745c0F5A2e","to":"0x8591589a1D9e21073084329Dde89aB745c0F5A2e","amount":Conf.Config.random_amount(18)},
    ]

    @allure.story("Transfers_ETH,单签地址转账!")
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

        signature = Conf.Config.sign(privatekey,res[5][0]['hash'])
        logger.info(signature)

        signatures = [
            {
                "hash":res[5][0]['hash'],
                "publickeys":PublicKeys,
                "signature":signature
            }
        ]
        sig = Http.HttpUtils.post_sign_transfers(res[1],res[2],res[3],res[4],res[5],res[6],signatures)

        # send = Http.HttpUtils.post_send_transfers()
