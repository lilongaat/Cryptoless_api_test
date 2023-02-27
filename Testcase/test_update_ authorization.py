from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
from Common import Http,Conf,Connect
from Common.Loguru import logger

from Config.readconfig import ReadConfig,WriteConfig
env_type = int(ReadConfig().get_env('type'))

@allure.feature("Users!")
class Test_create_custodial_account:

    if env_type == 0: #测试
        test_data = [
            ("用户登陆成功刷新token","test@qq.com")
        ]

    elif env_type == 1: #生产
        test_data = [
            ("用户登陆成功刷新token","lilongaat@gmail.com")
        ]

    @allure.story("User Update Authorization!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,email', test_data)
    def test_create_account_custodial(self, test_title, email):
        
        with allure.step("用户请求登陆"):
            connect_request = Http.HttpUtils.connect_req(email)
            assert connect_request.status_code == 200
        
        with allure.step("redis查询验证码"):
            verifycode = Connect.Redis.get_verifycode(email)
        
        with allure.step("用户确认连接"):
            confirm = Http.HttpUtils.connect_confirm(email,oneTimePassword=verifycode)
            assert confirm.status_code == 200
            token_vaule = confirm.json()['token']
            logger.debug(token_vaule)

        with allure.step("修改confing.ini文件"):
            WriteConfig.update_config('token',token_vaule)
            

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')