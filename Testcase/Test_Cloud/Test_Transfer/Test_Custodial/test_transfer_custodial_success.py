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

# custodial
@allure.feature("Transfers Success!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # BTC
            ("BTC Custodial账户转账","BTC","BTC","tb1q7ymdm79ryug7vttw4jrf87pdcmn67n3p9rgc5x","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","0.000008"),

            # GOERLI
            # ("GOERLI Custodial账户转账 nativecoin","GOERLI","GoerliETH","0xcc7a54ec1d39d1cf7b35f2b3b92031ad5fc7b6ca","0xbdb3bd7b3f3daeadc58d00ef5f15ed9a476b8fe3","0.00012"),
            # ("GOERLI Custodial账户转账 erc20coin","GOERLI","USDCC","0xcc7a54ec1d39d1cf7b35f2b3b92031ad5fc7b6ca","0xbdb3bd7b3f3daeadc58d00ef5f15ed9a476b8fe3","0.123"),

            # MATIC
            # ("MATIC Custodial账户转账 nativecoin","MATIC","MATIC","0x651a23f7bed98b52c7829ad668a4836c48064850","0xbdb3bd7b3f3daeadc58d00ef5f15ed9a476b8fe3","0.00012"),
            # ("MATIC Custodial账户转账 erc20coin","MATIC","USDC","0xcc7a54ec1d39d1cf7b35f2b3b92031ad5fc7b6ca","0xbdb3bd7b3f3daeadc58d00ef5f15ed9a476b8fe3","0.123"),

            #IRIS
            # ("IRIS Custodial账户转账","IRIS","IRIS","iaa1q2eql0hjd345tfxnzat6s7jfpwg3jansv8krwe","iaa15h0lvaa6slvj0hg4d64548j2c5fds2zv8tkvgs","0.000123"),

            #CLV
            # ("CLV Custodial账户转账","CLV","CLV","5G8W1b7pWa7zzcYAWomTaX2zmP1SHE7JDEGvQTdGh45d83te","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","0.000123"),
        ]
    elif env_type == 1: #生产
        test_data = [
            # BTC

            # DOGE
            ("DOGE Custodial账户转账","DOGE","DOGE","D9vakMz4cLhRXjjQyhSxMX7Wg3xmoFMeQ6","D9HfYYym4Ca49VE9FTTvmucCcyHTPspA3j","0.1001"),

            # ETH

            # BSC
            # ("BSC Custodial账户转账 erc20coin","BSC","USDC","0x5f0a7433a68626c018ecae3cb69889184e8db970","0x3d7f18ad2cea9b59e54dfaf09b327c1ccd899591","0.000123"),
            # ("BSC Custodial账户转账 nativecoin","BSC","BNB","0x5f0a7433a68626c018ecae3cb69889184e8db970","0x3d7f18ad2cea9b59e54dfaf09b327c1ccd899591","0.00012"),

            # MATIC
            # ("MATIC Custodial账户转账 erc20coin","MATIC","USDC","0xe458fd3e2515d42cbcd52a89b52fb662bf052143","0x3d7f18ad2cea9b59e54dfaf09b327c1ccd899591","0.000123"),
            # ("MATIC Custodial账户转账 nativecoin","MATIC","MATIC","0xe458fd3e2515d42cbcd52a89b52fb662bf052143","0x3d7f18ad2cea9b59e54dfaf09b327c1ccd899591","0.00012"),

            # ATOM
            # ("ATOM extarnal账户转账","ATOM","ATOM","cosmos1wde9r4gu5qtx3qelnfr2y5w7q7esj7pefx3urc","cosmos1tzk5mhnala4ncj6w8dlw9lwpqmrhee92lyjx06","0.000001"),

            # IRIS
            # ("IRIS extarnal账户转账","IRIS","IRIS","iaa1j9vswglv54xlmrza98ww44jgnm0j0hncw2t7v9","iaa15h0lvaa6slvj0hg4d64548j2c5fds2zv8tkvgs","0.000001"),

            # DOT

            # CLV
            # ("CLV Custodial账户转账","CLV","CLV","5DNA4hJL6YLKFwajJpPsvYW3ne9SRYcCminoYVMhKiThmBmc","5CAG6GuiuzFFbXR2fHhkqvuMRL7yVaj75tJpgKChA4EJELvH","0.00012"),
        ]

    @allure.story("Custodial Transfers Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_custodial(self,test_title,networkCode,symbol,from_add,to_add,amount):

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
            assert transfer.json()["_embedded"]["transactions"][0]["statusDesc"] == "SIGNED"

            id = transfer.json()["_embedded"]["transactions"][0]["id"]

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