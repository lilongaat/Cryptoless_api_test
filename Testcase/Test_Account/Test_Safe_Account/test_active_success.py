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
@allure.feature("Create Safe Account!")
class Test_create_safe_account_payer:

    if env_type == 0: #测试
        test_data = [
            # Goerli 
            # ("payer_relay 代付激活账户","0x79f255cec4b987a4b4fd10858bc815a3b6134006","",""),
            # ("payer_relay 自付激活账户","0xbb80978baa828a7296a5ae45f7d77a02ff5bcd72","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da",""),
            # ("payer_relay 指定payer激活账户","0xeb69947869312949ba6dcbbfead304662abba2ae","9cbca176aff8c48ebd9a27c31455e34ebc86e25a17e22b3d65a716fc851ada38","0326288a7bbff5dc672bfec0a0a02ccae3eeb3e93a0294c8e0f534c97438de0fce"),
        ]

    @allure.story("Create Safe Account Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,address,payer_prv,payer_pub', test_data)
    def test_create_account_safe(self, test_title,address,payer_prv,payer_pub):
        
        with allure.step("账户根据地址查询id"):
            acc = Http.HttpUtils.accounts(address=address)
            assert acc.status_code == 200
            id_acc = acc.json()["list"][0]["id"]
            

        with allure.step("payer创建激活安全账户交易"):
            activation_safe_account = Http.HttpUtils.activation_safe_account(id_acc,payer_pub)
            assert activation_safe_account.status_code == 200

        if len(payer_prv) == 0:
            pass
        else:
            with allure.step("payer签名交易"):
                id = activation_safe_account.json()["id"]
                hash = activation_safe_account.json()["requiredSignings"][0]["hash"]
                publickey = activation_safe_account.json()["requiredSignings"][0]["publicKeys"][0]
                signatures = {
                        "hash":hash,
                        "publicKey":publickey,
                        "signature":Conf.Config.sign(payer_prv,hash)

                    }

                sign1 = Http.HttpUtils.sign(id,signatures)
                assert sign1.status_code == 200
                assert sign1.json()["statusDesc"] == "SIGNED"
            

            with allure.step("广播交易"):
                send = Http.HttpUtils.send(id)
                assert send.status_code == 200
                assert send.json()["statusDesc"] == "PENDING"



if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')
