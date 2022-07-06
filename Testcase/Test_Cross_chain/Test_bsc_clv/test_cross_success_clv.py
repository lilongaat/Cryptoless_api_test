from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Conf
from Common.Loguru import logger


@allure.feature("Cross_Chain_Success!")
class Test_cross_success_usdc:
    test_data = [
        # 测试
        ("CLV在CLVP-BSC间正常跨链交易!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187","2f5dbc9722a4c23977e188565eaacb51b905e11927a5089f84df1c4aa1f07b0e"],"CLV-P","CLV","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","BSC","0x8d2cc82494299e0b9865d7bfd6131c1ab0c2c4f1","6","4"),
    ]

    @allure.story("Cross_Chain_Success!")
    @allure.title('跨链交易:{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,networkCode,symbol,from_add,tonetworkCode,to_add,amount,amount_', test_data)
    def test_crosschain(self,test_title,privatekey,networkCode,symbol,from_add,tonetworkCode,to_add,amount,amount_):
        
    ## CLV-P-->BSC (CLV)
        with allure.step("构建交易——cross chain:{networkCode}-->{tonetworkCode}"):
            res = Http.HttpUtils.post_crosschain(networkCode,symbol,from_add,tonetworkCode,to_add,amount)
            assert res[0].status_code == 200

        signature = Conf.Config.sign(privatekey[0],res[5][0]['hash'])
        signatures = [
            {
                "hash":res[5][0]['hash'],
                "publickey":res[5][0]['publicKeys'][0],
                "signature":signature
            }
        ]

        with allure.step("签名交易——sign"):
            sig = Http.HttpUtils.post_sign_transfers(res[1],res[2],res[3],res[4],res[5],res[6],signatures)
            assert sig.status_code == 200

        with allure.step("广播交易——send"):
            send = Http.HttpUtils.post_send_transfers(res[3])
            assert send.status_code == 200

        with allure.step("查询跨链交易信息 byId,检查交易:状态为-1"):
            transactions = Http.HttpUtils.get_transactions_byid(res[8])
            assert transactions.status_code == 200
            assert transactions.json()['status'] == -1

        with allure.step("循环查询跨链交易信息 byId,检查交易:状态变更为1,数量为2,状态都为“SETTLED"):
            sleep(180)
            for i in range(10):
                sleep(180)
                transactions2 = Http.HttpUtils.get_transactions_byid(res[8])
                assert transactions2.status_code == 200
                if (transactions2.json()['status'] == 1):
                    break
            assert len(transactions2.json()['_embedded']['transactions']) == 2
            assert transactions2.json()['_embedded']['transactions'][0]['status'] == "SETTLED"
            assert transactions2.json()['_embedded']['transactions'][1]['status'] == "SETTLED"
        
    ## BSC-->CLV-P (CLV)
        with allure.step("构建交易——cross chain:{tonetworkCode}-->{networkCode}"):
            res_ = Http.HttpUtils.post_crosschain(tonetworkCode,symbol,to_add,networkCode,from_add,amount_)
            assert res_[0].status_code == 200

        signature_ = Conf.Config.sign(privatekey[1],res_[5][0]['hash'])
        signatures_ = [
            {
                "hash":res_[5][0]['hash'],
                "publickey":res_[5][0]['publicKeys'][0],
                "signature":signature_
            }
        ]

        with allure.step("签名交易——sign"):
            sig_ = Http.HttpUtils.post_sign_transfers(res_[1],res_[2],res_[3],res_[4],res_[5],res_[6],signatures_)
            assert sig_.status_code == 200

        with allure.step("广播交易——send"):
            send_ = Http.HttpUtils.post_send_transfers(res_[3])
            assert send_.status_code == 200

        with allure.step("查询跨链交易信息 byId,检查交易:状态为-1"):
            transactions_ = Http.HttpUtils.get_transactions_byid(res_[8])
            assert transactions_.status_code == 200
            assert transactions_.json()['status'] == -1

        with allure.step("循环查询跨链交易信息 byId,检查交易:状态变更为1,数量为2,状态都为“SETTLED"):
            sleep(180)
            for i in range(10):
                sleep(180)
                transactions2_ = Http.HttpUtils.get_transactions_byid(res_[8])
                assert transactions2_.status_code == 200
                if (transactions2_.json()['status'] == 1):
                    break
        assert len(transactions2_.json()['_embedded']['transactions']) == 2
        assert transactions2_.json()['_embedded']['transactions'][0]['status'] == "SETTLED"
        assert transactions2_.json()['_embedded']['transactions'][1]['status'] == "SETTLED"