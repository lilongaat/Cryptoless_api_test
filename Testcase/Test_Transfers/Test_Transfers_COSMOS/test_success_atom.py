import decimal
import json
from time import sleep
from typing_extensions import assert_type
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Conf, Httpexplore
from Common.Loguru import logger

# 单签账户
@allure.feature("Transfers_Success!")
class Test_transfers_success_atom:
    test_data = [
        # 生产
        ("正常转账(自己转自己)!",["3f6c52cc8b317b9559cc13b3edcf7166eaadba1ca7d06d2848b7d2d530e0ec54"],["023b16c02f0b106c2bec8305d0e64593f7156da6a37dedbd2e85342b8ff500392f"],"ATOM","ATOM","cosmos1ku5klzmup3an5mxva6u9pr8jmhzrapa7lrtukh","cosmos1ku5klzmup3an5mxva6u9pr8jmhzrapa7lrtukh",Conf.Config.random_amount(4)),
        # ("正常转账maximum(自己转自己)!",["3f6c52cc8b317b9559cc13b3edcf7166eaadba1ca7d06d2848b7d2d530e0ec54"],["023b16c02f0b106c2bec8305d0e64593f7156da6a37dedbd2e85342b8ff500392f"],"ATOM","ATOM","cosmos1ku5klzmup3an5mxva6u9pr8jmhzrapa7lrtukh","cosmos1ku5klzmup3an5mxva6u9pr8jmhzrapa7lrtukh","maximum"),
        # ("正常转账!",["3f6c52cc8b317b9559cc13b3edcf7166eaadba1ca7d06d2848b7d2d530e0ec54"],["023b16c02f0b106c2bec8305d0e64593f7156da6a37dedbd2e85342b8ff500392f"],"ATOM","ATOM","cosmos1ku5klzmup3an5mxva6u9pr8jmhzrapa7lrtukh","cosmos1h5rgna0ca8tp9nv0alwx26sa5gdcszd62ln9y0",Conf.Config.random_amount(4)),
    ]

    @allure.story("Transfers_ATOM_Success!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers_atom(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        with allure.step("查询From账户ATOM余额"):
            holder = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holder.status_code == 200
            quantity = float(holder.json()[0]['quantity'])

        with allure.step("mintscan浏览器查询From账户ATOM余额"):
            holder_explore = Httpexplore.ATOM.balance(from_add)
            assert holder_explore.status_code == 200
            quantity_explore = int([b.get("amount") for b in holder_explore.json()["balances"] if b.get("denom") == "uatom"][0])/1000000

        with allure.step("余额对比"):
            assert quantity == quantity_explore


        # with allure.step("构建交易——instructions"):
        #     body = {
        #         "from":from_add,
        #         "to":to_add,
        #         "symbol":symbol,
        #         "amount":amount
        #     }
        #     transactionParams = {
        #         "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
        #     }
        #     transfer = Http.HttpUtils.post_instructions("Transfer",body,networkCode,PublicKeys,transactionParams)
        #     assert transfer.status_code == 200

        #     t_estimatedFee = transfer.json()['_embedded']['transactions'][0]['estimatedFee']
        #     t_hash = transfer.json()['_embedded']['transactions'][0]['hash']
        #     t_id = transfer.json()['_embedded']['transactions'][0]['id']
        #     t_networkCode = transfer.json()['_embedded']['transactions'][0]['networkCode']
        #     t_requiredSignings = transfer.json()['_embedded']['transactions'][0]['requiredSignings']
        #     t_serialized = transfer.json()['_embedded']['transactions'][0]['serialized']
        #     t_status = transfer.json()['_embedded']['transactions'][0]['status']
        #     ID = transfer.json()['id']
        #     body_amount = transfer.json()["body"]["amount"]

        # with allure.step("签名交易——sign"):
        #     signature = Conf.Config.sign(privatekey[0],t_requiredSignings[0]['hash'])
        #     signatures = [
        #         {
        #             "hash":t_requiredSignings[0]['hash'],
        #             "publickey":t_requiredSignings[0]['publicKeys'][0],
        #             "signature":signature
        #         }
        #     ]
        #     sig = Http.HttpUtils.post_sign_transfers(t_estimatedFee,t_hash,t_id,t_networkCode,t_requiredSignings,t_serialized,signatures)
        #     assert sig.status_code == 200

        # with allure.step("广播交易——send"):
        #     send = Http.HttpUtils.post_send_transfers(t_id)
        #     assert send.status_code == 200

        # with allure.step("查询交易记录——transfers by ID,交易状态变为:1"):
        #     # 循环查10次交易记录
        #     for i in range(1):
        #         sleep(20)
        #         logger.info("<----查询次数:第" + str(i+1) + "次---->")
        #         t = Http.HttpUtils.get_transactions_byid(ID)
        #         t_status = t.json()["_embedded"]["transactions"][0]["status"] #交易状态
        #         if (t_status == "PENDING" or t_status == "SENT"):
        #             assert t.json()["status"] == -1
        #         elif (t_status == "SETTLED"):
        #             assert t.json()["status"] == 1
        #             break             

        # with allure.step("查询关联交易记录——balance-transactions by hash"):
        #     sleep(15)
        #     transcations = Http.HttpUtils.get_transactions_byhash(send.json()["hash"])
   
        #     if (from_add == to_add):
        #         assert len(transcations.json()) == 3 # 自己转自己3条交易记录
        #     else:
        #         assert len(transcations.json()) == 4 # 转其他地址4条交易记录

        # with allure.step("查询From账户holders信息——holders"):
        #     holders_after = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
        #     assert holders_after.status_code == 200
        #     quantity_after = holders_after.json()[0]['quantity']

        # with allure.step("断言holders转出金额"):
        #     if from_add == to_add:
        #         assert quantity_before == quantity_after
        #     else:
        #         assert decimal.Decimal(body_amount) == decimal.Decimal(quantity_before) - decimal.Decimal(quantity_after)


if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')