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
            # MATIC 
            # ("MATIC extarnal账户转账 nativecoin","MATIC","MATIC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xe525E7cd17f6Dc950492755A089E452fd5d9d44f","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.000121"),
            # ("MATIC extarnal账户转账 erc20coin","MATIC","USDC","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0xe525E7cd17f6Dc950492755A089E452fd5d9d44f","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","maximum"),
        ]
    elif env_type == 1: #生产
        test_data = [
            # ETH

            # BSC
            # 地址钱不够，暂时别开
            # ("BSC extarnal账户转账nativecoin 超出maxfee","BSC","BNB","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x9b532cf5f662e51ba643672797ad3ec1a60bb939","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.000001",400,2101000),
            # ("BSC extarnal账户转账erc20coin 超出maxfee","BSC","USDC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x9b532cf5f662e51ba643672797ad3ec1a60bb939","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.000001",400,2101000),

            # MATIC
            ("MATIC extarnal账户转账nativecoin 超出maxfee","MATIC","MATIC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x9b532cf5f662e51ba643672797ad3ec1a60bb939","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.000001",400,2101000),
            ("MATIC extarnal账户转账erc20coin 超出maxfee","MATIC","USDC","100e876b446ee8a356cf2fa8082e12d8b5ff6792aa8fac7a01b534163cbefc33","0x9b532cf5f662e51ba643672797ad3ec1a60bb939","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.000001",400,2101000),
        ]

    @allure.story("Custodial Transfers Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,privatekey,from_add,to_add,amount,status_code_check,code_check', test_data)
    def test_custodial(self,test_title,networkCode,symbol,privatekey,from_add,to_add,amount,status_code_check,code_check):

        with allure.step("浏览器查询from账户balance信息"):
            if networkCode == "BTC":
                pass
            elif networkCode == "DOGE":
                response = Httpexplore.DOGE.balance(from_add)
                assert response.status_code == 200
                balance = Decimal(str(response.json()))
            elif networkCode == "ETH":
                pass
            elif networkCode == "BSC":
                if symbol == "BNB":
                    response = Httpexplore.BSC.balance(from_add)
                    assert response.status_code == 200
                    balance = Decimal(response.json()["result"])/Decimal(10**18)
                else:
                    response = Httpexplore.BSC.balance_erc20(from_add,"0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d")
                    assert response.status_code == 200
                    balance = Decimal(response.json()["result"])/Decimal(10**18)
            elif networkCode == "MATIC":
                if symbol == "MATIC":
                    response = Httpexplore.MATIC.balance(from_add)
                    assert response.status_code == 200
                    balance = Decimal(response.json()["result"])/Decimal(10**18)
                else:
                    response = Httpexplore.MATIC.balance_erc20(from_add,"0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174")
                    assert response.status_code == 200
                    balance = Decimal(response.json()["result"])/Decimal(10**6)
            elif networkCode == "IRIS":
                response = Httpexplore.IRIS.balance(from_add)
                assert response.status_code == 200
                balance_detail = [b for b in response.json()["balances"] if b.get("denom") == "uiris"][0]
                balance = Decimal(balance_detail["amount"])/Decimal(10**6)
            elif networkCode == "CLV":
                response = Httpexplore.CLV.balance(from_add)
                assert response.status_code == 200
                balance_detail = [b for b in response.json()["data"]["native"] if b.get("symbol") == "CLV"][0]
                balance = (Decimal(balance_detail["balance"]) - Decimal(balance_detail["lock"]) - Decimal(balance_detail["reserved"]))/Decimal(10**18)
                
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
            id = transfer.json()["_embedded"]["transactions"][0]["id"]

        with allure.step("rebuild交易"):
            if networkCode == "BSC":
                params = {
                    "gasPrice":"0x6edf2a079f"
                }
            else:
                params = {
                    "maxFeePerGas":"0x19fc4dda1b2c",
                    "maxPriorityFeePerGas":"0x19fc4dd9cd0c"
                }
            rebuild = Http.HttpUtils.rebuild(id,params)
            assert rebuild.status_code == 200
            assert rebuild.json()["statusDesc"] == "BUILDING"

            id = rebuild.json()["id"]
            requiredSignings = rebuild.json()["requiredSignings"]
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
            assert send.status_code == status_code_check
            assert send.json()["code"] == code_check


if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')