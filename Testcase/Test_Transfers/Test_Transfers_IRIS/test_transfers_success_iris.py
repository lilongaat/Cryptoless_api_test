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
class Test_transfers_success_iris:
    test_data = [
        # 测试
        ("正常转账(自己转自己)!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],["033511e38fd373c4515ada4826616146b4c3def47da9907b59d9555b19134dd683"],"IRIS","IRIS","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u",Conf.Config.random_amount(4)),
        ("正常转账maximum(自己转自己)!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],["033511e38fd373c4515ada4826616146b4c3def47da9907b59d9555b19134dd683"],"IRIS","IRIS","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u","maximum"),
        ("正常转账!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],["033511e38fd373c4515ada4826616146b4c3def47da9907b59d9555b19134dd683"],"IRIS","IRIS","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u","iaa1jlsefxjczxg23gldzt4qcuxhddgeu4757f2pmq",Conf.Config.random_amount(4)),
        ("正常转账maximum!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],["033511e38fd373c4515ada4826616146b4c3def47da9907b59d9555b19134dd683"],"IRIS","IRIS","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u","iaa1jlsefxjczxg23gldzt4qcuxhddgeu4757f2pmq","maximum"),
    ]
    # test_data = [
    #     # 生产
    #     ("正常转账(自己转自己)!",["973edd16fb9e4e01411a664ca771eee68314fa473d7e8a09c7e9c2c5e72384b5"],["029c9777b2ab9abff95d50011d476035ab80fef3b2962090fd04c5ea04157ccc87"],"IRIS","IRIS","iaa1j7p7j0kwceedzw6ra8jwtz9gn08h2sqzgp4ql7","iaa1j7p7j0kwceedzw6ra8jwtz9gn08h2sqzgp4ql7",Conf.Config.random_amount(4)),
    #     ("正常转账maximum(自己转自己)!",["973edd16fb9e4e01411a664ca771eee68314fa473d7e8a09c7e9c2c5e72384b5"],["029c9777b2ab9abff95d50011d476035ab80fef3b2962090fd04c5ea04157ccc87"],"IRIS","IRIS","iaa1j7p7j0kwceedzw6ra8jwtz9gn08h2sqzgp4ql7","iaa1j7p7j0kwceedzw6ra8jwtz9gn08h2sqzgp4ql7","maximum"),
    #     ("正常转账!",["973edd16fb9e4e01411a664ca771eee68314fa473d7e8a09c7e9c2c5e72384b5"],["029c9777b2ab9abff95d50011d476035ab80fef3b2962090fd04c5ea04157ccc87"],"IRIS","IRIS","iaa1j7p7j0kwceedzw6ra8jwtz9gn08h2sqzgp4ql7","iaa1qfx3a0rg6gufrf9n44et8cdjwwnx8zjf4wpp9a",Conf.Config.random_amount(4)),
    #     ("正常转账maximum!",["973edd16fb9e4e01411a664ca771eee68314fa473d7e8a09c7e9c2c5e72384b5"],["029c9777b2ab9abff95d50011d476035ab80fef3b2962090fd04c5ea04157ccc87"],"IRIS","IRIS","iaa1j7p7j0kwceedzw6ra8jwtz9gn08h2sqzgp4ql7","iaa1qfx3a0rg6gufrf9n44et8cdjwwnx8zjf4wpp9a","maximum"),
    # ]

    @allure.story("Transfers_IRIS_Success!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_iris(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        with allure.step("查询From账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders.status_code == 200

        with allure.step("构建交易——transfers"):
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            res = Http.HttpUtils.post_transfers(networkCode,symbol,PublicKeys,from_add,to_add,amount)
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
                elif (transfers.json()["_embedded"]["transactions"][0]["status"] == "FAILED"):
                    assert transfers.json()["status"] == 0
                    raise Exception("交易失败！")
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
                # assert transcations.json()[0]["amount"] ==  res[0].json()["amount"] + Conf.Config.amount_decimals(send.json()['estimatedFee'],6)
            else:
                assert len(transcations.json()) == 2
                # if(transcations.json()[0]["type"] == -1): # 判断第一个交易为转出地址
                #     assert transcations.json()[0]["address"] == res[0].json()["from"]
                #     # assert transcations.json()[0]["amount"] ==  res[0].json()["amount"] + Conf.Config.amount_decimals(send.json()['estimatedFee'],6)

                #     assert transcations.json()[1]["address"] == res[0].json()["to"]
                #     assert transcations.json()[1]["amount"] ==  res[0].json()["amount"]

                # else:
                #     assert transcations.json()[0]["address"] == res[0].json()["to"]
                #     assert transcations.json()[0]["amount"] ==  res[0].json()["amount"]

                #     assert transcations.json()[1]["address"] == res[0].json()["from"]
                #     assert transcations.json()[1]["amount"] ==  res[0].json()["amount"] + Conf.Config.amount_decimals(send.json()['estimatedFee'],6)

        with allure.step("查询From账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders.status_code == 200



# 多签账户
@allure.feature("Transfers_Success!")
class Test_transfers_success_iris_safe:
    test_data = [
        # 测试
        ("正常转账(自己转自己)!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],["026c37fcad8790e5a2b2e82e788fe36b68c0cfb9dc040b471a8a72f86a84d5fe18","033511e38fd373c4515ada4826616146b4c3def47da9907b59d9555b19134dd683"],"IRIS","IRIS","iaa16gtpwuqg9lerp0n39wj4xgmwyawt69p5gq9h8p","iaa16gtpwuqg9lerp0n39wj4xgmwyawt69p5gq9h8p",Conf.Config.random_amount(4)),
        # ("正常转账maximum(自己转自己)!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],["026c37fcad8790e5a2b2e82e788fe36b68c0cfb9dc040b471a8a72f86a84d5fe18","033511e38fd373c4515ada4826616146b4c3def47da9907b59d9555b19134dd683"],"IRIS","IRIS","iaa16gtpwuqg9lerp0n39wj4xgmwyawt69p5gq9h8p","iaa16gtpwuqg9lerp0n39wj4xgmwyawt69p5gq9h8p","maximum"),
        # ("正常转账!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],["026c37fcad8790e5a2b2e82e788fe36b68c0cfb9dc040b471a8a72f86a84d5fe18","033511e38fd373c4515ada4826616146b4c3def47da9907b59d9555b19134dd683"],"IRIS","IRIS","iaa16gtpwuqg9lerp0n39wj4xgmwyawt69p5gq9h8p","iaa1jlsefxjczxg23gldzt4qcuxhddgeu4757f2pmq",Conf.Config.random_amount(4)),
        # ("正常转账maximum!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],["026c37fcad8790e5a2b2e82e788fe36b68c0cfb9dc040b471a8a72f86a84d5fe18","033511e38fd373c4515ada4826616146b4c3def47da9907b59d9555b19134dd683"],"IRIS","IRIS","iaa16gtpwuqg9lerp0n39wj4xgmwyawt69p5gq9h8p","iaa1jlsefxjczxg23gldzt4qcuxhddgeu4757f2pmq","maximum"),
    ]
    # test_data = [
    #     # 生产
    #     ("正常转账(自己转自己)!",["973edd16fb9e4e01411a664ca771eee68314fa473d7e8a09c7e9c2c5e72384b5"],["026c37fcad8790e5a2b2e82e788fe36b68c0cfb9dc040b471a8a72f86a84d5fe18","029c9777b2ab9abff95d50011d476035ab80fef3b2962090fd04c5ea04157ccc87"],"IRIS","IRIS","iaa142rymfv9rc8x3npaahshpw09kdr470lq7vg7d7","iaa142rymfv9rc8x3npaahshpw09kdr470lq7vg7d7",Conf.Config.random_amount(4)),
    #     ("正常转账maximum(自己转自己)!",["973edd16fb9e4e01411a664ca771eee68314fa473d7e8a09c7e9c2c5e72384b5"],["026c37fcad8790e5a2b2e82e788fe36b68c0cfb9dc040b471a8a72f86a84d5fe18","029c9777b2ab9abff95d50011d476035ab80fef3b2962090fd04c5ea04157ccc87"],"IRIS","IRIS","iaa142rymfv9rc8x3npaahshpw09kdr470lq7vg7d7","iaa142rymfv9rc8x3npaahshpw09kdr470lq7vg7d7","maximum"),
    #     ("正常转账!",["973edd16fb9e4e01411a664ca771eee68314fa473d7e8a09c7e9c2c5e72384b5"],["026c37fcad8790e5a2b2e82e788fe36b68c0cfb9dc040b471a8a72f86a84d5fe18","029c9777b2ab9abff95d50011d476035ab80fef3b2962090fd04c5ea04157ccc87"],"IRIS","IRIS","iaa142rymfv9rc8x3npaahshpw09kdr470lq7vg7d7","iaa1qfx3a0rg6gufrf9n44et8cdjwwnx8zjf4wpp9a",Conf.Config.random_amount(4)),
    #     ("正常转账maximum!",["973edd16fb9e4e01411a664ca771eee68314fa473d7e8a09c7e9c2c5e72384b5"],["026c37fcad8790e5a2b2e82e788fe36b68c0cfb9dc040b471a8a72f86a84d5fe18","029c9777b2ab9abff95d50011d476035ab80fef3b2962090fd04c5ea04157ccc87"],"IRIS","IRIS","iaa142rymfv9rc8x3npaahshpw09kdr470lq7vg7d7","iaa1qfx3a0rg6gufrf9n44et8cdjwwnx8zjf4wpp9a","maximum"),
    # ]

    @allure.story("Transfers_IRIS_Success!")
    @allure.title('多签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_iris_safe(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

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
                    "publickey":PublicKeys[1],
                    "signature":signature
                }
            ]

        with allure.step("请求签名交易——req_sign"):
            requiredSignings = [{
                "message":res[5][0]['hash'],
                "publicKey":res[5][0]['publicKeys'][0]
                }]
            reqsign = Http.HttpUtils.post_req_sign(requiredSignings)
            assert reqsign.status_code == 200

        with allure.step("获取验证码——verify"):
            reqverify = Http.HttpUtils.post_req_Verify(reqsign.json()["id"])
            assert reqverify.status_code == 200
        
        with allure.step("托管key提交签名——confirm-sign"):
            confirmsign = Http.HttpUtils.post_confirm_sign(reqsign.json()["id"],"000000")
            assert confirmsign.status_code == 200

            signatures.append({
                "hash":confirmsign.json()[0]["message"],
                "publickey":confirmsign.json()[0]["publicKey"],
                "signature":confirmsign.json()[0]["signature"]
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
                assert len(transcations.json()) == 1
            else:
                assert len(transcations.json()) == 2

        with allure.step("查询From账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders.status_code == 200


if __name__ == '__main__':
    path = os.path.abspath(__file__) + "::Test_transfers_success_iris_safe"
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')