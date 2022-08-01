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
@allure.feature("Stake_Success!")
class Test_Stake_success_iris():
    test_data = [
        # 测试
        ("正常质押!!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],"IRIS","IRIS","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u",Conf.Config.random_amount(4)),
    ]

    @allure.story("Stake_CLV_Success!")
    @allure.title('单签账户质押-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,networkCode,symbol,delegator,amount', test_data)
    def test_staking_iris(self,test_title,privatekey,networkCode,symbol,delegator,amount):

        with allure.step("查询账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,delegator)
            assert holders.status_code == 200

        with allure.step("查询账户staking信息——staking"):
            holders = Http.HttpUtils.get_staking(networkCode,symbol)
            assert holders.status_code == 200
        
        with allure.step("构建交易——staking"):
            res = Http.HttpUtils.post_staking(networkCode,symbol,delegator,amount)
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
            sleep(30)
            transcations = Http.HttpUtils.get_transactions_byhash(send.json()["hash"])
            assert transcations.status_code == 200

        with allure.step("查询账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,delegator)
            assert holders.status_code == 200

        with allure.step("查询账户staking信息——staking"):
            holders = Http.HttpUtils.get_staking(networkCode,symbol)
            assert holders.status_code == 200


# 多签账户
@allure.feature("Stake_Success!")
class Test_Stake_success_iris():
    test_data = [
        # 测试
        ("正常质押!!",["49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85"],"IRIS","IRIS","iaa16gtpwuqg9lerp0n39wj4xgmwyawt69p5gq9h8p",Conf.Config.random_amount(4)),
    ]

    @allure.story("Stake_CLV_Success!")
    @allure.title('多签账户质押-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,networkCode,symbol,delegator,amount', test_data)
    def test_staking_iris(self,test_title,privatekey,networkCode,symbol,delegator,amount):

        with allure.step("查询账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,delegator)
            assert holders.status_code == 200

        with allure.step("查询账户staking信息——staking"):
            holders = Http.HttpUtils.get_staking(networkCode,symbol)
            assert holders.status_code == 200
        
        with allure.step("构建交易——staking"):
            res = Http.HttpUtils.post_staking(networkCode,symbol,delegator,amount)
            assert res[0].status_code == 200

            signature = Conf.Config.sign(privatekey[0],res[5][0]['hash'])
            signatures = [
                {
                    "hash":res[5][0]['hash'],
                    "publickey":res[5][0]['publicKeys'][1],
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

        with allure.step("查询关联交易记录——balance-transactions by hash"):
            sleep(30)
            transcations = Http.HttpUtils.get_transactions_byhash(send.json()["hash"])
            assert transcations.status_code == 200

        with allure.step("查询账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,delegator)
            assert holders.status_code == 200

        with allure.step("查询账户staking信息——staking"):
            holders = Http.HttpUtils.get_staking(networkCode,symbol)
            assert holders.status_code == 200