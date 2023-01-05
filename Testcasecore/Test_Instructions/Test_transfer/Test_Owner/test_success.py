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
from Common import Http, Conf, Httpcore
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))


@allure.feature("Transfers Success!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # BTC
            # ("BTC extarnal账户转账","BTC","BTC","b61190f8b2fcb4754ff8527f083bb3df68bf89285d7c5e428276f5f4572b7abe","tb1qhcuul2fcyv5rvr5mc5cy5saz0q5p3kx0gsy3c0","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq","0.000008"),

            #DOGE
            # ("DOGE extarnal账户转账","DOGE","DOGE","c64d119f7ed0b07bb8994c8dc067e7e48823e02f68b47973ce58fbbd516b6ea8","DEayChkUr3QAJHgNu5D7pYnaTxZuBJZc9W","D9HfYYym4Ca49VE9FTTvmucCcyHTPspA3j","1.2"),

            #母账户
            # ("DOGE extarnal账户转账","DOGE","DOGE","2a5157b59f278bad91ee7e3596d2b49aff80af9b8bc736ff8a717b6c133dd0f0","D9HfYYym4Ca49VE9FTTvmucCcyHTPspA3j","DEayChkUr3QAJHgNu5D7pYnaTxZuBJZc9W","3"),

            # GOERLI
            ("GOERLI extarnal账户转账 nativecoin","GOERLI","GoerliETH","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xe525E7cd17f6Dc950492755A089E452fd5d9d44f","0xa7A9E710f9A3B4184D4F8B7d379CEC262f2382c2","0.00012"),
            # ("GOERLI extarnal账户转账 erc20coin","GOERLI","USDCC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xe525E7cd17f6Dc950492755A089E452fd5d9d44f","0xa7A9E710f9A3B4184D4F8B7d379CEC262f2382c2","0.000123"),

            # ("MATIC extarnal账户转账 nativecoin","MATIC","MATIC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xe525E7cd17f6Dc950492755A089E452fd5d9d44f","0xa7A9E710f9A3B4184D4F8B7d379CEC262f2382c2","0.00012"),

            #IRIS
            # ("IRIS extarnal账户转账","IRIS","IRIS","d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b","iaa1ed68xf6453t7u4ttsmphdrwqflx2l90e6ymuaq","iaa15h0lvaa6slvj0hg4d64548j2c5fds2zv8tkvgs","0.0005"),

            #CLV
            # ("CLV extarnal账户转账","CLV","CLV","7967c43bd3f3874ccfa6ff6ceda5faa8c699ad0fe2be33f44c8bb8abcb23a2fd","5Hdmv7BeAe1XFJXso8oGMidGp186cb4uNTNMywp6fBY7UEsr","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","0.00123"),
            # ("CLV extarnal账户转账","CLV","CLV","7cc57c9ab4d60f6991dd32827927266c90a7c165db6c71ea344c86a05e582b68","5DzGiGqFXM2TSa7vmYn4jEjdrDYobjGBBsEmHNPCEPEDsALX","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","9.987"),
        ]
    elif env_type == 1: #生产
        test_data = []

    @allure.story("Custodial Transfers Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,privatekey,from_add,to_add,amount', test_data)
    def test_custodial(self,test_title,networkCode,symbol,privatekey,from_add,to_add,amount):

        with allure.step("core查询账户holder信息"):
            holder = Httpcore.HttpCoreUtils.holder(networkCode=networkCode,symbol=symbol,address=from_add)
            assert holder.status_code ==200
            quantity = holder.json()["list"][0]["quantity"]

        with allure.step("core构建交易——instructions"):
            body = {
                "networkCode":networkCode,
                "type":"transfer",
                "body":{
                    "from":from_add,
                    "to":to_add,
                    "symbol":symbol,
                    "amount":amount
                },
                "transactionParams":{
                    "memo":''.join(random.sample(string.ascii_letters + string.digits, 10))
                }
            }
            transfer = Httpcore.HttpCoreUtils.core_instructions(body)
            assert transfer.status_code == 200
            assert transfer.json()["_embedded"]["transactions"][0]["statusDesc"] == "BUILDING"

            id = transfer.json()["_embedded"]["transactions"][0]["id"]
            requiredSignings = transfer.json()["_embedded"]["transactions"][0]["requiredSignings"]
            signatures = []
            for i in range(len(requiredSignings)):
                hash = requiredSignings[i]["hash"]
                publickey = requiredSignings[i]["publicKeys"][0]
                signature = {
                    "hash":hash,
                    "publicKey":publickey,
                    "signature":Conf.Config.sign(privatekey,hash)

                }
                signatures.append(signature)

        with allure.step("签名交易"):
            sign = Httpcore.HttpCoreUtils.core_sign(id,signatures)
            assert sign.status_code == 200

        # with allure.step("广播交易"):
        #     send = Httpcore.HttpCoreUtils.core_send(id)
        #     assert send.status_code == 200
        #     assert send.json()["statusDesc"] == "PENDING"

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')