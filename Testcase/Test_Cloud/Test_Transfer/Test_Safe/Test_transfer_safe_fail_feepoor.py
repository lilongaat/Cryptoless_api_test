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
@allure.feature("Transfers!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # BTC
            ("BTC safe2-2账户转账余额不足,余额10聪,转账11聪","BTC","BTC","b61190f8b2fcb4754ff8527f083bb3df68bf89285d7c5e428276f5f4572b7abe","tb1ql6s0xl667zffpgp0j67gej4mljshgd78hgkl0azwvg69jrc5zpeqd5u8qx","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq","0.00000011",None,400,2102001),
            ("BTC safe2-3账户转账余额不足,余额10聪,转账11聪","BTC","BTC","b61190f8b2fcb4754ff8527f083bb3df68bf89285d7c5e428276f5f4572b7abe","tb1qhlh6azfgjutcdq3sajwt3u8tjaaqrh03t5aauzjy8mu85q82pevs5wckrj","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq","0.00000011",None,400,2102001),
            ("BTC safe2-2账户转账minfee,余额10聪,转账10聪","BTC","BTC","b61190f8b2fcb4754ff8527f083bb3df68bf89285d7c5e428276f5f4572b7abe","tb1ql6s0xl667zffpgp0j67gej4mljshgd78hgkl0azwvg69jrc5zpeqd5u8qx","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq","0.0000001",None,400,2102004),
            ("BTC safe2-3账户转账minfee,余额10聪,转账10聪","BTC","BTC","b61190f8b2fcb4754ff8527f083bb3df68bf89285d7c5e428276f5f4572b7abe","tb1qhlh6azfgjutcdq3sajwt3u8tjaaqrh03t5aauzjy8mu85q82pevs5wckrj","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq","0.0000001",None,400,2102004),

            # GOERLI
            ("GOERLI safe2-2账户转账 nativecoin 余额不足","GOERLI","GoerliETH","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xf687c6ceca235bdf8a4cf85110d0fc7f4ed19a9a","0xa7a9e710f9a3b4184d4f8b7d379cec262f2382c2","0.000000100000000001",None,400,2102001),
            ("GOERLI safe2-2账户转账 erc20coin 余额不足","GOERLI","USDCC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xf687c6ceca235bdf8a4cf85110d0fc7f4ed19a9a","0xa7a9e710f9a3b4184d4f8b7d379cec262f2382c2","1.000000000000000001",None,400,2102001),
            ("GOERLI safe2-2账户转账 nativecoin 手续费不足","GOERLI","GoerliETH","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xf687c6ceca235bdf8a4cf85110d0fc7f4ed19a9a","0xa7a9e710f9a3b4184d4f8b7d379cec262f2382c2","0.000000099999",None,400,2100000),
            ("GOERLI safe2-3账户转账 nativecoin 余额不足","GOERLI","GoerliETH","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0x38a9e3b35d5401847c7349de58cd4019f00e0d79","0xa7a9e710f9a3b4184d4f8b7d379cec262f2382c2","1",None,400,2102001),
            ("GOERLI safe2-3账户转账 erc20coin 余额不足","GOERLI","USDCC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0x38a9e3b35d5401847c7349de58cd4019f00e0d79","0xa7a9e710f9a3b4184d4f8b7d379cec262f2382c2","1000",None,400,2102001),
            ("GOERLI safe2-3账户激活+转账 nativecoin 手续费不足","GOERLI","GoerliETH","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0x38a9e3b35d5401847c7349de58cd4019f00e0d79","0xa7a9e710f9a3b4184d4f8b7d379cec262f2382c2","0.000000000000000099",None,400,2100000),
            ("GOERLI safe2-3账户激活+转账 erc20coin 手续费不足","GOERLI","GoerliETH","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0x38a9e3b35d5401847c7349de58cd4019f00e0d79","0xa7a9e710f9a3b4184d4f8b7d379cec262f2382c2","0.000000000000000099",None,400,2100000),
            ("GOERLI safe2-2账户转账 nativecoin payer手续费不足","GOERLI","GoerliETH","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xf687c6ceca235bdf8a4cf85110d0fc7f4ed19a9a","0xa7a9e710f9a3b4184d4f8b7d379cec262f2382c2","0.0000001","02f5f2c7ea48d85f4e8719e3af8b8e614625702f5035689ec5ba5d28b5ecb3803a",400,2100000),
            ("GOERLI safe2-2账户转账 erc20coin payer手续费不足","GOERLI","USDCC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xf687c6ceca235bdf8a4cf85110d0fc7f4ed19a9a","0xa7a9e710f9a3b4184d4f8b7d379cec262f2382c2","1","02f5f2c7ea48d85f4e8719e3af8b8e614625702f5035689ec5ba5d28b5ecb3803a",400,2100000),
            ("GOERLI safe2-3账户激活+转账 nativecoin payer手续费不足","GOERLI","GoerliETH","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0x38a9e3b35d5401847c7349de58cd4019f00e0d79","0xa7a9e710f9a3b4184d4f8b7d379cec262f2382c2","0.000000000000000099","02f5f2c7ea48d85f4e8719e3af8b8e614625702f5035689ec5ba5d28b5ecb3803a",400,2100000),
            ("GOERLI safe2-3账户激活+转账 erc20coin payer手续费不足","GOERLI","GoerliETH","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0x38a9e3b35d5401847c7349de58cd4019f00e0d79","0xa7a9e710f9a3b4184d4f8b7d379cec262f2382c2","0.000000000000000099","02f5f2c7ea48d85f4e8719e3af8b8e614625702f5035689ec5ba5d28b5ecb3803a",400,2100000),

            #IRIS
            ("IRIS safe2-2账户转账余额不足","IRIS","IRIS","d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b","iaa1nnx3fup8wzd58yyzdw743htzufspl8x0w6pj20","iaa15h0lvaa6slvj0hg4d64548j2c5fds2zv8tkvgs","0.000002",None,400,2102001),
            ("IRIS safe2-3账户转账余额不足","IRIS","IRIS","d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b","iaa1whqcycfaeukyxj4at58305xg4k0pdh9nym0pln","iaa15h0lvaa6slvj0hg4d64548j2c5fds2zv8tkvgs","0.000002",None,400,2102001),
            ("IRIS safe2-2账户转账fee不足","IRIS","IRIS","d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b","iaa1nnx3fup8wzd58yyzdw743htzufspl8x0w6pj20","iaa15h0lvaa6slvj0hg4d64548j2c5fds2zv8tkvgs","0.000001",None,400,2100000),
            ("IRIS safe2-3账户转账fee不足","IRIS","IRIS","d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b","iaa1whqcycfaeukyxj4at58305xg4k0pdh9nym0pln","iaa15h0lvaa6slvj0hg4d64548j2c5fds2zv8tkvgs","0.000001",None,400,2100000),
        ]
    elif env_type == 1: #生产
        test_data = [
            # BTC

            # DOGE
            # ("DOGE safe2-2账户转账","DOGE","DOGE","6a7e8dceb20664b93a7a901e23ba05c34b4378a58e8b409cfceac35a3740345f","AEhsyQZDp5yTRyb9SRg1eto1xVyhP4g4ij","D9HfYYym4Ca49VE9FTTvmucCcyHTPspA3j","0.1002"),
            # ("DOGE safe2-3账户转账","DOGE","DOGE","f4277914268b68080303d73c44a8adb38673bae19a99df921b4fba050a2ba86c","A19FU4dm95VZQ6JECwvZMaDEFc3QTkLbFC","D9HfYYym4Ca49VE9FTTvmucCcyHTPspA3j","0.1002"),

            # ETH

            # BSC 太贵了暂时不开
            # ("BSC safe2-2账户转账nativecoin","BSC","BNB","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x49624761fca25f4782f88dc67aac8e8a48f54411","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.0000014"),
            # ("BSC safe2-2账户转账erc20coin","BSC","USDC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x49624761fca25f4782f88dc67aac8e8a48f54411","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.00000141"),

            # MATIC
            # ("MATIC safe2-2账户转账nativecoin","MATIC","MATIC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x66c1d34c273cc09df9072f49aeba4b09e017bc5c","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.0000015"),
            # ("MATIC safe2-2账户转账erc20coin","MATIC","USDC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x66c1d34c273cc09df9072f49aeba4b09e017bc5c","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.000151"),
            # ("MATIC safe2-3账户转账nativecoin","MATIC","MATIC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0xa2109b6a714bb32854f4b9db01859b3b7f092088","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.0000015"),
            # ("MATIC safe2-3账户转账erc20coin","MATIC","USDC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0xa2109b6a714bb32854f4b9db01859b3b7f092088","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.000151"),

            # ATOM
            # ("ATOM safe2-2账户转账","ATOM","ATOM","4b49226b1669a687fb4f8479fa9048f1cbb79af74529a47bae7a0c07ce97f8c6","cosmos1gkcgpprzv4wkjteteynjr6l7hpq2xkxuuz0ulm","cosmos1tzk5mhnala4ncj6w8dlw9lwpqmrhee92lyjx06","0.0000106"),
            # ("ATOM safe2-3账户转账","ATOM","ATOM","4b49226b1669a687fb4f8479fa9048f1cbb79af74529a47bae7a0c07ce97f8c6","cosmos1xqf7n4sev34f2vfus036s2h6mealaxln90leph","cosmos1tzk5mhnala4ncj6w8dlw9lwpqmrhee92lyjx06","0.0000126"),

            # IRIS
            # ("IRIS safe2-2账户转账","IRIS","IRIS","a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c","iaa1mzan97ku09tyv3wcu5lktfwzrqfskal4eezv4j","iaa15h0lvaa6slvj0hg4d64548j2c5fds2zv8tkvgs","0.000107"),
            # ("IRIS safe2-3账户转账","IRIS","IRIS","a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c","iaa1c2q0j82mf9nqupz9re0cymrusls3xykhmyrs69","iaa15h0lvaa6slvj0hg4d64548j2c5fds2zv8tkvgs","0.000107"),

            # DOT

            # CLV --"CLV does not support safe accounts"
        ]

    @allure.story("Safe Transfers Fail Feepoor!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,privatekey,from_add,to_add,amount,priv_send,status_code,code', test_data)
    def test_safe(self,test_title,networkCode,symbol,privatekey,from_add,to_add,amount,priv_send,status_code,code):

        with allure.step("浏览器查询from账户balance信息"):
            balance = Httpexplore.Balances_explore.query(networkCode,from_add,symbol)
                
        with allure.step("查询from账户holder信息"):
            holder = Http.HttpUtils.holders(networkCode=networkCode,symbol=symbol,address=from_add)
            assert holder.status_code == 200
            if len(holder.json()["list"]) == 0:
                quantity = 0
            else:
                quantity = Decimal(holder.json()["list"][0]["quantity"])

        logger.debug("浏览器查询账户balance为:" + str(balance))
        logger.debug("查询账户holder为:" + str(quantity))

        with allure.step("账户余额相等验证 浏览器查询==holder"):
            assert balance == quantity
            del balance,quantity

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
            assert transfer.status_code == status_code
            assert transfer.json()["code"] == code
            

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')