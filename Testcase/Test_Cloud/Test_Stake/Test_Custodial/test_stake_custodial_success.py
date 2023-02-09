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

# custodial
@allure.feature("Stake!")
class Test_stake_success:
    if env_type == 0: #测试
        test_data = [
            # IRIS
            ("IRIS Custodial账户质押","IRIS","IRIS","stake","iaa1q2eql0hjd345tfxnzat6s7jfpwg3jansv8krwe",str(Conf.Config.random_amount(4))),
            ("IRIS Custodial账户赎回","IRIS","IRIS","un_stake","iaa1q2eql0hjd345tfxnzat6s7jfpwg3jansv8krwe",str(Conf.Config.random_amount(5))),
            ("IRIS Custodial账户claim","IRIS","IRIS","claim","iaa1q2eql0hjd345tfxnzat6s7jfpwg3jansv8krwe",0),

            # CLV
            ("CLV Custodial账户质押","CLV","CLV","stake","5CFStFse5QY5dyfeHeTDSnMeBBRgxXse2D8k1TUbM67HeA9h",str(Conf.Config.random_amount(4))),
            ("CLV Custodial账户赎回","CLV","CLV","un_stake","5CFStFse5QY5dyfeHeTDSnMeBBRgxXse2D8k1TUbM67HeA9h",str(Conf.Config.random_amount(5))),
            ("CLV Custodial账户claim","CLV","CLV","claim","5CFStFse5QY5dyfeHeTDSnMeBBRgxXse2D8k1TUbM67HeA9h",0),
        ]
    if env_type == 1: #生产
        test_data = [
            # ATOM
            ("ATOM Custodial账户质押","ATOM","ATOM","stake","cosmos1wde9r4gu5qtx3qelnfr2y5w7q7esj7pefx3urc",str(Conf.Config.random_amount(4))),
            ("ATOM Custodial账户赎回","ATOM","ATOM","un_stake","cosmos1wde9r4gu5qtx3qelnfr2y5w7q7esj7pefx3urc",str(Conf.Config.random_amount(5))),
            ("ATOM Custodial账户claim","ATOM","ATOM","claim","cosmos1wde9r4gu5qtx3qelnfr2y5w7q7esj7pefx3urc",0),

            # IRIS
            ("IRIS Custodial账户质押","IRIS","IRIS","stake","iaa1j9vswglv54xlmrza98ww44jgnm0j0hncw2t7v9",str(Conf.Config.random_amount(4))),
            ("IRIS Custodial账户赎回","IRIS","IRIS","un_stake","iaa1j9vswglv54xlmrza98ww44jgnm0j0hncw2t7v9",str(Conf.Config.random_amount(5))),
            ("IRIS Custodial账户claim","IRIS","IRIS","claim","iaa1j9vswglv54xlmrza98ww44jgnm0j0hncw2t7v9",0),

            # DOT

            # CLV
            ("CLV Custodial账户质押","CLV","CLV","stake","5DNA4hJL6YLKFwajJpPsvYW3ne9SRYcCminoYVMhKiThmBmc",str(Conf.Config.random_amount(4))),
            ("CLV Custodial账户赎回","CLV","CLV","un_stake","5DNA4hJL6YLKFwajJpPsvYW3ne9SRYcCminoYVMhKiThmBmc",str(Conf.Config.random_amount(5))),
            ("CLV Custodial账户claim","CLV","CLV","claim","5DNA4hJL6YLKFwajJpPsvYW3ne9SRYcCminoYVMhKiThmBmc",0),
        ]

    @allure.story("Custodial Stake Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,type,address,amount', test_data)
    def test_custodial(self,test_title,networkCode,symbol,type,address,amount):

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
            assert stake.json()["_embedded"]["transactions"][0]["statusDesc"] == "SIGNED"

            id = stake.json()["_embedded"]["transactions"][0]["id"]

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