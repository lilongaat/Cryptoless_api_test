import json
import random
from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
from Common import Http, Conf
from Common.Loguru import logger


Authorization = 'eyJzaWduYXR1cmUiOiIweDUwYWE1MzIzMGQyODZiOWNmOTQ1YmY3YjE1M2JlNjkzNDRkZWFiMzdlMDIxMjA5OWQzNDc1NTU3YzY4NDU3ZjgyNmY0N2RkOGZiODVjZDg1ZTc5NTYzYjZlOTY3MTRlMTNmYmE2Y2JkNjBjZDY5MmM3MzQ2MTkwMTcyNzVlMWJkMWIiLCJib2R5IjoiV2ViMyBUb2tlbiBWZXJzaW9uOiAyXG5Ob25jZTogMTM2ODA0MjBcbklzc3VlZCBBdDogV2VkLCAxMyBKdWwgMjAyMiAxNjoyNTo0NCBHTVRcbkV4cGlyYXRpb24gVGltZTogU3VuLCAxMyBKdWwgMjA0MiAxNjoyNTo0NCBHTVQifQ=='
# 单签账户
@allure.feature("Asset Recovery!")
class Test_transfers_Recovery():
    
    # test_data = [
    #     # 测试-Recovery
    #     ("ERC20_Recovery",["deacc6c15a33674b5d8b108b7e20ac93560c37265f9042ac65bd9d9fc6e93819"],["02fa18a7433497b2047116939f0306583c5ff05a7579e1e0125024a490035349ac"],"ETH-RINKEBY","symbol","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",round(random.uniform(1000,50000), random.randint(2,8))),
    #     ("ERC20_Recovery_safe",["deacc6c15a33674b5d8b108b7e20ac93560c37265f9042ac65bd9d9fc6e93819"],["02fa18a7433497b2047116939f0306583c5ff05a7579e1e0125024a490035349ac"],"ETH-RINKEBY","symbol","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","maximum"),
    #     ("ETH_Recovery",["deacc6c15a33674b5d8b108b7e20ac93560c37265f9042ac65bd9d9fc6e93819"],["02fa18a7433497b2047116939f0306583c5ff05a7579e1e0125024a490035349ac"],"ETH-RINKEBY","ETH","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",round(random.uniform(0.05,0.1), random.randint(2,8))),
    #     ("ETH_Recovery_safe",["deacc6c15a33674b5d8b108b7e20ac93560c37265f9042ac65bd9d9fc6e93819"],["02fa18a7433497b2047116939f0306583c5ff05a7579e1e0125024a490035349ac"],"ETH-RINKEBY","ETH","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","maximum"),
    #     ("IRIS_Recovery",["ff0f68b5c85cde99c36a464de44c20dc9a9e1e6a61749a3759a02b5a92384562"],["0365d96910927f91b441256c3b8e6a2e00db87dc9079f4101f6444a95da9e6e83b"],"IRIS","IRIS","iaa1jlsefxjczxg23gldzt4qcuxhddgeu4757f2pmq","iaa1t0x3v8gtkkza4d6pyvk6aguq9kxj8trqq6vv7u",round(random.uniform(0.5,1), random.randint(2,4))),
    #     ("IRIS_Recovery_safe",["ff0f68b5c85cde99c36a464de44c20dc9a9e1e6a61749a3759a02b5a92384562"],["0365d96910927f91b441256c3b8e6a2e00db87dc9079f4101f6444a95da9e6e83b"],"IRIS","IRIS","iaa1jlsefxjczxg23gldzt4qcuxhddgeu4757f2pmq","iaa16gtpwuqg9lerp0n39wj4xgmwyawt69p5gq9h8p","maximum"),
    #     ("CLV_Recovery",["a61953ddf67bab7b8a8fbcd1968cc2b87be5918594600ded6bdcb07acc0a831b"],["02ceaffa3bc63a161491e6ed6b054e0f0c161ffdd3417a310e95a1ae2ed000c9c2"],"CLV","CLV","5GsLke2jx8tneTn9EvfzppMhzU9KmEgCSNkbz1tfRaRsiX8J","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","maximum"),
    #     ("BTC_Recovery",["be3aad475627f9d68419c7753534129ae238a7ae95051b35998021844c4e0e7d"],["039c470672332cf51c403b74d25cef41f24190d13082b5884fdcf395e8d78791c6"],"BTC","BTC","tb1qxwtl4mmjrskgy4vtz6zcc8tkn8t6tv575mq6pf","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun",round(random.uniform(0.01,0.05), random.randint(3,5))),
    #     ("BTC_Recovery_safe",["be3aad475627f9d68419c7753534129ae238a7ae95051b35998021844c4e0e7d"],["039c470672332cf51c403b74d25cef41f24190d13082b5884fdcf395e8d78791c6"],"BTC","BTC","tb1qxwtl4mmjrskgy4vtz6zcc8tkn8t6tv575mq6pf","tb1qf8ejg80dqln4t2haceu096kfn0wfta075qgq4l9r2nfxjgc3kapsnsutu3","maximum"),
    # ]
    test_data = [
        # 生产
        ("DOGE_Recovery",["05e2c48d9291308e0665c8017aa1208762c7bfb6d3fe9a54f2415bf283c6f2ce"],["02b87959d40a072112fb858283011251b0180017e7f1880439bb85b4bc5c289298"],"DOGE","DOGE","DG4NBVs5zyz1fTmiWm4zVGUPKpeHEp4efE","DS2Nb2CSowTS12xVSSeMeHLiYio9PtvNDV",25),
        ("DOGE_Recovery_safe",["05e2c48d9291308e0665c8017aa1208762c7bfb6d3fe9a54f2415bf283c6f2ce"],["02b87959d40a072112fb858283011251b0180017e7f1880439bb85b4bc5c289298"],"DOGE","DOGE","DG4NBVs5zyz1fTmiWm4zVGUPKpeHEp4efE","9tEa1ZC6fvJBRSicoCovyAQzYfMSBSLugM","maximum"),
    ]

    @allure.story("Transfers_Asset Recovery!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_transfers(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount):

        with allure.step("查询账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add,Authorization)
            assert holders.status_code == 200

        if (float(holders.json()[0]["quantity"]) > 0):
            with allure.step("构建交易——transfers"):
                transactionParams = {
                    "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
                }
                res = Http.HttpUtils.post_transfers(networkCode,symbol,PublicKeys,from_add,to_add,amount,transactionParams,Authorization)
                assert res[0].status_code == 200

                signatures = []
                for i in range(len(res[5])):
                    signature = Conf.Config.sign(privatekey[0],res[5][i]['hash'])
                    signatures.append(
                        {
                        "hash":res[5][i]['hash'],
                        "publickey":PublicKeys[0],
                        "signature":signature
                    }
                    )

            with allure.step("签名交易——sign"):
                sig = Http.HttpUtils.post_sign_transfers(res[1],res[2],res[3],res[4],res[5],res[6],signatures,res[7],Authorization)
                assert sig.status_code == 200

            with allure.step("广播交易——send"):
                send = Http.HttpUtils.post_send_transfers(res[3],Authorization)
                assert send.status_code == 200

            if "BTC" in test_title:
                sleep(1200)
            else:
                sleep(30)

        logger.info("账户没有对应的资产!")


if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path])
