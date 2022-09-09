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

#### 多签账户(2-2)

## 老账户Swap

#  Swap PublicKeys不传/传一个/传两个
@allure.feature("Swap_MATIC!")
class Test_swap_success_matic_safe_pub:
    test_data = [
        # 测试
        ("USDT->USDC(PublicKeys不传)[]!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],[],"MATIC","USDT","USDC","swap","0xcb4D1bBF74F2b068Dc7d33c965c1Fdad3d7B4D43","10",'0.001'),
        ("USDT->USDC(PublicKeys不传)[]!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],[],"MATIC","USDT","USDC","swap","0xcb4D1bBF74F2b068Dc7d33c965c1Fdad3d7B4D43","10",'0.001'),
        ("USDC->USDT(PublicKeys传一个)[k1(托管)]!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228"],"MATIC","USDC","USDT","swap","0xcb4D1bBF74F2b068Dc7d33c965c1Fdad3d7B4D43","10",'0.01'),
        ("USDC->USDT(PublicKeys传两个)[k1(托管),k2(私有)]!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","0xcb4D1bBF74F2b068Dc7d33c965c1Fdad3d7B4D43","10",'0.01'),
        ]
    # test_data = [
    #     # 测试
    #     ("USDT->USDC(PublicKeys不传)[]!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],[],"MATIC","USDT","USDC","swap","0xcb4D1bBF74F2b068Dc7d33c965c1Fdad3d7B4D43","1",round(random.uniform(0.0001,0.001), random.randint(4,6))),
    #     ("USDC->USDT(PublicKeys传一个)[k1(托管)]!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228"],"MATIC","USDT","USDC","swap","0xcb4D1bBF74F2b068Dc7d33c965c1Fdad3d7B4D43","1",round(random.uniform(0.0001,0.001), random.randint(4,6))),
    #     ("USDC->USDT(PublicKeys传两个)[k1(托管),k2(私有)]!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDT","USDC","swap","0xcb4D1bBF74F2b068Dc7d33c965c1Fdad3d7B4D43","1",round(random.uniform(0.0001,0.001), random.randint(4,6))),
    #     ]

    @allure.story("Swap_MATIC_Success!")
    @allure.title('多签账户(2-2)Swap-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,fromAmount', test_data)
    def test_swap_matic_safe(self,test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,fromAmount):

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_coin,
                "to":to_coin,
                "address":address,
                "fromAmount":fromAmount,
                "slippage":slippage
            }
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            transfer = Http.HttpUtils.post_instructions(type,body,networkCode,PublicKeys,transactionParams)
            assert transfer.status_code == 200

            t_estimatedFee = transfer.json()['_embedded']['transactions'][0]['estimatedFee']
            t_hash = transfer.json()['_embedded']['transactions'][0]['hash']
            t_id = transfer.json()['_embedded']['transactions'][0]['id']
            t_networkCode = transfer.json()['_embedded']['transactions'][0]['networkCode']
            t_requiredSignings = transfer.json()['_embedded']['transactions'][0]['requiredSignings']
            t_serialized = transfer.json()['_embedded']['transactions'][0]['serialized']
            t_status = transfer.json()['_embedded']['transactions'][0]['status']
            ID = transfer.json()['id']

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
        sleep(10)

        # with allure.step("查询交易记录——transfers by ID,交易状态变为:1"):
        #     # 循环查10次交易记录
        #     for i in range(10):
        #         sleep(20)
        #         logger.info("<----查询次数:第" + str(i+1) + "次---->")
        #         t = Http.HttpUtils.get_transactions_byid(ID)
        #         t_status = t.json()["_embedded"]["transactions"][0]["status"] #交易状态
        #         if (t_status == "PENDING" or t_status == "SENT"):
        #             assert t.json()["status"] == -1
        #         elif (t_status == "SETTLED"):
        #             assert t.json()["status"] == 1
        #             break
        #         break
            
# 多签账户 Swap [k1,k2,k(私有)]
@allure.feature("Swap_MATIC!")
class Test_swap_success_matic_safe_mesender:
    test_data = [
        # 测试
        ("USDT->USDC(PublicKeys传两个)[k1(托管),k2(私有),k2(私有)]!!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDT","USDC","swap","0x61584dBEaFcd9cf2ad96b4A159eE74107595d26B","1",round(random.uniform(0.001,0.002), random.randint(4,6))),
        ("MATIC->USDC(PublicKeys传两个)[k1(私有),k2(托管),k2(私有)]!!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0","03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228"],"MATIC","MATIC","USDC","swap","0x61584dBEaFcd9cf2ad96b4A159eE74107595d26B","1",round(random.uniform(0.001,0.002), random.randint(4,6))),
        ("USDC->MATIC(PublicKeys传两个)[k1(托管),k2(私有),k2(私有)]!!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","MATIC","swap","0x61584dBEaFcd9cf2ad96b4A159eE74107595d26B","1",round(random.uniform(0.001,0.002), random.randint(4,6))),
        ]

    @allure.story("Swap_MATIC_Success!")
    @allure.title('多签账户(2-2)Swap]-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,fromAmount', test_data)
    def test_swap_matic_safe(self,test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,fromAmount):

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
                "from":from_coin,
                "to":to_coin,
                "address":address,
                "fromAmount":fromAmount,
                "slippage":slippage
            }
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            transfer = Http.HttpUtils.post_instructions(type,body,networkCode,PublicKeys,transactionParams)
            assert transfer.status_code == 200

            t_estimatedFee = transfer.json()['_embedded']['transactions'][0]['estimatedFee']
            t_hash = transfer.json()['_embedded']['transactions'][0]['hash']
            t_id = transfer.json()['_embedded']['transactions'][0]['id']
            t_networkCode = transfer.json()['_embedded']['transactions'][0]['networkCode']
            t_requiredSignings = transfer.json()['_embedded']['transactions'][0]['requiredSignings']
            t_serialized = transfer.json()['_embedded']['transactions'][0]['serialized']
            t_status = transfer.json()['_embedded']['transactions'][0]['status']
            ID = transfer.json()['id']


            # 私有key签名
            signatures = [{
                "hash":t_requiredSignings[0]['hash'],
                "publickey":PublicKey,
                "signature":Conf.Config.sign(privatekey[0],t_requiredSignings[0]['hash'])
            }]

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
            signatures.append({
                "hash":confirmsign.json()[0]["message"],
                "publickey":confirmsign.json()[0]["publicKey"],
                "signature":confirmsign.json()[0]["signature"]
            })

        with allure.step("签名交易——sign"):
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
            for i in range(5):
                sleep(20)
                logger.info("<----查询次数:第" + str(i+1) + "次---->")
                transfers = Http.HttpUtils.get_transactions_byid(ID)
                tx_status = (t.get("status") for t in transfers.json()["_embedded"]["transactions"] if t.get("hash") == send.json()["hash"])
                if (tx_status == "PENDING" or tx_status == "SENT"):
                    assert transfers.json()["status"] == -1
                elif (tx_status == "SETTLED"):
                    assert transfers.json()["status"] == 1
                    break
                break

# 多签账户 Swap [k1,k2,k3(代理)]
@allure.feature("Swap_MATIC!")
class Test_swap_success_matic_safe_agentsender:
    test_data = [
        # 测试
        ("USDT->USDC(PublicKeys传两个)[k1(托管),k2(私有),k3(代理)]!!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDT","USDC","swap","0x61584dBEaFcd9cf2ad96b4A159eE74107595d26B","1",round(random.uniform(0.001,0.002), random.randint(4,6))),
        ("USDC->USDT(PublicKeys传两个)[k1(私有),k2(托管),k3(代理)]!!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0","03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228"],"MATIC","USDT","USDC","swap","0x61584dBEaFcd9cf2ad96b4A159eE74107595d26B","1",round(random.uniform(0.001,0.002), random.randint(4,6)))
        ]

    @allure.story("Swap_MATIC_Success!")
    @allure.title('多签账户(2-2)Swap]-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,fromAmount', test_data)
    def test_swap_matic_safe(self,test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,fromAmount):

        with allure.step("查询账户代理key"):
            pub_agent = Http.HttpUtils.get_safe_agents()
            assert pub_agent.status_code == 200
            PublicKeys.append([k.get('agentPublicKey') for k in pub_agent.json() if k.get('networkCode') == networkCode][0])

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_coin,
                "to":to_coin,
                "address":address,
                "fromAmount":fromAmount,
                "slippage":slippage
            }
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            transfer = Http.HttpUtils.post_instructions(type,body,networkCode,PublicKeys,transactionParams)
            assert transfer.status_code == 200

            t_estimatedFee = transfer.json()['_embedded']['transactions'][0]['estimatedFee']
            t_hash = transfer.json()['_embedded']['transactions'][0]['hash']
            t_id = transfer.json()['_embedded']['transactions'][0]['id']
            t_networkCode = transfer.json()['_embedded']['transactions'][0]['networkCode']
            t_requiredSignings = transfer.json()['_embedded']['transactions'][0]['requiredSignings']
            t_serialized = transfer.json()['_embedded']['transactions'][0]['serialized']
            t_status = transfer.json()['_embedded']['transactions'][0]['status']
            ID = transfer.json()['id']

        with allure.step("查询账户托管key"):
            key_act  = Http.HttpUtils.get_keys()
            assert key_act.status_code == 200
            if PublicKeys[0] in key_act.text:
                PublicKey_act = PublicKeys[0]
                PublicKey = PublicKeys[1]
            else:
                PublicKey_act = PublicKeys[1]
                PublicKey = PublicKeys[0]
            # 私有key签名
            signatures = [{
                "hash":t_requiredSignings[0]['hash'],
                "publickey":PublicKey,
                "signature":Conf.Config.sign(privatekey[0],t_requiredSignings[0]['hash'])
            }]

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
            signatures.append({
                "hash":confirmsign.json()[0]["message"],
                "publickey":confirmsign.json()[0]["publicKey"],
                "signature":confirmsign.json()[0]["signature"]
            })

        with allure.step("签名交易——sign"):
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
            send = Http.HttpUtils.post_send_transfers(sig_agent.json()['id'])
            assert send.status_code == 200

        with allure.step("查询交易记录——transfers by ID,交易状态变为:1"):
            # 循环查10次交易记录
            for i in range(5):
                sleep(20)
                logger.info("<----查询次数:第" + str(i+1) + "次---->")
                transfers = Http.HttpUtils.get_transactions_byid(ID)
                tx_status = (t.get("status") for t in transfers.json()["_embedded"]["transactions"] if t.get("hash") == send.json()["hash"])
                if (tx_status == "PENDING" or tx_status == "SENT"):
                    assert transfers.json()["status"] == -1
                elif (tx_status == "SETTLED"):
                    assert transfers.json()["status"] == 1
                    break
                break

# ## 创建新账户Swap 
# @allure.feature("Swap_MATIC!")
# class Test_swap_success_matic_newsafe_agentsender:
#     test_data = [
#         # 测试
#         ("创建安全账户自动激活","ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187",["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","MATIC")
#     ]

#     @allure.story("Swap_MATIC!")
#     @allure.title('创建新多签账户(2-2) Swap-{test_title}')
#     @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol', test_data)
#     def test_create_account_safe(self, test_title, privatekey, PublicKeys, networkCode, symbol):
        
#         with allure.step("创建账户"):
#             acc = Http.HttpUtils.post_create_account(networkCode,symbol,PublicKeys,2)
#             assert acc.status_code == 200
#             assert acc.json()["status"] == 0
#             accountid = acc.json()["id"]
#             account_address = acc.json()["address"]

#         with allure.step("查询代理账户列表"):
#             agent = Http.HttpUtils.get_safe_agents()
#             assert agent.status_code == 200

#         with allure.step("激活账户"):
#             act = Http.HttpUtils.post_safe_activation(accountid)
#             assert act.status_code == 200
#             assert act.json()["status"] == 0

#         with allure.step("查询激活账户交易 交易成功"):
#             for i in range(10):
#                 sleep(20)
#                 act_ = Http.HttpUtils.get_safe_activation(accountid)
#                 assert act_.status_code == 200
#                 if (act_.json()[0]["transaction"]["status"] == "SETTLED"):
#                     assert act_.json()[0]["account"]["status"] == 2
#                     # assert act_.json()[0]["status"] == 1 状态变化慢
#                     break

#         with allure.step("查询账户状态"):
#             acc_detail = Http.HttpUtils.get_account(account_address)
#             assert acc_detail.status_code == 200
#             assert acc_detail.json()[0]["status"] == 2
        
#         with allure.step("向账户转入USDC"):
#             t = Http.HttpUtils.post_instructions()

if __name__ == '__main__':
    path = os.path.abspath(__file__) + "::Test_swap_success_matic_safe_pub"
    for i in range(5):
      pytest.main(["-vs", path,'--clean-alluredir','--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')