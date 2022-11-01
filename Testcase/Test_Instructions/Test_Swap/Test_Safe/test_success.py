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

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxNTczOTM3MDIxNzEzNzc2NjQyIiwiZXhwIjoxNjY0Njk1NjE2LCJpYXQiOjE2NjQwOTA4MTYsInVzZXJJZCI6MTU3MzkzNzAyMTcxMzc3NjY0Mn0.TfkTJsH4rp4FCmciMn1BUVlnev1JPI7glaTUjyVUz8M"
web3token = "eyJib2R5IjoiV2ViMyBUb2tlbiBWZXJzaW9uOiAyXG5Ob25jZTogMTU3MzkzNzAyMTcxMzc3NjY0MlxuSXNzdWVkIEF0OiBTdW4sIDI1IFNlcCAyMDIyIDA3OjI2OjQyIEdNVFxuRXhwaXJhdGlvbiBUaW1lOiBXZWQsIDIyIFNlcCAyMDMyIDA3OjI2OjQyIEdNVCIsInNpZ25hdHVyZSI6IjB4MDdhMzI4M2IxY2JmNWRkOTQwNTFhNWM5NjYxNWM4NTY5ZDQ0ZGEzZTJkODIzZGI4NzE5YjA0YWUwYmRhZWE4NzY4OTZiZGY5ZjEzZTU3YWUxMDRjNTExZDMwODQwMTgxMjE5Zjg1Y2ExZTkwNTIwYzgxMjRlM2I3MjAwNmI1YjUxYiJ9"

# safe
@allure.feature("Transfers_Success!")
class Test_transfers_success:
    test_data = [
        # MATIC网络
        # ("Safe2-2账户MATIC转账",["4d87c72cee9d4b257368f448f4f7406d0ce98947eb30fcaa8194319303534b13"],"MATIC","MATIC","0x584f8BD2E046BFDEb786Ab63482f6740E4d827D1","0x5981B8b531ee7f8ECf1b72138031Ca2D4cDB6E8E",str(Conf.Config.random_amount(4))),
        # ("Safe2-2账户USDC转账",["4d87c72cee9d4b257368f448f4f7406d0ce98947eb30fcaa8194319303534b13"],"MATIC","USDC","0x584f8BD2E046BFDEb786Ab63482f6740E4d827D1","0x5981B8b531ee7f8ECf1b72138031Ca2D4cDB6E8E",str(Conf.Config.random_amount(5))),
        # ("Safe2-2账户MATIC转账self",["4d87c72cee9d4b257368f448f4f7406d0ce98947eb30fcaa8194319303534b13"],"MATIC","MATIC","0x584f8BD2E046BFDEb786Ab63482f6740E4d827D1","0x584f8BD2E046BFDEb786Ab63482f6740E4d827D1",str(Conf.Config.random_amount(4))),
        # ("Safe2-2账户USDC转账self",["4d87c72cee9d4b257368f448f4f7406d0ce98947eb30fcaa8194319303534b13"],"MATIC","USDC","0x584f8BD2E046BFDEb786Ab63482f6740E4d827D1","0x584f8BD2E046BFDEb786Ab63482f6740E4d827D1",str(Conf.Config.random_amount(5))),
        # ("Safe2-3账户MATIC转账",["4d87c72cee9d4b257368f448f4f7406d0ce98947eb30fcaa8194319303534b13"],"MATIC","MATIC","0x276812F8cF009a9D6e69d0FBaF94Edc19D79b9Df","0x5981B8b531ee7f8ECf1b72138031Ca2D4cDB6E8E",str(Conf.Config.random_amount(4))),
        # ("Safe2-3账户USDC转账",["4d87c72cee9d4b257368f448f4f7406d0ce98947eb30fcaa8194319303534b13"],"MATIC","USDC","0x276812F8cF009a9D6e69d0FBaF94Edc19D79b9Df","0x5981B8b531ee7f8ECf1b72138031Ca2D4cDB6E8E",str(Conf.Config.random_amount(5))),
        # IRIS网络
        # ("Safe2-2账户IRIS转账",["050e2d7791425a80046e4a8ec2c5f0d48964453603d7cbbfb5d5cbecb76f0591"],"IRIS","IRIS","iaa1nwg4qcr07un797xk72c5vph4xaay02zdvaejxl","iaa18hxtn9lx9swxf4j7ytdmn8yxsvyknh86kdgpvc",str(Conf.Config.random_amount(4))),
        ("Safe2-2账户IRIS转账",["050e2d7791425a80046e4a8ec2c5f0d48964453603d7cbbfb5d5cbecb76f0591"],"IRIS","IRIS","iaa1nwg4qcr07un797xk72c5vph4xaay02zdvaejxl","iaa1nwg4qcr07un797xk72c5vph4xaay02zdvaejxl",str(Conf.Config.random_amount(4))),
        #BTC网络
        # ("Safe2-2账户BTC转账",["254e6db4f76209b7cb501e36dbb7d050dd1ff95f6c4d4b951d186b35ad7b295d"],"BTC","BTC","tb1qzd9jum9sels7zuezp0t575tkyttdaklgvzu2cdvfgx6agzj3v63qquf4k7","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq",str(Conf.Config.random_amount(6))),
        # ("Safe2-3账户BTC转账",["254e6db4f76209b7cb501e36dbb7d050dd1ff95f6c4d4b951d186b35ad7b295d"],"BTC","BTC","tb1qvnuj9aer9m9a4vm4rjnypdchfyrjrrp22tenzjrx9ajt6fjlzwuqrrkclj","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq",str(Conf.Config.random_amount(7))),
    ]

    @allure.story("Safe_Transfers_Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_safe(self,test_title,privatekey,networkCode,symbol,from_add,to_add,amount):

        with allure.step("查询From账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add,web3token)
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
            transfer = Http.HttpUtils.instructions("transfer",body,networkCode,[],transactionParams,token)

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
            sign = Http.HttpUtils.sign(id,signatures,serialized,token)
            assert sign.status_code == 200
            assert sign.json()["status"] == "PENDING"

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')