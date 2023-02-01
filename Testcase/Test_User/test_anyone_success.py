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
            "匿名用户登陆成功"
        ]

    elif env_type == 1: #生产
        test_data = [
            "匿名用户登陆成功"
        ]

    @allure.story("User Anonymous Connect Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title', test_data)
    def test_create_account_custodial(self, test_title):
        
        with allure.step("匿名用户登陆"):
            user = Http.HttpUtils.anonymous()
            assert user.status_code == 200
            

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')
