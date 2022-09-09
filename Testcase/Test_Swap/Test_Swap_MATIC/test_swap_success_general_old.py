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
        ("正常Swap(MATIC-USDT)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","MATIC","USDT","Swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","1",Conf.Config.random_amount(3)),
        ("正常Swap(USDT-MATIC)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDT","MATIC","Swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","1",Conf.Config.random_amount(3)),
        ("正常Swap(USDC-USDT)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","Swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","1",Conf.Config.random_amount(3)),
        ("正常Swap(USDT-USDC)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDT","USDC","Swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","1",Conf.Config.random_amount(3)),
        ("正常Swap(USDT-USDC滑点1~50)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDT","USDC","Swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",random.randint(1,50),Conf.Config.random_amount(3)),
        ("正常Swap(USDC-USDT滑点1~50)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDT","USDC","Swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",random.randint(1,50),Conf.Config.random_amount(3))
    ]

    @allure.story("Swap_MATIC_Success!")
    @allure.title('单签账户Swap-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,fromAmount', test_data)
    def test_swap_matic(self,test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,fromAmount):

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


if __name__ == '__main__':
    path = os.path.abspath(__file__) + "::Test_swap_success_matic"
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')