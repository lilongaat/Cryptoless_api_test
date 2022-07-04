import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Conf
from Common.Loguru import logger


@allure.feature("Transfers_Fail!")
class Test_transfers_fail_iris:

    test_data = [
        # 测试
        ("余额不足转账",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],["033511e38fd373c4515ada4826616146b4c3def47da9907b59d9555b19134dd683"],"IRIS","IRIS","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u",'1000000',400),
        ("精度超长(19位)转账!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],["033511e38fd373c4515ada4826616146b4c3def47da9907b59d9555b19134dd683"],"IRIS","IRIS","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u",Conf.Config.random_amount(19),400),
        ("转账金额为空!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],["033511e38fd373c4515ada4826616146b4c3def47da9907b59d9555b19134dd683"],"IRIS","IRIS","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u",0,400),
        ("转账金额为空!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],["033511e38fd373c4515ada4826616146b4c3def47da9907b59d9555b19134dd683"],"IRIS","IRIS","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u","",400),
        ("转账金额为负数!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],["033511e38fd373c4515ada4826616146b4c3def47da9907b59d9555b19134dd683"],"IRIS","IRIS","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u","-0.00000001",400),
        ("转账金额字符串类型异常!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],["033511e38fd373c4515ada4826616146b4c3def47da9907b59d9555b19134dd683"],"IRIS","IRIS","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u","99u9f",400),
        ("转账from地址异常!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],["033511e38fd373c4515ada4826616146b4c3def47da9907b59d9555b19134dd683"],"IRIS","IRIS","iat0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u",Conf.Config.random_amount(3),400),
        ("转账from地址为空!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],["033511e38fd373c4515ada4826616146b4c3def47da9907b59d9555b19134dd683"],"IRIS","IRIS","","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u",Conf.Config.random_amount(3),400),
        ("转账to地址异常!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],["033511e38fd373c4515ada4826616146b4c3def47da9907b59d9555b19134dd683"],"IRIS","IRIS","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u","a1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u",Conf.Config.random_amount(3),400),
        ("转账to地址为空!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],["033511e38fd373c4515ada4826616146b4c3def47da9907b59d9555b19134dd683"],"IRIS","IRIS","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u","",Conf.Config.random_amount(3),400),
    ]

    @allure.story("Transfers_IRIS_transfer_Fail!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check', test_data)
    def test_transfers_address(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check):

        with allure.step("构建交易——transfers"):
            res = Http.HttpUtils.post_transfers(networkCode,symbol,PublicKeys,from_add,to_add,amount)
            assert res.status_code == status_code_check

@allure.feature("Transfers_Fail!")
class Test_sign_fail_iris:
    test_data = [
        # 测试
        ("签名异常(私钥错误)!",["6b24012db8ae4047e4b0df7245b1bcd74272e4e4dc4085ab2185d79024fa0f44"],["033511e38fd373c4515ada4826616146b4c3def47da9907b59d9555b19134dd683"],"IRIS","IRIS","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u",Conf.Config.random_amount(4),400),
    ]

    @allure.story("Transfers_IRIS_sign_Fail!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check', test_data)
    def test_transfers_address(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check):

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