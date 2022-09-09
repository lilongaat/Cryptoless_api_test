import random
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Conf
from Common.Loguru import logger


# 单签账户转账 错误的私钥签名
@allure.feature("Transfers_Fail!")
class Test_sign_fail:
    test_data = [
        # 测试
        ("错误的私钥签名!",["0fcada5a2176b1807faacdf14a1518fd71837a4f5e9f916dc145949d010491a3"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",Conf.Config.random_amount(6),400,2300000),
        ("错误的私钥签名!",["0fcada5a2176b1807faacdf14a1518fd71837a4f5e9f916dc145949d010491a3"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",Conf.Config.random_amount(6),400,2300000),
    ]

    @allure.story("Transfers_send_Fail!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check,code_check', test_data)
    def test_transfers_send_fail(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check,code_check):

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_add,
                "to":to_add,
                "symbol":symbol,
                "amount":amount
            }
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            transfer = Http.HttpUtils.post_instructions("Transfer",body,networkCode,PublicKeys,transactionParams)
            assert transfer.status_code == 200

        with allure.step("查询From账户holders信息——holders"):
            holders_before = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders_before.status_code == 200
            quantity_before = holders_before.json()[0]['quantity']

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_add,
                "to":to_add,
                "symbol":symbol,
                "amount":amount
            }
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            transfer = Http.HttpUtils.post_instructions("Transfer",body,networkCode,PublicKeys,transactionParams)
            assert transfer.status_code == 200

            t_estimatedFee = transfer.json()['_embedded']['transactions'][0]['estimatedFee']
            t_hash = transfer.json()['_embedded']['transactions'][0]['hash']
            t_id = transfer.json()['_embedded']['transactions'][0]['id']
            t_networkCode = transfer.json()['_embedded']['transactions'][0]['networkCode']
            t_requiredSignings = transfer.json()['_embedded']['transactions'][0]['requiredSignings']
            t_serialized = transfer.json()['_embedded']['transactions'][0]['serialized']
            t_status = transfer.json()['_embedded']['transactions'][0]['status']
            ID = transfer.json()['id']
            body_amount = transfer.json()["body"]["amount"]

        with allure.step("签名交易——sign"):
            signature = Conf.Config.sign(privatekey[0],t_requiredSignings[0]['hash'])
            signatures = [
                {
                    "hash":t_requiredSignings[0]['hash'],
                    "publickey":t_requiredSignings[0]['publicKeys'][0],
                    "signature":signature
                }
            ]
            sig = Http.HttpUtils.post_sign_transfers(t_estimatedFee,t_hash,t_id,t_networkCode,t_requiredSignings,t_serialized,signatures)
            assert sig.status_code == status_code_check
            assert sig.json()['code'] == code_check

# 多签账户转账 错误的私钥签名
@allure.feature("Transfers_Fail!")
class Test_sign_fail_safe:
    test_data = [
        # 测试
        ("publickey[k1(托管),k2(私有),k2(私有)]",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(0.00001,0.0001), random.randint(5,18)),400,400),
        # ("publickey[k1(托管),k2(私有),k2(私有)]",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(1,1000), random.randint(5,18)),400,400),
    ]

    @allure.story("Transfers_send_Fail!")
    @allure.title('多签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check,code_check', test_data)
    def test_transfers_send_fail(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check,code_check):

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_add,
                "to":to_add,
                "symbol":symbol,
                "amount":amount
            }
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            transfer = Http.HttpUtils.post_instructions("Transfer",body,networkCode,PublicKeys,transactionParams)
            assert transfer.status_code == 200

        with allure.step("rebuild交易——rebuild"):
            params = {
                "gasPrice":"0x6edf2a079f"
                }
            rebuild = Http.HttpUtils.post_rebuild(transfer.json()['_embedded']['transactions'][0]['id'],params)
            assert rebuild[0].status_code == 200

            signature = Conf.Config.sign(privatekey[0],rebuild[5][0]['hash'])
            signatures = [
                {
                    "hash":rebuild[5][0]['hash'],
                    "publickey":PublicKeys[0],
                    "signature":signature
                }
            ]

        # with allure.step("签名交易——sign"):
        #     sig = Http.HttpUtils.post_sign_transfers(rebuild[1],rebuild[2],rebuild[3],rebuild[4],rebuild[5],rebuild[6],signatures)
        #     assert sig.status_code == 200

        # with allure.step("广播交易——send"):
        #     send = Http.HttpUtils.post_send_transfers(rebuild[3])
        #     assert send.status_code == status_code_check
        #     assert send.json()['code'] == code_check


if __name__ == '__main__':
    path = os.path.abspath(__file__) + "::Test_sign_fail"
    pytest.main(["-vs", path,'--clean-alluredir','--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')