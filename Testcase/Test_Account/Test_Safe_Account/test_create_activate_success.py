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


# 创建安全账户自动激活
@allure.feature("Create Safe Account!")
class Test_create_safe_account:
    if env_type == 0: #测试
        test_data = [
            ("Goerli创建2-2安全账户+Rely激活","安全账户MATIC2-2-"+str(Conf.Config.now_timestamp()),["0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113","03c420167aaf4fc7106646b2fe485519e5569ceb1584ae31d62537e349a4e4b5a9"],"GOERLI")
        ]

    @allure.story("Create Safe Account Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,name,PublicKeys,networkCode', test_data)
    def test_create_account_safe(self, test_title, name, PublicKeys, networkCode):

        with allure.step("创建安全账户"):
            safe_account = Http.HttpUtils.create_safe_account(name,networkCode,PublicKeys[0],PublicKeys[1])
            assert safe_account.status_code == 200
            assert safe_account.json()["status"] == "inactive"
            id = safe_account.json()["id"]
            address = safe_account.json()["address"]

        sleep(10)
        with allure.step("查询账户byid"):
            account_detail = Http.HttpUtils.get_account_byid(id)
            assert account_detail.status_code == 200
            assert account_detail.json()["address"] == address
            assert account_detail.json()["status"] == "pending"


# 一个payer构建激活安全账户交易
@allure.feature("Create Safe Account!")
class Test_create_safe_account_payer:

    if env_type == 0: #测试
        test_data = [
            # MATIC payer=0xDBA67bAa3CA1e89a2BDf0fEeE4592595b130888A
            ("MATIC创建2-2安全账户+payer激活","安全账户MATIC2-2-"+str(Conf.Config.now_timestamp()),["4d87c72cee9d4b257368f448f4f7406d0ce98947eb30fcaa8194319303534b13"],["02e5230ff44191de07476a79c8908374bec9cb7eefb4218513379b0450cd0e381d"],["0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113",""],"MATIC"),
            # ("MATIC创建2-3安全账户+payer激活","安全账户MATIC2-3-"+str(Conf.Config.now_timestamp()),["4d87c72cee9d4b257368f448f4f7406d0ce98947eb30fcaa8194319303534b13"],["02e5230ff44191de07476a79c8908374bec9cb7eefb4218513379b0450cd0e381d"],["0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113","03c420167aaf4fc7106646b2fe485519e5569ceb1584ae31d62537e349a4e4b5a9"],"MATIC"),

            # Goerli payer=0xDBA67bAa3CA1e89a2BDf0fEeE4592595b130888A
            # ("Goerli创建2-2安全账户+payer激活","安全账户Goerli2-2-"+str(Conf.Config.now_timestamp()),["4d87c72cee9d4b257368f448f4f7406d0ce98947eb30fcaa8194319303534b13"],["02e5230ff44191de07476a79c8908374bec9cb7eefb4218513379b0450cd0e381d"],["0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113",""],"GOERLI"),
            # ("Goerli创建2-3安全账户+payer激活","安全账户Goerli2-3-"+str(Conf.Config.now_timestamp()),["4d87c72cee9d4b257368f448f4f7406d0ce98947eb30fcaa8194319303534b13"],["02e5230ff44191de07476a79c8908374bec9cb7eefb4218513379b0450cd0e381d"],["0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113","03c420167aaf4fc7106646b2fe485519e5569ceb1584ae31d62537e349a4e4b5a9"],"GOERLI")
        ]

    @allure.story("Create Safe Account Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,name,payer_prv,payer_pub,PublicKeys,networkCode', test_data)
    def test_create_account_safe(self, test_title, name, payer_prv, payer_pub, PublicKeys, networkCode):
        
        with allure.step("创建安全账户"):
            safe_account = Http.HttpUtils.create_safe_account(name,networkCode,PublicKeys[0],PublicKeys[1])
            assert safe_account.status_code == 200
            assert safe_account.json()["status"] == "inactive"
            id = safe_account.json()["id"]
            address = safe_account.json()["address"]

        with allure.step("查询账户byid"):
            account_detail = Http.HttpUtils.get_account_byid(id)
            assert account_detail.status_code == 200
            assert account_detail.json()["address"] == address
            assert account_detail.json()["status"] == "inactive"

        with allure.step("payer创建激活安全账户交易"):
            activation_safe_account = Http.HttpUtils.activation_safe_account(id,payer_pub[0])
            assert activation_safe_account.status_code == 200

            id = activation_safe_account.json()["transaction"]["id"]
            hash = activation_safe_account.json()["transaction"]["requiredSignings"][0]["hash"]
            publickey = activation_safe_account.json()["transaction"]["requiredSignings"][0]["publicKeys"][0]
            signatures = {
                    "hash":hash,
                    "publicKey":publickey,
                    "signature":Conf.Config.sign(payer_prv[0],hash)

                }

        with allure.step("签名激活交易"):
            sign1 = Http.HttpUtils.sign(id,signatures,"")
            assert sign1.status_code == 200
            assert sign1.json()["status"] == "SIGNED"



# 两个payer构建激活安全账户交易
@allure.feature("Create Safe Account!")
class Test_create_safe_account_payer_repeat:

    if env_type == 0: #测试
        test_data = [
            # MATIC payer1=0xDBA67bAa3CA1e89a2BDf0fEeE4592595b130888A;payer2=0xa2bA38107A3bEe65031d8f427797d10dB626fbF6
            ("创建安全账户+payer激活","安全账户MATIC2-2-"+str(Conf.Config.now_timestamp()),["4d87c72cee9d4b257368f448f4f7406d0ce98947eb30fcaa8194319303534b13","9ff56ed61c94b8af33481f27826ae574adfa2a9640d9e68b7115594fb16934e0"],["02e5230ff44191de07476a79c8908374bec9cb7eefb4218513379b0450cd0e381d","022c8955ff17013456fd8b268afcc28dc091e65c6f217b5138d3b4d585924d7dda"],["0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113",""],"MATIC"),
            # ("创建安全账户+payer激活","安全账户MATIC2-3-"+str(Conf.Config.now_timestamp()),["4d87c72cee9d4b257368f448f4f7406d0ce98947eb30fcaa8194319303534b13","9ff56ed61c94b8af33481f27826ae574adfa2a9640d9e68b7115594fb16934e0"],["02e5230ff44191de07476a79c8908374bec9cb7eefb4218513379b0450cd0e381d","022c8955ff17013456fd8b268afcc28dc091e65c6f217b5138d3b4d585924d7dda"],["0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113","03c420167aaf4fc7106646b2fe485519e5569ceb1584ae31d62537e349a4e4b5a9"],"MATIC"),
            
            # GOERLI payer1=0xDBA67bAa3CA1e89a2BDf0fEeE4592595b130888A;payer2=0xa2bA38107A3bEe65031d8f427797d10dB626fbF6
            # ("创建安全账户+payer激活","安全账户GOERLI2-2-"+str(Conf.Config.now_timestamp()),["4d87c72cee9d4b257368f448f4f7406d0ce98947eb30fcaa8194319303534b13","9ff56ed61c94b8af33481f27826ae574adfa2a9640d9e68b7115594fb16934e0"],["02e5230ff44191de07476a79c8908374bec9cb7eefb4218513379b0450cd0e381d","022c8955ff17013456fd8b268afcc28dc091e65c6f217b5138d3b4d585924d7dda"],["0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113",""],"GOERLI")
        ]

    @allure.story("Create Safe Account Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,name,payer_prv,payer_pub,PublicKeys,networkCode', test_data)
    def test_create_account_safe(self, test_title, name, payer_prv, payer_pub, PublicKeys, networkCode):
        
        with allure.step("创建安全账户"):
            safe_account = Http.HttpUtils.create_safe_account(name,networkCode,PublicKeys[0],PublicKeys[1])
            assert safe_account.status_code == 200
            assert safe_account.json()["status"] == "inactive"
            id = safe_account.json()["id"]
            address = safe_account.json()["address"]

        with allure.step("查询账户byid"):
            account_detail = Http.HttpUtils.get_account_byid(id)
            assert account_detail.status_code == 200
            assert account_detail.json()["address"] == address
            assert account_detail.json()["status"] == "inactive"

        with allure.step("payer1创建激活安全账户交易"):
            activation1_safe_account = Http.HttpUtils.activation_safe_account(id,payer_pub[0])
            assert activation1_safe_account.status_code == 200

            id1 = activation1_safe_account.json()["transaction"]["id"]
            hash1 = activation1_safe_account.json()["transaction"]["requiredSignings"][0]["hash"]
            publickey1 = activation1_safe_account.json()["transaction"]["requiredSignings"][0]["publicKeys"][0]
            signatures1 = {
                    "hash":hash1,
                    "publicKey":publickey1,
                    "signature":Conf.Config.sign(payer_prv[0],hash1)

                }

        with allure.step("payer2创建激活安全账户交易"):
            activation2_safe_account = Http.HttpUtils.activation_safe_account(id,payer_pub[1])
            assert activation2_safe_account.status_code == 200

            id2 = activation2_safe_account.json()["transaction"]["id"]
            hash2 = activation2_safe_account.json()["transaction"]["requiredSignings"][0]["hash"]
            publickey2 = activation2_safe_account.json()["transaction"]["requiredSignings"][0]["publicKeys"][0]
            signatures2 = {
                    "hash":hash2,
                    "publicKey":publickey2,
                    "signature":Conf.Config.sign(payer_prv[1],hash2)

                }

        with allure.step("签名交易——instructions"):
            sign1 = Http.HttpUtils.sign(id1,signatures1,"")
            assert sign1.status_code == 200
            assert sign1.json()["status"] == "SIGNED"

        with allure.step("签名交易——instructions"):
            sign2 = Http.HttpUtils.sign(id2,signatures2,"")
            assert sign2.status_code == 200
            assert sign2.json()["status"] == "SIGNED"


if __name__ == '__main__':
    path = os.path.abspath(__file__) + "::Test_create_safe_account_payer_repeat"
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')
