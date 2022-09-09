import pytest_check
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
class Test_swap_success_matic:
    test_data = [
        # 测试&生产
        ("MATIC(USDT-USDC)","MATIC","USDT","USDC",round(random.uniform(0,1), random.randint(2,6))),
        ("BSC(USDT-USDC)","BSC","USDT","USDC",round(random.uniform(10,100), random.randint(2,5))),
        ("BSC(BURGER-WSG)","BSC","BURGER","WSG",round(random.uniform(100,1000), random.randint(2,6))),
        ("BSC(SpacePi-USDT)","BSC","SpacePi","USDT",round(random.uniform(0,800), random.randint(2,3))),
    ]

    @allure.story("Query_Swap_Route_Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,from_coin,to_coin,amount', test_data)
    def test_swap_matic(self,test_title,networkCode,from_coin,to_coin,amount):

        with allure.step("查询Swap路由信息"):
            res = Http.HttpUtils.get_swap_route(networkCode,from_coin,to_coin,str(amount))
            assert res.status_code == 200
            pytest_check.equal(res.json()["networkCode"],networkCode,'networkCode check error!')
            pytest_check.equal(res.json()["from"],from_coin,'from_coin check error!')
            pytest_check.equal(res.json()["to"],to_coin,'to_coin check error!')
            pytest_check.equal(float(res.json()["fromAmount"]),amount,'fromAmount check error!')
            pytest_check.greater(float(res.json()["toAmount"]),0,'toAmount check error!')

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')