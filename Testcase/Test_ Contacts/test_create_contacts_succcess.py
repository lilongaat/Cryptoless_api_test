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

@allure.feature("Contacts!")
class Test_create_custodial_account:

    if env_type == 0: #测试
        test_data = [
            ("创建联系人","name","GOERLI","0xeef04bfaf08a5b8b4aaf8d2e01f1519e507c9de6"),
            ("ENS创建联系人","name","GOERLI","lilong.eth"),
        ]

    elif env_type == 1: #生产
        test_data = []

    @allure.story("Contacts Create Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,name,networkCode,address', test_data)
    def test_create_contacts(self, test_title,name,networkCode,address):
        
        with allure.step("创建联系人"):
            user = Http.HttpUtils.contacts_add(name,networkCode,address)
            assert user.status_code == 200
            

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')
