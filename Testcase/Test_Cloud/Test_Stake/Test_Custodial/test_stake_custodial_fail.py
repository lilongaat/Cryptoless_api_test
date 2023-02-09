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
            # BTC
            ("网络不支持质押","BTC","BTC","stake","tb1q7ymdm79ryug7vttw4jrf87pdcmn67n3p9rgc5x","0.0000001",400,2100000),
            ("网络不支持赎回","BTC","BTC","un_stake","tb1q7ymdm79ryug7vttw4jrf87pdcmn67n3p9rgc5x","0.0000001",400,2100000),
            ("网络不支持claim","BTC","BTC","claim","tb1q7ymdm79ryug7vttw4jrf87pdcmn67n3p9rgc5x","0.0000001",400,2100000),
            
            # IRIS
            ("IRIS Custodial账户质押数量超过余额","IRIS","IRIS","stake","iaa1q2eql0hjd345tfxnzat6s7jfpwg3jansv8krwe","10000",400,2102001),
            ("IRIS Custodial账户质押数量超过精度","IRIS","IRIS","stake","iaa1q2eql0hjd345tfxnzat6s7jfpwg3jansv8krwe","0.000000001",400,2100000),
            ("IRIS Custodial账户质押手续费不足","IRIS","IRIS","stake","iaa1fryssfhcmp8jnzsqg750w8vgg426gcfdr9gezr","0.000007",400,2100000),
            ("IRIS Custodial账户赎回数量超过质押金额","IRIS","IRIS","un_stake","iaa1q2eql0hjd345tfxnzat6s7jfpwg3jansv8krwe","10000",400,2100000),
            ("IRIS Custodial账户赎回数量超过精度","IRIS","IRIS","un_stake","iaa1q2eql0hjd345tfxnzat6s7jfpwg3jansv8krwe","0.000000001",400,2100000),
            ("IRIS Custodial账户赎回手续费不足","IRIS","IRIS","un_stake","iaa1fryssfhcmp8jnzsqg750w8vgg426gcfdr9gezr","0.000007",400,2100000),
            ("IRIS Custodial账户claim手续费不足","IRIS","IRIS","claim","iaa1fryssfhcmp8jnzsqg750w8vgg426gcfdr9gezr",0,400,2100000),

            # CLV
            ("CLV Custodial账户质押超过余额","CLV","CLV","stake","5G8W1b7pWa7zzcYAWomTaX2zmP1SHE7JDEGvQTdGh45d83te","1000",400,2102001),
            ("CLV Custodial账户质押超过精度","CLV","CLV","stake","5G8W1b7pWa7zzcYAWomTaX2zmP1SHE7JDEGvQTdGh45d83te","0.0000000000000000009",400,2100000),
            ("CLV Custodial账户质押手续费不足","CLV","CLV","stake","5Hbo5z1FjYYDFvHtrKrCZfemwNRHPLhjH69hZbtFj56QbgtM","0.000000000001",400,2100000),
            ("CLV Custodial账户赎回数量超过质押金额","CLV","CLV","un_stake","5G8W1b7pWa7zzcYAWomTaX2zmP1SHE7JDEGvQTdGh45d83te","100",400,2100000),
            ("CLV Custodial账户赎回数量超过精度","CLV","CLV","un_stake","5G8W1b7pWa7zzcYAWomTaX2zmP1SHE7JDEGvQTdGh45d83te","0.0000000000000000009",400,2100000),
            ("CLV Custodial账户赎回手续费不足","CLV","CLV","un_stake","5Hbo5z1FjYYDFvHtrKrCZfemwNRHPLhjH69hZbtFj56QbgtM","0.0008",400,2100000),
            ("CLV Custodial账户claim手续费不足或者没有rewards","CLV","CLV","claim","5Hbo5z1FjYYDFvHtrKrCZfemwNRHPLhjH69hZbtFj56QbgtM",0,400,2100000),
        ]
    if env_type == 1: #生产
        test_data = [
            # DOGE
            ("网络不支持质押","DOGE","DOGE","stake","D9vakMz4cLhRXjjQyhSxMX7Wg3xmoFMeQ6","0.0000001",400,2100000),
            ("网络不支持赎回","DOGE","DOGE","un_stake","D9vakMz4cLhRXjjQyhSxMX7Wg3xmoFMeQ6","0.0000001",400,2100000),
            ("网络不支持claim","DOGE","DOGE","claim","D9vakMz4cLhRXjjQyhSxMX7Wg3xmoFMeQ6","0.0000001",400,2100000),

            # ATOM
            ("ATOM Custodial账户质押数量超过余额","ATOM","ATOM","stake","cosmos1wde9r4gu5qtx3qelnfr2y5w7q7esj7pefx3urc","10000",400,2102001),
            ("ATOM Custodial账户质押数量超过精度","ATOM","ATOM","stake","cosmos1wde9r4gu5qtx3qelnfr2y5w7q7esj7pefx3urc","0.000000001",400,2100000),
            ("ATOM Custodial账户质押手续费不足","ATOM","ATOM","stake","cosmos1gwq08rk3lgh4ck86tp2lv7tk9jxht2nd5dgxpv","0.000007",400,2100000),
            ("ATOM Custodial账户赎回数量超过质押金额","ATOM","ATOM","un_stake","cosmos1wde9r4gu5qtx3qelnfr2y5w7q7esj7pefx3urc","10000",400,2100000),
            ("ATOM Custodial账户赎回数量超过精度","ATOM","ATOM","un_stake","cosmos1wde9r4gu5qtx3qelnfr2y5w7q7esj7pefx3urc","0.000000001",400,2100000),
            ("ATOM Custodial账户赎回手续费不足","ATOM","ATOM","un_stake","cosmos1gwq08rk3lgh4ck86tp2lv7tk9jxht2nd5dgxpv","0.000007",400,2100000),
            ("ATOM Custodial账户claim手续费不足","ATOM","ATOM","claim","cosmos1gwq08rk3lgh4ck86tp2lv7tk9jxht2nd5dgxpv",0,400,2100000),

            # IRIS
            ("IRIS Custodial账户质押数量超过余额","IRIS","IRIS","stake","iaa1j9vswglv54xlmrza98ww44jgnm0j0hncw2t7v9","10000",400,2102001),
            ("IRIS Custodial账户质押数量超过精度","IRIS","IRIS","stake","iaa1j9vswglv54xlmrza98ww44jgnm0j0hncw2t7v9","0.000000001",400,2100000),
            ("IRIS Custodial账户质押手续费不足","IRIS","IRIS","stake","iaa18uz67zyva2nxqskr8d3nqszzyg0j085pwtxr5a","0.000007",400,2100000),
            ("IRIS Custodial账户赎回数量超过质押金额","IRIS","IRIS","un_stake","iaa1j9vswglv54xlmrza98ww44jgnm0j0hncw2t7v9","10000",400,2100000),
            ("IRIS Custodial账户赎回数量超过精度","IRIS","IRIS","un_stake","iaa1j9vswglv54xlmrza98ww44jgnm0j0hncw2t7v9","0.000000001",400,2100000),
            ("IRIS Custodial账户赎回手续费不足","IRIS","IRIS","un_stake","iaa18uz67zyva2nxqskr8d3nqszzyg0j085pwtxr5a","0.000007",400,2100000),
            ("IRIS Custodial账户claim手续费不足","IRIS","IRIS","claim","iaa18uz67zyva2nxqskr8d3nqszzyg0j085pwtxr5a",0,400,2100000),

            # DOT

            # CLV
            ("CLV Custodial账户质押超过余额","CLV","CLV","stake","5DNA4hJL6YLKFwajJpPsvYW3ne9SRYcCminoYVMhKiThmBmc","1000",400,2102001),
            ("CLV Custodial账户质押超过精度","CLV","CLV","stake","5DNA4hJL6YLKFwajJpPsvYW3ne9SRYcCminoYVMhKiThmBmc","0.0000000000000000009",400,2100000),
            ("CLV Custodial账户质押手续费不足","CLV","CLV","stake","5Fa3DYnfmMgyeWqo92Dx2PAzEiVBRkFH85g5NaVdQ87HhsZ7","0.000000000001",400,2100000),
            ("CLV Custodial账户赎回数量超过质押金额","CLV","CLV","un_stake","5DNA4hJL6YLKFwajJpPsvYW3ne9SRYcCminoYVMhKiThmBmc","100",400,2100000),
            ("CLV Custodial账户赎回数量超过精度","CLV","CLV","un_stake","5DNA4hJL6YLKFwajJpPsvYW3ne9SRYcCminoYVMhKiThmBmc","0.0000000000000000009",400,2100000),
            ("CLV Custodial账户赎回手续费不足","CLV","CLV","un_stake","5Fa3DYnfmMgyeWqo92Dx2PAzEiVBRkFH85g5NaVdQ87HhsZ7","0.0008",400,2100000),
            ("CLV Custodial账户claim手续费不足或者没有rewards","CLV","CLV","claim","5Fa3DYnfmMgyeWqo92Dx2PAzEiVBRkFH85g5NaVdQ87HhsZ7",0,400,2100000),
        ]

    @allure.story("Custodial Stake Fail!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,type,address,amount,status_code,code', test_data)
    def test_custodial(self,test_title,networkCode,symbol,type,address,amount,status_code,code):

        with allure.step("查询from账户holder信息"):
            holder = Http.HttpUtils.holders(networkCode=networkCode,symbol=symbol,address=address)
            assert holder.status_code ==200

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

            assert stake.status_code == status_code
            assert stake.json()["code"] == code


if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')