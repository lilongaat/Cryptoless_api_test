from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Conf
from Common.Loguru import logger

# 单签地址
@allure.feature("Cross_Chain_Fail!")
class Test_cross_fail_usdc:
    test_data = [
        # 测试
        # pubkey ["02413bfdb8f16d812aa0096c2c8bcdc86fc852f9ab9eb372f4db07ee755bb5c43d"]["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"]
        ("BSC(USDC)—MATIC(USDC)间正常跨链交易!",["2f5dbc9722a4c23977e188565eaacb51b905e11927a5089f84df1c4aa1f07b0e"],"CROSSCHAIN_TRANSFER","BSC","USDT","0x8d2cc82494299e0b9865d7bfd6131c1ab0c2c4f1","MATIC","0xbdb3bd7b3f3daeadc58d00ef5f15ed9a476b8fe3","0.0000000001"),
        # ("USDC在MATIC-BSC间正常跨链交易!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],"CROSSCHAIN_TRANSFER","MATIC","USDC","0xbdb3bd7b3f3daeadc58d00ef5f15ed9a476b8fe3","BSC","0x8d2cc82494299e0b9865d7bfd6131c1ab0c2c4f1","12.5")
    ]

    @allure.story("Cross_Chain_Fail!")
    @allure.title('单签地址-跨链交易:{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,type,networkCode,symbol,from_add,toNetworkCode,to_add,amount', test_data)
    def test_crosschain(self,test_title,privatekey,type,networkCode,symbol,from_add,toNetworkCode,to_add,amount):

        with allure.step("构建交易——cross chain:{networkCode}-->{toNetworkCode}"):
            body = {
                "from":from_add,
                "to":to_add,
                "symbol":symbol,
                "amount":amount,
                "toNetworkCode":toNetworkCode
            }
            transfer = Http.HttpUtils.post_instructions(type,body,networkCode,[])
            assert transfer.status_code == 200

            t_estimatedFee = transfer.json()['_embedded']['transactions'][0]['estimatedFee']
            t_hash = transfer.json()['_embedded']['transactions'][0]['hash']
            t_id = transfer.json()['_embedded']['transactions'][0]['id']
            t_networkCode = transfer.json()['_embedded']['transactions'][0]['networkCode']
            t_requiredSignings = transfer.json()['_embedded']['transactions'][0]['requiredSignings']
            t_serialized = transfer.json()['_embedded']['transactions'][0]['serialized']
            t_status = transfer.json()['_embedded']['transactions'][0]['status']
            ID = transfer.json()['id']

            signature = Conf.Config.sign(privatekey[0],t_requiredSignings[0]['hash'])
            signatures = [
                {
                    "hash":t_requiredSignings[0]['hash'],
                    "publickey":t_requiredSignings[0]['publicKeys'][0],
                    "signature":signature
                }
            ]

        with allure.step("签名交易——sign"):
            sig = Http.HttpUtils.post_sign_transfers(t_estimatedFee,t_hash,t_id,t_networkCode,t_requiredSignings,t_serialized,signatures)
            assert sig.status_code == 200

        with allure.step("广播交易——send"):
            send = Http.HttpUtils.post_send_transfers(t_id)
            assert send.status_code == 200

        with allure.step("查询跨链交易信息 byID,检查交易:状态为-1"):
            transactions = Http.HttpUtils.get_transactions_byid(ID)
            assert transactions.status_code == 200
            assert transactions.json()['status'] == -1

        with allure.step("循环查询跨链交易信息 byID,检查交易:状态变更为1,数量为2,状态都为“SETTLED"):
            sleep(180)
            for i in range(10):
                sleep(180)
                t = Http.HttpUtils.get_transactions_byid(ID)
                assert t.status_code == 200
                if (t.json()['status'] == 1):
                    break
            assert len(t.json()['_embedded']['transactions']) == 2 #BSC上第一笔成功后，MATIC创建第二笔
            assert t.json()['_embedded']['transactions'][0]['status'] == "SETTLED"
            assert t.json()['_embedded']['transactions'][1]['status'] == "SETTLED"


if __name__ == '__main__':
    path = os.path.abspath(__file__) + "::Test_cross_fail_usdc"
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')