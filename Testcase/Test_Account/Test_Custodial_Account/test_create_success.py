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
            ("BTC 创建+查询+删除托管账户","托管账户BTC"+str(Conf.Config.now_timestamp()),"BTC"),
            # ("DOGE 创建+查询+删除托管账户","托管账户DOGE"+str(Conf.Config.now_timestamp()),"DOGE"),
            # ("ETH 创建+查询+删除托管账户","托管账户ETH"+str(Conf.Config.now_timestamp()),"ETH"),
            # ("GOERLI 创建+查询+删除托管账户","托管账户GOERLI"+str(Conf.Config.now_timestamp()),"GOERLI"),
            # ("MATIC 创建+查询+删除托管账户","托管账户MATIC"+str(Conf.Config.now_timestamp()),"MATIC"),
            # ("BSC 创建+查询+删除托管账户","托管账户BSC"+str(Conf.Config.now_timestamp()),"BSC"),
            # ("IRIS 创建+查询+删除托管账户","托管账户IRIS"+str(Conf.Config.now_timestamp()),"IRIS"),
            # ("ATOM 创建+查询+删除托管账户","托管账户ATOM"+str(Conf.Config.now_timestamp()),"ATOM"),
            # ("CLV 创建+查询+删除托管账户","托管账户CLV"+str(Conf.Config.now_timestamp()),"CLV"),
            # ("DOT 创建+查询+删除托管账户","托管账户DOT"+str(Conf.Config.now_timestamp()),"DOT")
        ]

    if env_type == 1: #生产
        test_data = [
            ("BTC 创建+查询+删除托管账户","托管账户BTC"+str(Conf.Config.now_timestamp()),"BTC"),
            ("DOGE 创建+查询+删除托管账户","托管账户DOGE"+str(Conf.Config.now_timestamp()),"DOGE"),
            ("ETH 创建+查询+删除托管账户","托管账户ETH"+str(Conf.Config.now_timestamp()),"ETH"),
            ("MATIC 创建+查询+删除托管账户","托管账户MATIC"+str(Conf.Config.now_timestamp()),"MATIC"),
            ("BSC 创建+查询+删除托管账户","托管账户BSC"+str(Conf.Config.now_timestamp()),"BSC"),
            ("IRIS 创建+查询+删除托管账户","托管账户IRIS"+str(Conf.Config.now_timestamp()),"IRIS"),
            ("ATOM 创建+查询+删除托管账户","托管账户ATOM"+str(Conf.Config.now_timestamp()),"ATOM"),
            ("CLV 创建+查询+删除托管账户","托管账户CLV"+str(Conf.Config.now_timestamp()),"CLV"),
            ("DOT 创建+查询+删除托管账户","托管账户DOT"+str(Conf.Config.now_timestamp()),"DOT")
        ]

    @allure.story("Create Custodial Account Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,name,networkCode', test_data)
    def test_create_account_custodial(self, test_title, name, networkCode):
        
        with allure.step("创建托管账户"):
            custodial_account = Http.HttpUtils.create_custodial_account(name,networkCode)
            assert custodial_account.status_code == 200
            assert custodial_account.json()["status"] == "enable"
            id = custodial_account.json()["id"]
            address = custodial_account.json()["address"]

        with allure.step("查询账户列表"):
            account_list = Http.HttpUtils.get_account_list(networkCode,address,"custodial")
            assert account_list.status_code == 200
            assert account_list.json()[0]["id"] == id
            assert account_list.json()[0]["address"] == address

        with allure.step("查询账户byid"):
            account_detail = Http.HttpUtils.get_account_byid(id)
            assert account_detail.status_code == 200
            assert account_detail.json()["id"] == id
            assert account_detail.json()["address"] == address

        with allure.step("修改账户byid"):
            name_update = name + "_" + str(Conf.Config.now_timestamp())
            account_update = Http.HttpUtils.update_account_byid(id,name_update)
            assert account_update.status_code == 200
            assert account_update.json()["name"] == name_update

        with allure.step("删除账户byid"):
            account_del = Http.HttpUtils.del_account_byid(id)
            assert account_del.status_code == 200

        with allure.step("查询账户byid"):
            account_detail = Http.HttpUtils.get_account_byid(id)
            assert account_detail.status_code == 404
            assert account_detail.json()["code"] == 2200000
            assert account_detail.json()["message"] == "account not found"

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')
