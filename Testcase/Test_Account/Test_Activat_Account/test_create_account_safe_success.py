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
class Test_create_account:

    test_data = [
        # 测试
        ("创建安全账户自动激活","ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187",["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0","02ac5e97a0659d6ce59c5b10b2ace331bffa276a555ff333b09beda99bd6b9f52e"],"ETH-RINKEBY","ETH")
    ]

    @allure.story("Create Account_Safe Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol', test_data)
    def test_create_account_safe(self, test_title, privatekey, PublicKeys, networkCode, symbol):
        
        with allure.step("创建账户"):
            acc = Http.HttpUtils.post_create_account(networkCode,symbol,PublicKeys,2)
            assert acc.status_code == 200
            assert acc.json()["status"] == 0
            accountid = acc.json()["id"]
            account_address = acc.json()["address"]

        with allure.step("查询代理账户列表"):
            agent = Http.HttpUtils.get_safe_agents()
            assert agent.status_code == 200

        with allure.step("激活账户"):
            act = Http.HttpUtils.post_safe_activation(accountid)
            assert act.status_code == 200
            assert act.json()["status"] == 0

        with allure.step("查询激活账户交易 交易成功"):
            for i in range(10):
                sleep(10)
                act_ = Http.HttpUtils.get_safe_activation(accountid)
                assert act_.status_code == 200
                if (act_.json()[0]["transaction"]["status"] == "SETTLED"):
                    assert act_.json()[0]["account"]["status"] == 2
                    assert act_.json()[0]["status"] == 1
                    break

        with allure.step("查询账户状态"):
            acc_detail = Http.HttpUtils.get_account(account_address)
            assert acc_detail.status_code == 200
            assert acc_detail.json()[0]["status"] == 2


if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')
