import random
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Conf
from Common.Loguru import logger

# 单签账户
@allure.feature("Query_Swap_Route!")
class Test_swap_fail_matic:
    test_data = [
        # 测试&生产
        ("networkCode为空","","USDT","USDC",round(random.uniform(100,500), random.randint(2,4)),404,2200000,"network not found"),
        ("networkCode不支持","BTC","USDT","USDC",round(random.uniform(100,500), random.randint(2,4)),400,2100000,"only supports evm"),
        ("from资产未关联网络","ETH","USDC","USDT",round(random.uniform(100,500), random.randint(2,4)),404,2200000,"from token not found"),
        ("to资产未关联网络","ETH","USDT","USDC",round(random.uniform(100,500), random.randint(2,4)),404,2200000,"to token not found"),
        ("from coin为空","MATIC","","USDC",round(random.uniform(100,500), random.randint(2,4)),404,2200000,"from not found"),
        ("from coin不支持","MATIC","CRV","USDC",round(random.uniform(100,500), random.randint(2,4)),404,2200000,"from not found"),
        ("to coin为空","MATIC","USDT","",round(random.uniform(100,500), random.randint(2,4)),404,2200000,"to not found"),
        ("to coin不支持","MATIC","USDT","CRV",round(random.uniform(100,500), random.randint(2,4)),404,2200000,"to not found"),
        ("amount为空","MATIC","USDT","USDC","",400,2402001,"insufficient liquidity for this trade"),
        ("amount超出精度","MATIC","USDT","USDC",round(random.uniform(100,500), random.randint(18,19)),400,2100000,"amount decimals long too"),
        ("amount异常字符串","MATIC","USDT","USDC","maximum",400,2300000,"program exception"),
        ("流动性不足","BSC","CLV","xBURGER",round(random.uniform(100,500), random.randint(2,4)),400,2402001,"insufficient liquidity for this trade"),
    ]

    @allure.story("Query_Swap_Route_Fail!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,from_coin,to_coin,amount,status_code_check,code_check,message_check', test_data)
    def test_swap_matic(self,test_title,networkCode,from_coin,to_coin,amount,status_code_check,code_check,message_check):

        with allure.step("查询Swap路由信息"):
            res = Http.HttpUtils.get_swap_route(networkCode,from_coin,to_coin,str(amount))
            assert res.status_code == status_code_check
            assert res.json()['code'] == code_check
            assert res.json()['message'] == message_check

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')