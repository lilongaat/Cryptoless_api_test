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
@allure.feature("Account!")
class Test_create_safe_account:
    if env_type == 0: #测试
        test_data = [
            # BTC
            ("BTC创建2-2安全账户 全custodial","安全账户BTC2-2-"+str(Conf.Config.now_timestamp()),"BTC",None,None),
            ("BTC创建2-2安全账户 custodial+owner","安全账户BTC2-2-"+str(Conf.Config.now_timestamp()),"BTC","02e8852463021b47fe5214c599e87e431f2eb1219044946bbff397afd0518b85a6",None),
            ("BTC创建2-3安全账户","安全账户BTC2-3-"+str(Conf.Config.now_timestamp()),"BTC","02e8852463021b47fe5214c599e87e431f2eb1219044946bbff397afd0518b85a6","0231e263a7e95bf5107b88b85b49918841b937305cce5dae7dd7ba9b86fc460f70"),

            #GOERLI
            ("Goerli创建2-2安全账户 全custodial","安全账户GOERLI2-2-"+str(Conf.Config.now_timestamp()),"GOERLI",None,None),
            ("Goerli创建2-2安全账户 custodial+owner","安全账户GOERLI2-2-"+str(Conf.Config.now_timestamp()),"GOERLI","0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113",None),
            ("Goerli创建2-3安全账户","安全账户GOERLI2-3-"+str(Conf.Config.now_timestamp()),"GOERLI","0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113","03c420167aaf4fc7106646b2fe485519e5569ceb1584ae31d62537e349a4e4b5a9"),

            #MATIC
            ("MATIC创建2-2安全账户 全custodial","安全账户MATIC2-2-"+str(Conf.Config.now_timestamp()),"MATIC",None,None),
            ("MATIC创建2-2安全账户 custodial+owner","安全账户MATIC2-2-"+str(Conf.Config.now_timestamp()),"MATIC","0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113",None),
            ("MATIC创建2-3安全账户","安全账户MATIC2-3-"+str(Conf.Config.now_timestamp()),"MATIC","0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113","03c420167aaf4fc7106646b2fe485519e5569ceb1584ae31d62537e349a4e4b5a9"),

            #IRIS
            ("IRIS创建2-2安全账户 全custodial","安全账户IRIS2-2-"+str(Conf.Config.now_timestamp()),"IRIS",None,None),
            ("IRIS创建2-2安全账户 custodial+owner","安全账户IRIS2-2-"+str(Conf.Config.now_timestamp()),"IRIS","0260fbc9e026fe789a5a3c26289577719900c6046dc1d9ac1471b8eb08d15d0de4",None),
            ("IRIS创建2-3安全账户","安全账户IRIS2-3-"+str(Conf.Config.now_timestamp()),"IRIS","0260fbc9e026fe789a5a3c26289577719900c6046dc1d9ac1471b8eb08d15d0de4","02e3209ac96c70b2d3366bb2a7cf54b93592b63093431a853679ca8c74b4dbb545"),

            #ATOM
            ("ATOM创建2-2安全账户 全custodial","安全账户ATOM2-2-"+str(Conf.Config.now_timestamp()),"ATOM",None,None),
            ("ATOM创建2-2安全账户 custodial+owner","安全账户ATOM2-2-"+str(Conf.Config.now_timestamp()),"ATOM","027243806b1abdb1737b45d4a0619112bf464e13407b7d37dd2da2821bc6fbcac4",None),
            ("ATOM创建2-3安全账户","安全账户ATOM2-3-"+str(Conf.Config.now_timestamp()),"ATOM","027243806b1abdb1737b45d4a0619112bf464e13407b7d37dd2da2821bc6fbcac4","03d36556045bc8bac44e1fb88bd1840d68077fded4371e8e8c45ffb9788b525329"),
            
        ]
    elif env_type == 1: #生产
        test_data = [
            # BTC
            ("BTC创建2-2安全账户 全custodial","安全账户BTC2-2-"+str(Conf.Config.now_timestamp()),"BTC",None,None),
            ("BTC创建2-2安全账户 custodial+owner","安全账户BTC2-2-"+str(Conf.Config.now_timestamp()),"BTC","02e8852463021b47fe5214c599e87e431f2eb1219044946bbff397afd0518b85a6",None),
            ("BTC创建2-3安全账户","安全账户BTC2-3-"+str(Conf.Config.now_timestamp()),"BTC","02e8852463021b47fe5214c599e87e431f2eb1219044946bbff397afd0518b85a6","0231e263a7e95bf5107b88b85b49918841b937305cce5dae7dd7ba9b86fc460f70"),

            #MATIC
            ("MATIC创建2-2安全账户 全custodial","安全账户MATIC2-2-"+str(Conf.Config.now_timestamp()),"MATIC",None,None),
            ("MATIC创建2-2安全账户 custodial+owner","安全账户MATIC2-2-"+str(Conf.Config.now_timestamp()),"MATIC","0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113",None),
            ("MATIC创建2-3安全账户","安全账户MATIC2-3-"+str(Conf.Config.now_timestamp()),"MATIC","0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113","03c420167aaf4fc7106646b2fe485519e5569ceb1584ae31d62537e349a4e4b5a9"),

            #IRIS
            ("IRIS创建2-2安全账户 全custodial","安全账户IRIS2-2-"+str(Conf.Config.now_timestamp()),"IRIS",None,None),
            ("IRIS创建2-2安全账户 custodial+owner","安全账户IRIS2-2-"+str(Conf.Config.now_timestamp()),"IRIS","0260fbc9e026fe789a5a3c26289577719900c6046dc1d9ac1471b8eb08d15d0de4",None),
            ("IRIS创建2-3安全账户","安全账户IRIS2-3-"+str(Conf.Config.now_timestamp()),"IRIS","0260fbc9e026fe789a5a3c26289577719900c6046dc1d9ac1471b8eb08d15d0de4","02e3209ac96c70b2d3366bb2a7cf54b93592b63093431a853679ca8c74b4dbb545"),

            #ATOM
            ("ATOM创建2-2安全账户 全custodial","安全账户ATOM2-2-"+str(Conf.Config.now_timestamp()),"ATOM",None,None),
            ("ATOM创建2-2安全账户 custodial+owner","安全账户ATOM2-2-"+str(Conf.Config.now_timestamp()),"ATOM","027243806b1abdb1737b45d4a0619112bf464e13407b7d37dd2da2821bc6fbcac4",None),
            ("ATOM创建2-3安全账户","安全账户ATOM2-3-"+str(Conf.Config.now_timestamp()),"ATOM","027243806b1abdb1737b45d4a0619112bf464e13407b7d37dd2da2821bc6fbcac4","03d36556045bc8bac44e1fb88bd1840d68077fded4371e8e8c45ffb9788b525329"),
        ]

    @allure.story("Create Safe Account Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,name,networkCode,owner,recovery', test_data)
    def test_create_account_safe(self, test_title,name,networkCode,owner,recovery):

        with allure.step("创建安全账户"):
            safe_account = Http.HttpUtils.create_safe_account(name,networkCode,owner,recovery)
            assert safe_account.status_code == 200
            if networkCode == "GOERLI" or networkCode == "MATIC":
                assert safe_account.json()["status"] == "inactive"
            else:
                assert safe_account.json()["status"] == "enable"
            id = safe_account.json()["id"]
            address = safe_account.json()["address"]

        sleep(3)
        with allure.step("查询账户byid"):
            account_detail = Http.HttpUtils.account_byid(id)
            assert account_detail.status_code == 200
            assert account_detail.json()["address"] == address
            if networkCode == "GOERLI" or networkCode == "MATIC":
                assert safe_account.json()["status"] == "inactive"
            else:
                assert safe_account.json()["status"] == "enable"

        logger.debug("\n\n"+test_title+"\n"+address)

        with allure.step("删除账户byid"):
            account_del = Http.HttpUtils.del_account_byid(id)
            assert account_del.status_code == 200




if __name__ == '__main__':
    path = os.path.abspath(__file__) + "::Test_create_safe_account"
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')
