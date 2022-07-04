import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Conf
from Common.Loguru import logger


@allure.feature("Transfers_Fail!")
class Test_transfers_fail_btc():
    test_data = [
        # 测试
        ("余额不足转账!",["dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b"],["022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"],"BTC","BTC","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","1000000",400),
        ("精度超长(19位)转账!",["dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b"],["022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"],"BTC","BTC","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun",Conf.Config.random_amount(19),400),
        ("转账金额为空!",["dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b"],["022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"],"BTC","BTC","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","",400),
        ("转账金额为负数!",["dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b"],["022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"],"BTC","BTC","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","-0.0000001",400),
        ("转账金额字符串类型异常!",["dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b"],["022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"],"BTC","BTC","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","0.00000i",400),
        ("转账from地址异常!",["dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b"],["022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"],"BTC","BTC","0xE20FD35a849Ad67B2db3287d1dc3669067B237B6","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun",Conf.Config.random_amount(6),400),
        ("转账from地址为空!",["dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b"],["022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"],"BTC","BTC","","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun",Conf.Config.random_amount(7),400),
        ("转账to地址异常!",["dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b"],["022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"],"BTC","BTC","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","0xFEdd6BA870090f44CE20d06fBE0806B60De6D562",Conf.Config.random_amount(9),400),
        ("转账to地址为空!",["dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b"],["022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"],"BTC","BTC","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","",Conf.Config.random_amount(8),400),
    ]

    @allure.story("Transfers_BTC_transfer_Fail!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check', test_data)
    def test_transfers_address(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check):

        with allure.step("构建交易——transfers"):
            res = Http.HttpUtils.post_transfers(networkCode,symbol,PublicKeys,from_add,to_add,amount)
            assert res.status_code == status_code_check

@allure.feature("Transfers_Fail!")
class Test_sign_fail_btc():
    test_data = [
        # 测试
        ("签名异常(私钥错误)!",["6b24012db8ae4047e4b0df7245b1bcd74272e4e4dc4085ab2185d79024fa0f44"],["022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"],"BTC","BTC","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","0.1",400),
    ]

    @allure.story("Transfers_BTC_sign_Fail!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check', test_data)
    def test_transfers_address(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check):

        with allure.step("构建交易——transfers"):
            res = Http.HttpUtils.post_transfers(networkCode,symbol,PublicKeys,from_add,to_add,amount)
            assert res[0].status_code == 200

        signatures = []
        for i in range(len(res[5])):
            signature = Conf.Config.sign(privatekey[0],res[5][i]['hash'])
            logger.info(signature)
            signatures.append(
                {
                "hash":res[5][i]['hash'],
                "publickey":PublicKeys[0],
                "signature":signature
            }
            )

        with allure.step("签名交易——sign"):
            sig = Http.HttpUtils.post_sign_transfers(res[1],res[2],res[3],res[4],res[5],res[6],signatures)
            assert sig.status_code == status_code_check