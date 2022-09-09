import json
import random
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
class Test_transfers_success_doge():
    test_data = [
        # 生产
        ("正常转账(自己转自己)!",["075a141217e765672c4ee57bc2b0dab0774aad0488ac018e045b9e1dae58573d"],["03d006ca425eb30e314c0de2ef0a656f1e30f1f0e320e2c364418b0b60132b89b1"],"DOGE","DOGE","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV",round(random.uniform(1,3), random.randint(3,5))),
        ("正常转账maximum(自己转自己)!",["075a141217e765672c4ee57bc2b0dab0774aad0488ac018e045b9e1dae58573d"],["03d006ca425eb30e314c0de2ef0a656f1e30f1f0e320e2c364418b0b60132b89b1"],"DOGE","DOGE","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV","maximum"),
        # ("正常转账!",["075a141217e765672c4ee57bc2b0dab0774aad0488ac018e045b9e1dae58573d"],["03d006ca425eb30e314c0de2ef0a656f1e30f1f0e320e2c364418b0b60132b89b1"],"DOGE","DOGE","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV","DG4NBVs5zyz1fTmiWm4zVGUPKpeHEp4efE",round(random.uniform(1,3), random.randint(3,6))),
        # ("正常转账maximum!",["075a141217e765672c4ee57bc2b0dab0774aad0488ac018e045b9e1dae58573d"],["03d006ca425eb30e314c0de2ef0a656f1e30f1f0e320e2c364418b0b60132b89b1"],"DOGE","DOGE","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV","DG4NBVs5zyz1fTmiWm4zVGUPKpeHEp4efE","maximum"),
    ]

    @allure.story("Transfers_DOGE_Success!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_address(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        with allure.step("查询From账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders.status_code == 200

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_add,
                "to":to_add,
                "symbol":symbol,
                "amount":amount
            }
            transfer = Http.HttpUtils.post_instructions("Transfer",body,networkCode,PublicKeys)
            assert transfer.status_code == 200

            t_estimatedFee = transfer.json()['_embedded']['transactions'][0]['estimatedFee']
            t_hash = transfer.json()['_embedded']['transactions'][0]['hash']
            t_id = transfer.json()['_embedded']['transactions'][0]['id']
            t_networkCode = transfer.json()['_embedded']['transactions'][0]['networkCode']
            t_requiredSignings = transfer.json()['_embedded']['transactions'][0]['requiredSignings']
            t_serialized = transfer.json()['_embedded']['transactions'][0]['serialized']
            t_status = transfer.json()['_embedded']['transactions'][0]['status']
            ID = transfer.json()['id']
            body_amount = transfer.json()["body"]["amount"]

            signatures = []
            for i in range(len(t_requiredSignings)):
                signature = Conf.Config.sign(privatekey[0],t_requiredSignings[i]['hash'])
                signatures.append(
                    {
                    "hash":t_requiredSignings[i]['hash'],
                    "publickey":t_requiredSignings[i]["publicKeys"][0],
                    "signature":signature
                }
                )

        with allure.step("签名交易——sign"):
            sig = Http.HttpUtils.post_sign_transfers(t_estimatedFee,t_hash,t_id,t_networkCode,t_requiredSignings,t_serialized,signatures)
            assert sig.status_code == 200

        with allure.step("广播交易——send"):
            send = Http.HttpUtils.post_send_transfers(t_id)
            assert send.status_code == 200

        # with allure.step("查询交易记录——transfers by id,交易状态变为:1"):
        #     # 循环查10次交易记录
        #     for i in range(10):
        #         sleep(20)
        #         logger.info("<----查询次数:第" + str(i+1) + "次---->")
        #         transfers = Http.HttpUtils.get_transactions_byid(res[8])
        #         if (transfers.json()["_embedded"]["transactions"][0]["status"] == "PENDING"):
        #             assert transfers.json()["status"] == -1
        #         elif (transfers.json()["_embedded"]["transactions"][0]["status"] == "SENT"):
        #             assert transfers.json()["status"] == -1
        #         elif (transfers.json()["_embedded"]["transactions"][0]["status"] == "SETTLED"):
        #             assert transfers.json()["status"] == 1
        #             break

        # with allure.step("查询关联交易记录——balance-transactions by hash"):
        #     sleep(30)
        #     transcations = Http.HttpUtils.get_transactions_byhash(send.json()["hash"])
        #     assert transcations.status_code == 200
            
        #     if (from_add == to_add):
        #         assert len(transcations.json()) == 1 # 自己转自己一条交易记录
        #         # assert transcations.json()[0]["type"] == -1 # type 是 -1
        #         # assert transcations.json()[0]["address"] == res[0].json()["from"] # address 是转出地址
        #         # assert transcations.json()[0]["amount"] ==  res[0].json()["amount"] + Conf.Config.amount_decimals(send.json()['estimatedFee'],8)
        #     else:
        #         assert len(transcations.json()) == 2
        #         # if(transcations.json()[0]["type"] == -1): # 判断第一个交易为转出地址
        #         #     assert transcations.json()[0]["address"] == res[0].json()["from"]
        #         #     # assert transcations.json()[0]["amount"] ==  res[0].json()["amount"] + Conf.Config.amount_decimals(send.json()['estimatedFee'],8)

        #         #     assert transcations.json()[1]["address"] == res[0].json()["to"]
        #         #     assert transcations.json()[1]["amount"] ==  res[0].json()["amount"]

        #         # else:
        #         #     assert transcations.json()[0]["address"] == res[0].json()["to"]
        #         #     assert transcations.json()[0]["amount"] ==  res[0].json()["amount"]

        #         #     assert transcations.json()[1]["address"] == res[0].json()["from"]
        #             # assert transcations.json()[1]["amount"] ==  res[0].json()["amount"] + Conf.Config.amount_decimals(send.json()['estimatedFee'],8)
        
        # with allure.step("查询From账户holders信息——holders"):
        #     holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
        #     assert holders.status_code == 200


# 多签账户
@allure.feature("Transfers_Success!")
class Test_transfers_success_doge_safe():
    test_data = [
        # 生产
        ("正常转账(自己转自己)!",["075a141217e765672c4ee57bc2b0dab0774aad0488ac018e045b9e1dae58573d"],["03d4c0eb608082b31cf1830f280aa38f513c2be8740f28cc006ebd8270e6cc46e7","03d006ca425eb30e314c0de2ef0a656f1e30f1f0e320e2c364418b0b60132b89b1"],"DOGE","DOGE","9tEa1ZC6fvJBRSicoCovyAQzYfMSBSLugM","9tEa1ZC6fvJBRSicoCovyAQzYfMSBSLugM",round(random.uniform(1,2), random.randint(3,5))),
        ("正常转账maximum(自己转自己)!",["075a141217e765672c4ee57bc2b0dab0774aad0488ac018e045b9e1dae58573d"],["03d4c0eb608082b31cf1830f280aa38f513c2be8740f28cc006ebd8270e6cc46e7","03d006ca425eb30e314c0de2ef0a656f1e30f1f0e320e2c364418b0b60132b89b1"],"DOGE","DOGE","9tEa1ZC6fvJBRSicoCovyAQzYfMSBSLugM","9tEa1ZC6fvJBRSicoCovyAQzYfMSBSLugM","maximum"),
        ("正常转账!",["075a141217e765672c4ee57bc2b0dab0774aad0488ac018e045b9e1dae58573d"],["03d4c0eb608082b31cf1830f280aa38f513c2be8740f28cc006ebd8270e6cc46e7","03d006ca425eb30e314c0de2ef0a656f1e30f1f0e320e2c364418b0b60132b89b1"],"DOGE","DOGE","9tEa1ZC6fvJBRSicoCovyAQzYfMSBSLugM","DG4NBVs5zyz1fTmiWm4zVGUPKpeHEp4efE",round(random.uniform(1,2), random.randint(3,5))),
        ("正常转账maximum!",["075a141217e765672c4ee57bc2b0dab0774aad0488ac018e045b9e1dae58573d"],["03d4c0eb608082b31cf1830f280aa38f513c2be8740f28cc006ebd8270e6cc46e7","03d006ca425eb30e314c0de2ef0a656f1e30f1f0e320e2c364418b0b60132b89b1"],"DOGE","DOGE","9tEa1ZC6fvJBRSicoCovyAQzYfMSBSLugM","DG4NBVs5zyz1fTmiWm4zVGUPKpeHEp4efE","maximum"),
    ]

    @allure.story("Transfers_DOGE_Success!")
    @allure.title('多签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_address_safe(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        with allure.step("查询From账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders.status_code == 200

        with allure.step("查询to账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,to_add)
            assert holders.status_code == 200

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
        
        with allure.step("查询From账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders.status_code == 200

        with allure.step("查询to账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,to_add)
            assert holders.status_code == 200

if __name__ == '__main__':
    path = os.path.abspath(__file__) + "::Test_transfers_success_doge"
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')