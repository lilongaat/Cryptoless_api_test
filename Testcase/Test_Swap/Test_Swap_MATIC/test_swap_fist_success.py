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
        ("正常Swap(USDC-USDT)!",["71f57c1da24e44daf355b632eff29bf4507b238d087d88d41e80df46264ff83f"],["03a74734fc178069e52780c6896909d9880f33d89a613f589658805e517748f37f"],"MATIC","USDC","USDT","swap","0x27cf9D25eD98DF2cf12a5a6D1c67a56Ae989030A","1",Conf.Config.random_amount(4))
    ]

    @allure.story("Swap_MATIC_Success!")
    @allure.title('单签账户Swap-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,fromamount', test_data)
    def test_swap_matic(self,test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,fromamount):

        with allure.step("注册账户"):
            account = Http.HttpUtils.post_create_account(networkCode,PublicKeys)
            assert account.status_code == 200
            assert account.json()["address"] == address

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

        with allure.step("查询交易记录——transfers by ID,交易状态变为:1"):
            # 循环查5次交易记录
            for i in range(5):
                sleep(20)
                logger.info("<----查询次数:第" + str(i+1) + "次---->")
                transfers = Http.HttpUtils.get_transactions_byid(ID)

                tx_status = (t.get("status") for t in transfers.json()["_embedded"]["transactions"] if t.get("hash") == send.json()["hash"])

                if (tx_status == "PENDING" or tx_status == "SENT"):
                    assert transfers.json()["status"] == -1
                elif (tx_status == "SETTLED"):
                    break
                break

        with allure.step("判断是否有第二笔交易"):
            # 第一次swap，需授权额度+Swap两笔交易
            sleep(121)
            if (transfers.json()["status"] == -1):
                assert len(transfers.json()["_embedded"]["transactions"]) == 2,'授权额度交易后未正常构建Swap交易!'

                # 第二笔交易数据
                t_estimatedFee_ = transfer.json()['_embedded']['transactions'][1]['estimatedFee']
                t_hash_ = transfer.json()['_embedded']['transactions'][1]['hash']
                t_id_ = transfer.json()['_embedded']['transactions'][1]['id']
                t_networkCode_ = transfer.json()['_embedded']['transactions'][1]['networkCode']
                t_requiredSignings_ = transfer.json()['_embedded']['transactions'][1]['requiredSignings']
                t_serialized_ = transfer.json()['_embedded']['transactions'][1]['serialized']
                t_status_ = transfer.json()['_embedded']['transactions'][1]['status']
                with allure.step("签名交易-sign"):
                    signature_ = Conf.Config.sign(privatekey[0],t_requiredSignings_[0]['hash'])
                    signatures_ = [
                        {
                            "hash":t_requiredSignings_[0]['hash'],
                            "publickey":t_requiredSignings_[0]["publicKeys"][0],
                            "signature":signature_
                        }
                    ]
                    sig_ = Http.HttpUtils.post_sign_transfers(t_estimatedFee_,t_hash_,t_id_,t_networkCode_,t_requiredSignings_,t_serialized_,signatures_)
                    assert sig_.status_code == 200

                with allure.step("广播交易——send"):
                    send = Http.HttpUtils.post_send_transfers(t_id_)
                    assert send.status_code == 200
            else:
                assert transfers.json()["status"] == 1


if __name__ == '__main__':
    path = os.path.abspath(__file__) + "::Test_swap_success_matic"
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')