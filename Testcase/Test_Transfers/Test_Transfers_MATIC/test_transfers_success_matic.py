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
        # 生产
        # ("正常转账(自己转自己)!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","Mask","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C",Conf.Config.random_amount(1)),
        # ("正常转账maximum(自己转自己)!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","Mask","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C","maximum"),
        ("正常转账!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","Mask","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C","0xc78D5E7212484B01857B702B7895e16dB442CA2e",Conf.Config.random_amount(2)),
        # ("正常转账maximum!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","Mask","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C","0xc78D5E7212484B01857B702B7895e16dB442CA2e","maximum"),
    ]

    @allure.story("Transfers_ERC20_Success!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_erc20(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        with allure.step("查询From账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders.status_code == 200

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

        with allure.step("查询From账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders.status_code == 200



# 多签账户
@allure.feature("Transfers_Success!")
class Test_transfers_success_erc20_safe:
    test_data = [
        # 生产
        # ("正常转账(自己转自己)!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","Mask","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8",Conf.Config.random_amount(6)),
        # ("正常转账maximum(自己转自己)!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","Mask","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","maximum"),
        ("正常转账!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","Mask","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","0xc78D5E7212484B01857B702B7895e16dB442CA2e",Conf.Config.random_amount(6)),
        # ("正常转账maximum!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","Mask","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","0xc78D5E7212484B01857B702B7895e16dB442CA2e","maximum"),
    ]

    @allure.story("Transfers_ERC20_Success!")
    @allure.title('多签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_erc20_safe(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        with allure.step("查询From账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders.status_code == 200

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

        with allure.step("查询From账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders.status_code == 200


# 多签账户
@allure.feature("Transfers_Success!")
class Test_transfers_success_matic_safe:
    test_data = [
        # 生产
        # ("正常转账(自己转自己)!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8",Conf.Config.random_amount(6)),
        # ("正常转账maximum(自己转自己)!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","maximum"),
        ("正常转账!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","0xc78D5E7212484B01857B702B7895e16dB442CA2e",Conf.Config.random_amount(6)),
        # ("正常转账maximum!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","0xc78D5E7212484B01857B702B7895e16dB442CA2e","maximum"),
    ]

    @allure.story("Transfers_MATIC_Success!")
    @allure.title('多签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_matic_safe(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

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

        with allure.step("查询From账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders.status_code == 200

        with allure.step("查询to账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,to_add)
            assert holders.status_code == 200


# 单签账户
@allure.feature("Transfers_Success!")
class Test_transfers_success_matic:
    test_data = [
        # 测试
        # ("正常转账(自己转自己)!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C",Conf.Config.random_amount(6)),
        # ("正常转账maximum(自己转自己)!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C","maximum"),
        ("正常转账!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C","0xc78D5E7212484B01857B702B7895e16dB442CA2e",Conf.Config.random_amount(6)),
        # ("正常转账maximum!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","0xa402336EfECc8D644CBAaA9633d7d02B7D9d585C","0xc78D5E7212484B01857B702B7895e16dB442CA2e","maximum"),
    ]

    @allure.story("Transfers_MATIC_Success!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_matic(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        with allure.step("查询From账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders.status_code == 200

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

        with allure.step("查询From账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders.status_code == 200