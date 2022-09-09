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
@allure.feature("Cross_Chain_Success!")
class Test_cross_success_usdc:
    test_data = [
        # 测试
        # pubkey ["02413bfdb8f16d812aa0096c2c8bcdc86fc852f9ab9eb372f4db07ee755bb5c43d","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"]
        ("USDC在BSC—MATIC间正常跨链交易!",["2f5dbc9722a4c23977e188565eaacb51b905e11927a5089f84df1c4aa1f07b0e","ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],"CROSSCHAIN_TRANSFER","BSC","USDC","0x8d2cc82494299e0b9865d7bfd6131c1ab0c2c4f1","MATIC","0xbdb3bd7b3f3daeadc58d00ef5f15ed9a476b8fe3","13","12.5"),
    ]

    @allure.story("Cross_Chain_Success!")
    @allure.title('单签地址-跨链交易:{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,type,networkCode,symbol,from_add,toNetworkCode,to_add,amount,amount_', test_data)
    def test_crosschain(self,test_title,privatekey,type,networkCode,symbol,from_add,toNetworkCode,to_add,amount,amount_):

    ## BSC—->MATIC (USDC)
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


    ## MATIC—->BSC (USDC)
        with allure.step("构建交易——cross chain:{toNetworkCode}-->{networkCode}"):
            body = {
                "from":to_add,
                "to":from_add,
                "symbol":symbol,
                "amount":amount_,
                "toNetworkCode":networkCode
            }
            transfer = Http.HttpUtils.post_instructions(type,body,toNetworkCode,[])
            assert transfer.status_code == 200

            t_estimatedFee = transfer.json()['_embedded']['transactions'][0]['estimatedFee']
            t_hash = transfer.json()['_embedded']['transactions'][0]['hash']
            t_id = transfer.json()['_embedded']['transactions'][0]['id']
            t_networkCode = transfer.json()['_embedded']['transactions'][0]['networkCode']
            t_requiredSignings = transfer.json()['_embedded']['transactions'][0]['requiredSignings']
            t_serialized = transfer.json()['_embedded']['transactions'][0]['serialized']
            t_status = transfer.json()['_embedded']['transactions'][0]['status']
            ID = transfer.json()['id']

            signature = Conf.Config.sign(privatekey[1],t_requiredSignings[0]['hash'])
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


# 多签地址 2-2
@allure.feature("Cross_Chain_Success!")
class Test_cross_success_usdc_safe:
    test_data = [
        # 测试
        # pubkey ["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228,02413bfdb8f16d812aa0096c2c8bcdc86fc852f9ab9eb372f4db07ee755bb5c43d","02ac5e97a0659d6ce59c5b10b2ace331bffa276a555ff333b09beda99bd6b9f52e,0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"]
        ("USDC在BSC—MATIC间正常跨链交易!",["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],"BSC","USDC","0xE75659D14cf5436e54B8885D664959CE1a4faB45","MATIC","0xE8e140D77F9Ff1f5b4eaC5388D182ac16D80E0f2","13","12.5"),
    ]

    @allure.story("Cross_Chain_Success!")
    @allure.title('多签地址-跨链交易:{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,networkCode,symbol,from_add,toNetworkCode,to_add,amount,amount_', test_data)
    def test_crosschain_safe(self,test_title,privatekey,networkCode,symbol,from_add,toNetworkCode,to_add,amount,amount_):

    ## BSC—->MATIC (USDC)
        with allure.step("构建交易——cross chain:{networkCode}-->{tonetworkCode}"):
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

        signature = Conf.Config.sign(privatekey[0],res[5][0]['hash'])
        signatures = [
            {
                "hash":res[5][0]['hash'],
                "publickey":res[5][0]['publicKeys'][0],
                "signature":signature
            }
        ]

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


    ## MATIC—->BSC (USDC)
        # with allure.step("构建交易——cross chain:{tonetworkCode}-->{networkCode}"):
        #     res_ = Http.HttpUtils.post_crosschain(tonetworkCode,symbol,to_add,networkCode,from_add,amount_)
        #     assert res_[0].status_code == 200

        # signature_ = Conf.Config.sign(privatekey[1],res_[5][0]['hash'])
        # signatures_ = [
        #     {
        #         "hash":res_[5][0]['hash'],
        #         "publickey":res_[5][0]['publicKeys'][0],
        #         "signature":signature_
        #     }
        # ]

        # with allure.step("签名交易——sign"):
        #     sig_ = Http.HttpUtils.post_sign_transfers(res_[1],res_[2],res_[3],res_[4],res_[5],res_[6],signatures_)
        #     assert sig_.status_code == 200

        # with allure.step("广播交易——send"):
        #     send_ = Http.HttpUtils.post_send_transfers(res_[3])
        #     assert send_.status_code == 200

        # with allure.step("查询跨链交易信息 byId,检查交易:状态为-1"):
        #     transactions_ = Http.HttpUtils.get_transactions_byid(res_[8])
        #     assert transactions_.status_code == 200
        #     assert transactions_.json()['status'] == -1

        # with allure.step("循环查询跨链交易信息 byId,检查交易:状态变更为1,数量为2,状态都为“SETTLED"):
        #     sleep(180)
        #     for i in range(10):
        #         sleep(180)
        #         transactions2_ = Http.HttpUtils.get_transactions_byid(res_[8])
        #         assert transactions2_.status_code == 200
        #         if (transactions2_.json()['status'] == 1):
        #             break
        # assert len(transactions2_.json()['_embedded']['transactions']) == 2
        # assert transactions2_.json()['_embedded']['transactions'][0]['status'] == "SETTLED"
        # assert transactions2_.json()['_embedded']['transactions'][1]['status'] == "SETTLED"

if __name__ == '__main__':
    path = os.path.abspath(__file__) + "::Test_cross_success_usdc"
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')