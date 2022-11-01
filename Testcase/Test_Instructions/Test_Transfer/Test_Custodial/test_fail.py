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

# custodial
@allure.feature("Transfers_Fail!")
class Test_transfers_fail:
    if env_type == 0: #测试
        test_data = [
            #BTC网络
            ("Custodial账户BTC转账from地址为空","BTC","BTC","","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun",str(round(random.uniform(1,3), random.randint(3,5))),400,2300000),
            ("Custodial账户BTC转账from地址不属于该用户","BTC","BTC","mpUC1Ypz43ixUQbLnn9PesgQpA6RZr9Lib","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun",str(round(random.uniform(1,3), random.randint(3,5))),404,2200000),
            ("Custodial账户BTC转账from地址非BTC地址","BTC","BTC","0xC0959365ca20e3e587FEfAEaf48DaEC479bE83eD","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun",str(round(random.uniform(1,3), random.randint(3,5))),404,2200000),
            ("Custodial账户BTC转账to地址为空","BTC","BTC","tb1q8g0jhxa3t0uyufec29xexw6fwnkvw94v3jlw7e","",str(round(random.uniform(1,3), random.randint(3,5))),400,2300000),
            ("Custodial账户BTC转账to地址非BTC地址","BTC","BTC","tb1q8g0jhxa3t0uyufec29xexw6fwnkvw94v3jlw7e","0x46F66EeFf67c809A7EF728aC823133ccaBa2506F",str(round(random.uniform(1,3), random.randint(3,5))),400,2400000),
            ("Custodial账户BTC转账amount超出余额","BTC","BTC","tb1q8g0jhxa3t0uyufec29xexw6fwnkvw94v3jlw7e","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","100000000",400,2102001),
            ("Custodial账户BTC转账amount超出精度","BTC","BTC","tb1q8g0jhxa3t0uyufec29xexw6fwnkvw94v3jlw7e","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","0.000000001",400,2100000),
            ("Custodial账户BTC转账amount=0","BTC","BTC","tb1q8g0jhxa3t0uyufec29xexw6fwnkvw94v3jlw7e","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","0",400,2300000),
            ("Custodial账户BTC转账amount为负","BTC","BTC","tb1q8g0jhxa3t0uyufec29xexw6fwnkvw94v3jlw7e","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","-1",400,2300000),
            ("Custodial账户BTC转账amount为异常字符串","BTC","BTC","tb1q8g0jhxa3t0uyufec29xexw6fwnkvw94v3jlw7e","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","maxxx",400,2300000),
            ("Custodial账户BTC转账networkCode为空","","BTC","tb1q8g0jhxa3t0uyufec29xexw6fwnkvw94v3jlw7e","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun",str(round(random.uniform(1,3), random.randint(3,5))),400,2100000),
            ("Custodial账户BTC转账networkCode不存在","BTCC","BTC","tb1q8g0jhxa3t0uyufec29xexw6fwnkvw94v3jlw7e","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun",str(round(random.uniform(1,3), random.randint(3,5))),404,2200000),
            ("Custodial账户BTC转账symbol为空","BTC","","tb1q8g0jhxa3t0uyufec29xexw6fwnkvw94v3jlw7e","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun",str(round(random.uniform(1,3), random.randint(3,5))),400,2300000),
            ("Custodial账户BTC转账symbol不存在","BTC","ETH","tb1q8g0jhxa3t0uyufec29xexw6fwnkvw94v3jlw7e","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun",str(round(random.uniform(1,3), random.randint(3,5))),400,2200000),
            #Goerli网络
            ("Custodial账户Goerli转账from地址为空","GOERLI","GoerliETH","","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",str(round(random.uniform(1,3), random.randint(3,5))),400,2300000),
            ("Custodial账户Goerli转账from地址不属于该用户","GOERLI","GoerliETH","0xd586aae43a128ba080b0d60cb0cb9577e27aa722","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",str(round(random.uniform(1,3), random.randint(3,5))),404,2200000),
            ("Custodial账户Goerli转账from地址非Goerli地址","GOERLI","GoerliETH","mpUC1Ypz43ixUQbLnn9PesgQpA6RZr9Lib","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",str(round(random.uniform(1,3), random.randint(3,5))),404,2200000),
            ("Custodial账户Goerli转账to地址为空","GOERLI","GoerliETH","0x821647aF7f50717500E008dE239f8692216cBC67","",str(round(random.uniform(1,3), random.randint(3,5))),400,2300000),
            ("Custodial账户Goerli转账to地址非Goerli地址","GOERLI","GoerliETH","0x821647aF7f50717500E008dE239f8692216cBC67","mpUC1Ypz43ixUQbLnn9PesgQpA6RZr9Lib",str(round(random.uniform(1,3), random.randint(3,5))),400,2400000),
            ("Custodial账户Goerli转账amount超出余额","GOERLI","GoerliETH","0x821647aF7f50717500E008dE239f8692216cBC67","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","100000000",400,2102001),
            ("Custodial账户Goerli转账amount超出精度","GOERLI","GoerliETH","0x821647aF7f50717500E008dE239f8692216cBC67","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0.0000000010000000001",400,2100000),
            ("Custodial账户Goerli转账amount=0","GOERLI","GoerliETH","0x821647aF7f50717500E008dE239f8692216cBC67","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0",400,2300000),
            ("Custodial账户Goerli转账amount为负","GOERLI","GoerliETH","0x821647aF7f50717500E008dE239f8692216cBC67","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","-1",400,2300000),
            ("Custodial账户Goerli转账amount为异常字符串","GOERLI","GoerliETH","0x821647aF7f50717500E008dE239f8692216cBC67","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","maxxx",400,2300000),
            ("Custodial账户Goerli转账networkCode为空","","GoerliETH","0x821647aF7f50717500E008dE239f8692216cBC67","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",str(round(random.uniform(1,3), random.randint(3,5))),400,2100000),
            ("Custodial账户Goerli转账networkCode不存在","GOERL","GoerliETH","0x821647aF7f50717500E008dE239f8692216cBC67","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",str(round(random.uniform(1,3), random.randint(3,5))),404,2200000),
            ("Custodial账户Goerli转账symbol为空","GOERLI","","0x821647aF7f50717500E008dE239f8692216cBC67","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",str(round(random.uniform(1,3), random.randint(3,5))),400,2300000),
            ("Custodial账户Goerli转账symbol不存在","GOERLI","ETH","0x821647aF7f50717500E008dE239f8692216cBC67","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",str(round(random.uniform(1,3), random.randint(3,5))),400,2200000)
        ]
    elif env_type == 1: #生产
        test_data = [
            #DOGE网络
            ("Custodial账户DOGE转账from地址为空","DOGE","DOGE","","DGnb5SNRnEyAx9xNuHGxbiY4ysHPsxegP9",str(round(random.uniform(1,3), random.randint(3,5))),400,2300000),
            ("Custodial账户DOGE转账from地址不属于该用户","DOGE","DOGE","DE5opaXjFgDhFBqL6tBDxTAQ56zkX6EToX","DGnb5SNRnEyAx9xNuHGxbiY4ysHPsxegP9",str(round(random.uniform(1,3), random.randint(3,5))),404,2200000),
            ("Custodial账户DOGE转账from地址非DOGE地址","DOGE","DOGE","0xC0959365ca20e3e587FEfAEaf48DaEC479bE83eD","DGnb5SNRnEyAx9xNuHGxbiY4ysHPsxegP9",str(round(random.uniform(1,3), random.randint(3,5))),404,2200000),
            ("Custodial账户DOGE转账to地址为空","DOGE","DOGE","DDgRrcfZ1ZFgonHzNU7b1xbFMbDSakPGT9","",str(round(random.uniform(1,3), random.randint(3,5))),400,2300000),
            ("Custodial账户DOGE转账to地址非DOGE地址","DOGE","DOGE","DDgRrcfZ1ZFgonHzNU7b1xbFMbDSakPGT9","0x46F66EeFf67c809A7EF728aC823133ccaBa2506F",str(round(random.uniform(1,3), random.randint(3,5))),400,2400000),
            ("Custodial账户DOGE转账amount超出余额","DOGE","DOGE","DDgRrcfZ1ZFgonHzNU7b1xbFMbDSakPGT9","DGnb5SNRnEyAx9xNuHGxbiY4ysHPsxegP9","100000000",400,2102001),
            ("Custodial账户DOGE转账amount超出精度","DOGE","DOGE","DDgRrcfZ1ZFgonHzNU7b1xbFMbDSakPGT9","DGnb5SNRnEyAx9xNuHGxbiY4ysHPsxegP9","0.000000001",400,2100000),
            ("Custodial账户DOGE转账amount=0","DOGE","DOGE","DDgRrcfZ1ZFgonHzNU7b1xbFMbDSakPGT9","DGnb5SNRnEyAx9xNuHGxbiY4ysHPsxegP9","0",400,2300000),
            ("Custodial账户DOGE转账amount为负","DOGE","DOGE","DDgRrcfZ1ZFgonHzNU7b1xbFMbDSakPGT9","DGnb5SNRnEyAx9xNuHGxbiY4ysHPsxegP9","-1",400,2300000),
            ("Custodial账户DOGE转账amount为异常字符串","DOGE","DOGE","DDgRrcfZ1ZFgonHzNU7b1xbFMbDSakPGT9","DGnb5SNRnEyAx9xNuHGxbiY4ysHPsxegP9","maxxx",400,2300000),
            ("Custodial账户DOGE转账networkCode为空","","DOGE","DDgRrcfZ1ZFgonHzNU7b1xbFMbDSakPGT9","DGnb5SNRnEyAx9xNuHGxbiY4ysHPsxegP9",str(round(random.uniform(1,3), random.randint(3,5))),400,2100000),
            ("Custodial账户DOGE转账networkCode不存在","DOGEE","DOGE","DDgRrcfZ1ZFgonHzNU7b1xbFMbDSakPGT9","DGnb5SNRnEyAx9xNuHGxbiY4ysHPsxegP9",str(round(random.uniform(1,3), random.randint(3,5))),404,2200000),
            ("Custodial账户DOGE转账symbol为空","DOGE","","DDgRrcfZ1ZFgonHzNU7b1xbFMbDSakPGT9","DGnb5SNRnEyAx9xNuHGxbiY4ysHPsxegP9",str(round(random.uniform(1,3), random.randint(3,5))),400,2300000),
            ("Custodial账户DOGE转账symbol不存在","DOGE","ETH","DDgRrcfZ1ZFgonHzNU7b1xbFMbDSakPGT9","DGnb5SNRnEyAx9xNuHGxbiY4ysHPsxegP9",str(round(random.uniform(1,3), random.randint(3,5))),400,2200000)
        ]

    @allure.story("Custodial_Transfers_Fail!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,from_add,to_add,amount,status_check,code_check', test_data)
    def test_custodial(self,test_title,networkCode,symbol,from_add,to_add,amount,status_check,code_check):

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_add,
                "to":to_add,
                "symbol":symbol,
                "amount":amount
            }
            transactionParams = {
                "memo":''.join(random.sample(string.ascii_letters + string.digits, 10))
            }
            transfer = Http.HttpUtils.instructions("transfer",body,networkCode,[],transactionParams)

        with allure.step("断言status==200,code"):

            assert transfer.status_code == status_check
            assert transfer.json()["code"] == code_check

# custodial 手续费不足账户转帐
@allure.feature("Transfers_Fail!")
class Test_transfers_fee_fail:
    if env_type == 0: #测试
        test_data = [
            # BTC网络
            ("Custodial账户BTC手续费不足转账","BTC","BTC","tb1qwc23lh8cvc8wm086h88905gxt03pkq0pu3cnth","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun",str(Conf.Config.random_amount(8)),400,2400000),
            # GOERLI网络
            ("Custodial账户GOERLI手续费不足转账","GOERLI","goerliETH","0xA78026a21EDDdCB43Da6aB0c163CE1649B3701F8","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",str(Conf.Config.random_amount(8)),400,2400000),
            # MATIC网络
            ("Custodial账户MATIC手续费不足转账","MATIC","MATIC","0x86cfeDCb5cC8826eA804Fc516Da72a6D2801F0d1","0xdba67baa3ca1e89a2bdf0feee4592595b130888a",str(Conf.Config.random_amount(8)),400,2400000),
            ("Custodial账户MATIC-USDC手续费不足转账","MATIC","MATIC","0x86cfeDCb5cC8826eA804Fc516Da72a6D2801F0d1","0xdba67baa3ca1e89a2bdf0feee4592595b130888a",str(Conf.Config.random_amount(8)),400,2400000),
            # IRIS网络
            ("Custodial账户IRIS手续费不足转账","IRIS","IRIS","iaa180qh39f68devetnda4t28drsrhgxnjha5eqhus","iaa18hxtn9lx9swxf4j7ytdmn8yxsvyknh86kdgpvc",str(Conf.Config.random_amount(6)),400,2400000),
            # CLV网络
            ("Custodial账户CLV手续费不足转账","CLV","CLV","5Hgu6xq1ETv3kbjBnhqZCzaDFtqUhxfFBogZuJ2RnqsoXmWk","5HWsR2E9YLKqfz6ybMufU5t1qyjUMzmBwFjppsaEwZHegViT",str(Conf.Config.random_amount(7)),400,2400000),
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
    path = os.path.abspath(__file__) + "::Test_transfers_fee_fail"
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')