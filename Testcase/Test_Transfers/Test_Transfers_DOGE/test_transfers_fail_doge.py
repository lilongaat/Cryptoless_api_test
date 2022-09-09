import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Conf
from Common.Loguru import logger


@allure.feature("Transfers_Fail!")
class Test_transfers_fail_doge():
    test_data = [
        # 测试
        ("余额不足转账!",["075a141217e765672c4ee57bc2b0dab0774aad0488ac018e045b9e1dae58573d"],["03d006ca425eb30e314c0de2ef0a656f1e30f1f0e320e2c364418b0b60132b89b1"],"DOGE","DOGE","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV","1000000",400),
        ("精度超长(9位)转账!",["075a141217e765672c4ee57bc2b0dab0774aad0488ac018e045b9e1dae58573d"],["03d006ca425eb30e314c0de2ef0a656f1e30f1f0e320e2c364418b0b60132b89b1"],"DOGE","DOGE","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV",Conf.Config.random_amount(9),400),
        ("转账金额为空!",["075a141217e765672c4ee57bc2b0dab0774aad0488ac018e045b9e1dae58573d"],["03d006ca425eb30e314c0de2ef0a656f1e30f1f0e320e2c364418b0b60132b89b1"],"DOGE","DOGE","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV","",400),
        ("转账金额为负数!",["075a141217e765672c4ee57bc2b0dab0774aad0488ac018e045b9e1dae58573d"],["03d006ca425eb30e314c0de2ef0a656f1e30f1f0e320e2c364418b0b60132b89b1"],"DOGE","DOGE","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV","-0.0000001",400),
        ("转账金额字符串类型异常!",["075a141217e765672c4ee57bc2b0dab0774aad0488ac018e045b9e1dae58573d"],["03d006ca425eb30e314c0de2ef0a656f1e30f1f0e320e2c364418b0b60132b89b1"],"DOGE","DOGE","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV","0.00000i",400),
        ("转账from地址异常!",["075a141217e765672c4ee57bc2b0dab0774aad0488ac018e045b9e1dae58573d"],["03d006ca425eb30e314c0de2ef0a656f1e30f1f0e320e2c364418b0b60132b89b1"],"DOGE","DOGE","0xE20FD35a849Ad67B2db3287d1dc3669067B237B6","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV",Conf.Config.random_amount(6),400),
        ("转账from地址为空!",["075a141217e765672c4ee57bc2b0dab0774aad0488ac018e045b9e1dae58573d"],["03d006ca425eb30e314c0de2ef0a656f1e30f1f0e320e2c364418b0b60132b89b1"],"DOGE","DOGE","","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV",Conf.Config.random_amount(7),400),
        ("转账to地址异常!",["075a141217e765672c4ee57bc2b0dab0774aad0488ac018e045b9e1dae58573d"],["03d006ca425eb30e314c0de2ef0a656f1e30f1f0e320e2c364418b0b60132b89b1"],"DOGE","DOGE","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV","0xFEdd6BA870090f44CE20d06fBE0806B60De6D562",Conf.Config.random_amount(9),400),
        ("转账to地址为空!",["075a141217e765672c4ee57bc2b0dab0774aad0488ac018e045b9e1dae58573d"],["03d006ca425eb30e314c0de2ef0a656f1e30f1f0e320e2c364418b0b60132b89b1"],"DOGE","DOGE","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV","",Conf.Config.random_amount(8),400),
    ]

    @allure.story("Transfers_DOGE_transfer_Fail!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check', test_data)
    def test_transfers_address(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check):

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_add,
                "to":to_add,
                "symbol":symbol,
                "amount":amount
            }
            transfer = Http.HttpUtils.post_instructions("Transfer",body,networkCode,PublicKeys)
            assert transfer.status_code == status_code_check

@allure.feature("Transfers_Fail!")
class Test_sign_fail_doge():
    test_data = [
        # 测试
        ("签名异常(私钥错误)!",["6b24012db8ae4047e4b0df7245b1bcd74272e4e4dc4085ab2185d79024fa0f44"],["03d006ca425eb30e314c0de2ef0a656f1e30f1f0e320e2c364418b0b60132b89b1"],"DOGE","DOGE","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV",Conf.Config.random_amount(6),400),
    ]

    @allure.story("Transfers_DOGE_sign_Fail!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check', test_data)
    def test_transfers_address(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check):

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_add,
                "to":to_add,
                "symbol":symbol,
                "amount":amount
            }
            transfer = Http.HttpUtils.post_instructions("Transfer",body,networkCode,PublicKeys)
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

            signatures = []
            for i in range(len(t_requiredSignings)):
                signature = Conf.Config.sign(privatekey[0],t_requiredSignings[i]['hash'])
                signatures.append(
                    {
                    "hash":t_requiredSignings[i]['hash'],
                    "publickey":t_requiredSignings[i]["publicKeys"][0],
                    "signature":signature
                }
                )

        with allure.step("签名交易——sign"):
            sig = Http.HttpUtils.post_sign_transfers(t_estimatedFee,t_hash,t_id,t_networkCode,t_requiredSignings,t_serialized,signatures)
            assert sig.status_code == status_code_check

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')