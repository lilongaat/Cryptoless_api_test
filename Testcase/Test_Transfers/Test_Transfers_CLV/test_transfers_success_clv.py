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
class Test_transfers_success_clv:
    test_data = [
        # 测试
        ("正常转账!",["053d329fb54f8ab36473e74fd4905644a4d5857836274d3116675bad4cfa4273"],["02fd88692ce948598b310d9ac081d551e74a7b4a70661f45e92544e0c3fa0b70f1"],"CLV","CLV","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","5EMjsczhZw8mUYfyfDJT69PUBAirrviW2bH4chQxKHheCvX3",Conf.Config.random_amount(8)),
        ("正常转账(自己转自己)!",["053d329fb54f8ab36473e74fd4905644a4d5857836274d3116675bad4cfa4273"],["02fd88692ce948598b310d9ac081d551e74a7b4a70661f45e92544e0c3fa0b70f1"],"CLV","CLV","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT",Conf.Config.random_amount(9)),
    ]

    @allure.story("Transfers_CLV_Success!")
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
                "publickey":res[5][0]['publicKeys'][0],
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
                sleep(60)
                logger.info("<----查询次数:第" + str(i+1) + "次---->")
                transcations = Http.HttpUtils.get_transactions_byhash(send.json()["hash"])
                assert transcations.status_code == 200
                if (len(transcations.json()) > 0):
                    break
            
            if (from_add == to_add):
                assert len(transcations.json()) == 1 # 自己转自己一条交易记录
                assert transcations.json()[0]["type"] == -1 # type 是 -1
                assert transcations.json()[0]["address"] == res[0].json()["from"] # address 是转出地址
                assert transcations.json()[0]["amount"] ==  res[0].json()["amount"] + Conf.Config.amount_decimals(send.json()['estimatedFee'],18)
            else:
                assert len(transcations.json()) == 2
                if(transcations.json()[0]["type"] == -1): # 判断第一个交易为转出地址
                    assert transcations.json()[0]["address"] == res[0].json()["from"]
                    assert transcations.json()[0]["amount"] ==  res[0].json()["amount"] + Conf.Config.amount_decimals(send.json()['estimatedFee'],18)

                    assert transcations.json()[1]["address"] == res[0].json()["to"]
                    assert transcations.json()[1]["amount"] ==  res[0].json()["amount"]

                else:
                    assert transcations.json()[0]["address"] == res[0].json()["to"]
                    assert transcations.json()[0]["amount"] ==  res[0].json()["amount"]

                    assert transcations.json()[1]["address"] == res[0].json()["from"]
                    assert transcations.json()[1]["amount"] ==  res[0].json()["amount"] + Conf.Config.amount_decimals(send.json()['estimatedFee'],18)