from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http
from Common.Loguru import logger

@allure.feature("Create Account!")
class Test_create_account_Fail:

    test_data = [
        ("激活账户 accountId 为空","",400),
        ("激活账户 accountId 不存在","155657419896488345",404)
    ]

    @allure.story("Create Account_Safe Fail!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,accountid,status_code_check', test_data,)
    def test_create_account_safe(self, test_title, accountid,status_code_check):
        with allure.step("激活账户"):
            act = Http.HttpUtils.post_safe_activation(accountid)
            assert act.status_code == status_code_check


if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')
