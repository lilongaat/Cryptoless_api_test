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

# extarnal
@allure.feature("Transfers Success!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # BTC
            ("BTC extarnal账户转账","BTC","BTC","b61190f8b2fcb4754ff8527f083bb3df68bf89285d7c5e428276f5f4572b7abe","tb1qhcuul2fcyv5rvr5mc5cy5saz0q5p3kx0gsy3c0","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq","0.000008"),

            # GOERLI 
            ("GOERLI extarnal账户转账 nativecoin","GOERLI","GoerliETH","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xe525E7cd17f6Dc950492755A089E452fd5d9d44f","0xa7A9E710f9A3B4184D4F8B7d379CEC262f2382c2","0.000121"),
            # ("GOERLI extarnal账户转账 erc20coin","GOERLI","USDCC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xe525E7cd17f6Dc950492755A089E452fd5d9d44f","0xa7A9E710f9A3B4184D4F8B7d379CEC262f2382c2","0.000123"),

            # MATIC 
            ("MATIC extarnal账户转账 nativecoin","MATIC","MATIC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xe525E7cd17f6Dc950492755A089E452fd5d9d44f","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.000121"),
            ("MATIC extarnal账户转账 erc20coin","MATIC","USDC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xe525E7cd17f6Dc950492755A089E452fd5d9d44f","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","maximum"),

            #IRIS
            ("IRIS extarnal账户转账","IRIS","IRIS","2b60bd0bc95c6ac9a9afa76fbe732fa4eb455a8de328d1df2250a6d10bc33c2a","iaa15h0lvaa6slvj0hg4d64548j2c5fds2zv8tkvgs","iaa18y4kun6wupgly9kja8awhnqpjhxt6hlj348923","0.0005"),

            #CLV
            ("CLV extarnal账户转账","CLV","CLV","7967c43bd3f3874ccfa6ff6ceda5faa8c699ad0fe2be33f44c8bb8abcb23a2fd","5Hdmv7BeAe1XFJXso8oGMidGp186cb4uNTNMywp6fBY7UEsr","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","0.0004"),
        ]
    elif env_type == 1: #生产
        test_data = [
            # BTC

            # DOGE
            ("DOGE extarnal账户转账","DOGE","DOGE","6a7e8dceb20664b93a7a901e23ba05c34b4378a58e8b409cfceac35a3740345f","DK2mfHibfaudY7EviQ1KESpLjyiQXHLbAA","D9HfYYym4Ca49VE9FTTvmucCcyHTPspA3j","0.12"),

            # ETH

            # BSC
            # ("BSC extarnal账户转账nativecoin","BSC","BNB","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x9b532cf5f662e51ba643672797ad3ec1a60bb939","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.0000014"),
            # ("BSC extarnal账户转账erc20coin","BSC","USDC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x9b532cf5f662e51ba643672797ad3ec1a60bb939","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.00000141"),

            # MATIC
            # ("MATIC extarnal账户转账nativecoin","MATIC","MATIC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x9b532cf5f662e51ba643672797ad3ec1a60bb939","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.0000015"),
            # ("MATIC extarnal账户转账erc20coin","MATIC","USDC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x9b532cf5f662e51ba643672797ad3ec1a60bb939","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.00000151"),

            # ATOM
            # ("ATOM extarnal账户转账","ATOM","ATOM","4b49226b1669a687fb4f8479fa9048f1cbb79af74529a47bae7a0c07ce97f8c6","cosmos1uxezv8wcd44hp340acnmrqhcnzau4wzhlshcag","cosmos1tzk5mhnala4ncj6w8dlw9lwpqmrhee92lyjx06","0.0000016"),
            # ("ATOM extarnal账户转账","ATOM","ATOM","844edf6d8a3d415d6dcba4e5c35cd465f37b98b5055eaf24be722a9db14935ca","cosmos1l3wqrt20ugmv3nc5xm0jg3pusm92naa54trk68","cosmos1gkcgpprzv4wkjteteynjr6l7hpq2xkxuuz0ulm","0.101"),

            # IRIS
            # ("IRIS extarnal账户转账","IRIS","IRIS","a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c","iaa18j8rds5hqwp88s4qsrytq5w4eafu288cfza9th","iaa15h0lvaa6slvj0hg4d64548j2c5fds2zv8tkvgs","0.00017"),

            # DOT

            # CLV
            # ("CLV extarnal账户转账","CLV","CLV","426a6690c29c5ee0052712c1fda0cc38691f3faf2a571f4b04c9705bbf3f921b","5GF2XqzK1ERH6AGkyHz1jmMLMCVGBUEyRBxJb5TFWxhiS6EY","5CAG6GuiuzFFbXR2fHhkqvuMRL7yVaj75tJpgKChA4EJELvH","0.000019"),

            # 母账户
            # ("CLV extarnal账户转账","CLV","CLV","47b81eca9356ddc7e9bcd80eb9927357510b696e72413198754b613648c3fe58","5CAG6GuiuzFFbXR2fHhkqvuMRL7yVaj75tJpgKChA4EJELvH","5DNA4hJL6YLKFwajJpPsvYW3ne9SRYcCminoYVMhKiThmBmc","0.1"),
        ]

    @allure.story("External Transfers Success!")
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
            sign  =Http.HttpUtils.sign(id,signatures)
            assert sign.status_code == 200

        with allure.step("广播交易"):
            send = Http.HttpUtils.send(id)
            assert send.status_code == 200
            assert send.json()["statusDesc"] == "PENDING"

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