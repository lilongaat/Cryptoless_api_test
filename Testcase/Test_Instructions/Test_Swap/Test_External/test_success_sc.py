import json
import random
import string
from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
from Common import Http, Conf
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))

# external
@allure.feature("Swap_Success!")
class Test_swap_success:
    test_data = [
        # BSC网络
        # ("正常SWAP(BNB-USDC)",["100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33"],"BSC","BNB","USDC","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","1",str(Conf.Config.random_amount(7))),
        # ("正常SWAP(USDC-BNB)",["100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33"],"BSC","USDC","BNB","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","1",str(Conf.Config.random_amount(4))),
        # ("正常SWAP(USDC-USDT)",["100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33"],"BSC","USDC","USDT","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","1",str(Conf.Config.random_amount(4))),
        # MATIC网络
        # ("正常SWAP(MATIC-USDC)",["100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33"],"MATIC","MATIC","USDC","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","1",str(Conf.Config.random_amount(4))),
        # ("正常SWAP(USDC-MATIC)",["100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33"],"MATIC","USDC","MATIC","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","1",str(Conf.Config.random_amount(4))),
        # ("正常SWAP(USDC-USDT)",["100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33"],"MATIC","USDC","USDT","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","1",str(Conf.Config.random_amount(4))),
    ]

    @allure.story("External_Swap_Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,networkCode,from_coin,to_coin,address,slippage,fromAmount', test_data)
    def test_external(self,test_title,privatekey,networkCode,from_coin,to_coin,address,slippage,fromAmount):

        with allure.step("查询账户from_coin holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,from_coin,address)
            assert holders.status_code == 200

        with allure.step("查询账户to_coin holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,to_coin,address)
            assert holders.status_code == 200

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_coin,
                "to":to_coin,
                "address":address,
                "fromAmount":fromAmount,
                "slippage":slippage
            }
            transactionParams = {
                "memo":''.join(random.sample(string.ascii_letters + string.digits, 10))
            }
            transfer = Http.HttpUtils.instructions("swap",body,networkCode,[],transactionParams)

            assert transfer.status_code == 200

            id = transfer.json()["_embedded"]["transactions"][0]["id"]
            requiredSignings = transfer.json()["_embedded"]["transactions"][0]["requiredSignings"]
            serialized = transfer.json()["_embedded"]["transactions"][0]["serialized"]

            signatures = []
            for i in range(len(requiredSignings)):
                hash = requiredSignings[i]["hash"]
                publickey = requiredSignings[i]["publicKeys"][0]
                signature = {
                    "hash":hash,
                    "publicKey":publickey,
                    "signature":Conf.Config.sign(privatekey[0],hash)

                }
                signatures.append(signature)

        with allure.step("签名交易——instructions"):
            sign = Http.HttpUtils.sign(id,signatures,serialized)
            assert sign.status_code == 200
            assert sign.json()["status"] == "PENDING"

        # with allure.step("查询账户from_coin holders信息——holders"):
        #     holders = Http.HttpUtils.get_holders(networkCode,from_coin,address)
        #     assert holders.status_code == 200

        # with allure.step("查询账户to_coin holders信息——holders"):
        #     holders = Http.HttpUtils.get_holders(networkCode,to_coin,address)
        #     assert holders.status_code == 200

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')