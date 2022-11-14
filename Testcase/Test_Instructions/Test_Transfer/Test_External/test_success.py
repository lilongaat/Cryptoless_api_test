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
@allure.feature("Transfers_Success!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # BTC网络
            # ("External账户BTC转账",["b61190f8b2fcb4754ff8527f083bb3df68bf89285d7c5e428276f5f4572b7abe"],"BTC","BTC","tb1qhcuul2fcyv5rvr5mc5cy5saz0q5p3kx0gsy3c0","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun",str(Conf.Config.random_amount(8))),
            # # Goerli网络
            # ("External账户Goerli转账",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da"],"GOERLI","GoerliETH","0xe525E7cd17f6Dc950492755A089E452fd5d9d44f","0x2B0EfCF16EC1E4C5eD82dBB4Fce9B4811485e650",str(Conf.Config.random_amount(7))),
            # ("External账户ERC20转账",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da"],"GOERLI","Long","0xe525E7cd17f6Dc950492755A089E452fd5d9d44f","0x2B0EfCF16EC1E4C5eD82dBB4Fce9B4811485e650",str(round(random.uniform(1,10), random.randint(1,18)))),
            # # MATIC网络
            # ("External账户MATIC转账",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da"],"MATIC","MATIC","0xe525E7cd17f6Dc950492755A089E452fd5d9d44f","0xDBA67bAa3CA1e89a2BDf0fEeE4592595b130888A",str(Conf.Config.random_amount(7))),
            ("External账户MATIC转账",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da"],"MATIC","USDC","0xe525E7cd17f6Dc950492755A089E452fd5d9d44f","0xDBA67bAa3CA1e89a2BDf0fEeE4592595b130888A",str(Conf.Config.random_amount(5))),
            # IRIS
            # ("External账户IRIS转账",["d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b"],"IRIS","IRIS","iaa1ed68xf6453t7u4ttsmphdrwqflx2l90e6ymuaq","iaa18hxtn9lx9swxf4j7ytdmn8yxsvyknh86kdgpvc",str(Conf.Config.random_amount(5))),
            # CLV
            # ("External账户CLV转账",["7967c43bd3f3874ccfa6ff6ceda5faa8c699ad0fe2be33f44c8bb8abcb23a2fd"],"CLV","CLV","5Hdmv7BeAe1XFJXso8oGMidGp186cb4uNTNMywp6fBY7UEsr","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT",str(Conf.Config.random_amount(5))),
        ]
    elif env_type == 1: #生产
        test_data = [
            # DOGE网络
            # ("External账户DOGE转账",["6a7e8dceb20664b93a7a901e23ba05c34b4378a58e8b409cfceac35a3740345f"],"DOGE","DOGE","DK2mfHibfaudY7EviQ1KESpLjyiQXHLbAA","DGnb5SNRnEyAx9xNuHGxbiY4ysHPsxegP9",str(round(random.uniform(2,3), random.randint(3,5)))),
            # BSC网络
            # ("External账户BNB转账",["100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33"],"BSC","BNB","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","0xDBA67bAa3CA1e89a2BDf0fEeE4592595b130888A",str(Conf.Config.random_amount(8))),
            # ("External账户USDC转账",["100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33"],"BSC","USDC","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","0xDBA67bAa3CA1e89a2BDf0fEeE4592595b130888A",str(Conf.Config.random_amount(8))),
            # # MATIC网络
            # ("External账户MATIC转账",["100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33"],"MATIC","MATIC","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","0xDBA67bAa3CA1e89a2BDf0fEeE4592595b130888A",str(Conf.Config.random_amount(4))),
            # ("External账户USDC转账",["100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33"],"MATIC","USDC","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","0xDBA67bAa3CA1e89a2BDf0fEeE4592595b130888A",str(Conf.Config.random_amount(5))),
            # ("External账户MATIC转账self",["100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33"],"MATIC","MATIC","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939",str(Conf.Config.random_amount(4))),
            # ("External账户USDC转账self",["100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33"],"MATIC","USDC","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","0x9b532cf5F662e51ba643672797Ad3eC1A60bb939",str(Conf.Config.random_amount(5))),
            # IRIS网络
            ("External账户IRIS转账",["a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c"],"IRIS","IRIS","iaa18j8rds5hqwp88s4qsrytq5w4eafu288cfza9th","iaa18hxtn9lx9swxf4j7ytdmn8yxsvyknh86kdgpvc",str(Conf.Config.random_amount(4))),
            # CLV网络
            ("External账户CLV转账",["426a6690c29c5ee0052712c1fda0cc38691f3faf2a571f4b04c9705bbf3f921b"],"CLV","CLV","5GF2XqzK1ERH6AGkyHz1jmMLMCVGBUEyRBxJb5TFWxhiS6EY","5FXjWgPEDvrc5A3SDVHayVGfdAp9QquU5jANaZMfLzVue5k6",str(Conf.Config.random_amount(4))),
        ]

    @allure.story("External_Transfers_Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_external(self,test_title,privatekey,networkCode,symbol,from_add,to_add,amount):

        with allure.step("查询From账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders.status_code == 200

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_add,
                "to":to_add,
                "symbol":symbol,
                "amount":amount
            }
            transactionParams = {
                "memo":''.join(random.sample(string.ascii_letters + string.digits, 10))
            }
            transfer = Http.HttpUtils.instructions("transfer",body,networkCode,[],transactionParams)

            assert transfer.status_code == 200
            assert transfer.json()["_embedded"]["transactions"][0]["status"] == "BUILDING"
            assert transfer.json()["body"]["symbol"] == symbol
            assert transfer.json()["body"]["amount"] == amount
            assert transfer.json()["body"]["from"] == from_add
            assert transfer.json()["body"]["to"] == to_add

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
            assert sign.json()["status"] == "SIGNED"

        with allure.step("广播交易"):
            send = Http.HttpUtils.send(id)
            assert send.status_code == 200
            assert send.json()["status"] == "PENDING"

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')