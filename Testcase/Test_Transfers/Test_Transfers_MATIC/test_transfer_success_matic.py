import json
import random
import decimal
from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Conf
from Common.Loguru import logger

# 多签账户转账MATIC 构建交易publickey不传/传一个/传两个
@allure.feature("Transfers_Success!")
class Test_transfers_success_matic_safe_pub:
    test_data = [
        # 生产
        ("publickey不传[]!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],[],"MATIC","MATIC","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","0xc78D5E7212484B01857B702B7895e16dB442CA2e",round(random.uniform(0.00001,0.001), random.randint(5,18))),
        ("publickey传一个[k1(托管)]!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","0xc78D5E7212484B01857B702B7895e16dB442CA2e",round(random.uniform(0.00001,0.001), random.randint(5,18))),
        ("publickey传两个[k1(托管),k2(私有)]!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","0xc78D5E7212484B01857B702B7895e16dB442CA2e",round(random.uniform(0.00001,0.001), random.randint(5,18))),
    ]

    @allure.story("Transfers_MATIC_Success!")
    @allure.title('多签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_matic_safe(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        # with allure.step("查询From账户holders信息——holders"):
        #     holders_before = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
        #     assert holders_before.status_code == 200
        #     quantity_before = holders_before.json()[0]['quantity']

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_add,
                "to":to_add,
                "symbol":symbol,
                "amount":amount
            }
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            transfer = Http.HttpUtils.post_instructions("Transfer",body,networkCode,PublicKeys,transactionParams)
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

        with allure.step("请求签名交易——req_sign"):
            requiredSignings = [{
                "message":t_requiredSignings[0]['hash'],
                "publicKey":t_requiredSignings[0]['publicKeys'][0]
                }]
            reqsign = Http.HttpUtils.post_req_sign(requiredSignings)
            assert reqsign.status_code == 200

        with allure.step("获取验证码——verify"):
            reqverify = Http.HttpUtils.post_req_Verify(reqsign.json()["id"])
            assert reqverify.status_code == 200
        
        with allure.step("托管key提交签名——confirm-sign"):
            confirmsign = Http.HttpUtils.post_confirm_sign(reqsign.json()["id"],"000000")
            assert confirmsign.status_code == 200
            signatures = [{
                "hash":confirmsign.json()[0]["message"],
                "publickey":confirmsign.json()[0]["publicKey"],
                "signature":confirmsign.json()[0]["signature"]
            }]

        with allure.step("托管key签名交易——sign"):
            sig_agent = Http.HttpUtils.post_sign_transfers(t_estimatedFee,t_hash,t_id,t_networkCode,t_requiredSignings,t_serialized,signatures)
            assert sig_agent.status_code == 200

            s_estimatedFee = sig_agent.json()['estimatedFee']
            s_hash = sig_agent.json()['hash']
            s_id = sig_agent.json()['id']
            s_networkCode = sig_agent.json()['networkCode']
            s_requiredSignings = sig_agent.json()['requiredSignings']
            s_serialized = sig_agent.json()['serialized']
            s_status = sig_agent.json()['status']

        with allure.step("私有key签名交易——sign"):
            signature_me = Conf.Config.sign(privatekey[0],s_requiredSignings[0]['hash'])
            signatures_me = {
                "hash":s_requiredSignings[0]['hash'],
                "publickey":s_requiredSignings[0]['publicKeys'][0],
                "signature":signature_me
            }
            sig_me = Http.HttpUtils.post_sign_transfers(s_estimatedFee,s_hash,s_id,s_networkCode,s_requiredSignings,s_serialized,signatures_me)
            assert sig_me.status_code == 200

        with allure.step("广播交易——send"):
            send = Http.HttpUtils.post_send_transfers(sig_me.json()['id'])
            assert send.status_code == 200

        with allure.step("查询交易记录——transfers by ID,交易状态变为:1"):
            # 循环查10次交易记录
            for i in range(10):
                sleep(20)
                logger.info("<----查询次数:第" + str(i+1) + "次---->")
                t = Http.HttpUtils.get_transactions_byid(ID)
                t_status = t.json()["_embedded"]["transactions"][0]["status"] #交易状态
                if (t_status == "PENDING" or t_status == "SENT"):
                    assert t.json()["status"] == -1
                elif (t_status == "SETTLED"):
                    assert t.json()["status"] == 1
                    break  

        with allure.step("查询关联交易记录——balance-transactions by hash"):
            sleep(15)
            transcations = Http.HttpUtils.get_transactions_byhash(send.json()["hash"])
            assert transcations.status_code == 200

            
            if (from_add == to_add):
                assert len(transcations.json()) == 2 
            else:
                assert len(transcations.json()) == 3

        # with allure.step("查询From账户holders信息——holders"):
        #     holders_after = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
        #     assert holders_after.status_code == 200
        #     quantity_after = holders_after.json()[0]['quantity']

        # with allure.step("断言holders转出金额"):
        #     assert decimal.Decimal(body_amount) == decimal.Decimal(quantity_before) - decimal.Decimal(quantity_after)


# 多签账户转账MATIC 构建交易publickey传三个,sender是代理key
@allure.feature("Transfers_Success!")
class Test_transfers_success_matic_safe_pub3_agentsender:
    test_data = [
        # 测试
        ("自己转自己publickey[k1(托管),k2(私有),k2(私有)]!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","MATIC","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8",round(random.uniform(0.00001,0.1), random.randint(5,18))),
        ("自己转自己maximum[k2(私有),k1(托管),k2(私有)]!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","maximum"),
        ("publickey[k1(托管),k2(私有),k2(私有)]",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","MATIC","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(0.00001,0.1), random.randint(5,18)))
    ]

    @allure.story("Transfers_MATIC_Success!")
    @allure.title('多签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_matic_safe(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        with allure.step("查询From账户holders信息——holders"):
            holders_before = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders_before.status_code == 200
            quantity_before = holders_before.json()[0]['quantity']

        with allure.step("查询账户托管key和私有key"):
            key_act  = Http.HttpUtils.get_keys()
            assert key_act.status_code == 200
            # PublicKey_act 托管key
            # PublicKey 私有key
            if PublicKeys[0] in key_act.text:
                PublicKey_act = PublicKeys[0]
                PublicKey = PublicKeys[1]
            else:
                PublicKey_act = PublicKeys[1]
                PublicKey = PublicKeys[0]
                
        with allure.step("查询系统代理key"):
            pub_agent = Http.HttpUtils.get_safe_agents()
            assert pub_agent.status_code == 200
            PublicKeys.append([k.get('agentPublicKey') for k in pub_agent.json() if k.get('networkCode') == networkCode][0])

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_add,
                "to":to_add,
                "symbol":symbol,
                "amount":amount
            }
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            transfer = Http.HttpUtils.post_instructions("Transfer",body,networkCode,PublicKeys,transactionParams)
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

        with allure.step("请求签名交易——req_sign"):
            requiredSignings = [{
                "message":t_requiredSignings[0]['hash'],
                "publicKey":PublicKey_act
                }]
            reqsign = Http.HttpUtils.post_req_sign(requiredSignings)
            assert reqsign.status_code == 200

        with allure.step("获取验证码——verify"):
            reqverify = Http.HttpUtils.post_req_Verify(reqsign.json()["id"])
            assert reqverify.status_code == 200
        
        with allure.step("托管key提交签名——confirm-sign"):
            confirmsign = Http.HttpUtils.post_confirm_sign(reqsign.json()["id"],"000000")
            assert confirmsign.status_code == 200
            signatures = [{
                "hash":confirmsign.json()[0]["message"],
                "publickey":confirmsign.json()[0]["publicKey"],
                "signature":confirmsign.json()[0]["signature"]
            }]

        with allure.step("签名交易——sign"):
            signature_me = Conf.Config.sign(privatekey[0],t_requiredSignings[0]['hash'])
            signatures.append({
                "hash":t_requiredSignings[0]['hash'],
                "publickey":PublicKey,
                "signature":signature_me
            })
            sig = Http.HttpUtils.post_sign_transfers(t_estimatedFee,t_hash,t_id,t_networkCode,t_requiredSignings,t_serialized,signatures)
            assert sig.status_code == 200

        with allure.step("请求代理签名"):
            qsig_agent = Http.HttpUtils.post_safe_agents_sign(networkCode,sig.json()['requiredSignings'][0]['hash'])
            assert qsig_agent.status_code == 200
            signatures_agent = qsig_agent.json()

        with allure.step("代理签名交易"):
            sig_agent = Http.HttpUtils.post_sign_transfers(
                sig.json()['estimatedFee'],
                sig.json()['hash'],
                sig.json()['id'],
                sig.json()['networkCode'],
                sig.json()['requiredSignings'],
                sig.json()['serialized'],
                signatures_agent
                )

        with allure.step("广播交易——send"):
            send = Http.HttpUtils.post_send_transfers(t_id)
            assert send.status_code == 200

        with allure.step("查询交易记录——transfers by ID,交易状态变为:1"):
            # 循环查10次交易记录
            for i in range(10):
                sleep(20)
                logger.info("<----查询次数:第" + str(i+1) + "次---->")
                t = Http.HttpUtils.get_transactions_byid(ID)
                t_status = t.json()["_embedded"]["transactions"][0]["status"] #交易状态
                if (t_status == "PENDING" or t_status == "SENT"):
                    assert t.json()["status"] == -1
                elif (t_status == "SETTLED"):
                    assert t.json()["status"] == 1
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
            holders_after = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders_after.status_code == 200
            quantity_after = holders_after.json()[0]["quantity"]

        with allure.step("断言holders转出金额"):
            if from_add == to_add:
                assert quantity_before == quantity_after
            else:
                assert decimal.Decimal(body_amount) == decimal.Decimal(quantity_before) - decimal.Decimal(quantity_after)


# 多签账户转账MATIC 构建交易publickey传三个,sender是账户key
@allure.feature("Transfers_Success!")
class Test_transfers_success_matic_safe_pub3_mesender:
    test_data = [
        # 测试
        ("自己转自己publickey[k1(托管),k2(私有),k2(私有)]!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","MATIC","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8",round(random.uniform(0.00001,0.001), random.randint(5,18))),
        ("自己转自己maximum[k2(私有),k1(托管),k2(私有)]!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","maximum"),
        ("publickey[k1(托管),k2(私有),k2(私有)]",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","MATIC","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(0.00001,0.001), random.randint(5,18))),
        ("maximum publickey[k2(私有),k1(托管),k2(私有)]!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","MATIC","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be","maximum"),
    ]

    @allure.story("Transfers_MATIC_Success!")
    @allure.title('多签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_matic_safe(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        with allure.step("查询From账户holders信息——holders"):
            holders_before = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders_before.status_code == 200
            quantity_before = holders_before.json()[0]['quantity']

        with allure.step("查询账户托管key"):
            key_act  = Http.HttpUtils.get_keys()
            assert key_act.status_code == 200
            if PublicKeys[0] in key_act.text:
                PublicKey_act = PublicKeys[0]
                PublicKey = PublicKeys[1]
            else:
                PublicKey_act = PublicKeys[1]
                PublicKey = PublicKeys[0]
            PublicKeys.append(PublicKey)

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_add,
                "to":to_add,
                "symbol":symbol,
                "amount":amount
            }
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            transfer = Http.HttpUtils.post_instructions("Transfer",body,networkCode,PublicKeys,transactionParams)
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

        with allure.step("请求签名交易——req_sign"):
            requiredSignings = [{
                "message":t_requiredSignings[0]['hash'],
                "publicKey":PublicKey_act
                }]
            reqsign = Http.HttpUtils.post_req_sign(requiredSignings)
            assert reqsign.status_code == 200

        with allure.step("获取验证码——verify"):
            reqverify = Http.HttpUtils.post_req_Verify(reqsign.json()["id"])
            assert reqverify.status_code == 200
        
        with allure.step("托管key提交签名——confirm-sign"):
            confirmsign = Http.HttpUtils.post_confirm_sign(reqsign.json()["id"],"000000")
            assert confirmsign.status_code == 200
            signatures = [{
                "hash":confirmsign.json()[0]["message"],
                "publickey":confirmsign.json()[0]["publicKey"],
                "signature":confirmsign.json()[0]["signature"]
            }]

        with allure.step("签名交易——sign"):
            signature_me = Conf.Config.sign(privatekey[0],t_requiredSignings[0]['hash'])
            signatures.append({
                "hash":t_requiredSignings[0]['hash'],
                "publickey":PublicKey,
                "signature":signature_me
            })
            sig = Http.HttpUtils.post_sign_transfers(t_estimatedFee,t_hash,t_id,t_networkCode,t_requiredSignings,t_serialized,signatures)
            assert sig.status_code == 200

        with allure.step("sender签名交易——sign"):
            signature_sender = Conf.Config.sign(privatekey[0],sig.json()['requiredSignings'][0]['hash'])
            signatures_ = [{
                "hash":sig.json()['requiredSignings'][0]['hash'],
                "publickey":sig.json()['requiredSignings'][0]['publicKeys'][0],
                "signature":signature_sender
            }]
            sig_me = Http.HttpUtils.post_sign_transfers(t_estimatedFee,t_hash,t_id,t_networkCode,t_requiredSignings,t_serialized,signatures_)
            assert sig_me.status_code == 200

        with allure.step("广播交易——send"):
            send = Http.HttpUtils.post_send_transfers(t_id)
            assert send.status_code == 200

        with allure.step("查询交易记录——transfers by ID,交易状态变为:1"):
            # 循环查10次交易记录
            for i in range(10):
                sleep(20)
                logger.info("<----查询次数:第" + str(i+1) + "次---->")
                t = Http.HttpUtils.get_transactions_byid(ID)
                t_status = t.json()["_embedded"]["transactions"][0]["status"] #交易状态
                if (t_status == "PENDING" or t_status == "SENT"):
                    assert t.json()["status"] == -1
                elif (t_status == "SETTLED"):
                    assert t.json()["status"] == 1
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
            holders_after = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders_after.status_code == 200
            quantity_after = holders_after.json()[0]["quantity"]

        with allure.step("断言holders转出金额"):
            if from_add == to_add:
                assert quantity_before == quantity_after
            else:
                assert decimal.Decimal(body_amount) == decimal.Decimal(quantity_before) - decimal.Decimal(quantity_after)


# 单签账户转账MATIC
@allure.feature("Transfers_Success!")
class Test_transfers_success_matic:
    test_data = [
        # 测试
        # ("自己转自己!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","MATIC","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",round(random.uniform(0.00001,0.001), random.randint(5,18))),
        # ("自己转自己maximum!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","MATIC","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","maximum"),
        ("正常转账!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","MATIC","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(0.00001,0.001), random.randint(5,18))),
        # ("正常转账maximum!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","MATIC","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be","maximum"),
    ]

    @allure.story("Transfers_MATIC_Success!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_matic(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        with allure.step("查询From账户holders信息——holders"):
            holders_before = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders_before.status_code == 200
            quantity_before = holders_before.json()[0]['quantity']

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_add,
                "to":to_add,
                "symbol":symbol,
                "amount":amount
            }
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            transfer = Http.HttpUtils.post_instructions("Transfer",body,networkCode,PublicKeys,transactionParams)
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

        with allure.step("签名交易——sign"):
            signature = Conf.Config.sign(privatekey[0],t_requiredSignings[0]['hash'])
            signatures = [
                {
                    "hash":t_requiredSignings[0]['hash'],
                    "publickey":t_requiredSignings[0]['publicKeys'][0],
                    "signature":signature
                }
            ]
            sig = Http.HttpUtils.post_sign_transfers(t_estimatedFee,t_hash,t_id,t_networkCode,t_requiredSignings,t_serialized,signatures)
            assert sig.status_code == 200

        with allure.step("广播交易——send"):
            send = Http.HttpUtils.post_send_transfers(t_id)
            assert send.status_code == 200

        with allure.step("查询交易记录——transfers by ID,交易状态变为:1"):
            # 循环查10次交易记录
            for i in range(1):
                sleep(20)
                logger.info("<----查询次数:第" + str(i+1) + "次---->")
                t = Http.HttpUtils.get_transactions_byid(ID)
                t_status = t.json()["_embedded"]["transactions"][0]["status"] #交易状态
                if (t_status == "PENDING" or t_status == "SENT"):
                    assert t.json()["status"] == -1
                elif (t_status == "SETTLED"):
                    assert t.json()["status"] == 1
                    break             

        with allure.step("查询关联交易记录——balance-transactions by hash"):
            sleep(15)
            transcations = Http.HttpUtils.get_transactions_byhash(send.json()["hash"])
   
            if (from_add == to_add):
                assert len(transcations.json()) == 3 # 自己转自己3条交易记录
            else:
                assert len(transcations.json()) == 4 # 转其他地址4条交易记录

        with allure.step("查询From账户holders信息——holders"):
            holders_after = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders_after.status_code == 200
            quantity_after = holders_after.json()[0]['quantity']

        with allure.step("断言holders转出金额"):
            if from_add == to_add:
                assert quantity_before == quantity_after
            else:
                assert decimal.Decimal(body_amount) == decimal.Decimal(quantity_before) - decimal.Decimal(quantity_after)



if __name__ == '__main__':
    path = os.path.abspath(__file__) + "::Test_transfers_success_matic_safe_pub"
    pytest.main(["-vs", path,'--clean-alluredir','--alluredir=Report/Allure'])
    os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')