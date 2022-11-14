import json
import random
import string
from time import sleep
from decimal import Decimal
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
from Common import Http, Conf
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))

# custodial
@allure.feature("Swap Fail!")
class Test_swap_fail:
    if env_type == 0: #测试
        test_data = [
        ("Swap网络不支持!","BTC","BTC","USDC","tb1q8g0jhxa3t0uyufec29xexw6fwnkvw94v3jlw7e","1",Conf.Config.random_amount(8),400,2402001),
        ("Swap网络禁用!","RINKEBY","ETH","USDC","0x821647aF7f50717500E008dE239f8692216cBC67","1",Conf.Config.random_amount(8),400,2300000),
        ("Swap网络为空!","","MATIC","USDC","0x55D6AB99596d002AF4d51CDCD83259030F4d4B5c","1",Conf.Config.random_amount(8),400,2100000),
        ("Swap from为空!","MATIC","","USDC","0x55D6AB99596d002AF4d51CDCD83259030F4d4B5c","1",Conf.Config.random_amount(8),400,2300000),
        ("Swap to为空!","MATIC","MATIC","","0x55D6AB99596d002AF4d51CDCD83259030F4d4B5c","1",Conf.Config.random_amount(8),400,2300000),
        ("Swap from不属于该网络!","MATIC","ETH","USDC","0x55D6AB99596d002AF4d51CDCD83259030F4d4B5c","1",Conf.Config.random_amount(8),400,2200000),
        ("Swap to不属于该网络!","MATIC","MATIC","BTC","0x55D6AB99596d002AF4d51CDCD83259030F4d4B5c","1",Conf.Config.random_amount(8),400,2402001),
        ("Swap address为空!","MATIC","MATIC","USDC","","1",Conf.Config.random_amount(8),400,2300000),
        ("Swap address不属于用户!","MATIC","MATIC","USDC","0x0b1c8f78F0d8CE21e284b5Acd521f8d13DC0AC94","1",Conf.Config.random_amount(8),404,2200000),
        ("Swap amount为空!","MATIC","MATIC","USDC","0x55D6AB99596d002AF4d51CDCD83259030F4d4B5c","1","",400,2300000),
        ("Swap amount超过余额!","MATIC","MATIC","USDC","0x55D6AB99596d002AF4d51CDCD83259030F4d4B5c","1","1000",400,2102001),
        ("Swap amount超过精度!","MATIC","MATIC","USDC","0x55D6AB99596d002AF4d51CDCD83259030F4d4B5c","1",Conf.Config.random_amount(19),400,2100000),
        ("Swap amount数量太小!","MATIC","MATIC","USDC","0x55D6AB99596d002AF4d51CDCD83259030F4d4B5c","1",Conf.Config.random_amount(10),400,2400000),
        ("Swap 手续费不足!","MATIC","MATIC","USDC","0x55D6AB99596d002AF4d51CDCD83259030F4d4B5c","1","0.2000101",400,2400000),
        ("Swap slippage为空!","MATIC","MATIC","USDC","0x55D6AB99596d002AF4d51CDCD83259030F4d4B5c","",Conf.Config.random_amount(8),400,2300000),
        ("Swap slippage小于1!","MATIC","MATIC","USDC","0x55D6AB99596d002AF4d51CDCD83259030F4d4B5c","0.9",Conf.Config.random_amount(8),400,2300000),
        ("Swap slippage大于50!","MATIC","MATIC","USDC","0x55D6AB99596d002AF4d51CDCD83259030F4d4B5c","51",Conf.Config.random_amount(8),400,2300000),
        ]
    elif env_type == 1: #生产
        test_data = [
        ]

    @allure.story("Custodial Swap Fail!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,from_coin,to_coin,address,slippage,fromAmount,status_check,code_check', test_data)
    def test_custodial(self,test_title,networkCode,from_coin,to_coin,address,slippage,fromAmount,status_check,code_check):

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_coin,
                "to":to_coin,
                "address":address,
                "fromAmount":fromAmount,
                "slippage":slippage
            }
            transactionParams = {
                "memo":''.join(random.sample(string.ascii_letters + string.digits, 10))
            }
            swap = Http.HttpUtils.instructions("swap",body,networkCode,[],transactionParams)

            assert swap.status_code == status_check
            assert swap.json()["code"] == code_check


if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')