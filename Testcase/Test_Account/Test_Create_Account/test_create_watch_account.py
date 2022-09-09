import requests
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http,Conf
from Common.Loguru import logger

path_eth_address = "/Users/lilong/Documents/Test_Api/Testcase/Test_Account/Test_Create_Account/eth_address_d.csv"
list_address = Conf.Config.read_csv(path_eth_address)[0:1]

token = 'eyJzaWduYXR1cmUiOiIweGU4YzU0YjkzYTRlZDBmM2UxY2FkMDVjMDQzZmQzY2U0MjUwNTExNzY4MGY4NWViMmViMzAzZjQ5ZjNhMGFmYjU1OWExOWQxNDg2OTI1YTM0YzFmYTMxNWYzMzhjYTRhNGM2NzY0YjNmNjhiODMxY2VkMmZlNGUxOGVkMWVkNTMwMWMiLCJib2R5IjoiV2ViMyBUb2tlbiBWZXJzaW9uOiAyXG5Ob25jZTogNDE0NDU2MDhcbklzc3VlZCBBdDogVGh1LCAyNSBBdWcgMjAyMiAxMTozMjoyMCBHTVRcbkV4cGlyYXRpb24gVGltZTogTW9uLCAyNSBBdWcgMjA0MiAxMTozMjoyMCBHTVQifQ=='

@allure.feature("Create Accounts!")
class Test_create_Account:
    test_data = list_address

    @allure.story("Create ETH Accounts!")
    @allure.title('hhh')
    @pytest.mark.parametrize('key,value', test_data)
    def test_create_account_eth(self, key, value):

        with allure.step("注册观察账户"):
            creat_account = Http.HttpUtils.post_create_account("ETH",[],1,value,token)
            assert creat_account.status_code == 200

        with allure.step("查询用户所有账户"):
            accounts  = Http.HttpUtils.get_account("",token)
            assert accounts.status_code == 200

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--clean-alluredir','--alluredir=Report/Allure'])
    os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')