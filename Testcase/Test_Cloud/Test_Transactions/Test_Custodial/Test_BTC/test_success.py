import json
import random
import string
from time import sleep
from decimal import Decimal
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))))
from Common import Httpcore, Conf, Http
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))


@allure.feature("Transfer Success!")
class Test_transfer_success:
    if env_type == 0: #测试
        test_data = [
            ("BTC custodial账户转账","BTC","tb1q7ymdm79ryug7vttw4jrf87pdcmn67n3p9rgc5x",["tb1qhcuul2fcyv5rvr5mc5cy5saz0q5p3kx0gsy3c0"],["100"]),
            # ("BTC custodial账户批量转账","BTC","tb1q7ymdm79ryug7vttw4jrf87pdcmn67n3p9rgc5x",["tb1q0558s53xchyghw34tqm4x8t2n8swf666nvhffq","tb1qn0qrq4zfxjc89c773s6k86faym3ugpcje9eras","tb1qk50y4995th8tffhc90tz7533lygzwz57zxmhtj"],["100","200","300"]),
        ]
    elif env_type == 1: #生产
        test_data = []

    @allure.story("Transfer Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,fromaddress,toaddress,value', test_data)
    def test_custodial(self,test_title,networkCode,fromaddress,toaddress,value):

        with allure.step("查询账户publickeys"):
            pub = Http.HttpUtils.accounts(address=fromaddress)
            assert pub.status_code == 200
            publickeys  = [pub.json()["list"][0]["publicKeys"][0]["value"]]

        with allure.step("查询地址UTXO"):
            utxo = Httpcore.HttpCoreUtils.query_utxo(networkCode,fromaddress)
            assert utxo.status_code == 200
            utxos = []
            for i in range(len(utxo.json())):
                utxo_ = {
                    "amount": utxo.json()[i]["value"],
                    "scriptPubKey": utxo.json()[0]["script"],
                    "signers":publickeys,
                    "txid": utxo.json()[i]["mintTxid"],
                    "vout": utxo.json()[i]["mintIndex"],
                }
                utxos.append(utxo_)

        with allure.step("构建交易——transactions"):
            recipients = []
            for i in range(len(toaddress)):
                recipient = {
                    "address":toaddress[i],
                    "value":value[i]
                }
                recipients.append(recipient)

            body = {
                    "networkCode": networkCode,
                    "payload": {
                        "changer": fromaddress,
                        "recipients": recipients,
                        "utxos": utxos
                    },
                    "type": "TRANSACTION"
                }

            ts = Http.HttpUtils.transactions(body)
            assert ts.status_code == 200
            id = ts.json()["id"]

        with allure.step("广播交易"):
            send = Http.HttpUtils.send(id)
            assert send.status_code == 200

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')