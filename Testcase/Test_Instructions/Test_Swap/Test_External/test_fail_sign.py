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
@allure.feature("Swap Fail!")
class Test_swap_fail:
    if env_type == 0: #测试
        test_data = [
            # MATIC网络
            ("正常SWAP(MATIC-USDC)",["0e7262525d4090224c33252906908ac9bbbcf51711261020c9eba35f6e76b508"],"MATIC","MATIC","USDC","0xe525E7cd17f6Dc950492755A089E452fd5d9d44f","1",str(Conf.Config.random_amount(4)),400,2300000),
            ("正常SWAP(USDC-MATIC)",["0e7262525d4090224c33252906908ac9bbbcf51711261020c9eba35f6e76b508"],"MATIC","USDC","MATIC","0xe525E7cd17f6Dc950492755A089E452fd5d9d44f","1",str(Conf.Config.random_amount(4)),400,2300000),
            ("正常SWAP(USDC-USDT)",["0e7262525d4090224c33252906908ac9bbbcf51711261020c9eba35f6e76b508"],"MATIC","USDC","USDT","0xe525E7cd17f6Dc950492755A089E452fd5d9d44f","1",str(Conf.Config.random_amount(4)),400,2300000),
        ]
    if env_type == 1: #生产
        test_data = [
            # BSC网络
            # ("正常SWAP(BNB-USDC)",["0e7262525d4090224c33252906908ac9bbbcf51711261020c9eba35f6e76b508"],"BSC","BNB","USDC","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","1",str(Conf.Config.random_amount(7)),400,2300000),
            # ("正常SWAP(USDC-BNB)",["0e7262525d4090224c33252906908ac9bbbcf51711261020c9eba35f6e76b508"],"BSC","USDC","BNB","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","1",str(Conf.Config.random_amount(4)),400,2300000),
            # ("正常SWAP(USDC-USDT)",["0e7262525d4090224c33252906908ac9bbbcf51711261020c9eba35f6e76b508"],"BSC","USDC","USDT","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","1",str(Conf.Config.random_amount(4)),400,2300000),
            # MATIC网络
            # ("正常SWAP(MATIC-USDC)",["0e7262525d4090224c33252906908ac9bbbcf51711261020c9eba35f6e76b508"],"MATIC","MATIC","USDC","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","1",str(Conf.Config.random_amount(4)),400,2300000),
            # ("正常SWAP(USDC-MATIC)",["0e7262525d4090224c33252906908ac9bbbcf51711261020c9eba35f6e76b508"],"MATIC","USDC","MATIC","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","1",str(Conf.Config.random_amount(4)),400,2300000),
            # ("正常SWAP(USDC-USDT)",["0e7262525d4090224c33252906908ac9bbbcf51711261020c9eba35f6e76b508"],"MATIC","USDC","USDT","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","1",str(Conf.Config.random_amount(4)),400,2300000),
        ]

    @allure.story("External Swap Sign Fail!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,networkCode,from_coin,to_coin,address,slippage,fromAmount,status_check,code_check', test_data)
    def test_external(self,test_title,privatekey,networkCode,from_coin,to_coin,address,slippage,fromAmount,status_check,code_check):

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
            assert sign.status_code == status_check
            assert sign.json()["code"] == code_check


if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')