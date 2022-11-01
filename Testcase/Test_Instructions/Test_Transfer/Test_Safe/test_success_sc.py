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

# safe
@allure.feature("Transfers_Success!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # # BTC网络
            # ("Safe2-2账户BTC转账",["b61190f8b2fcb4754ff8527f083bb3df68bf89285d7c5e428276f5f4572b7abe"],"BTC","BTC","tb1qep77zcg9gaxxeend0cfmz7e7jzsh52x57y56z7rva36tg04mgj0q40yx6w","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun",str(Conf.Config.random_amount(8))),
            # ("Safe2-3账户BTC转账",["b61190f8b2fcb4754ff8527f083bb3df68bf89285d7c5e428276f5f4572b7abe"],"BTC","BTC","tb1qc5a0dcam4fzqpmn7upvze5arzw7khrd8ngfd8xs489ta7uqs5tyqsm6dns","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun",str(Conf.Config.random_amount(8))),
            # # Goerli网络
            # ("Safe2-2账户Goerli转账",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da"],"GOERLI","GoerliETH","0xD79CF3C3FdAaC5F7114e5Dc67376E86206cc313D","0x2B0EfCF16EC1E4C5eD82dBB4Fce9B4811485e650",str(Conf.Config.random_amount(7))),
            # ("Safe2-3账户Goerli转账",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da"],"GOERLI","GoerliETH","0x81B806cf821c5C298Bef4261602bf636F72Bf620","0x2B0EfCF16EC1E4C5eD82dBB4Fce9B4811485e650",str(Conf.Config.random_amount(7))),
            # MATIC网络
            # ("Safe2-2账户MATIC转账",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da"],"MATIC","MATIC","0x42aD4f9111c14C1beE0c142EF275Ee08AA7B1E5e","0xDBA67bAa3CA1e89a2BDf0fEeE4592595b130888A",str(Conf.Config.random_amount(7))),
            # ("Safe2-2账户MATIC转账",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da"],"MATIC","USDC","0x42aD4f9111c14C1beE0c142EF275Ee08AA7B1E5e","0xDBA67bAa3CA1e89a2BDf0fEeE4592595b130888A",str(Conf.Config.random_amount(5))),
            # ("Safe2-3账户MATIC转账",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da"],"MATIC","MATIC","0x1037477a2e863DA6f242ee06E106E8116857bF6E","0xDBA67bAa3CA1e89a2BDf0fEeE4592595b130888A",str(Conf.Config.random_amount(7))),
            # ("Safe2-3账户MATIC转账",["dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da"],"MATIC","USDC","0x1037477a2e863DA6f242ee06E106E8116857bF6E","0xDBA67bAa3CA1e89a2BDf0fEeE4592595b130888A",str(Conf.Config.random_amount(5))),
            # IRIS
            ("Safe2-2账户IRIS转账",["d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b"],"IRIS","IRIS","iaa1x5m8vh53addgrdtnsxc07tryn46f9d7x4q3p40","iaa18hxtn9lx9swxf4j7ytdmn8yxsvyknh86kdgpvc",str(Conf.Config.random_amount(5))),
            ("Safe2-3账户IRIS转账",["d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b"],"IRIS","IRIS","iaa1rflt7r2qz7sv83dtt3kgek5a05g9dghshkjjdu","iaa18hxtn9lx9swxf4j7ytdmn8yxsvyknh86kdgpvc",str(Conf.Config.random_amount(5))),
            # CLV
            # ("Safe账户IRIS转账",["7967c43bd3f3874ccfa6ff6ceda5faa8c699ad0fe2be33f44c8bb8abcb23a2fd"],"CLV","CLV","5Hdmv7BeAe1XFJXso8oGMidGp186cb4uNTNMywp6fBY7UEsr","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT",str(Conf.Config.random_amount(5))),
        ]
    elif env_type == 1: #生产
        test_data = [
            # # DOGE网络
            # ("Safe2-2账户DOGE转账",["6a7e8dceb20664b93a7a901e23ba05c34b4378a58e8b409cfceac35a3740345f"],"DOGE","DOGE","AF5UUawSaatGJTYZd65RCBp4D6aSXxEvjm","DGnb5SNRnEyAx9xNuHGxbiY4ysHPsxegP9",str(round(random.uniform(2,3), random.randint(3,5)))),
            # ("Safe2-3账户DOGE转账",["f4277914268b68080303d73c44a8adb38673bae19a99df921b4fba050a2ba86c"],"DOGE","DOGE","A6eYDsPe5AhAdRnidjY4mJxxDC2w1tikjG","DGnb5SNRnEyAx9xNuHGxbiY4ysHPsxegP9",str(round(random.uniform(2,3), random.randint(3,5)))),
            # # BSC网络
            # ("Safe2-2账户BNB转账",["100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33"],"BSC","BNB","0x790a34b998Ad6b2Fcfe0a3669E860B29847C5Ef9","0xDBA67bAa3CA1e89a2BDf0fEeE4592595b130888A",str(Conf.Config.random_amount(4))),
            # ("Safe2-2账户USDC转账",["100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33"],"BSC","USDC","0x790a34b998Ad6b2Fcfe0a3669E860B29847C5Ef9","0xDBA67bAa3CA1e89a2BDf0fEeE4592595b130888A",str(Conf.Config.random_amount(4))),
            # # MATIC网络
            ("Safe2-2账户MATIC转账",["100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33"],"MATIC","MATIC","0x266d59b84c1CDc55E8fE11C5e27810de581C8037","0xDBA67bAa3CA1e89a2BDf0fEeE4592595b130888A",str(Conf.Config.random_amount(4))),
            ("Safe2-2账户USDC转账",["100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33"],"MATIC","USDC","0x266d59b84c1CDc55E8fE11C5e27810de581C8037","0xDBA67bAa3CA1e89a2BDf0fEeE4592595b130888A",str(Conf.Config.random_amount(5))),
            # ("Safe2-2账户MATIC转账self",["100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33"],"MATIC","MATIC","0x266d59b84c1CDc55E8fE11C5e27810de581C8037","0x266d59b84c1CDc55E8fE11C5e27810de581C8037",str(Conf.Config.random_amount(4))),
            # ("Safe2-2账户USDC转账self",["100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33"],"MATIC","USDC","0x266d59b84c1CDc55E8fE11C5e27810de581C8037","0x266d59b84c1CDc55E8fE11C5e27810de581C8037",str(Conf.Config.random_amount(5))),
            # ("Safe2-3账户MATIC转账",["100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33"],"MATIC","MATIC","0x758F970611dccE463e6CC6Bd5C3F5c1E582faF89","0x5981B8b531ee7f8ECf1b72138031Ca2D4cDB6E8E",str(Conf.Config.random_amount(4))),
            # ("Safe2-3账户USDC转账",["100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33"],"MATIC","USDC","0x758F970611dccE463e6CC6Bd5C3F5c1E582faF89","0x5981B8b531ee7f8ECf1b72138031Ca2D4cDB6E8E",str(Conf.Config.random_amount(5))),
            # # IRIS网络
            # ("Safe2-2账户IRIS转账",["a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c"],"IRIS","IRIS","iaa1mmdw5mw2nw9wvqrzjzarkt46pkfn2n5hwpwz0w","iaa18hxtn9lx9swxf4j7ytdmn8yxsvyknh86kdgpvc",str(Conf.Config.random_amount(4))),
            # ("Safe2-3账户IRIS转账",["a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c"],"IRIS","IRIS","iaa1n367xt7536vhcxrnjx60na77afw2dzecxlmnah","iaa18hxtn9lx9swxf4j7ytdmn8yxsvyknh86kdgpvc",str(Conf.Config.random_amount(4))),
            # # CLV网络
            # ("Safe2-2账户CLV转账",["426a6690c29c5ee0052712c1fda0cc38691f3faf2a571f4b04c9705bbf3f921b"],"CLV","CLV","5Eud43L2RufGoFQpsJjeGYPiyKdYd5JMNWy81RjzeBknXHgG","5FXjWgPEDvrc5A3SDVHayVGfdAp9QquU5jANaZMfLzVue5k6",str(Conf.Config.random_amount(5))),
            # ("Safe2-3账户CLV转账",["426a6690c29c5ee0052712c1fda0cc38691f3faf2a571f4b04c9705bbf3f921b"],"CLV","CLV","5Dv3e5CrUXHifRMfjDyMPtEKs8NQssEPmaoxK1EdpPpDbrjm","5FXjWgPEDvrc5A3SDVHayVGfdAp9QquU5jANaZMfLzVue5k6",str(Conf.Config.random_amount(5))),
        ]


    @allure.story("Safe_Transfers_Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_safe(self,test_title,privatekey,networkCode,symbol,from_add,to_add,amount):

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

        with allure.step("签名交易——sign"):
            sign = Http.HttpUtils.sign(id,signatures,serialized)
            assert sign.status_code == 200
            assert sign.json()["status"] == "PENDING"

        # with allure.step("查询From账户holders信息——holders"):
        #     holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
        #     assert holders.status_code == 200

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')