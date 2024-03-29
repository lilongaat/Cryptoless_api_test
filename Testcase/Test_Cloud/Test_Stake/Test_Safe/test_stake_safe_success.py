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
from Common import Http, Httpexplore ,Conf
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))

# External
@allure.feature("Stake!")
class Test_stake_success:
    if env_type == 0: #测试
        test_data = [
            # IRIS
            ("IRIS safe2-2账户质押","IRIS","IRIS","stake","d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b","iaa1laewhl28xx9fujqawfnmt4wls2dgyvs6qz7vle",str(Conf.Config.random_amount(4))),
            ("IRIS safe2-2账户赎回","IRIS","IRIS","un_stake","d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b","iaa1laewhl28xx9fujqawfnmt4wls2dgyvs6qz7vle",str(Conf.Config.random_amount(5))),
            ("IRIS safe2-2账户claim","IRIS","IRIS","claim","d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b","iaa1laewhl28xx9fujqawfnmt4wls2dgyvs6qz7vle",0),
            ("IRIS safe2-3账户质押","IRIS","IRIS","stake","d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b","iaa10n27w23n42p58alv960cwfdzgxdg5y3d6f8j2u",str(Conf.Config.random_amount(4))),
            ("IRIS safe2-3账户赎回","IRIS","IRIS","un_stake","d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b","iaa10n27w23n42p58alv960cwfdzgxdg5y3d6f8j2u",str(Conf.Config.random_amount(5))),
            ("IRIS safe2-3账户claim","IRIS","IRIS","claim","d10003ebe2876bd53bf2bb2200eb873a089520a3395b63a4f04330c00e9a885b","iaa10n27w23n42p58alv960cwfdzgxdg5y3d6f8j2u",0),

            # CLV
        ]
    if env_type == 1: #生产
        test_data = [
            # ATOM
            ("ATOM safe2-2账户质押","ATOM","ATOM","stake","4b49226b1669a687fb4f8479fa9048f1cbb79af74529a47bae7a0c07ce97f8c6","cosmos1gkcgpprzv4wkjteteynjr6l7hpq2xkxuuz0ulm",str(Conf.Config.random_amount(4))),
            ("ATOM safe2-2账户赎回","ATOM","ATOM","un_stake","4b49226b1669a687fb4f8479fa9048f1cbb79af74529a47bae7a0c07ce97f8c6","cosmos1gkcgpprzv4wkjteteynjr6l7hpq2xkxuuz0ulm",str(Conf.Config.random_amount(5))),
            ("ATOM safe2-2户claim","ATOM","ATOM","claim","4b49226b1669a687fb4f8479fa9048f1cbb79af74529a47bae7a0c07ce97f8c6","cosmos1gkcgpprzv4wkjteteynjr6l7hpq2xkxuuz0ulm",0),
            ("ATOM safe2-3账户质押","ATOM","ATOM","stake","4b49226b1669a687fb4f8479fa9048f1cbb79af74529a47bae7a0c07ce97f8c6","cosmos1xqf7n4sev34f2vfus036s2h6mealaxln90leph",str(Conf.Config.random_amount(4))),
            ("ATOM safe2-3账户赎回","ATOM","ATOM","un_stake","4b49226b1669a687fb4f8479fa9048f1cbb79af74529a47bae7a0c07ce97f8c6","cosmos1xqf7n4sev34f2vfus036s2h6mealaxln90leph",str(Conf.Config.random_amount(5))),
            ("ATOM safe2-3户claim","ATOM","ATOM","claim","4b49226b1669a687fb4f8479fa9048f1cbb79af74529a47bae7a0c07ce97f8c6","cosmos1xqf7n4sev34f2vfus036s2h6mealaxln90leph",0),

            # IRIS
            ("IRIS safe2-2账户质押","IRIS","IRIS","stake","a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c","iaa1mzan97ku09tyv3wcu5lktfwzrqfskal4eezv4j",str(Conf.Config.random_amount(4))),
            ("IRIS safe2-2账户赎回","IRIS","IRIS","un_stake","a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c","iaa1mzan97ku09tyv3wcu5lktfwzrqfskal4eezv4j",str(Conf.Config.random_amount(5))),
            ("IRIS safe2-2账户claim","IRIS","IRIS","claim","a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c","iaa1mzan97ku09tyv3wcu5lktfwzrqfskal4eezv4j",0),
            ("IRIS safe2-3账户质押","IRIS","IRIS","stake","a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c","iaa1c2q0j82mf9nqupz9re0cymrusls3xykhmyrs69",str(Conf.Config.random_amount(4))),
            ("IRIS safe2-3账户赎回","IRIS","IRIS","un_stake","a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c","iaa1c2q0j82mf9nqupz9re0cymrusls3xykhmyrs69",str(Conf.Config.random_amount(5))),
            ("IRIS safe2-3账户claim","IRIS","IRIS","claim","a8cb5ffed23dda8a84d2612b5b7f17a7739b208640a3cc04b1b28cd4239fcd0c","iaa1c2q0j82mf9nqupz9re0cymrusls3xykhmyrs69",0),

            # DOT

            # CLV
        ]

    @allure.story("Safe_Stake_Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,type,privatekey,address,amount', test_data)
    def test_External(self,test_title,networkCode,symbol,type,privatekey,address,amount):

        with allure.step("浏览器查询from账户balance信息"):
            balance = Httpexplore.Balances_explore.query(networkCode,address,symbol)

        with allure.step("查询from账户holder信息"):
            holder = Http.HttpUtils.holders(networkCode=networkCode,symbol=symbol,address=address)
            assert holder.status_code ==200
            quantity = Decimal(holder.json()["list"][0]["quantity"])

        logger.debug("浏览器查询账户balance为:" + str(balance))
        logger.debug("查询账户holder为:" + str(quantity))

        with allure.step("账户余额相等验证 浏览器查询==holder"):
            assert balance == quantity
            del balance,quantity

        with allure.step("查询账户staking信息"):
            staking = Http.HttpUtils.staking(networkCode,address)
            assert staking.status_code == 200

        with allure.step("构建交易——instructions"):
            if type == "claim":
                body = {
                    "networkCode": networkCode,
                    "type": type,
                    "body": {
                        "delegator":address,
                        "coinSymbol":symbol
                    },
                    "transactionParams":{
                        "memo":''.join(random.sample(string.ascii_letters + string.digits, 10))
                    }
                }
            else:
                body = {
                    "networkCode": networkCode,
                    "type": type,
                    "body": {
                        "delegator":address,
                        "coinSymbol":symbol,
                        "amount":amount
                    },
                    "transactionParams":{
                        "memo":''.join(random.sample(string.ascii_letters + string.digits, 10))
                    }
                }

            stake = Http.HttpUtils.instructions(body)

            assert stake.status_code == 200
            assert stake.json()["_embedded"]["transactions"][0]["statusDesc"] == "SIGNING"

            id = stake.json()["_embedded"]["transactions"][0]["id"]
            requiredSignings = stake.json()["_embedded"]["transactions"][0]["requiredSignings"]
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
            balance = Httpexplore.Balances_explore.query(networkCode,address,symbol)
                
        with allure.step("查询from账户holder信息"):
            holder = Http.HttpUtils.holders(networkCode=networkCode,symbol=symbol,address=address)
            assert holder.status_code ==200
            quantity = Decimal(holder.json()["list"][0]["quantity"])

        logger.debug("浏览器查询账户balance为:" + str(balance))
        logger.debug("查询账户holder为:" + str(quantity))

        with allure.step("账户余额相等验证 浏览器查询==holder"):
            assert balance == quantity
            del balance,quantity

        with allure.step("查询账户staking信息"):
            staking = Http.HttpUtils.staking(networkCode,address)
            assert staking.status_code == 200

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')