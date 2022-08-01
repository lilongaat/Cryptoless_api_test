import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Conf
from Common.Loguru import logger


@allure.feature("Transfers_Fail!")
class Test_transfers_fail_eth:
    test_data = [
        # 测试
        ("余额不足转账!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",'1000000',400),
        ("精度超长(19位)转账!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",Conf.Config.random_amount(19),400),
        ("转账金额为空!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",'',400),
        ("转账金额为负数!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","-0.000001",400),
        ("转账金额字符串类型异常!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","max",400),
        ("转账from地址异常!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","bDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",Conf.Config.random_amount(6),400),
        ("转账from地址为空!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",Conf.Config.random_amount(6),400),
        ("转账to地址异常!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","bDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",Conf.Config.random_amount(6),400),
        ("转账to地址为空!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","",Conf.Config.random_amount(6),400),
    ]

    @allure.story("Transfers_ETH_transfer_Fail!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check', test_data)
    def test_transfers_transfer_fail(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check):

        with allure.step("构建交易——transfers"):
            res = Http.HttpUtils.post_transfers(networkCode,symbol,PublicKeys,from_add,to_add,amount)
            assert res.status_code == status_code_check

@allure.feature("Transfers_Fail!")
class Test_sign_fail_eth:
    test_data = [
        # 测试
        ("签名异常(私钥错误)!",["6b24012db8ae4047e4b0df7245b1bcd74272e4e4dc4085ab2185d79024fa0f44"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",Conf.Config.random_amount(6),400),
    ]

    @allure.story("Transfers_ETH_sign_Fail!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check', test_data)
    def test_transfers_sign_fail(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check):

        with allure.step("构建交易——transfers"):
            res = Http.HttpUtils.post_transfers(networkCode,symbol,PublicKeys,from_add,to_add,amount)
            assert res[0].status_code == 200

            signature = Conf.Config.sign(privatekey[0],res[5][0]['hash'])
            signatures = [
                {
                    "hash":res[5][0]['hash'],
                    "publickey":PublicKeys[0],
                    "signature":signature
                }
            ]

        with allure.step("签名交易——sign"):
            sig = Http.HttpUtils.post_sign_transfers(res[1],res[2],res[3],res[4],res[5],res[6],signatures)
            assert sig.status_code == status_code_check

@allure.feature("Transfers_Fail!")
class Test_send_fail_eth:
    test_data = [
        # 测试
        ("ETH转账手续费超出限制!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",Conf.Config.random_amount(6),400),
        ("ERC20转账手续费超出限制!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",Conf.Config.random_amount(2),400),
    ]

    @allure.story("Transfers_ETH_send_Fail!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check', test_data)
    def test_transfers_send_fail(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check):

        with allure.step("构建交易——transfers"):
            res = Http.HttpUtils.post_transfers(networkCode,symbol,PublicKeys,from_add,to_add,amount)
            assert res[0].status_code == 200

        with allure.step("rebuild交易——rebuild"):
            params = {
                "gasPrice":"0x6edf2a079f"
                }
            rebuild = Http.HttpUtils.post_rebuild(res[3],params)
            assert rebuild[0].status_code == 200

            signature = Conf.Config.sign(privatekey[0],rebuild[5][0]['hash'])
            signatures = [
                {
                    "hash":rebuild[5][0]['hash'],
                    "publickey":PublicKeys[0],
                    "signature":signature
                }
            ]

        with allure.step("签名交易——sign"):
            sig = Http.HttpUtils.post_sign_transfers(rebuild[1],rebuild[2],rebuild[3],rebuild[4],rebuild[5],rebuild[6],signatures)
            assert sig.status_code == 200

        with allure.step("广播交易——send"):
            send = Http.HttpUtils.post_send_transfers(rebuild[3])
            assert send.status_code == status_code_check