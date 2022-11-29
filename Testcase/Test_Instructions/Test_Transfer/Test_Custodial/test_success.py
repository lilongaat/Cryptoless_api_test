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
@allure.feature("Transfers_Success!")
class Test_transfers_success:
    if env_type == 0: #测试
        test_data = [
            # BTC网络
            ("Custodial账户BTC转账","BTC","BTC","tb1q8g0jhxa3t0uyufec29xexw6fwnkvw94v3jlw7e","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun",str(Conf.Config.random_amount(8))),
            # Goerli网络
            # ("Custodial账户Goerli转账","GOERLI","GoerliETH","0x821647aF7f50717500E008dE239f8692216cBC67","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",str(Conf.Config.random_amount(8))),
            # ("Custodial账户ERC20转账","GOERLI","Long","0x821647aF7f50717500E008dE239f8692216cBC67","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",str(round(random.uniform(1,10), random.randint(1,18)))),
            # MATIC网络
            # ("Custodial账户MATIC转账","MATIC","MATIC","0x343d0b801Fcb032ccEB7D5411cd404816d203B91","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591",str(Conf.Config.random_amount(8))),
            # ("Custodial账户MATIC转账","MATIC","USDC","0x343d0b801Fcb032ccEB7D5411cd404816d203B91","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591",str(Conf.Config.random_amount(5))),
            # IRIS
            # ("Custodial账户IRIS转账","IRIS","IRIS","iaa1vywcfmff44nlhud05nlzlpw0hrlxenptn9ff7r","iaa18hxtn9lx9swxf4j7ytdmn8yxsvyknh86kdgpvc",str(Conf.Config.random_amount(5))),
            # CLV
            # ("Custodial账户CLV转账","CLV","CLV","5CFStFse5QY5dyfeHeTDSnMeBBRgxXse2D8k1TUbM67HeA9h","5FXjWgPEDvrc5A3SDVHayVGfdAp9QquU5jANaZMfLzVue5k6",str(Conf.Config.random_amount(5))),
        ]
    elif env_type == 1: #生产
        test_data = [
            # DOGE网络
            # ("Custodial账户DOGE转账","DOGE","DOGE","DDgRrcfZ1ZFgonHzNU7b1xbFMbDSakPGT9","DDgRrcfZ1ZFgonHzNU7b1xbFMbDSakPGT9",str(round(random.uniform(2,3), random.randint(3,5)))),
            # ("Custodial账户DOGE转账self","DOGE","DOGE","DDgRrcfZ1ZFgonHzNU7b1xbFMbDSakPGT9","DGnb5SNRnEyAx9xNuHGxbiY4ysHPsxegP9",str(round(random.uniform(2,3), random.randint(3,5)))),
            # BSC网络
            # ("Custodial账户BNB转账","BSC","BNB","0x4adf9724723CAB3263a5f4adfBE28888EDB785b5","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591",str(Conf.Config.random_amount(8))),
            # ("Custodial账户BNB转账","BSC","USDT","0x4adf9724723CAB3263a5f4adfBE28888EDB785b5","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591",str(Conf.Config.random_amount(8))),
            # ("Custodial账户BNB转账","BSC","USDC","0x4adf9724723CAB3263a5f4adfBE28888EDB785b5","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591",str(Conf.Config.random_amount(8))),
            # # MATIC网络
            ("Custodial账户MATIC转账","MATIC","MATIC","0x985f8D18a50AF2Cb91f52f9A63d9b5eEc1f60047","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591",str(Conf.Config.random_amount(4))),
            ("Custodial账户USDC转账","MATIC","USDC","0x985f8D18a50AF2Cb91f52f9A63d9b5eEc1f60047","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591",str(Conf.Config.random_amount(5))),
            # ("Custodial账户MATIC转账self","MATIC","MATIC","0x985f8D18a50AF2Cb91f52f9A63d9b5eEc1f60047","0x985f8D18a50AF2Cb91f52f9A63d9b5eEc1f60047",str(Conf.Config.random_amount(4))),
            # ("Custodial账户USDC转账self","MATIC","USDC","0x985f8D18a50AF2Cb91f52f9A63d9b5eEc1f60047","0x985f8D18a50AF2Cb91f52f9A63d9b5eEc1f60047",str(Conf.Config.random_amount(5))),
            # # IRIS网络
            # ("Custodial账户IRIS转账","IRIS","IRIS","iaa1yvgc6tjuetv6hzchnvnqg4r09ltzk8ld6m0vcu","iaa18hxtn9lx9swxf4j7ytdmn8yxsvyknh86kdgpvc",str(Conf.Config.random_amount(4))),
            # ("Custodial账户IRIS转账self","IRIS","IRIS","iaa1yvgc6tjuetv6hzchnvnqg4r09ltzk8ld6m0vcu","iaa1yvgc6tjuetv6hzchnvnqg4r09ltzk8ld6m0vcu",str(Conf.Config.random_amount(4))),
            # # CLV网络
            # ("Custodial账户CLV转账","CLV","CLV","5DiDtDkGFJ4CtgdEnGHaWU3JwSmCro26FozcqyTY8Brk3KSo","5FXjWgPEDvrc5A3SDVHayVGfdAp9QquU5jANaZMfLzVue5k6",str(Conf.Config.random_amount(4))),
            # ("Custodial账户CLV转账self","CLV","CLV","5DiDtDkGFJ4CtgdEnGHaWU3JwSmCro26FozcqyTY8Brk3KSo","5DiDtDkGFJ4CtgdEnGHaWU3JwSmCro26FozcqyTY8Brk3KSo",str(Conf.Config.random_amount(4))),
        ]

    @allure.story("Custodial_Transfers_Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,from_add,to_add,amount', test_data)
    def test_custodial(self,test_title,networkCode,symbol,from_add,to_add,amount):

        with allure.step("查询From账户holders信息——holders"):
            holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
            assert holders.status_code == 200

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

            assert transfer.status_code == 200
            assert transfer.json()["body"]["symbol"] == symbol
            assert transfer.json()["body"]["amount"] == amount
            assert transfer.json()["body"]["from"] == from_add
            assert transfer.json()["body"]["to"] == to_add
            assert transfer.json()["_embedded"]["transactions"][0]["status"] == "SIGNED"

            id = transfer.json()["_embedded"]["transactions"][0]["id"]

        with allure.step("广播交易"):
            send = Http.HttpUtils.send(id)
            assert send.status_code == 200
            assert send.json()["status"] == "PENDING"
            # sleep(30)

        # with allure.step("查询From账户holders信息——holders"):
        #     holders = Http.HttpUtils.get_holders(networkCode,symbol,from_add)
        #     assert holders.status_code == 200

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')