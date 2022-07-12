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
class Test_transfers_success_erc20:
    test_data = [
        # 测试
        ("正常转账(自己转自己)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",Conf.Config.random_amount(1)),
        ("正常转账maximum(自己转自己)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","maximum"),
        ("正常转账!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",Conf.Config.random_amount(2)),
        ("正常转账maximum!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be","maximum"),
    ]

    @allure.story("Transfers_ERC20_Success!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_erc20(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        with allure.step("构建交易——transfers"):
            # transactionParams = {
            #     "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            # }
            res = Http.HttpUtils.post_transfers(networkCode,symbol,PublicKeys,from_add,to_add,amount)
            assert res[0].status_code == 200

        with allure.step("签名交易——sign"):
            signature = Conf.Config.sign(privatekey[0],res[5][0]['hash'])
            signatures = [
                {
                    "hash":res[5][0]['hash'],
                    "publickey":res[5][0]['publicKeys'][0],
                    "signature":signature
                }
            ]
            sig = Http.HttpUtils.post_sign_transfers(res[1],res[2],res[3],res[4],res[5],res[6],signatures)
            assert sig.status_code == 200

        with allure.step("广播交易——send"):
            send = Http.HttpUtils.post_send_transfers(res[3])
            assert send.status_code == 200

        with allure.step("查询交易记录——transfers by id,交易状态变为:1"):
            # 循环查10次交易记录
            for i in range(1):
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
   
            if (from_add == to_add):
                assert len(transcations.json()) == 3 # 自己转自己3条交易记录
            else:
                assert len(transcations.json()) == 4 # 转其他地址4条交易记录

# 多签账户
@allure.feature("Transfers_Success!")
class Test_transfers_success_erc20_safe:
    test_data = [
        # 测试
        # ("正常转账(自己转自己)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3",Conf.Config.random_amount(6)),
        # ("正常转账maximum(自己转自己)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","maximum"),
        # ("正常转账!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",Conf.Config.random_amount(6)),
        ("正常转账maximum!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be","maximum"),
    ]

    @allure.story("Transfers_ERC20_Success!")
    @allure.title('多签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_erc20_safe(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        with allure.step("构建交易——transfers"):
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            res = Http.HttpUtils.post_transfers(networkCode,symbol,PublicKeys,from_add,to_add,amount,transactionParams)
            assert res[0].status_code == 200

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

        with allure.step("托管key签名交易——sign"):
            signatures_key = [
            {
                "hash":confirmsign.json()[0]["message"],
                "publickey":confirmsign.json()[0]["publicKey"],
                "signature":confirmsign.json()[0]["signature"]
            }
        ]
            sig_key = Http.HttpUtils.post_sign_transfers(res[1],res[2],res[3],res[4],res[5],res[6],signatures_key)
            assert sig_key.status_code == 200

        with allure.step("签名交易——sign"):
            signature_me = Conf.Config.sign(privatekey[0],sig_key.json()["requiredSignings"][0]["hash"])
            signatures = [
            {
                "hash":sig_key.json()["requiredSignings"][0]["hash"],
                "publickey":sig_key.json()["requiredSignings"][0]["publicKeys"][0],
                "signature":signature_me
            }
        ]
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
                assert len(transcations.json()) == 3 
            else:
                assert len(transcations.json()) == 4


# 单签账户
@allure.feature("Transfers_Success!")
class Test_transfers_success_eth:
    test_data = [
        # 测试
        # ("正常转账(自己转自己)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",Conf.Config.random_amount(6)),
        # ("正常转账maximum(自己转自己)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","maximum"),
        # ("正常转账!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",Conf.Config.random_amount(6)),
        ("正常转账maximum!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be","maximum"),
    ]

    @allure.story("Transfers_ETH_Success!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_eth(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        with allure.step("构建交易——transfers"):
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            res = Http.HttpUtils.post_transfers(networkCode,symbol,PublicKeys,from_add,to_add,amount,transactionParams)
            assert res[0].status_code == 200

        with allure.step("签名交易——sign"):
            signature = Conf.Config.sign(privatekey[0],res[5][0]['hash'])
            signatures = [
                {
                    "hash":res[5][0]['hash'],
                    "publickey":res[5][0]['publicKeys'][0],
                    "signature":signature
                }
            ]
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
                assert transcations.json()[0]["type"] == -1 # type 是 -1
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

# 多签账户
@allure.feature("Transfers_Success!")
class Test_transfers_success_eth_safe:
    test_data = [
        # 测试
        ("正常转账(自己转自己)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3",Conf.Config.random_amount(6)),
        ("正常转账maximum(自己转自己)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","maximum"),
        ("正常转账!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",Conf.Config.random_amount(6)),
        ("正常转账maximum!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be","maximum"),
    ]

    @allure.story("Transfers_ETH_Success!")
    @allure.title('多签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_eth_safe(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        with allure.step("构建交易——transfers"):
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            res = Http.HttpUtils.post_transfers(networkCode,symbol,PublicKeys,from_add,to_add,amount,transactionParams)
            assert res[0].status_code == 200

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

        with allure.step("托管key签名交易——sign"):
            signatures_key = [
            {
                "hash":confirmsign.json()[0]["message"],
                "publickey":confirmsign.json()[0]["publicKey"],
                "signature":confirmsign.json()[0]["signature"]
            }
        ]
            sig_key = Http.HttpUtils.post_sign_transfers(res[1],res[2],res[3],res[4],res[5],res[6],signatures_key)
            assert sig_key.status_code == 200

        with allure.step("签名交易——sign"):
            signature_me = Conf.Config.sign(privatekey[0],sig_key.json()["requiredSignings"][0]["hash"])
            signatures = [
            {
                "hash":sig_key.json()["requiredSignings"][0]["hash"],
                "publickey":sig_key.json()["requiredSignings"][0]["publicKeys"][0],
                "signature":signature_me
            }
        ]
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
                assert len(transcations.json()) == 2
            else:
                assert len(transcations.json()) == 3