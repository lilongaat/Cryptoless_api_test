import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Conf
from Common.Loguru import logger


@allure.feature("Transfers_Fail!")
class Test_transfers_fail_matic:
    test_data = [
        # 生产
        ("余额不足转账!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C","0xc78D5E7212484B01857B702B7895e16dB442CA2e",'1000000',400),
        ("精度超长(19位)转账!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C","0xc78D5E7212484B01857B702B7895e16dB442CA2e",Conf.Config.random_amount(19),400),
        ("转账金额为空!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C","0xc78D5E7212484B01857B702B7895e16dB442CA2e",'',400),
        ("转账金额为负数!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C","0xc78D5E7212484B01857B702B7895e16dB442CA2e","-0.000001",400),
        ("转账金额字符串类型异常!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C","0xc78D5E7212484B01857B702B7895e16dB442CA2e","max",400),
        ("转账from地址异常!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","bDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xc78D5E7212484B01857B702B7895e16dB442CA2e",Conf.Config.random_amount(6),400),
        ("转账from地址为空!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C",Conf.Config.random_amount(6),400),
        ("转账to地址异常!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C","0xc78D5E7212484B01857B702B7895e16dB442CA2ee",Conf.Config.random_amount(6),400),
        ("转账to地址为空!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C","",Conf.Config.random_amount(6),400),
    ]

    @allure.story("Transfers_MATIC_transfer_Fail!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check', test_data)
    def test_transfers_transfer_fail(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check):

        with allure.step("构建交易——transfers"):
            res = Http.HttpUtils.post_transfers(networkCode,symbol,PublicKeys,from_add,to_add,amount)
            assert res.status_code == status_code_check

@allure.feature("Transfers_Fail!")
class Test_sign_fail_MATIC:
    test_data = [
        # 生产
        ("签名异常(私钥错误)!",["6b24012db8ae4047e4b0df7245b1bcd74272e4e4dc4085ab2185d79024fa0f44"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C","0xc78D5E7212484B01857B702B7895e16dB442CA2e",Conf.Config.random_amount(6),400),
    ]

    @allure.story("Transfers_MATIC_sign_Fail!")
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
class Test_send_fail_matic:
    test_data = [
        # 生产
        ("MATIC转账手续费超出限制!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C","0xc78D5E7212484B01857B702B7895e16dB442CA2e",Conf.Config.random_amount(6),400),
        ("ERC20转账手续费超出限制!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","Mask","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C","0xc78D5E7212484B01857B702B7895e16dB442CA2e",Conf.Config.random_amount(2),400),
    ]

    @allure.story("Transfers_MATIC_send_Fail!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check', test_data)
    def test_transfers_send_fail(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check):

        with allure.step("构建交易——transfers"):
            res = Http.HttpUtils.post_transfers(networkCode,symbol,PublicKeys,from_add,to_add,amount)
            assert res[0].status_code == 200

        with allure.step("rebuild交易——rebuild"):
            params = {
                # hex(1000000000000000000/2100)
                "gasPrice":"0x1b117bc2dc30d"
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