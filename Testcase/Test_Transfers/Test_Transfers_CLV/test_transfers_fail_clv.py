import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Conf
from Common.Loguru import logger


@allure.feature("Transfers_Fail!")
class Test_transfers_fail_clv:
    # test_data = [
    #     # 测试
    #     # ("余额不足转账!",["053d329fb54f8ab36473e74fd4905644a4d5857836274d3116675bad4cfa4273"],["02fd88692ce948598b310d9ac081d551e74a7b4a70661f45e92544e0c3fa0b70f1"],"CLV","CLV","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","5EMjsczhZw8mUYfyfDJT69PUBAirrviW2bH4chQxKHheCvX3",'1000000',400),
    #     ("精度超长(19位)转账!",["053d329fb54f8ab36473e74fd4905644a4d5857836274d3116675bad4cfa4273"],["02fd88692ce948598b310d9ac081d551e74a7b4a70661f45e92544e0c3fa0b70f1"],"CLV","CLV","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","5EMjsczhZw8mUYfyfDJT69PUBAirrviW2bH4chQxKHheCvX3",Conf.Config.random_amount(19),400),
    #     ("转账金额为空!",["053d329fb54f8ab36473e74fd4905644a4d5857836274d3116675bad4cfa4273"],["02fd88692ce948598b310d9ac081d551e74a7b4a70661f45e92544e0c3fa0b70f1"],"CLV","CLV","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","5EMjsczhZw8mUYfyfDJT69PUBAirrviW2bH4chQxKHheCvX3",'',400),
    #     ("转账金额为负数!",["053d329fb54f8ab36473e74fd4905644a4d5857836274d3116675bad4cfa4273"],["02fd88692ce948598b310d9ac081d551e74a7b4a70661f45e92544e0c3fa0b70f1"],"CLV","CLV","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","5EMjsczhZw8mUYfyfDJT69PUBAirrviW2bH4chQxKHheCvX3","-0.000001",400),
    #     ("转账金额字符串类型异常!",["053d329fb54f8ab36473e74fd4905644a4d5857836274d3116675bad4cfa4273"],["02fd88692ce948598b310d9ac081d551e74a7b4a70661f45e92544e0c3fa0b70f1"],"CLV","CLV","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","5EMjsczhZw8mUYfyfDJT69PUBAirrviW2bH4chQxKHheCvX3","vvvv",400),
    #     ("转账from地址异常!",["053d329fb54f8ab36473e74fd4905644a4d5857836274d3116675bad4cfa4273"],["02fd88692ce948598b310d9ac081d551e74a7b4a70661f45e92544e0c3fa0b70f1"],"CLV","CLV","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT0oi","5EMjsczhZw8mUYfyfDJT69PUBAirrviW2bH4chQxKHheCvX3",Conf.Config.random_amount(6),400),
    #     ("转账from地址为空!",["053d329fb54f8ab36473e74fd4905644a4d5857836274d3116675bad4cfa4273"],["02fd88692ce948598b310d9ac081d551e74a7b4a70661f45e92544e0c3fa0b70f1"],"CLV","CLV","","5EMjsczhZw8mUYfyfDJT69PUBAirrviW2bH4chQxKHheCvX3",Conf.Config.random_amount(6),400),
    #     ("转账to地址异常!",["053d329fb54f8ab36473e74fd4905644a4d5857836274d3116675bad4cfa4273"],["02fd88692ce948598b310d9ac081d551e74a7b4a70661f45e92544e0c3fa0b70f1"],"CLV","CLV","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","5EMjsczhZw8mUYfyfDJT69PUBAirrviW2bH4chQxKHheCvX",Conf.Config.random_amount(6),400),
    #     ("转账to地址为空!",["053d329fb54f8ab36473e74fd4905644a4d5857836274d3116675bad4cfa4273"],["02fd88692ce948598b310d9ac081d551e74a7b4a70661f45e92544e0c3fa0b70f1"],"CLV","CLV","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT","",Conf.Config.random_amount(6),400),
    # ]
    test_data = [
        # 生产
        # ("余额不足转账!",["460d181b618e1748fc6632324609fd8e8e0058571fb7a932cd86596f59b2079c"],["033b345f6c30788674ff9799b377cc5da28ceb2be631c5b9e5ca538e0b4ae4dce5"],"CLV","CLV","5G7h24hiSHuewgtVBXe1dhqvRjJ5VKMzZmL1ntJb1pnW4FiC","5DPQQRu3Xne5KEKXCzFuVt7VJzkX9MiNPJBPWL66uFvBeKmU",'1000000',400),
        ("精度超长(19位)转账!",["460d181b618e1748fc6632324609fd8e8e0058571fb7a932cd86596f59b2079c"],["033b345f6c30788674ff9799b377cc5da28ceb2be631c5b9e5ca538e0b4ae4dce5"],"CLV","CLV","5G7h24hiSHuewgtVBXe1dhqvRjJ5VKMzZmL1ntJb1pnW4FiC","5DPQQRu3Xne5KEKXCzFuVt7VJzkX9MiNPJBPWL66uFvBeKmU",Conf.Config.random_amount(19),400),
        ("转账金额为空!",["460d181b618e1748fc6632324609fd8e8e0058571fb7a932cd86596f59b2079c"],["033b345f6c30788674ff9799b377cc5da28ceb2be631c5b9e5ca538e0b4ae4dce5"],"CLV","CLV","5G7h24hiSHuewgtVBXe1dhqvRjJ5VKMzZmL1ntJb1pnW4FiC","5DPQQRu3Xne5KEKXCzFuVt7VJzkX9MiNPJBPWL66uFvBeKmU",'',400),
        ("转账金额为负数!",["460d181b618e1748fc6632324609fd8e8e0058571fb7a932cd86596f59b2079c"],["033b345f6c30788674ff9799b377cc5da28ceb2be631c5b9e5ca538e0b4ae4dce5"],"CLV","CLV","5G7h24hiSHuewgtVBXe1dhqvRjJ5VKMzZmL1ntJb1pnW4FiC","5DPQQRu3Xne5KEKXCzFuVt7VJzkX9MiNPJBPWL66uFvBeKmU","-0.000001",400),
        ("转账金额字符串类型异常!",["460d181b618e1748fc6632324609fd8e8e0058571fb7a932cd86596f59b2079c"],["033b345f6c30788674ff9799b377cc5da28ceb2be631c5b9e5ca538e0b4ae4dce5"],"CLV","CLV","5G7h24hiSHuewgtVBXe1dhqvRjJ5VKMzZmL1ntJb1pnW4FiC","5DPQQRu3Xne5KEKXCzFuVt7VJzkX9MiNPJBPWL66uFvBeKmU","vvvv",400),
        ("转账from地址异常!",["460d181b618e1748fc6632324609fd8e8e0058571fb7a932cd86596f59b2079c"],["033b345f6c30788674ff9799b377cc5da28ceb2be631c5b9e5ca538e0b4ae4dce5"],"CLV","CLV","5G7h24hiSHuewgtVBXe1dhqvRjJ5VKMzZmL1ntJb1pnW4FiCpppppp","5DPQQRu3Xne5KEKXCzFuVt7VJzkX9MiNPJBPWL66uFvBeKmU",Conf.Config.random_amount(6),400),
        ("转账from地址为空!",["460d181b618e1748fc6632324609fd8e8e0058571fb7a932cd86596f59b2079c"],["033b345f6c30788674ff9799b377cc5da28ceb2be631c5b9e5ca538e0b4ae4dce5"],"CLV","CLV","","5G7h24hiSHuewgtVBXe1dhqvRjJ5VKMzZmL1ntJb1pnW4FiC",Conf.Config.random_amount(6),400),
        ("转账to地址异常!",["460d181b618e1748fc6632324609fd8e8e0058571fb7a932cd86596f59b2079c"],["033b345f6c30788674ff9799b377cc5da28ceb2be631c5b9e5ca538e0b4ae4dce5"],"CLV","CLV","5G7h24hiSHuewgtVBXe1dhqvRjJ5VKMzZmL1ntJb1pnW4FiC","5DPQQRu3Xne5KEKXCzFuVt7VJzkX9MiNPJBPWL66uF",Conf.Config.random_amount(6),400),
        ("转账to地址为空!",["460d181b618e1748fc6632324609fd8e8e0058571fb7a932cd86596f59b2079c"],["033b345f6c30788674ff9799b377cc5da28ceb2be631c5b9e5ca538e0b4ae4dce5"],"CLV","CLV","5G7h24hiSHuewgtVBXe1dhqvRjJ5VKMzZmL1ntJb1pnW4FiC","",Conf.Config.random_amount(6),400),
    ]

    @allure.story("Transfers_CLV_transfer_Fail!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check', test_data)
    def test_transfers_address(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check):

        with allure.step("构建交易——transfers"):
            res = Http.HttpUtils.post_transfers(networkCode,symbol,PublicKeys,from_add,to_add,amount)
            assert res.status_code == status_code_check

@allure.feature("Transfers_Fail!")
class Test_sign_fail_clv:
    test_data = [
        # 测试
        ("签名异常(私钥错误)!",["6b24012db8ae4047e4b0df7245b1bcd74272e4e4dc4085ab2185d79024fa0f44"],["033b345f6c30788674ff9799b377cc5da28ceb2be631c5b9e5ca538e0b4ae4dce5"],"CLV","CLV","5G7h24hiSHuewgtVBXe1dhqvRjJ5VKMzZmL1ntJb1pnW4FiC","5DPQQRu3Xne5KEKXCzFuVt7VJzkX9MiNPJBPWL66uFvBeKmU",Conf.Config.random_amount(6),400),
    ]

    @allure.story("Transfers_CLV_sign_Fail!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check', test_data)
    def test_transfers_address(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check):

        with allure.step("构建交易——transfers"):
            res = Http.HttpUtils.post_transfers(networkCode,symbol,PublicKeys,from_add,to_add,amount)
            assert res[0].status_code == 200

            signature = Conf.Config.sign(privatekey[0],res[5][0]['hash'])
            signatures = [
                {
                    "hash":res[5][0]['hash'],
                    "publickey":PublicKeys[0],
                    "signature":signature
                }
            ]

        with allure.step("签名交易——sign"):
            sig = Http.HttpUtils.post_sign_transfers(res[1],res[2],res[3],res[4],res[5],res[6],signatures)
            assert sig.status_code == status_code_check

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')