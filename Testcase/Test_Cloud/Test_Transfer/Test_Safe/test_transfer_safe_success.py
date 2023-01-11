from decimal import Decimal
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
from Common import Http, Httpexplore, Conf
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))

# safe
@allure.feature("Transfers Success!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # BTC
            ("BTC safe账户转账","BTC","BTC","b61190f8b2fcb4754ff8527f083bb3df68bf89285d7c5e428276f5f4572b7abe","tb1qxrunvz3ywjtpzaasfgjjek96a33sxks740v58x7lzke0kc9urvgs0cczgd","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq","0.0000001"),

            # GOERLI
            ("GOERLI safe账户转账 nativecoin","GOERLI","GoerliETH","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0x9D055026eB8D83eF561D5D8084F2DD02e7AD2C17","0xa7a9e710f9a3b4184d4f8b7d379cec262f2382c2","0.00012"),
            ("GOERLI safe账户转账 erc20coin","GOERLI","USDCC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0x9D055026eB8D83eF561D5D8084F2DD02e7AD2C17","0xa7a9e710f9a3b4184d4f8b7d379cec262f2382c2","0.00123"),

            # GOERLI 激活+转账
            ("GOERLI safe账户转账 nativecoin","GOERLI","GoerliETH","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xacd5c6a98407469856b47d333309ed814fc64ebe","0xa7a9e710f9a3b4184d4f8b7d379cec262f2382c2","0.00023"),
            ("GOERLI safe账户转账 erc20coin","GOERLI","USDCC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xacd5c6a98407469856b47d333309ed814fc64ebe","0xa7a9e710f9a3b4184d4f8b7d379cec262f2382c2","0.000123"),

            # MATIC
            ("MATIC safe账户转账 nativecoin","MATIC","MATIC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0x585eab16d5494f01bae462d4719d12214a443eec","0x3d7f18ad2cea9b59e54dfaf09b327c1ccd899591","0.000012"),
            ("MATIC safe账户转账 erc20coin","MATIC","USDC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0x585eab16d5494f01bae462d4719d12214a443eec","0x3d7f18ad2cea9b59e54dfaf09b327c1ccd899591","0.00123"),

            #IRIS
            ("IRIS safe账户转账","IRIS","IRIS","d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b","iaa1laewhl28xx9fujqawfnmt4wls2dgyvs6qz7vle","iaa15h0lvaa6slvj0hg4d64548j2c5fds2zv8tkvgs","0.000101"),
        ]
    elif env_type == 1: #生产
        test_data = [
            # BTC

            # DOGE
            # ("DOGE safe账户转账","DOGE","DOGE","6a7e8dceb20664b93a7a901e23ba05c34b4378a58e8b409cfceac35a3740345f","AEhsyQZDp5yTRyb9SRg1eto1xVyhP4g4ij","D9HfYYym4Ca49VE9FTTvmucCcyHTPspA3j","0.1002"),

            # ETH

            # BSC 太贵了暂时不开
            # ("BSC safe账户转账nativecoin","BSC","BNB","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x49624761fca25f4782f88dc67aac8e8a48f54411","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.0000014"),
            # ("BSC safe账户转账erc20coin","BSC","USDC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x49624761fca25f4782f88dc67aac8e8a48f54411","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.00000141"),

            # MATIC
            # ("MATIC safe账户转账nativecoin","MATIC","MATIC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x66c1d34c273cc09df9072f49aeba4b09e017bc5c","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.0000015"),
            # ("MATIC safe账户转账erc20coin","MATIC","USDC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x66c1d34c273cc09df9072f49aeba4b09e017bc5c","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.000151"),

            # ATOM
            # ("ATOM safe账户转账","ATOM","ATOM","4b49226b1669a687fb4f8479fa9048f1cbb79af74529a47bae7a0c07ce97f8c6","cosmos1gkcgpprzv4wkjteteynjr6l7hpq2xkxuuz0ulm","cosmos1tzk5mhnala4ncj6w8dlw9lwpqmrhee92lyjx06","0.0000106"),

            # IRIS
            # ("IRIS safe账户转账","IRIS","IRIS","a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c","iaa1mzan97ku09tyv3wcu5lktfwzrqfskal4eezv4j","iaa15h0lvaa6slvj0hg4d64548j2c5fds2zv8tkvgs","0.000107"),

            # DOT

            # CLV --"CLV does not support safe accounts"
        ]

    @allure.story("Safe Transfers Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,privatekey,from_add,to_add,amount', test_data)
    def test_custodial(self,test_title,networkCode,symbol,privatekey,from_add,to_add,amount):

        with allure.step("浏览器查询from账户balance信息"):
            balance = Httpexplore.Balances_explore.query(networkCode,from_add,symbol)
                
        with allure.step("查询from账户holder信息"):
            holder = Http.HttpUtils.holders(networkCode=networkCode,symbol=symbol,address=from_add)
            assert holder.status_code ==200
            quantity = Decimal(holder.json()["list"][0]["quantity"])

        logger.debug("浏览器查询账户balance为:" + str(balance))
        logger.debug("查询账户holder为:" + str(quantity))

        with allure.step("账户余额相等验证 浏览器查询==holder"):
            assert balance == quantity

        with allure.step("构建交易——instructions"):
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
            transfer = Http.HttpUtils.instructions(body)
            assert transfer.status_code == 200
            # assert transfer.json()["_embedded"]["transactions"][0]["statusDesc"] == "SIGNING"

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
            sign  =Http.HttpUtils.sign(id,signatures)
            assert sign.status_code == 200

        with allure.step("广播交易"):
            send = Http.HttpUtils.send(id)
            assert send.status_code == 200
            assert send.json()["statusDesc"] == "PENDING"

            hash = send.json()["hash"]

        
        # logger.error("\n\n"+networkCode+"--"+symbol+"--"+test_title+"\n"+from_add+"--"+quantity+"\n"+hash+"\n\n")

        with allure.step("通过id查询交易记录"):
            sleep(30)
            for n in range(10):
                transaction = Http.HttpUtils.transactions_byid(id)
                assert transaction.status_code == 200
                statusDesc = transaction.json()["statusDesc"]
                if statusDesc == "SETTLED" and len(transaction.json()["balanceChanges"]) > 0:
                    break
                else:
                    sleep(30)
            sleep(5)

        with allure.step("浏览器查询from账户balance信息"):
            balance = Httpexplore.Balances_explore.query(networkCode,from_add,symbol)
                
        with allure.step("查询from账户holder信息"):
            holder = Http.HttpUtils.holders(networkCode=networkCode,symbol=symbol,address=from_add)
            assert holder.status_code ==200
            quantity = Decimal(holder.json()["list"][0]["quantity"])

        logger.debug("浏览器查询账户balance为:" + str(balance))
        logger.debug("查询账户holder为:" + str(quantity))

        with allure.step("账户余额相等验证 浏览器查询==holder"):
            assert balance == quantity

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')