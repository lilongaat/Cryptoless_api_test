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

@allure.feature("Users Success!")
class Test_create_custodial_account:

    if env_type == 0: #测试
        test_data = [
            ("用户登陆成功","15873664023@163.com"),
        ]

    elif env_type == 1: #生产
        test_data = [
        ]

    @allure.story("User Connect Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,email', test_data)
    def test_create_account_custodial(self, test_title, email):
        
        with allure.step("用户请求登陆"):
            connect_request = Http.HttpUtils.connect_req(email)
            assert connect_request.status_code == 200
        
        with allure.step("用户确认连接"):
            confirm = Http.HttpUtils.connect_confirm(email)
            assert confirm.status_code == 200
            

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')
