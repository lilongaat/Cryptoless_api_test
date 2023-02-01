from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
from Common import Http,Conf
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))

@allure.feature("Users!")
class Test_create_custodial_account:

    if env_type == 0: #测试
        test_data = [
            ("用户60s内请求登陆多次","15873664025@163.com"),
        ]

    elif env_type == 1: #生产
        test_data = [
            ("用户60s内请求登陆多次","15873664025@163.com"),
        ]

    @allure.story("User Connect Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,email', test_data)
    def test_create_account_custodial(self, test_title, email):

        with allure.step("用户请求登陆"):
            connect_request = Http.HttpUtils.connect_req(email)
            assert connect_request.status_code == 200

        sleep(60)
        
        with allure.step("用户请求登陆"):
            connect_request = Http.HttpUtils.connect_req(email)
            assert connect_request.status_code == 200
            

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')
