import json
import random
import string
from time import sleep
from decimal import Decimal
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
from Common import Httpcore, Conf
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))


@allure.feature("Transfer Success!")
class Test_transfer_success:
    if env_type == 0: #测试
        test_data = [
            # ("BTC多签账户账户转账",["b61190f8b2fcb4754ff8527f083bb3df68bf89285d7c5e428276f5f4572b7abe","320e15269f5d12054ff67dbe1e7984c6af2f58db8f4ca3f429e98fe6a01c9e47"],["02e8852463021b47fe5214c599e87e431f2eb1219044946bbff397afd0518b85a6","0231e263a7e95bf5107b88b85b49918841b937305cce5dae7dd7ba9b86fc460f70"],"BTC","tb1q4t8jtp4fwjg4spfjh7ux5ckhrallj652kwrj48gcvd0rt5g9ea3q4vlm33",["tb1q0558s53xchyghw34tqm4x8t2n8swf666nvhffq"],["100"]),
            ("BTC多签账户批量转账",["b61190f8b2fcb4754ff8527f083bb3df68bf89285d7c5e428276f5f4572b7abe","320e15269f5d12054ff67dbe1e7984c6af2f58db8f4ca3f429e98fe6a01c9e47"],["02e8852463021b47fe5214c599e87e431f2eb1219044946bbff397afd0518b85a6","0231e263a7e95bf5107b88b85b49918841b937305cce5dae7dd7ba9b86fc460f70"],"BTC","tb1q4t8jtp4fwjg4spfjh7ux5ckhrallj652kwrj48gcvd0rt5g9ea3q4vlm33",["tb1qyczy479xgg8flr4amkrxp6s4an7huecg9mq2ay","tb1q9ps855ksckycta6kqjecszvu39pg4nedkx540t","tb1q0r3zhkjf408nf069dd9z7lal6zzyhva860pt3y"],["100","200","300"]),
        ]
    elif env_type == 1: #生产
        test_data = []

    @allure.story("Transfer Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,publickey,networkCode,fromaddress,toaddress,value', test_data)
    def test_custodial(self,test_title,privatekey,publickey,networkCode,fromaddress,toaddress,value):

        with allure.step("查询地址UTXO"):
            utxo = Httpcore.HttpCoreUtils.query_utxo(networkCode,fromaddress)
            assert utxo.status_code == 200
            utxos = []
            for i in range(len(utxo.json())):
                utxo_ = {
                    "amount": utxo.json()[i]["value"],
                    "witnessScript": Conf.Config.witnessScript(["0231e263a7e95bf5107b88b85b49918841b937305cce5dae7dd7ba9b86fc460f70","02e8852463021b47fe5214c599e87e431f2eb1219044946bbff397afd0518b85a6"]),
                    "signers":publickey,
                    "txid": utxo.json()[i]["mintTxid"],
                    "vout": utxo.json()[i]["mintIndex"],
                }
                utxos.append(utxo_)

        with allure.step("Build交易"):
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

            ts = Httpcore.HttpCoreUtils.core_build(body)
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
            sign = Httpcore.HttpCoreUtils.core_sign(id,signatures)
            assert sign.status_code == 200

        with allure.step("广播交易"):
            send = Httpcore.HttpCoreUtils.core_send(id)
            assert send.status_code == 200

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')