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
from Common import Httpcore, Conf,Http
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))


@allure.feature("Transfer Success!")
class Test_transfer_success:
    if env_type == 0: #测试
        test_data = [
            ("BTC多签账户账户转账",["b61190f8b2fcb4754ff8527f083bb3df68bf89285d7c5e428276f5f4572b7abe"],["02e8852463021b47fe5214c599e87e431f2eb1219044946bbff397afd0518b85a6"],"BTC","tb1qxrunvz3ywjtpzaasfgjjek96a33sxks740v58x7lzke0kc9urvgs0cczgd",["tb1q0558s53xchyghw34tqm4x8t2n8swf666nvhffq"],["100"]),
            # ("BTC多签账户批量转账",["b61190f8b2fcb4754ff8527f083bb3df68bf89285d7c5e428276f5f4572b7abe"],["02e8852463021b47fe5214c599e87e431f2eb1219044946bbff397afd0518b85a6"],"BTC","tb1qxrunvz3ywjtpzaasfgjjek96a33sxks740v58x7lzke0kc9urvgs0cczgd",["tb1qyczy479xgg8flr4amkrxp6s4an7huecg9mq2ay","tb1q9ps855ksckycta6kqjecszvu39pg4nedkx540t","tb1q0r3zhkjf408nf069dd9z7lal6zzyhva860pt3y"],["100","200","300"]),
        ]
    elif env_type == 1: #生产
        test_data = []

    @allure.story("Transfer Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,publickeys,networkCode,fromaddress,toaddress,value', test_data)
    def test_custodial(self,test_title,privatekey,publickeys,networkCode,fromaddress,toaddress,value):

        with allure.step("查询账户publickey"):
            pubs  = Http.HttpUtils.accounts(address=fromaddress)
            publickeys = []
            for p in range(len(pubs.json()["list"][0]["publicKeys"])):
                publickey = pubs.json()["list"][0]["publicKeys"][p]["value"]
                publickeys.append(publickey)


        with allure.step("查询地址UTXO"):
            utxo = Httpcore.HttpCoreUtils.query_utxo(networkCode,fromaddress)
            assert utxo.status_code == 200
            utxos = []
            for i in range(len(utxo.json())):
                utxo_ = {
                    "amount": utxo.json()[i]["value"],
                    "witnessScript": Conf.Config.witnessScript(publickeys),
                    "signers":publickeys,
                    "txid": utxo.json()[i]["mintTxid"],
                    "vout": utxo.json()[i]["mintIndex"],
                }
                utxos.append(utxo_)

        with allure.step("构建交易"):
            recipients = []
            for i in range(len(toaddress)):
                recipient = {
                    "address": toaddress[i],
                    "value": value[i]
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
            requiredSignings = ts.json()["requiredSignings"]

            signatures = []
            for i in range(len(requiredSignings)):
                hash = requiredSignings[i]["hash"]
                for j in range(len(requiredSignings[i]["publicKeys"])):
                    signature = {
                        "hash":hash,
                        "publicKey":requiredSignings[i]["publicKeys"][j],
                        "signature":Conf.Config.sign(privatekey[j],hash)

                    }
                    signatures.append(signature)

        with allure.step("Sign交易"):
            sign = Http.HttpUtils.sign(id,signatures)
            assert sign.status_code == 200

        with allure.step("广播交易"):
            send = Http.HttpUtils.send(id)
            assert send.status_code == 200

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')