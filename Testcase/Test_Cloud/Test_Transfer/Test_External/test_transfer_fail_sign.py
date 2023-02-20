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
@allure.feature("Transfers!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # BTC
            ("BTC extarnal账户转账","BTC","BTC","f802c565a6a32e55a511fde45e8b36dba4dc38eb4280a8906ec5e582141711b7","tb1qhcuul2fcyv5rvr5mc5cy5saz0q5p3kx0gsy3c0","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq","0.000008",400,2100000),

            # GOERLI 
            ("GOERLI extarnal账户转账 nativecoin","GOERLI","GoerliETH","f802c565a6a32e55a511fde45e8b36dba4dc38eb4280a8906ec5e582141711b7","0xe525E7cd17f6Dc950492755A089E452fd5d9d44f","0xa7A9E710f9A3B4184D4F8B7d379CEC262f2382c2","0.000121",400,2100000),
            ("GOERLI extarnal账户转账 erc20coin","GOERLI","USDCC","f802c565a6a32e55a511fde45e8b36dba4dc38eb4280a8906ec5e582141711b7","0xe525E7cd17f6Dc950492755A089E452fd5d9d44f","0xa7A9E710f9A3B4184D4F8B7d379CEC262f2382c2","0.000123",400,2100000),

            #IRIS
            ("IRIS extarnal账户转账","IRIS","IRIS","f802c565a6a32e55a511fde45e8b36dba4dc38eb4280a8906ec5e582141711b7","iaa15h0lvaa6slvj0hg4d64548j2c5fds2zv8tkvgs","iaa18y4kun6wupgly9kja8awhnqpjhxt6hlj348923","0.0005",400,2100000),

            #CLV
            ("CLV extarnal账户转账","CLV","CLV","f802c565a6a32e55a511fde45e8b36dba4dc38eb4280a8906ec5e582141711b7","5Hdmv7BeAe1XFJXso8oGMidGp186cb4uNTNMywp6fBY7UEsr","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","0.0004",400,2100000),
        ]
    elif env_type == 1: #生产
        test_data = [
            # BTC

            # DOGE
            ("DOGE extarnal账户转账","DOGE","DOGE","3fd8cd13dcf592b21f3c1c63b557b10ad8ebd3de9e9014927d97315879ce4783","DK2mfHibfaudY7EviQ1KESpLjyiQXHLbAA","D9HfYYym4Ca49VE9FTTvmucCcyHTPspA3j","0.1001",400,2100000),

            # ETH

            # BSC

            # MATIC
            ("MATIC extarnal账户转账nativecoin","MATIC","MATIC","3fd8cd13dcf592b21f3c1c63b557b10ad8ebd3de9e9014927d97315879ce4783","0x9b532cf5f662e51ba643672797ad3ec1a60bb939","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.0000015",400,2100000),
            ("MATIC extarnal账户转账erc20coin","MATIC","USDC","3fd8cd13dcf592b21f3c1c63b557b10ad8ebd3de9e9014927d97315879ce4783","0x9b532cf5f662e51ba643672797ad3ec1a60bb939","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591","0.00001",400,2100000),

            # ATOM
            ("ATOM extarnal账户转账","ATOM","ATOM","3fd8cd13dcf592b21f3c1c63b557b10ad8ebd3de9e9014927d97315879ce4783","cosmos1uxezv8wcd44hp340acnmrqhcnzau4wzhlshcag","cosmos1tzk5mhnala4ncj6w8dlw9lwpqmrhee92lyjx06","0.000001",400,2100000),

            # IRIS
            ("IRIS extarnal账户转账","IRIS","IRIS","3fd8cd13dcf592b21f3c1c63b557b10ad8ebd3de9e9014927d97315879ce4783","iaa18j8rds5hqwp88s4qsrytq5w4eafu288cfza9th","iaa15h0lvaa6slvj0hg4d64548j2c5fds2zv8tkvgs","0.00017",400,2100000),

            # DOT

            # CLV
            ("CLV extarnal账户转账","CLV","CLV","3fd8cd13dcf592b21f3c1c63b557b10ad8ebd3de9e9014927d97315879ce4783","5GF2XqzK1ERH6AGkyHz1jmMLMCVGBUEyRBxJb5TFWxhiS6EY","5CAG6GuiuzFFbXR2fHhkqvuMRL7yVaj75tJpgKChA4EJELvH","0.000019",400,2100000),
        ]

    @allure.story("External Transfers Fail Sign!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,privatekey,from_add,to_add,amount,status_code,code', test_data)
    def test_custodial(self,test_title,networkCode,symbol,privatekey,from_add,to_add,amount,status_code,code):

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
            assert sign.status_code == status_code
            assert sign.json()["code"] == code

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')