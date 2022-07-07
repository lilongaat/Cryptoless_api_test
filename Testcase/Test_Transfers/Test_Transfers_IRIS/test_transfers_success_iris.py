import json
from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Conf
from Common.Loguru import logger


@allure.feature("Transfers_Success!")
class Test_transfers_success_iris:
    test_data = [
        # 测试
        ("正常转账!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],["033511e38fd373c4515ada4826616146b4c3def47da9907b59d9555b19134dd683"],"IRIS","IRIS","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u","iaa1q4c4v460lnfezw4p2jzt85d7mahxu9sk0nfhvf",Conf.Config.random_amount(4)),
        ("正常转账(自己转自己)!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],["033511e38fd373c4515ada4826616146b4c3def47da9907b59d9555b19134dd683"],"IRIS","IRIS","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u",Conf.Config.random_amount(4)),
    ]

    @allure.story("Transfers_IRIS_Success!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_address(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        with allure.step("构建交易——transfers"):
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            res = Http.HttpUtils.post_transfers(networkCode,symbol,PublicKeys,from_add,to_add,amount,transactionParams)
            assert res[0].status_code == 200

        signature = Conf.Config.sign(privatekey[0],res[5][0]['hash'])
        signatures = [
            {
                "hash":res[5][0]['hash'],
                "publickey":PublicKeys[0],
                "signature":signature
            }
        ]

        with allure.step("签名交易——sign"):
            sig = Http.HttpUtils.post_sign_transfers(res[1],res[2],res[3],res[4],res[5],res[6],signatures)
            assert sig.status_code == 200

        with allure.step("广播交易——send"):
            send = Http.HttpUtils.post_send_transfers(res[3])
            assert send.status_code == 200
        
        with allure.step("查询关联交易记录——balance-transactions by hash"):
            # 循环查10次关联交易记录
            for i in range(10):
                sleep(20)
                logger.info("<----查询次数:第" + str(i+1) + "次---->")
                transcations = Http.HttpUtils.get_transactions_byhash(send.json()["hash"])
                assert transcations.status_code == 200
                if (len(transcations.json()) > 0):
                    break
            
            if (from_add == to_add):
                assert len(transcations.json()) == 1 # 自己转自己一条交易记录
                assert transcations.json()[0]["type"] == -1 # type 是 -1
                assert transcations.json()[0]["address"] == res[0].json()["from"] # address 是转出地址
                assert transcations.json()[0]["amount"] ==  res[0].json()["amount"] + Conf.Config.amount_decimals(send.json()['estimatedFee'],6)
            else:
                assert len(transcations.json()) == 2
                if(transcations.json()[0]["type"] == -1): # 判断第一个交易为转出地址
                    assert transcations.json()[0]["address"] == res[0].json()["from"]
                    assert transcations.json()[0]["amount"] ==  res[0].json()["amount"] + Conf.Config.amount_decimals(send.json()['estimatedFee'],6)

                    assert transcations.json()[1]["address"] == res[0].json()["to"]
                    assert transcations.json()[1]["amount"] ==  res[0].json()["amount"]

                else:
                    assert transcations.json()[0]["address"] == res[0].json()["to"]
                    assert transcations.json()[0]["amount"] ==  res[0].json()["amount"]

                    assert transcations.json()[1]["address"] == res[0].json()["from"]
                    assert transcations.json()[1]["amount"] ==  res[0].json()["amount"] + Conf.Config.amount_decimals(send.json()['estimatedFee'],6)