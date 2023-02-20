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


# payer激活安全账户
@allure.feature("Account!")
class Test_create_safe_account_payer:

    if env_type == 0: #测试
        test_data = [
            # Goerli 
            ("safe账户relay自付激活账户手续费不足","0xef437c56695d58d1186a26b78fb218475cc9552a","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da",None,400,2100000),
            ("safe账户指定payer激活账户手续费不足","0xef437c56695d58d1186a26b78fb218475cc9552a","8fc20f7478c1a6eb5b260fabcdf378fd23c765947867ca6ee84a78c93d9b9301","030f5075174fdc05d1094448eb74eca9fe2c4d4c02e659aa650c249b660913fd9f",400,2100000),
        ]
    elif env_type == 0: #生产
        test_data = []

    @allure.story("Active Safe Account Fail Feepoor!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,address,payer_prv,payer_pub,status_code,code', test_data)
    def test_create_account_safe(self, test_title,address,payer_prv,payer_pub,status_code,code):
        
        with allure.step("账户根据地址查询id"):
            acc = Http.HttpUtils.accounts(address=address)
            assert acc.status_code == 200
            id_acc = acc.json()["list"][0]["id"]
            
        with allure.step("payer创建激活安全账户交易"):
            activation_safe_account = Http.HttpUtils.activation_safe_account(id_acc,payer_pub)
            assert activation_safe_account.status_code == status_code
            assert activation_safe_account.json()["code"] == code


if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')
