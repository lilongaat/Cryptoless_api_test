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
class Test_transfers_success_btc():
    test_data = [
        # 测试
        # ("正常转账(自己转自己)!",["dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b"],["022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"],"BTC","BTC","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun",Conf.Config.random_amount(5)),
        # ("正常转账maximum(自己转自己)!",["dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b"],["022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"],"BTC","BTC","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","maximum"),
        # ("正常转账!",["dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b"],["022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"],"BTC","BTC","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","tb1qxwtl4mmjrskgy4vtz6zcc8tkn8t6tv575mq6pf",Conf.Config.random_amount(6)),
        ("正常转账maximum!",["dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b"],["022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"],"BTC","BTC","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","tb1qxwtl4mmjrskgy4vtz6zcc8tkn8t6tv575mq6pf","maximum"),
    ]

    @allure.story("Transfers_BTC_Success!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_address(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        with allure.step("构建交易——transfers"):
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            res = Http.HttpUtils.post_transfers(networkCode,symbol,PublicKeys,from_add,to_add,amount,transactionParams)
            assert res[0].status_code == 200

        signatures = []
        for i in range(len(res[5])):
            signature = Conf.Config.sign(privatekey[0],res[5][i]['hash'])
            signatures.append(
                {
                "hash":res[5][i]['hash'],
                "publickey":PublicKeys[0],
                "signature":signature
            }
            )

        with allure.step("签名交易——sign"):
            sig = Http.HttpUtils.post_sign_transfers(res[1],res[2],res[3],res[4],res[5],res[6],signatures)
            assert sig.status_code == 200

        with allure.step("广播交易——send"):
            send = Http.HttpUtils.post_send_transfers(res[3])
            assert send.status_code == 200

        with allure.step("查询交易记录——transfers by id,交易状态变为:1"):
            # 循环查10次交易记录
            for i in range(10):
                sleep(20)
                logger.info("<----查询次数:第" + str(i+1) + "次---->")
                transfers = Http.HttpUtils.get_transactions_byid(res[8])
                if (transfers.json()["_embedded"]["transactions"][0]["status"] == "PENDING"):
                    assert transfers.json()["status"] == -1
                elif (transfers.json()["_embedded"]["transactions"][0]["status"] == "SENT"):
                    assert transfers.json()["status"] == -1
                elif (transfers.json()["_embedded"]["transactions"][0]["status"] == "SETTLED"):
                    assert transfers.json()["status"] == 1
                    break

        with allure.step("查询关联交易记录——balance-transactions by hash"):
            sleep(30)
            transcations = Http.HttpUtils.get_transactions_byhash(send.json()["hash"])
            assert transcations.status_code == 200
            
            if (from_add == to_add):
                assert len(transcations.json()) == 1 # 自己转自己一条交易记录
                assert transcations.json()[0]["type"] == -1 # type 是 -1
                assert transcations.json()[0]["address"] == res[0].json()["from"] # address 是转出地址
                # assert transcations.json()[0]["amount"] ==  res[0].json()["amount"] + Conf.Config.amount_decimals(send.json()['estimatedFee'],8)
            else:
                assert len(transcations.json()) == 2
                if(transcations.json()[0]["type"] == -1): # 判断第一个交易为转出地址
                    assert transcations.json()[0]["address"] == res[0].json()["from"]
                    # assert transcations.json()[0]["amount"] ==  res[0].json()["amount"] + Conf.Config.amount_decimals(send.json()['estimatedFee'],8)

                    assert transcations.json()[1]["address"] == res[0].json()["to"]
                    assert transcations.json()[1]["amount"] ==  res[0].json()["amount"]

                else:
                    assert transcations.json()[0]["address"] == res[0].json()["to"]
                    assert transcations.json()[0]["amount"] ==  res[0].json()["amount"]

                    assert transcations.json()[1]["address"] == res[0].json()["from"]
                    # assert transcations.json()[1]["amount"] ==  res[0].json()["amount"] + Conf.Config.amount_decimals(send.json()['estimatedFee'],8)