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

# 单签账户
@allure.feature("Stake_Fail!")
class Test_Stake_fail_iris():
    test_data = [
        # 测试
        ("质押金额为空!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],"IRIS","IRIS","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u","",400),
        ("质押金额不足!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],"IRIS","IRIS","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u","10000",400),
        ("质押精度超长(7位)!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],"IRIS","IRIS","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u",Conf.Config.random_amount(7),400),
        ("质押网络为空!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],"BTC","IRIS","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u",Conf.Config.random_amount(3),404),
        ("质押网络不支持!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],"BTC","IRIS","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u",Conf.Config.random_amount(3),404),
        ("质押symbol为空!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],"BTC","IRIS","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u",Conf.Config.random_amount(3),404),
        ("质押symbol不支持!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],"IRIS","ETH","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u",Conf.Config.random_amount(3),400),
        ("质押地址为空!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],"IRIS","IRIS","",Conf.Config.random_amount(3),400),
        ("质押地址错误!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],"IRIS","IRIS","0x3a6851df39c4c46a982d77319b5e37b470d20f80",Conf.Config.random_amount(3),400),
    ]

    @allure.story("Stake_CLV_Success!")
    @allure.title('单签账户质押-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,networkCode,symbol,delegator,amount,status_code_check', test_data)
    def test_staking_iris(self,test_title,privatekey,networkCode,symbol,delegator,amount,status_code_check):

        with allure.step("构建交易——staking"):
            res = Http.HttpUtils.post_staking(networkCode,symbol,delegator,amount)
            assert res.status_code == status_code_check