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

# 单签账户
@allure.feature("Transfers_Success!")
class Test_transfers_success_btc():
    test_data = [
        # 测试
        ("正常转账(自己转自己)!",["dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b"],["022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"],"BTC","BTC","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun",Conf.Config.random_amount(5)),
        ("正常转账maximum(自己转自己)!",["dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b"],["022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"],"BTC","BTC","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","maximum"),
        ("正常转账!",["dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b"],["022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"],"BTC","BTC","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","tb1qxwtl4mmjrskgy4vtz6zcc8tkn8t6tv575mq6pf",Conf.Config.random_amount(6)),
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

# 多签账户
@allure.feature("Transfers_Success!")
class Test_transfers_success_btc_safe():
    test_data = [
        # 测试
        ("正常转账(自己转自己)!",["dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b"],["024071bf3a05b971def0e7b01b63357e2de43b6b0f02ca43c3d8405ad52da79b4b","022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"],"BTC","BTC","tb1qf8ejg80dqln4t2haceu096kfn0wfta075qgq4l9r2nfxjgc3kapsnsutu3","tb1qf8ejg80dqln4t2haceu096kfn0wfta075qgq4l9r2nfxjgc3kapsnsutu3",Conf.Config.random_amount(5)),
        ("正常转账maximum(自己转自己)!",["dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b"],["024071bf3a05b971def0e7b01b63357e2de43b6b0f02ca43c3d8405ad52da79b4b","022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"],"BTC","BTC","tb1qf8ejg80dqln4t2haceu096kfn0wfta075qgq4l9r2nfxjgc3kapsnsutu3","tb1qf8ejg80dqln4t2haceu096kfn0wfta075qgq4l9r2nfxjgc3kapsnsutu3","maximum"),
        ("正常转账!",["dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b"],["024071bf3a05b971def0e7b01b63357e2de43b6b0f02ca43c3d8405ad52da79b4b","022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"],"BTC","BTC","tb1qf8ejg80dqln4t2haceu096kfn0wfta075qgq4l9r2nfxjgc3kapsnsutu3","tb1qxwtl4mmjrskgy4vtz6zcc8tkn8t6tv575mq6pf",Conf.Config.random_amount(6)),
        ("正常转账maximum!",["dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b"],["024071bf3a05b971def0e7b01b63357e2de43b6b0f02ca43c3d8405ad52da79b4b","022bf595281b06dcb38c9261c5dfeb979ee63c79d47ad328bb8606f6b000d855ea"],"BTC","BTC","tb1qf8ejg80dqln4t2haceu096kfn0wfta075qgq4l9r2nfxjgc3kapsnsutu3","tb1qxwtl4mmjrskgy4vtz6zcc8tkn8t6tv575mq6pf","maximum"),
    ]

    @allure.story("Transfers_BTC_Success!")
    @allure.title('多签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_address_safe(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

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
                    "publickey":PublicKeys[1],
                    "signature":signature
                }
                )
            logger.error(signatures)

        with allure.step("请求签名交易——req_sign"):
            requiredSignings = []
            for i in range(len(res[5])):
                requiredSignings.append(
                    {
                    "message":res[5][i]['hash'],
                    "publicKey":res[5][i]['publicKeys'][0]
                    }
                )
            reqsign = Http.HttpUtils.post_req_sign(requiredSignings)
            assert reqsign.status_code == 200

        with allure.step("获取验证码——verify"):
            reqverify = Http.HttpUtils.post_req_Verify(reqsign.json()["id"])
            assert reqverify.status_code == 200
        
        with allure.step("托管key提交签名——confirm-sign"):
            confirmsign = Http.HttpUtils.post_confirm_sign(reqsign.json()["id"],"000000")
            assert confirmsign.status_code == 200

            for i in range(len(confirmsign.json())):
                signatures.append({
                    "hash":confirmsign.json()[i]["message"],
                    "publickey":confirmsign.json()[i]["publicKey"],
                    "signature":confirmsign.json()[i]["signature"]
                })
            logger.error(signatures)

        with allure.step("签名交易——sign"):
            sig = Http.HttpUtils.post_sign_transfers(res[1],res[2],res[3],res[4],res[5],res[6],signatures)
            assert sig.status_code == 200

        with allure.step("广播交易——send"):
            send = Http.HttpUtils.post_send_transfers(res[3])
            assert send.status_code == 200

        with allure.step("查询交易记录——transfers by id,交易状态变为:1"):
            # 循环查10次交易记录
            for i in range(10):
                sleep(30)
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
                # assert transcations.json()[0]["type"] == -1 # type 是 -1
                # assert transcations.json()[0]["address"] == res[0].json()["from"] # address 是转出地址
                # # assert transcations.json()[0]["amount"] ==  res[0].json()["amount"] + Conf.Config.amount_decimals(send.json()['estimatedFee'],8)
            else:
                assert len(transcations.json()) == 2
                # if(transcations.json()[0]["type"] == -1): # 判断第一个交易为转出地址
                #     assert transcations.json()[0]["address"] == res[0].json()["from"]
                #     # assert transcations.json()[0]["amount"] ==  res[0].json()["amount"] + Conf.Config.amount_decimals(send.json()['estimatedFee'],8)

                #     assert transcations.json()[1]["address"] == res[0].json()["to"]
                #     assert transcations.json()[1]["amount"] ==  res[0].json()["amount"]

                # else:
                #     assert transcations.json()[0]["address"] == res[0].json()["to"]
                #     assert transcations.json()[0]["amount"] ==  res[0].json()["amount"]

                #     assert transcations.json()[1]["address"] == res[0].json()["from"]
                #     # assert transcations.json()[1]["amount"] ==  res[0].json()["amount"] + Conf.Config.amount_decimals(send.json()['estimatedFee'],8)