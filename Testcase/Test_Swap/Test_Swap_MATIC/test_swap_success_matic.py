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
@allure.feature("Swap_MATIC!")
class Test_swap_success_matic:
    test_data = [
        # 测试&生产
        ("正常Swap(USDC-USDT)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","1",Conf.Config.random_amount(3)),
        ("正常Swap(USDC-USDT)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","1",Conf.Config.random_amount(3)),
        ("正常Swap(USDT-USDC)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDT","USDC","swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","8",Conf.Config.random_amount(3)),
    ]

    @allure.story("Swap_MATIC_Success!")
    @allure.title('单签账户Swap-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,amount', test_data)
    def test_swap_matic(self,test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,amount):

        with allure.step("构建交易——transfers"):
            # transactionParams = {
            #     "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            # }
            res = Http.HttpUtils.post_instructions(networkCode,from_coin,to_coin,PublicKeys,address,slippage,amount,type)
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
            for i in range(5):
                sleep(20)
                logger.info("<----查询次数:第" + str(i+1) + "次---->")
                transfers = Http.HttpUtils.get_transactions_byid(res[8])

                tx_status = (t.get("status") for t in transfers.json()["_embedded"]["transactions"] if t.get("hash") == send.json()["hash"])

                if (tx_status == "PENDING" or tx_status == "SENT"):
                    assert transfers.json()["status"] == -1
                elif (tx_status == "SETTLED"):
                    # 第一次swap，需授权额度+Swap两笔交易
                    if (transfers.json()["status"] == -1):
                        sleep(61)
                        assert len(transfers.json()["_embedded"]["transactions"]) == 2,'授权额度交易后未正常构建Swap交易!'

                        with allure.step("授权额度成功后,再次签名Swap交易"):
                            estimatedFee = (t.get("estimatedFee") for t in transfers.json()["_embedded"]["transactions"] if t.get("hash") != send.json()["hash"])
                            hash_ = (t.get("hash") for t in transfers.json()["_embedded"]["transactions"] if t.get("hash") != send.json()["hash"])
                            id = (t.get("id") for t in transfers.json()["_embedded"]["transactions"] if t.get("hash") != send.json()["hash"])
                            networkCode = (t.get("networkCode") for t in transfers.json()["_embedded"]["transactions"] if t.get("hash") != send.json()["hash"])
                            requiredSignings = (t.get("requiredSignings") for t in transfers.json()["_embedded"]["transactions"] if t.get("hash") != send.json()["hash"])
                            serialized = (t.get("serialized") for t in transfers.json()["_embedded"]["transactions"] if t.get("hash") != send.json()["hash"])


                            signature_me = Conf.Config.sign(privatekey[0],hash)
                            signatures = [
                            {
                                "hash":hash,
                                "publickey":requiredSignings["publicKeys"][0],
                                "signature":signature_me
                            }
                        ]
                            sig = Http.HttpUtils.post_sign_transfers(estimatedFee,hash_,id,networkCode,requiredSignings,serialized,signatures)
                            assert sig.status_code == 200

                        with allure.step("广播交易——send"):
                            send = Http.HttpUtils.post_send_transfers(sig.json()["id"])
                            assert send.status_code == 200

                    else:
                        assert transfers.json()["status"] == 1
                        break
                    break
                break



# 多签账户
@allure.feature("Swap_MATIC!")
class Test_swap_success_matic_safe:
    test_data = [
        # 测试
        ("正常Swap(合约地址有matic)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","0xcb4D1bBF74F2b068Dc7d33c965c1Fdad3d7B4D43","1",Conf.Config.random_amount(2)),
        ("正常Swap(合约地址无matic)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["02ac5e97a0659d6ce59c5b10b2ace331bffa276a555ff333b09beda99bd6b9f52e","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","0xE8e140D77F9Ff1f5b4eaC5388D182ac16D80E0f2","1",Conf.Config.random_amount(2)),
        ]
    # test_data = [
    #     # 生产
    #     ("正常Swap(USDC-USDT)!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","USDC","USDT","swap","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","1",Conf.Config.random_amount(2)),
    #     ("正常Swap(USDT-USDC)!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","USDT","USDC","swap","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","1",Conf.Config.random_amount(2)),
    #     ("正常Swap(USDC-USDT滑点0)!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","USDC","USDT","swap","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","0",Conf.Config.random_amount(2)),
    #     ("正常Swap(USDT-USDC滑点10)!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","USDT","USDC","swap","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","10",Conf.Config.random_amount(2)),
    # ]

    @allure.story("Swap_MATIC_Success!")
    @allure.title('多签账户Swap-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,amount', test_data)
    def test_swap_matic_safe(self,test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,amount):

        with allure.step("构建交易——transfers"):
            # transactionParams = {
            #     "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            # }
            res = Http.HttpUtils.post_instructions(networkCode,from_coin,to_coin,PublicKeys,address,slippage,amount,type)
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
            for i in range(5):
                sleep(20)
                logger.info("<----查询次数:第" + str(i+1) + "次---->")
                transfers = Http.HttpUtils.get_transactions_byid(res[8])

                tx_status = (t.get("status") for t in transfers.json()["_embedded"]["transactions"] if t.get("hash") == send.json()["hash"])

                if (tx_status == "PENDING" or tx_status == "SENT"):
                    assert transfers.json()["status"] == -1
                elif (tx_status == "SETTLED"):
                    # 第一次swap，需授权额度+Swap两笔交易
                    if (transfers.json()["status"] == -1):
                        sleep(61)
                        assert len(transfers.json()["_embedded"]["transactions"]) == 2,'授权额度交易后未正常构建Swap交易!'

                        with allure.step("授权额度成功后,再次请求签名Swap交易!"):
                            requiredSignings = [{
                                "message":(t.get("hash") for t in transfers.json()["_embedded"]["transactions"] if t.get("hash") != send.json()["hash"]),
                                "publicKey":(t.get("publicKey") for t in transfers.json()["_embedded"]["transactions"] if t.get("hash") != send.json()["hash"])
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
                            # sig_key = Http.HttpUtils.post_sign_transfers(res[1],res[2],res[3],res[4],res[5],res[6],signatures_key)
                            estimatedFee = (t.get("estimatedFee") for t in transfers.json()["_embedded"]["transactions"] if t.get("hash") != send.json()["hash"])
                            hash_ = (t.get("hash") for t in transfers.json()["_embedded"]["transactions"] if t.get("hash") != send.json()["hash"])
                            id = (t.get("id") for t in transfers.json()["_embedded"]["transactions"] if t.get("hash") != send.json()["hash"])
                            networkCode = (t.get("networkCode") for t in transfers.json()["_embedded"]["transactions"] if t.get("hash") != send.json()["hash"])
                            requiredSignings = (t.get("requiredSignings") for t in transfers.json()["_embedded"]["transactions"] if t.get("hash") != send.json()["hash"])
                            serialized = (t.get("serialized") for t in transfers.json()["_embedded"]["transactions"] if t.get("hash") != send.json()["hash"])

                            sig_key = Http.HttpUtils.post_sign_transfers(estimatedFee,hash_,id,networkCode,requiredSignings,serialized,signatures_key)
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
                            sig = Http.HttpUtils.post_sign_transfers(estimatedFee,hash_,id,networkCode,requiredSignings,serialized,signatures)
                            assert sig.status_code == 200

                        with allure.step("广播交易——send"):
                            send = Http.HttpUtils.post_send_transfers(sig.json()["id"])
                            assert send.status_code == 200

                    elif (transfers.json()["status"] == 1):
                        break
                    break
                break
            

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')