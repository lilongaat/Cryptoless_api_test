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
class Test_transfers_success_clv:
    test_data = [
        # 测试
        ("正常转账(自己转自己)!",["053d329fb54f8ab36473e74fd4905644a4d5857836274d3116675bad4cfa4273"],["02fd88692ce948598b310d9ac081d551e74a7b4a70661f45e92544e0c3fa0b70f1"],"CLV","CLV","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT",Conf.Config.random_amount(9)),
        ("正常转账maximum(自己转自己)!",["053d329fb54f8ab36473e74fd4905644a4d5857836274d3116675bad4cfa4273"],["02fd88692ce948598b310d9ac081d551e74a7b4a70661f45e92544e0c3fa0b70f1"],"CLV","CLV","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","maximum"),
        ("正常转账!",["053d329fb54f8ab36473e74fd4905644a4d5857836274d3116675bad4cfa4273"],["02fd88692ce948598b310d9ac081d551e74a7b4a70661f45e92544e0c3fa0b70f1"],"CLV","CLV","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","5GsLke2jx8tneTn9EvfzppMhzU9KmEgCSNkbz1tfRaRsiX8J",Conf.Config.random_amount(8)),
        ("正常转账maximum!",["053d329fb54f8ab36473e74fd4905644a4d5857836274d3116675bad4cfa4273"],["02fd88692ce948598b310d9ac081d551e74a7b4a70661f45e92544e0c3fa0b70f1"],"CLV","CLV","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","5GsLke2jx8tneTn9EvfzppMhzU9KmEgCSNkbz1tfRaRsiX8J","maximum"),
    ]
    # test_data = [
    #     # 生产
    #     ("正常转账(自己转自己)!",["460d181b618e1748fc6632324609fd8e8e0058571fb7a932cd86596f59b2079c"],["033b345f6c30788674ff9799b377cc5da28ceb2be631c5b9e5ca538e0b4ae4dce5"],"CLV","CLV","5G7h24hiSHuewgtVBXe1dhqvRjJ5VKMzZmL1ntJb1pnW4FiC","5DPQQRu3Xne5KEKXCzFuVt7VJzkX9MiNPJBPWL66uFvBeKmU",Conf.Config.random_amount(4)),
    #     ("正常转账maximum(自己转自己)!",["460d181b618e1748fc6632324609fd8e8e0058571fb7a932cd86596f59b2079c"],["033b345f6c30788674ff9799b377cc5da28ceb2be631c5b9e5ca538e0b4ae4dce5"],"CLV","CLV","5G7h24hiSHuewgtVBXe1dhqvRjJ5VKMzZmL1ntJb1pnW4FiC","5DPQQRu3Xne5KEKXCzFuVt7VJzkX9MiNPJBPWL66uFvBeKmU","maximum"),
    #     ("正常转账!",["460d181b618e1748fc6632324609fd8e8e0058571fb7a932cd86596f59b2079c"],["033b345f6c30788674ff9799b377cc5da28ceb2be631c5b9e5ca538e0b4ae4dce5"],"CLV","CLV","5G7h24hiSHuewgtVBXe1dhqvRjJ5VKMzZmL1ntJb1pnW4FiC","5DPQQRu3Xne5KEKXCzFuVt7VJzkX9MiNPJBPWL66uFvBeKmU",Conf.Config.random_amount(8)),
    #     ("正常转账maximum!",["460d181b618e1748fc6632324609fd8e8e0058571fb7a932cd86596f59b2079c"],["033b345f6c30788674ff9799b377cc5da28ceb2be631c5b9e5ca538e0b4ae4dce5"],"CLV","CLV","5G7h24hiSHuewgtVBXe1dhqvRjJ5VKMzZmL1ntJb1pnW4FiC","5DPQQRu3Xne5KEKXCzFuVt7VJzkX9MiNPJBPWL66uFvBeKmU","maximum"),
    # ]

    @allure.story("Transfers_CLV_Success!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_address(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        with allure.step("查询From账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders.status_code == 200

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
            sleep(15)
            transcations = Http.HttpUtils.get_transactions_byhash(send.json()["hash"])
            assert transcations.status_code == 200
            
            if (from_add == to_add):
                assert len(transcations.json()) == 1 # 自己转自己一条交易记录
                # assert transcations.json()[0]["type"] == -1 # type 是 -1
                # assert transcations.json()[0]["address"] == res[0].json()["from"] # address 是转出地址
                # assert transcations.json()[0]["amount"] ==  res[0].json()["amount"] + Conf.Config.amount_decimals(send.json()['estimatedFee'],18)
            else:
                assert len(transcations.json()) == 2
                # if(transcations.json()[0]["type"] == -1): # 判断第一个交易为转出地址
                #     assert transcations.json()[0]["address"] == res[0].json()["from"]
                #     # assert transcations.json()[0]["amount"] ==  res[0].json()["amount"] + Conf.Config.amount_decimals(send.json()['estimatedFee'],18)

                #     assert transcations.json()[1]["address"] == res[0].json()["to"]
                #     assert transcations.json()[1]["amount"] ==  res[0].json()["amount"]

                # else:
                #     assert transcations.json()[0]["address"] == res[0].json()["to"]
                #     assert transcations.json()[0]["amount"] ==  res[0].json()["amount"]

                #     assert transcations.json()[1]["address"] == res[0].json()["from"]
                #     # assert transcations.json()[1]["amount"] ==  res[0].json()["amount"] + Conf.Config.amount_decimals(send.json()['estimatedFee'],18)

        with allure.step("查询From账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders.status_code == 200

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')