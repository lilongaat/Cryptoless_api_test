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


# 多签账户转账ETH 构建交易publickey传三个,sender是账户key
@allure.feature("Transfers_Batch!")
class Test_transfers_batch_eth_safe_pub3_mesender:
    test_data = [
        # 测试
        # ("ETH转账publickey[k1(私有),k2(私有),k2(sender)]",["b07cc7fe1144f17954aec1155eb216777cdd8679f1641cfa71c83223cf0a8666","ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["025d28205f144187b4db46c2080406f4655a8e15e58681a4f3833618bc6738ccb4","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0x728583717C23379398FBCA67CE43A6B3EFD3466e","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3",round(random.uniform(0.00001,0.0001), random.randint(5,18))),
        ("ETH转账publickey[k1(私有),k2(私有),k2(sender)]",["b07cc7fe1144f17954aec1155eb216777cdd8679f1641cfa71c83223cf0a8666","ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["025d28205f144187b4db46c2080406f4655a8e15e58681a4f3833618bc6738ccb4","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0x728583717C23379398FBCA67CE43A6B3EFD3466e","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3",round(random.uniform(1,10), random.randint(2,5))),
    ]

    @allure.story("Transfers_batch_Success!")
    @allure.title('多签账户-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_batch_safe(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        for i in range(2):
            with allure.step("构建交易——instructions"):
                body = {
                    "from":from_add,
                    "to":to_add,
                    "symbol":symbol,
                    "amount":amount
                }
                transactionParams = {}
                transfer = Http.HttpUtils.post_instructions("Transfer",body,networkCode,PublicKeys,transactionParams)
                if i == 0:
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
                        signatures = [
                            {
                                "hash":t_requiredSignings[0]['hash'],
                                "publickey":PublicKeys[0],
                                "signature":Conf.Config.sign(privatekey[0],t_requiredSignings[0]['hash'])
                            },
                            {
                                "hash":t_requiredSignings[0]['hash'],
                                "publickey":PublicKeys[1],
                                "signature":Conf.Config.sign(privatekey[1],t_requiredSignings[0]['hash'])
                            }
                            ]
                        sig = Http.HttpUtils.post_sign_transfers(t_estimatedFee,t_hash,t_id,t_networkCode,t_requiredSignings,t_serialized,signatures)
                        assert sig.status_code == 200

                    with allure.step("sender签名交易"):
                        sig_agent = Http.HttpUtils.post_sign_transfers(
                            sig.json()['estimatedFee'],
                            sig.json()['hash'],
                            sig.json()['id'],
                            sig.json()['networkCode'],
                            sig.json()['requiredSignings'],
                            sig.json()['serialized'],
                            {
                                "hash":sig.json()['requiredSignings'][0]['hash'],
                                "publickey":PublicKeys[1],
                                "signature":Conf.Config.sign(privatekey[1],sig.json()['requiredSignings'][0]['hash'])
                            }
                            )

                    with allure.step("广播交易——send"):
                        send = Http.HttpUtils.post_send_transfers(t_id)
                        assert send.status_code == 200
                else:
                    assert transfer.status_code == 400
                    assert transfer.json()['code'] == 2300000
                    assert "non-reproducible build" in transfer.json()['message']


# 单签账户转账
@allure.feature("Transfers_Batch!")
class Test_transfers_batch_eth:
    test_data = [
        # 测试
        ("ETH转账!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(0.00001,0.001), random.randint(5,18))),
        # ("ERC20转账!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(0.00001,0.001), random.randint(5,18))),
    ]

    @allure.story("Transfers_Batch_批量构建交易后批量send!")
    @allure.title('单签账户-{test_title}')
    @pytest.mark.skip(reason="暂不支持改流程!")
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_batch_send(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        transcations_id = []
        transcations_hash = []
        for i in range(2):
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
                # 保存交易id
                transcations_id.append(t_id)              
                
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
            for j in range(len(transcations_id)):
                send = Http.HttpUtils.post_send_transfers(transcations_id[j])
                assert send.status_code == 200
                transcations_hash.append(send.json()['hash'])
            logger.error(transcations_hash)
        
    @allure.story("Transfers_Batch_批量 构建+send 交易!")
    @allure.title('单签账户-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_batch(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        transcations_hash = []
        for i in range(10):
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
                    transcations_hash.append(send.json()['hash'])
        logger.error(transcations_hash)

if __name__ == '__main__':
    path = os.path.abspath(__file__) + "::Test_transfers_batch_eth_safe_pub3_mesender"
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')