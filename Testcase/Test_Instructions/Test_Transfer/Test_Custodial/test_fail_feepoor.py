import json
import random
import string
from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
from Common import Http, Conf
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))


# custodial 手续费不足账户转帐
@allure.feature("Transfers_Fail!")
class Test_transfers_fee_fail:
    if env_type == 0: #测试
        test_data = [
            # BTC网络
            ("Custodial账户BTC手续费不足转账","BTC","BTC","tb1qwc23lh8cvc8wm086h88905gxt03pkq0pu3cnth","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun",str(Conf.Config.random_amount(8)),400,2400000),
            # GOERLI网络
            # ("Custodial账户GOERLI手续费不足转账","GOERLI","goerliETH","0xA78026a21EDDdCB43Da6aB0c163CE1649B3701F8","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",str(Conf.Config.random_amount(8)),400,2400000),
            # # MATIC网络
            # ("Custodial账户MATIC手续费不足转账","MATIC","MATIC","0x86cfeDCb5cC8826eA804Fc516Da72a6D2801F0d1","0xdba67baa3ca1e89a2bdf0feee4592595b130888a",str(Conf.Config.random_amount(8)),400,2400000),
            # ("Custodial账户MATIC-USDC手续费不足转账","MATIC","MATIC","0x86cfeDCb5cC8826eA804Fc516Da72a6D2801F0d1","0xdba67baa3ca1e89a2bdf0feee4592595b130888a",str(Conf.Config.random_amount(8)),400,2400000),
            # # IRIS网络
            # ("Custodial账户IRIS手续费不足转账","IRIS","IRIS","iaa180qh39f68devetnda4t28drsrhgxnjha5eqhus","iaa18hxtn9lx9swxf4j7ytdmn8yxsvyknh86kdgpvc",str(Conf.Config.random_amount(6)),400,2400000),
            # # CLV网络
            # ("Custodial账户CLV手续费不足转账","CLV","CLV","5Hgu6xq1ETv3kbjBnhqZCzaDFtqUhxfFBogZuJ2RnqsoXmWk","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT",str(Conf.Config.random_amount(7)),400,2400000),
        ]
    elif env_type == 1: #生产
        test_data = [
            # MATIC网络
            ("Custodial账户MATIC手续费不足转账","MATIC","MATIC","0x8d26F59840a4c960e1FbEbae317b47C6759141Dd","0xdba67baa3ca1e89a2bdf0feee4592595b130888a",str(Conf.Config.random_amount(8)),400,2400000),
            # IRIS网络
            ("Custodial账户IRIS手续费不足转账","IRIS","IRIS","iaa1plhhsnmjy5uzpdm84gpmjcfkw3vpmmmtq6fq2k","iaa18hxtn9lx9swxf4j7ytdmn8yxsvyknh86kdgpvc",str(Conf.Config.random_amount(6)),400,2400000),
            # CLV网络
            ("Custodial账户CLV手续费不足转账","CLV","CLV","5EUNMnhcjb6KQCPMiBj54Pc4ydjWFnGnYDcJya4QGREbjfe6","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT",str(Conf.Config.random_amount(7)),400,2400000),
        ]

    @allure.story("Custodial_Transfers_Fail!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,from_add,to_add,amount,status_check,code_check', test_data)
    def test_custodial_nofee(self,test_title,networkCode,symbol,from_add,to_add,amount,status_check,code_check):

        with allure.step("查询from账户holder"):
            holder = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holder.status_code == 200
            holder_before = holder.json()[0]["quantity"]

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_add,
                "to":to_add,
                "symbol":symbol,
                "amount":amount
            }
            transactionParams = {
                # "memo":''.join(random.sample(string.ascii_letters + string.digits, 10))
            }
            transfer = Http.HttpUtils.instructions("transfer",body,networkCode,[],transactionParams)
            assert transfer.status_code == 200

        with allure.step("交易状态是-SIGNED"):
            assert transfer.json()["_embedded"]["transactions"][0]["status"] == "SIGNED"
            id = transfer.json()["_embedded"]["transactions"][0]["id"]

        with allure.step("手动广播失败"):
            send  = Http.HttpUtils.post_send_transfers(id)

            assert send.status_code == status_check
            assert send.json()["code"] == code_check

        with allure.step("查询from账户holder"):
            holder_ = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holder_.status_code == 200
            holder_after = holder_.json()[0]["quantity"]

        with allure.step("断言from账户 holder_before==holder_after"):
            assert holder_before == holder_after


if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')