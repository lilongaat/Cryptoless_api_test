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
@allure.feature("Swap_MATIC!")
class Test_swap_success_matic:
    test_data = [
        # 测试&生产
        ("正常Swap(MATIC-USDT)!",["6bac9b5536fe6d8758084b25f2cab21f4c5429de292ec699d28dc441701fdc23"],["03413dbd6dd45d9146ec635971672dbaf0fb9032672a7e475beb7e6f727fb8e53c"],"MATIC","USDT","USDC","swap","0xeA4669366cc50ddf3DFc5CB3c46CA07F7799Cb02","1",Conf.Config.random_amount(3)),
        # ("正常Swap(MATIC-USDT)!",["b07cc7fe1144f17954aec1155eb216777cdd8679f1641cfa71c83223cf0a8666"],["025d28205f144187b4db46c2080406f4655a8e15e58681a4f3833618bc6738ccb4"],"MATIC","MATIC","USDT","swap","0x137ab2863110a608B4d6B55b20539AA785F73998","1",Conf.Config.random_amount(3)),
        # ("正常Swap(USDC-USDT)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","1",Conf.Config.random_amount(3)),
        # ("正常Swap(USDC-USDT)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","1",Conf.Config.random_amount(3)),
        # ("正常Swap(USDT-USDC滑点1~50)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDT","USDC","swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",random.randint(1,50),Conf.Config.random_amount(3)),
    ]

    @allure.story("Swap_MATIC_Success!")
    @allure.title('单签账户Swap-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,fromamount', test_data)
    def test_swap_matic(self,test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,fromamount):

        with allure.step("构建交易——swap"):
            body = {
                "from":from_coin,
                "to":to_coin,
                "address":address,
                "fromAmount":fromamount,
                "slippage":slippage

            }
            transfer = Http.HttpUtils.post_instructions(type,body,networkCode,PublicKeys)
            assert transfer.status_code == 200

            t_estimatedFee = transfer.json()['_embedded']['transactions'][0]['estimatedFee']
            t_hash = transfer.json()['_embedded']['transactions'][0]['hash']
            t_id = transfer.json()['_embedded']['transactions'][0]['id']
            t_networkCode = transfer.json()['_embedded']['transactions'][0]['networkCode']
            t_requiredSignings = transfer.json()['_embedded']['transactions'][0]['requiredSignings']
            t_serialized = transfer.json()['_embedded']['transactions'][0]['serialized']
            t_status = transfer.json()['_embedded']['transactions'][0]['status']
            ID = transfer.json()['id']

        with allure.step("签名交易——sign"):
            signature = Conf.Config.sign(privatekey[0],t_requiredSignings[0]['hash'])
            signatures = [
                {
                    "hash":t_requiredSignings[0]['hash'],
                    "publickey":t_requiredSignings[0]["publicKeys"][0],
                    "signature":signature
                }
            ]
            sig = Http.HttpUtils.post_sign_transfers(t_estimatedFee,t_hash,t_id,t_networkCode,t_requiredSignings,t_serialized,signatures)
            assert sig.status_code == 200

        with allure.step("广播交易——send"):
            send = Http.HttpUtils.post_send_transfers(t_id)
            assert send.status_code == 200

        with allure.step("查询交易记录——transfers by id,交易状态变为:1"):
            # 循环查10次交易记录
            for i in range(5):
                sleep(20)
                logger.info("<----查询次数:第" + str(i+1) + "次---->")
                transfers = Http.HttpUtils.get_transactions_byid(ID)

                tx_status = (t.get("status") for t in transfers.json()["_embedded"]["transactions"] if t.get("hash") == send.json()["hash"])

                if (tx_status == "PENDING" or tx_status == "SENT"):
                    assert transfers.json()["status"] == -1
                elif (tx_status == "SETTLED"):
                    # 第一次swap，需授权额度+Swap两笔交易
                    if (transfers.json()["status"] == -1):
                        sleep(61)
                        assert len(transfers.json()["_embedded"]["transactions"]) == 2,'授权额度交易后未正常构建Swap交易!'
                    else:
                        assert transfers.json()["status"] == 1
                        break
                    break
                break



# 多签账户 Swap [k1,k2,k1]-k2是托管key
@allure.feature("Swap_MATIC!")
class Test_swap_success_matic_safe:
    test_data = [
        # 测试
        ("MATIC->USDC[k1(自己),k2(托管),k1](合约地址有matic)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0","03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228"],"MATIC","MATIC","USDC","swap","0xcb4D1bBF74F2b068Dc7d33c965c1Fdad3d7B4D43","1",Conf.Config.random_amount(2)),
        ("USDT->MATIC[k1(自己),k2(托管),k1](合约地址有matic)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0","03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228"],"MATIC","USDT","MATIC","swap","0xcb4D1bBF74F2b068Dc7d33c965c1Fdad3d7B4D43","1",Conf.Config.random_amount(2)),
        ("USDT->USDC[k1(托管),k2(自己),k2](合约地址有matic)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDT","USDC","swap","0xcb4D1bBF74F2b068Dc7d33c965c1Fdad3d7B4D43","1",Conf.Config.random_amount(2)),
        ("USDC->USDT[k1(托管),k2(自己),k2](合约地址有matic)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","0xcb4D1bBF74F2b068Dc7d33c965c1Fdad3d7B4D43","1",Conf.Config.random_amount(2)),

        ("USDC->USDT[k1(自己),k2(托管),k1](合约地址无matic)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0","02ac5e97a0659d6ce59c5b10b2ace331bffa276a555ff333b09beda99bd6b9f52e"],"MATIC","USDC","USDT","swap","0xE8e140D77F9Ff1f5b4eaC5388D182ac16D80E0f2","1",Conf.Config.random_amount(2)),
        ("USDT->USDC[k1(托管),k2(自己),k1](合约地址无matic)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["02ac5e97a0659d6ce59c5b10b2ace331bffa276a555ff333b09beda99bd6b9f52e","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","0xE8e140D77F9Ff1f5b4eaC5388D182ac16D80E0f2","1",Conf.Config.random_amount(2)),
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
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,fromamount', test_data)
    def test_swap_matic_safe(self,test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,fromamount):

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

        with allure.step("构建交易——swap"):
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            res = Http.HttpUtils.post_instructions(networkCode,from_coin,to_coin,PublicKeys,address,slippage,fromamount,type,transactionParams)
            assert res[0].status_code == 200

            # 私有key签名
            signatures = [{
                "hash":res[5][0]['hash'],
                "publickey":PublicKey,
                "signature":Conf.Config.sign(privatekey[0],res[5][0]['hash'])
            }]

        with allure.step("请求签名交易——req_sign"):
            requiredSignings = [{
                "message":res[5][0]['hash'],
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
            sig = Http.HttpUtils.post_sign_transfers(res[1],res[2],res[3],res[4],res[5],res[6],signatures)
            assert sig.status_code == 200
        
        with allure.step("sender签名交易——sign"):
            signatures_sender = {
                "hash":sig.json()['requiredSignings'][0]['hash'],
                "publickey":sig.json()['requiredSignings'][0]['publicKeys'][0],
                "signature":Conf.Config.sign(privatekey[0],sig.json()['requiredSignings'][0]['hash'])
            }

            sig_ = Http.HttpUtils.post_sign_transfers(sig.json()['estimatedFee'],sig.json()['hash'],sig.json()['id'],sig.json()['networkCode'],sig.json()['requiredSignings'],sig.json()['serialized'],signatures_sender)
            assert sig_.status_code == 200

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
                    assert transfers.json()["status"] == 1
                    break
                break
            

# 多签账户 Swap [k1,k2,k3]-k2是托管key,k3是代理key
@allure.feature("Swap_MATIC!")
class Test_swap_success_matic_safe_sender:
    test_data = [
        # 测试
        ("正常Swap!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0","03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228"],"MATIC","USDC","USDT","swap","0x61584dBEaFcd9cf2ad96b4A159eE74107595d26B","1",Conf.Config.random_amount(2)),
        ]

    @allure.story("Swap_MATIC_Success!")
    @allure.title('多签账户Swap[k1(自己),k2(托管),k3(代理)]-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,fromamount', test_data)
    def test_swap_matic_safe(self,test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,fromamount):

        with allure.step("查询账户代理key"):
            pub_agent = Http.HttpUtils.get_safe_agents()
            assert pub_agent.status_code == 200
            PublicKeys.append([k.get('agentPublicKey') for k in pub_agent.json() if k.get('networkCode') == networkCode][0])

        with allure.step("构建交易——swap"):
            res = Http.HttpUtils.post_instructions(networkCode,from_coin,to_coin,PublicKeys,address,slippage,fromamount,type)
            assert res[0].status_code == 200

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
                "hash":res[5][0]['hash'],
                "publickey":PublicKey,
                "signature":Conf.Config.sign(privatekey[0],res[5][0]['hash'])
            }]

        with allure.step("请求签名交易——req_sign"):
            requiredSignings = [{
                "message":res[5][0]['hash'],
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
            sig = Http.HttpUtils.post_sign_transfers(res[1],res[2],res[3],res[4],res[5],res[6],signatures)
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
                    assert transfers.json()["status"] == 1
                    break

if __name__ == '__main__':
    path = os.path.abspath(__file__) + "::Test_swap_success_matic"
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')