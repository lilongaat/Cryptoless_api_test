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

# custodial 异常转账
@allure.feature("Transfers!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # BTC
            ("BTC Custodial账户转账 networkCode空","","BTC","tb1q78qch48dw8fqc4xc8f374y88f93ys4xldqvunt","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq","0.00000001",400,2100000),
            ("BTC Custodial账户转账 networkCode不存在","WBTC","BTC","tb1q78qch48dw8fqc4xc8f374y88f93ys4xldqvunt","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq","0.00000001",404,2200000),
            ("BTC Custodial账户转账 symbol空","BTC","","tb1q78qch48dw8fqc4xc8f374y88f93ys4xldqvunt","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq","0.00000001",400,2300000),
            ("BTC Custodial账户转账 symbol不存在","BTC","WBTC","tb1q78qch48dw8fqc4xc8f374y88f93ys4xldqvunt","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq","0.00000001",400,2200000),
            ("BTC Custodial账户转账 from空","BTC","BTC","","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq","0.00000001",400,2300000),
            ("BTC Custodial账户转账 from不属于该用户","BTC","BTC","bc1qgdjqv0av3q56jvd82tkdjpy7gdp9ut8tlqmgrpmv24sq90ecnvqqjwvw97","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq","0.00000002",404,2200000),
            ("BTC Custodial账户转账 from地址不匹配网络","BTC","BTC","0x18b50a6c8c4c158572a2c9d70ed5e7b76d425aab","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq","0.00000001",404,2200000),
            ("BTC Custodial账户转账 to空","BTC","BTC","tb1q78qch48dw8fqc4xc8f374y88f93ys4xldqvunt","","0.00000001",400,2300000),
            ("BTC Custodial账户转账 to地址不匹配网络","BTC","BTC","tb1q78qch48dw8fqc4xc8f374y88f93ys4xldqvunt","0x18b50a6c8c4c158572a2c9d70ed5e7b76d425aab","0.00000001",400,2400000),
            ("BTC Custodial账户转账 amount空","BTC","BTC","tb1q78qch48dw8fqc4xc8f374y88f93ys4xldqvunt","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq","",400,2300000),
            ("BTC Custodial账户转账 amount超出精度","BTC","BTC","tb1q78qch48dw8fqc4xc8f374y88f93ys4xldqvunt","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq","0.000000001",400,2100000),
            ("BTC Custodial账户转账 amount超出余额","BTC","BTC","tb1q78qch48dw8fqc4xc8f374y88f93ys4xldqvunt","tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq","0.00000002",400,2102001),
            
            # DOGE
            ("DOGE Custodial账户转账 dust","DOGE","DOGE","DS2cpSDvZXHzhZEyBEbTNuQTgonoHkFM4n","D9HfYYym4Ca49VE9FTTvmucCcyHTPspA3j","0.09999999",400,2100000),

            # GOERLI
            ("GOERLI Custodial账户转账 nativecoin 超出精度","GOERLI","GoerliETH","0x18b50a6c8c4c158572a2c9d70ed5e7b76d425aab","0xa7A9E710f9A3B4184D4F8B7d379CEC262f2382c2","0.0000000000000000009",400,2100000),
            ("GOERLI Custodial账户转账 nativecoin 超出余额","GOERLI","GoerliETH","0x18b50a6c8c4c158572a2c9d70ed5e7b76d425aab","0xa7A9E710f9A3B4184D4F8B7d379CEC262f2382c2","0.000000000000000002",400,2102001),
            ("GOERLI Custodial账户转账 erc20 超出精度","GOERLI","USDCC","0x18b50a6c8c4c158572a2c9d70ed5e7b76d425aab","0xa7A9E710f9A3B4184D4F8B7d379CEC262f2382c2","0.0000000000000000009",400,2100000),
            ("GOERLI Custodial账户转账 erc20 超出余额","GOERLI","USDCC","0x18b50a6c8c4c158572a2c9d70ed5e7b76d425aab","0xa7A9E710f9A3B4184D4F8B7d379CEC262f2382c2","0.000001000000000001",400,2102001),

            # IRIS
            ("IRIS Custodial账户转账 amount超出精度","IRIS","IRIS","iaa1q2eql0hjd345tfxnzat6s7jfpwg3jansv8krwe","iaa15h0lvaa6slvj0hg4d64548j2c5fds2zv8tkvgs","0.00000001",400,2100000),
            ("IRIS Custodial账户转账 amount超出余额","IRIS","IRIS","iaa1q2eql0hjd345tfxnzat6s7jfpwg3jansv8krwe","iaa15h0lvaa6slvj0hg4d64548j2c5fds2zv8tkvgs","100",400,2102001),
            ("IRIS Custodial账户转账 手续费不足","IRIS","IRIS","iaa1fryssfhcmp8jnzsqg750w8vgg426gcfdr9gezr","iaa15h0lvaa6slvj0hg4d64548j2c5fds2zv8tkvgs","100",400,2100000),

            # CLV
            ("CLV Custodial账户转账 amount超出精度","CLV","CLV","5G8W1b7pWa7zzcYAWomTaX2zmP1SHE7JDEGvQTdGh45d83te","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","0.0000000000000000009",400,2100000),
            ("CLV Custodial账户转账 amount超出余额","CLV","CLV","5G8W1b7pWa7zzcYAWomTaX2zmP1SHE7JDEGvQTdGh45d83te","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","100",400,2102001),
        ]
    elif env_type == 1: #生产
        test_data = [
            # # BTC
            ("BTC Custodial账户转账 账户没钱","BTC","BTC","bc1qhw7kvldh52n3glud3mf94uundm2pwkznyuqyv3","bc1qhw7kvldh52n3glud3mf94uundm2pwkznyuqyv3","0.0000001",400,2102001),

            # # DOGE
            ("DOGE Custodial账户转账 networkCode空","","DOGE","D9vakMz4cLhRXjjQyhSxMX7Wg3xmoFMeQ6","D9HfYYym4Ca49VE9FTTvmucCcyHTPspA3j","0.00001",400,2100000),
            ("DOGE Custodial账户转账 networkCode不存在","DOGEE","DOGE","D9vakMz4cLhRXjjQyhSxMX7Wg3xmoFMeQ6","D9HfYYym4Ca49VE9FTTvmucCcyHTPspA3j","0.00001",404,2200000),
            ("DOGE Custodial账户转账 symbol空","DOGE","","D9vakMz4cLhRXjjQyhSxMX7Wg3xmoFMeQ6","D9HfYYym4Ca49VE9FTTvmucCcyHTPspA3j","0.00001",400,2300000),
            ("DOGE Custodial账户转账 symbol不存在","DOGE","DOGEE","D9vakMz4cLhRXjjQyhSxMX7Wg3xmoFMeQ6","D9HfYYym4Ca49VE9FTTvmucCcyHTPspA3j","0.00001",400,2200000),
            ("DOGE Custodial账户转账 symbol不在网络下","DOGE","BTC","D9vakMz4cLhRXjjQyhSxMX7Wg3xmoFMeQ6","D9HfYYym4Ca49VE9FTTvmucCcyHTPspA3j","0.00001",400,2200000),
            ("DOGE Custodial账户转账 from空","DOGE","DOGE","","D9HfYYym4Ca49VE9FTTvmucCcyHTPspA3j","0.00001",400,2300000),
            ("DOGE Custodial账户转账 from不属于该用户","DOGE","DOGE","DDogepartyxxxxxxxxxxxxxxxxxxw1dfzr","D9HfYYym4Ca49VE9FTTvmucCcyHTPspA3j","0.000002",404,2200000),
            ("DOGE Custodial账户转账 from地址不匹配网络","DOGE","DOGE","0x18b50a6c8c4c158572a2c9d70ed5e7b76d425aab","D9HfYYym4Ca49VE9FTTvmucCcyHTPspA3j","0.000001",404,2200000),
            ("DOGE Custodial账户转账 to空","DOGE","DOGE","D9vakMz4cLhRXjjQyhSxMX7Wg3xmoFMeQ6","","0.00001",400,2300000),
            ("DOGE Custodial账户转账 to地址不匹配网络","DOGE","DOGE","D9vakMz4cLhRXjjQyhSxMX7Wg3xmoFMeQ6","0x18b50a6c8c4c158572a2c9d70ed5e7b76d425aab","0.00001",400,2400000),
            ("DOGE Custodial账户转账 amount空","DOGE","DOGE","D9vakMz4cLhRXjjQyhSxMX7Wg3xmoFMeQ6","D9HfYYym4Ca49VE9FTTvmucCcyHTPspA3j","",400,2300000),
            ("DOGE Custodial账户转账 amount超出余额","DOGE","DOGE","D9vakMz4cLhRXjjQyhSxMX7Wg3xmoFMeQ6","D9HfYYym4Ca49VE9FTTvmucCcyHTPspA3j","100",400,2102001),
            ("DOGE Custodial账户转账 amount超出精度","DOGE","DOGE","D9vakMz4cLhRXjjQyhSxMX7Wg3xmoFMeQ6","D9HfYYym4Ca49VE9FTTvmucCcyHTPspA3j","0.000000001",400,2100000),
            ("DOGE Custodial账户转账 dust","DOGE","DOGE","D9vakMz4cLhRXjjQyhSxMX7Wg3xmoFMeQ6","D9HfYYym4Ca49VE9FTTvmucCcyHTPspA3j","0.09999999",400,2100000),

            # ETH
            ("ETH Custodial账户转账 账户没钱","ETH","ETH","0x6d1f7e8503d9c88e998fb1236ccd1f6a2dde2a4e","0x6d1f7e8503d9c88e998fb1236ccd1f6a2dde2a4e","0.0000000001",400,2102001),

            # BSC
            ("BSC Custodial账户转账nativecoin 超出余额","BSC","BNB","0x5f0a7433a68626c018ecae3cb69889184e8db970","0x3d7f18ad2cea9b59e54dfaf09b327c1ccd899591","1.21",400,2102001),
            ("BSC Custodial账户转账nativecoin 超出精度","BSC","BNB","0x5f0a7433a68626c018ecae3cb69889184e8db970","0x3d7f18ad2cea9b59e54dfaf09b327c1ccd899591","0.0000000001000000009",400,2100000),
            ("BSC Custodial账户转账erc20coin 超出余额","BSC","USDC","0x5f0a7433a68626c018ecae3cb69889184e8db970","0x3d7f18ad2cea9b59e54dfaf09b327c1ccd899591","64",400,2102001),
            ("BSC Custodial账户转账erc20coin 超出精度","BSC","USDC","0x5f0a7433a68626c018ecae3cb69889184e8db970","0x3d7f18ad2cea9b59e54dfaf09b327c1ccd899591","0.0000000001000000009",400,2100000),

        ]

    @allure.story("Custodial Transfers Fail!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,from_add,to_add,amount,status_code,code', test_data)
    def test_custodial(self,test_title,networkCode,symbol,from_add,to_add,amount,status_code,code):

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