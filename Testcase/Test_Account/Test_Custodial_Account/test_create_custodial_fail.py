from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http,Conf
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))

@allure.feature("Create Custodial Account!")
class Test_create_custodial_account:

    if env_type == 0: #测试
        test_data = [
            ("创建托管账户name为空","","BTC",400,2100000),
            ("创建托管账户name超长","uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu","DOGE",400,2100000),
            ("创建托管账户网络不存在","Custodial_account","SOL",404,2200000),
            ("创建托管账户网络被禁用","Custodial_account","RINKEBY",400,2300000)
        ]

    elif env_type == 1: #生产
        test_data = [
            ("创建托管账户name为空","","BTC",400,2100000),
            ("创建托管账户name超长","uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu","DOGE",400,2100000),
            ("创建托管账户网络不存在","Custodial_account","SOL",404,2200000)
        ]

    @allure.story("Create Custodial Account Fail!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,name,networkCode,status_check,code_check', test_data)
    def test_create_account_custodial(self, test_title, name, networkCode, status_check, code_check):
        
        with allure.step("创建托管账户"):
            custodial_account = Http.HttpUtils.create_custodial_account(name,networkCode)
            assert custodial_account.status_code == status_check
            assert custodial_account.json()["code"] == code_check

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')
